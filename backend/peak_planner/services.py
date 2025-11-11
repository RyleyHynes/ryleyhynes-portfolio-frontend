"""Peak Planner service utilities (NPS integration + helpers)."""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from .models import Peak, Route

log = logging.getLogger(__name__)

NPS_CACHE_PREFIX = "nps_places:v1"
OPEN_PEAKS_CACHE_PREFIX = "open_peaks:v1"


class NpsApiError(Exception):
  """Base exception for National Park Service API failures."""


class NpsApiNotFound(NpsApiError):
  """Raised when the requested resource is not found."""


class NpsApiRateLimited(NpsApiError):
  """Raised when the NPS API responds with rate-limit semantics."""

class OpenPeaksError(Exception):
  """Base exception for Open Peaks integration failures."""


class OpenPeaksNotFound(OpenPeaksError):
  """Raised when Open Peaks returns no data."""


class OpenPeaksRateLimited(OpenPeaksError):
  """Raised when Open Peaks throttles requests."""


@dataclass
class NpsPlaceSnapshot:
  """Normalized snapshot for an NPS place."""

  source: str
  external_id: Optional[str]
  name: Optional[str]
  states: Optional[str]
  designation: Optional[str]
  description: Optional[str]
  lat: Optional[float]
  lon: Optional[float]
  retrieved_at: timezone.datetime
  raw: Optional[Dict[str, Any]] = None


@dataclass
class OpenPeaksSnapshot:
  """Normalized Open Peaks record representing an actual summit."""

  source: str
  external_id: Optional[str]
  name: Optional[str]
  country: Optional[str]
  region: Optional[str]
  range: Optional[str]
  elevation_m: Optional[int]
  prominence_m: Optional[int]
  lat: Optional[float]
  lon: Optional[float]
  retrieved_at: timezone.datetime
  raw: Optional[Dict[str, Any]] = None


def _nps_cache_key(peak: Peak) -> str:
  lat = f"{float(peak.lat):.4f}" if peak.lat is not None else "-"
  lon = f"{float(peak.lon):.4f}" if peak.lon is not None else "-"
  name = slugify(peak.name or "unknown")
  return f"{NPS_CACHE_PREFIX}:{name}:{lat}:{lon}"


def _base_headers() -> Dict[str, str]:
  headers = {
      "Accept": "application/json",
      "User-Agent": getattr(settings, "NPS_API_USER_AGENT", "PeakPlanner/1.0"),
  }
  api_key = getattr(settings, "NPS_API_KEY", "")
  if api_key:
    headers["X-Api-Key"] = api_key
  return headers


def _request_nps(params: Dict[str, Any]) -> httpx.Response:
  timeout_seconds = float(getattr(settings, "NPS_API_TIMEOUT", 5))
  retries = max(int(getattr(settings, "NPS_API_MAX_RETRIES", 1)), 0)

  last_exc: Optional[Exception] = None
  for attempt in range(retries + 1):
    try:
      with httpx.Client(timeout=timeout_seconds) as client:
        response = client.get(
            getattr(settings, "NPS_API_BASE_URL"),
            params=params,
            headers=_base_headers(),
        )
      if response.status_code == 429:
        raise NpsApiRateLimited("NPS API temporarily rate-limited the request. Please retry shortly.")
      return response
    except (httpx.TimeoutException, httpx.TransportError) as exc:  # pragma: no cover - network failure path
      last_exc = exc
      if attempt == retries:
        raise NpsApiError("NPS request failed.") from exc
      time.sleep(0.2 * (attempt + 1))

  assert last_exc  # pragma: no cover
  raise NpsApiError("NPS request failed.") from last_exc


def _extract_records(payload: Any) -> List[Dict[str, Any]]:
  if isinstance(payload, dict):
    data = payload.get("data")
    if isinstance(data, list):
      return [item for item in data if isinstance(item, dict)]
  if isinstance(payload, list):
    return [item for item in payload if isinstance(item, dict)]
  return []


def _normalize_record(record: Dict[str, Any]) -> NpsPlaceSnapshot:
  def _to_float(value: Any) -> Optional[float]:
    try:
      return float(value)
    except (TypeError, ValueError):
      return None

  now = timezone.now()
  return NpsPlaceSnapshot(
      source="nps",
      external_id=str(record.get("id") or record.get("placeId") or ""),
      name=record.get("title") or record.get("name"),
      states=record.get("states"),
      designation=record.get("designation"),
      description=record.get("listingdescription") or record.get("description"),
      lat=_to_float(record.get("latitude")),
      lon=_to_float(record.get("longitude")),
      retrieved_at=now,
      raw=record,
  )


DEFAULT_PLACE_TYPES = ["mountain","summit","peak","alpine","trail","landform","mesa","rock","volcano"]
DEFAULT_TOPICS = ["Mountains","Geology","Science"]

