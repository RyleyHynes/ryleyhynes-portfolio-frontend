"""OpenStreetMap + OpenTopoData + Open-Meteo helpers for Peak Planner."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx
from django.core.cache import cache
from django.utils import timezone
from django.utils.text import slugify

import textwrap

from .models import Peak

log = logging.getLogger(__name__)


OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
OPEN_TOPO_URL = os.getenv("OPEN_TOPO_URL", "https://api.opentopodata.org/v1/etopo1")
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
OVERPASS_CACHE_TTL = 60 * 30
TOPO_CACHE_TTL = 60 * 60
WEATHER_CACHE_TTL = 60 * 60


class OsmError(Exception):
    """Base exception for OpenStreetMap lookups."""


class OsmNotFound(OsmError):
    """Raised when no OSM peaks match the query."""


class WeatherError(Exception):
    """Raised when the weather API fails."""


@dataclass
class OsmPeakSnapshot:
    osm_id: str
    name: str
    lat: Optional[float]
    lon: Optional[float]
    elevation_m: Optional[float]
    country: Optional[str]
    region: Optional[str]
    range: Optional[str]
    retrieved_at: timezone.datetime
    raw: Dict[str, Any]


def _build_overpass_query(
    name_query: Optional[str],
    lat: Optional[float],
    lon: Optional[float],
    radius_m: int,
    limit: int,
) -> str:
    natural_filter = '["natural"~"peak|mountain_pass|volcano"]'
    name_filter = ""
    if name_query:
        escaped = _escape_query(name_query.strip())
        name_filter = f'["name"~"{escaped}",i]'
    area_filter = ""
    if lat is not None and lon is not None:
        area_filter = f"(around:{radius_m},{lat},{lon})"
    limit_clause = f" out body {limit};" if limit else " out body;"
    query = textwrap.dedent(
        f"""
        [out:json][timeout:25];
        node{natural_filter}{name_filter}{area_filter};
        {limit_clause}
        """
    ).strip()
    return query


def _escape_query(value: str) -> str:
    return value.replace('"', "").replace("\\", "")


def _fetch_overpass(
    name_query: Optional[str],
    lat: Optional[float],
    lon: Optional[float],
    radius_m: int,
    limit: int,
) -> Dict[str, Any]:
    query = _build_overpass_query(name_query, lat, lon, radius_m, limit)
    cache_key = f"osm:query:{slugify(name_query or 'all')}:{lat or 'x'}:{lon or 'x'}:{radius_m}:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    with httpx.Client(timeout=25.0) as client:
        response = client.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        data = response.json()
    cache.set(cache_key, data, OVERPASS_CACHE_TTL)
    return data


def _fetch_elevation(lat: float, lon: float) -> Optional[float]:
    cache_key = f"elevation:{round(lat,4)}:{round(lon,4)}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(OPEN_TOPO_URL, params={"locations": f"{lat},{lon}"})
            response.raise_for_status()
            payload = response.json()
            results = payload.get("results", [])
            elevation = results[0].get("elevation") if results else None
    except Exception as exc:  # pragma: no cover - external API
        log.warning("OpenTopoData request failed: %s", exc)
        elevation = None
    cache.set(cache_key, elevation, TOPO_CACHE_TTL)
    return elevation


def _normalize_osm_element(element: Dict[str, Any]) -> OsmPeakSnapshot:
    tags = element.get("tags", {})
    lat = element.get("lat")
    lon = element.get("lon")
    elevation = tags.get("ele")
    try:
        elevation = float(elevation)
    except (TypeError, ValueError):
        elevation = None
    country = tags.get("addr:country") or tags.get("is_in:country") or tags.get("country")
    region = (
        tags.get("addr:state")
        or tags.get("is_in:state")
        or tags.get("state")
        or tags.get("is_in:province")
    )
    mountain_range = tags.get("mountain_range") or tags.get("range")
    name = tags.get("name") or tags.get("alt_name") or tags.get("int_name") or "Unnamed peak"

    return OsmPeakSnapshot(
        osm_id=f"{element.get('type', 'node')}:{element.get('id')}",
        name=name,
        lat=lat,
        lon=lon,
        elevation_m=elevation,
        country=country,
        region=region,
        range=mountain_range,
        retrieved_at=timezone.now(),
        raw=element,
    )


def search_osm_peaks(
    query: Optional[str],
    *,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_m: int = 50_000,
    limit: int = 10,
) -> List[OsmPeakSnapshot]:
    if not query and (lat is None or lon is None):
        raise ValueError("Provide a search term or coordinates.")

    data = _fetch_overpass(query, lat, lon, radius_m, limit)
    elements = data.get("elements", [])
    snapshots: List[OsmPeakSnapshot] = []
    for element in elements:
        if element.get("type") != "node":
            continue
        snapshot = _normalize_osm_element(element)
        if snapshot.elevation_m is None and snapshot.lat is not None and snapshot.lon is not None:
            snapshot.elevation_m = _fetch_elevation(snapshot.lat, snapshot.lon)
        snapshots.append(snapshot)

    if not snapshots:
        raise OsmNotFound("No peaks found for that query.")
    return snapshots


def fetch_osm_snapshot_for_peak(peak: Peak, force_refresh: bool = False) -> Tuple[OsmPeakSnapshot, bool]:
    if not peak.name:
        raise OsmError("Peak name required to look up OpenStreetMap data.")

    cache_key = f"osm:snapshot:{slugify(peak.name)}:{round(float(peak.lat),3) if peak.lat else 'x'}:{round(float(peak.lon),3) if peak.lon else 'x'}"
    cached = cache.get(cache_key)
    if cached and not force_refresh:
        return cached, True

    lat = float(peak.lat) if peak.lat is not None else None
    lon = float(peak.lon) if peak.lon is not None else None
    snapshots = search_osm_peaks(peak.name, lat=lat, lon=lon, limit=1)
    snapshot = snapshots[0]
    cache.set(cache_key, snapshot, OVERPASS_CACHE_TTL)
    return snapshot, False


def apply_osm_snapshot(peak: Peak, snapshot: OsmPeakSnapshot) -> Peak:
    peak.external_source = "osm"
    peak.external_id = snapshot.osm_id
    peak.external_country = snapshot.country or ""
    peak.external_range = snapshot.range or snapshot.region or ""
    peak.external_elevation_m = snapshot.elevation_m
    peak.external_prominence_m = None
    peak.external_retrieved_at = snapshot.retrieved_at
    peak.external_payload = snapshot.raw

    if snapshot.region and not peak.region:
        peak.region = snapshot.region
    if snapshot.lat is not None:
        peak.lat = snapshot.lat
    if snapshot.lon is not None:
        peak.lon = snapshot.lon
    if snapshot.elevation_m and not peak.elevation_ft:
        peak.elevation_ft = int(round(float(snapshot.elevation_m) * 3.28084))

    peak.save(
        update_fields=[
            "external_source",
            "external_id",
            "external_country",
            "external_range",
            "external_elevation_m",
            "external_retrieved_at",
            "external_payload",
            "region",
            "lat",
            "lon",
            "elevation_ft",
        ]
    )
    return peak


def fetch_weather_forecast(lat: float, lon: float) -> Dict[str, Any]:
    if lat is None or lon is None:
        raise WeatherError("Latitude and longitude are required for weather forecasts.")

    cache_key = f"weather:{round(lat,2)}:{round(lon,2)}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max",
        "forecast_days": 3,
        "timezone": "auto",
    }
    with httpx.Client(timeout=OPEN_METEO_TIMEOUT) as client:
        response = client.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        data = response.json()

    payload = {
        "location": {"latitude": data.get("latitude"), "longitude": data.get("longitude")},
        "hourly": data.get("hourly"),
        "daily": data.get("daily"),
    }
    cache.set(cache_key, payload, WEATHER_CACHE_TTL)
    return payload