def search_nps_places(
    query: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    limit: int = 5,
    place_types: Optional[List[str]] = None,
    topics: Optional[List[str]] = None,
) -> Tuple[List[NpsPlaceSnapshot], bool]:
  """Query the NPS Places endpoint."""

  if not query or not query.strip():
    raise ValueError("Query parameter 'q' is required.")

  cache_key = f"{NPS_CACHE_PREFIX}:search:{slugify(query.strip())}:{lat or '-'}:{lon or '-'}:{limit}"
  cached = cache.get(cache_key)
  if cached:
    return cached["data"], True

  params: Dict[str, Any] = {
      "q": query.strip(),
      "limit": limit,
      "fields": "latitude,longitude,listingdescription,states,designation,placeType,topics",
  }
  if lat is not None and lon is not None:
    params.update({"latitude": lat, "longitude": lon})
  types = place_types or DEFAULT_PLACE_TYPES
  topics_param = topics or DEFAULT_TOPICS
  if types:
    params["placeType"] = ",".join(types)
  if topics_param:
    params["topic"] = ",".join(topics_param)

  response = _request_nps(params)
  response.raise_for_status()
  payload = response.json()
  records = _extract_records(payload)
  if not records:
    raise NpsApiNotFound("NPS places returned no results.")

  snapshots = [_normalize_record(record) for record in records[:limit]]
  cache.set(cache_key, {"data": snapshots}, getattr(settings, "NPS_API_CACHE_TTL", 1800))
  return snapshots, False


def fetch_nps_snapshot(peak: Peak, force_refresh: bool = False) -> Tuple[NpsPlaceSnapshot, bool]:

  if not peak.name:
    raise NpsApiError("Peak name required to query NPS.")

  cache_key = _nps_cache_key(peak)
  cached = cache.get(cache_key)
  if cached and not force_refresh:
    return cached["data"], True

  snapshots, from_cache = search_nps_places(peak.name, limit=1)
  snapshot = snapshots[0]
  cache.set(cache_key, {"data": snapshot}, getattr(settings, "NPS_API_CACHE_TTL", 1800))
  return snapshot, from_cache


def apply_nps_snapshot(peak: Peak, snapshot: NpsPlaceSnapshot) -> Peak:
  """Persist a normalized NPS snapshot onto a Peak record."""

  update_fields = [
      "external_source",
      "external_id",
      "external_country",
      "external_range",
      "external_elevation_m",
      "external_retrieved_at",
      "external_payload",
  ]

  peak.external_source = snapshot.source
  peak.external_id = snapshot.external_id or ""
  peak.external_country = "USA"
  peak.external_range = snapshot.designation or snapshot.states or ""
  peak.external_elevation_m = None
  peak.external_prominence_m = None
  peak.external_retrieved_at = snapshot.retrieved_at
  peak.external_payload = snapshot.raw or {}

  if snapshot.states and not peak.region:
    peak.region = snapshot.states
    update_fields.append("region")

  if snapshot.description and not peak.description:
    peak.description = snapshot.description
    update_fields.append("description")

  if snapshot.lat is not None and peak.lat is None:
    peak.lat = snapshot.lat
    update_fields.append("lat")
  if snapshot.lon is not None and peak.lon is None:
    peak.lon = snapshot.lon
    update_fields.append("lon")

  peak.save(update_fields=list(dict.fromkeys(update_fields)))
  return peak


def _open_peaks_headers() -> Dict[str, str]:
  return {
      "Accept": "application/json",
      "User-Agent": getattr(settings, "OPEN_PEAKS_USER_AGENT", "PeakPlanner/1.0"),
  }


def _request_open_peaks(params: Dict[str, Any]) -> httpx.Response:
  timeout_seconds = float(getattr(settings, "OPEN_PEAKS_TIMEOUT", 5))
  retries = max(int(getattr(settings, "OPEN_PEAKS_MAX_RETRIES", 1)), 0)

  last_exc: Optional[Exception] = None
  for attempt in range(retries + 1):
    try:
      with httpx.Client(timeout=timeout_seconds) as client:
        response = client.get(
            getattr(settings, "OPEN_PEAKS_API_BASE_URL"),
            params=params,
            headers=_open_peaks_headers(),
        )
      if response.status_code == 429:
        raise OpenPeaksRateLimited("Open Peaks temporarily limited requests. Please retry.")
      return response
    except (httpx.TimeoutException, httpx.TransportError) as exc:
      last_exc = exc
      if attempt == retries:
        raise OpenPeaksError("Open Peaks request failed.") from exc
      time.sleep(0.2 * (attempt + 1))

  assert last_exc
  raise OpenPeaksError("Open Peaks request failed.") from last_exc


def _normalize_open_peaks_record(record: Dict[str, Any]) -> OpenPeaksSnapshot:
  def _to_int(value: Any) -> Optional[int]:
    try:
      return int(round(float(value)))
    except (TypeError, ValueError):
      return None

  def _to_float(value: Any) -> Optional[float]:
    try:
      return float(value)
    except (TypeError, ValueError):
      return None

  return OpenPeaksSnapshot(
      source="open_peaks",
      external_id=str(record.get("id") or record.get("_id") or record.get("slug") or ""),
      name=record.get("name"),
      country=record.get("country"),
      region=record.get("region"),
      range=record.get("range"),
      elevation_m=_to_int(record.get("elevation") or record.get("elevation_m")),
      prominence_m=_to_int(record.get("prominence") or record.get("prominence_m")),
      lat=_to_float(record.get("latitude") or record.get("lat")),
      lon=_to_float(record.get("longitude") or record.get("lon")),
      retrieved_at=now(),
      raw=record,
  )


def search_open_peaks(
    query: str,
    limit: int = 5,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> Tuple[List[OpenPeaksSnapshot], bool]:
  if not query or not query.strip():
    raise ValueError("Query parameter 'q' is required.")

  cache_key = f"{OPEN_PEAKS_CACHE_PREFIX}:search:{slugify(query.strip())}:{lat or '-'}:{lon or '-'}:{limit}"
  cached = cache.get(cache_key)
  if cached:
    return cached["data"], True

  params: Dict[str, Any] = {
      "q": query.strip(),
      "limit": limit,
  }
  if lat is not None and lon is not None:
    params.update({"lat": lat, "lon": lon, "radius": 40})

  response = _request_open_peaks(params)
  response.raise_for_status()
  payload = response.json()
  records = []
  if isinstance(payload, dict):
    data = payload.get("data") or payload.get("results") or []
    if isinstance(data, list):
      records = data
  elif isinstance(payload, list):
    records = payload

  if not records:
    raise OpenPeaksNotFound("No peaks found for that query.")

  snapshots = [_normalize_open_peaks_record(rec) for rec in records[:limit]]
  cache.set(cache_key, {"data": snapshots}, getattr(settings, "OPEN_PEAKS_CACHE_TTL", 1800))
  return snapshots, False


def search_peaks_with_context(
    query: str,
    limit: int = 5,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> Tuple[List[Dict[str, Any]], bool]:
  peaks, from_cache = search_open_peaks(query, limit=limit, lat=lat, lon=lon)
  combined: List[Dict[str, Any]] = []

  for peak_snapshot in peaks:
    nps_snapshot = None
    if peak_snapshot.country and peak_snapshot.country.lower() in {"usa", "united states"}:
      try:
        nps_results, _ = search_nps_places(
            peak_snapshot.name or query,
            lat=peak_snapshot.lat,
            lon=peak_snapshot.lon,
            limit=1,
        )
        nps_snapshot = nps_results[0]
      except (NpsApiError, ValueError):
        nps_snapshot = None

    combined.append(
        {
            "peak": _serialize_open_snapshot(peak_snapshot),
            "nps": _serialize_nps_snapshot(nps_snapshot) if nps_snapshot else None,
        }
    )

  return combined, from_cache


def _serialize_open_snapshot(snapshot: OpenPeaksSnapshot) -> Dict[str, Any]:
  return {
      "source": snapshot.source,
      "external_id": snapshot.external_id,
      "name": snapshot.name,
      "country": snapshot.country,
      "region": snapshot.region,
      "range": snapshot.range,
      "elevation_m": snapshot.elevation_m,
      "prominence_m": snapshot.prominence_m,
      "lat": snapshot.lat,
      "lon": snapshot.lon,
      "retrieved_at": snapshot.retrieved_at.isoformat(),
      "raw": snapshot.raw,
  }


def _serialize_nps_snapshot(snapshot: Optional[NpsPlaceSnapshot]) -> Optional[Dict[str, Any]]:
  if snapshot is None:
    return None
  return {
      "source": snapshot.source,
      "external_id": snapshot.external_id,
      "name": snapshot.name,
      "states": snapshot.states,
      "designation": snapshot.designation,
      "description": snapshot.description,
      "lat": snapshot.lat,
      "lon": snapshot.lon,
      "retrieved_at": snapshot.retrieved_at.isoformat(),
      "raw": snapshot.raw,
  }


def estimate_time_hours(route: Route, pace_up_ft_per_hr: int = 1100, pace_flat_mi_per_hr: float = 2.5) -> float:
  """Rough Naismith-style estimate for time on route."""

  vert = route.vert_gain_ft or 0
  distance = route.distance_mi or 0
  return (vert / pace_up_ft_per_hr) + (float(distance) / pace_flat_mi_per_hr)
