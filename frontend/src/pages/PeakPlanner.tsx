import { useMemo, useState } from 'react'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

import {
  ExternalPeakResult,
  Peak,
  useCreatePeakMutation,
  useDeletePeakMutation,
  useListPeaksQuery,
  useLazySearchGlobalPeaksQuery,
  useRefreshPeakExternalMutation,
  useUpdatePeakMutation,
} from '@/features/api/peakPlannerApi'

type PeakFormState = {
  name: string
  region: string
  grade: string
  elevation_ft: string
  lat: string
  lon: string
  description: string
}

const initialFormState: PeakFormState = {
  name: '',
  region: '',
  grade: '',
  elevation_ft: '',
  lat: '',
  lon: '',
  description: '',
}

const SNAPSHOT_TTL_MS = 30 * 60 * 1000

export default function PeakPlanner() {
  const tabs = useMemo(
    () => [
      { to: 'peaks', label: 'Peaks', ready: true },
      { to: 'routes', label: 'Routes', ready: false },
      { to: 'plans', label: 'Trip Plans', ready: false },
    ],
    []
  )

  return (
    <section className="grid gap-6">
      <header className="max-w-3xl space-y-3">
        <h2 className="section-title">Peak Planner</h2>
        <p className="text-slate-600 dark:text-slate-300">
          Track alpine objectives, catalog peaks, and build itineraries. Peaks are live today — routes
          and trip plans are rolling out next.
        </p>
      </header>

      <nav className="flex flex-wrap gap-3 border-b border-slate-200/70 dark:border-slate-800/60 pb-3">
        {tabs.map(tab =>
          tab.ready ? (
            <NavLink
              key={tab.to}
              to={tab.to}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded-xl text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-brand-600 text-white shadow-soft'
                    : 'text-slate-600 dark:text-slate-300 hover:text-brand-600 dark:hover:text-brand-300'
                }`
              }
              end
            >
              {tab.label}
            </NavLink>
          ) : (
            <span
              key={tab.to}
              className="px-3 py-1.5 rounded-xl text-sm font-medium text-slate-400 dark:text-slate-600 border border-dashed border-slate-200/70 dark:border-slate-700/70 cursor-not-allowed select-none"
            >
              {tab.label} (soon)
            </span>
          )
        )}
      </nav>

      <div className="card p-6">
        <Routes>
          <Route index element={<Navigate to="peaks" replace />} />
          <Route path="peaks" element={<PeaksPanel />} />
          <Route path="*" element={<Navigate to="peaks" replace />} />
        </Routes>
      </div>
    </section>
  )
}

function PeaksPanel() {
  const {
    peaks,
    isInitialLoading,
    isRefreshing,
    queryError,
    refetch,
  } = useListPeaksQuery(undefined, {
    selectFromResult: ({ data, isLoading, isFetching, error, refetch }) => ({
      peaks: data ?? [],
      isInitialLoading: isLoading,
      isRefreshing: isFetching && !isLoading,
      queryError: error,
      refetch,
    }),
  })
  const [form, setForm] = useState<PeakFormState>(initialFormState)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [refreshingId, setRefreshingId] = useState<number | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [triggerSearch, searchState] = useLazySearchGlobalPeaksQuery()
  const [searchError, setSearchError] = useState<string | null>(null)

  const [createPeak, { isLoading: creating }] = useCreatePeakMutation()
  const [updatePeak, { isLoading: updating }] = useUpdatePeakMutation()
  const [deletePeak] = useDeletePeakMutation()
  const [refreshPeakExternal] = useRefreshPeakExternalMutation()

  const saving = creating || updating
  const hasPeaks = peaks.length > 0

  function updateField(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = event.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  function resetForm() {
    setForm(initialFormState)
    setEditingId(null)
    setFormError(null)
  }

  function toNumber(value: string) {
    if (!value.trim()) return null
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : null
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!form.name.trim()) {
      setFormError('Name is required')
      return
    }

    setFormError(null)

    const payload = {
      name: form.name.trim(),
      region: form.region.trim() || undefined,
      grade: form.grade.trim() || undefined,
      description: form.description.trim() || undefined,
      elevation_ft: toNumber(form.elevation_ft),
      lat: toNumber(form.lat),
      lon: toNumber(form.lon),
    }

    try {
      if (editingId) {
        await updatePeak({ id: editingId, body: payload }).unwrap()
      } else {
        await createPeak(payload).unwrap()
      }
      resetForm()
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Unable to save peak')
    }
  }

  function startEdit(peak: Peak) {
    setEditingId(peak.id)
    setForm({
      name: peak.name ?? '',
      region: peak.region ?? '',
      grade: peak.grade ?? '',
      elevation_ft: peak.elevation_ft?.toString() ?? '',
      lat: peak.lat?.toString() ?? '',
      lon: peak.lon?.toString() ?? '',
      description: peak.description ?? '',
    })
  }

  async function handleDelete(id: number) {
    if (!window.confirm('Delete this peak?')) return
    setDeletingId(id)
    setFormError(null)
    try {
      await deletePeak(id).unwrap()
      if (editingId === id) resetForm()
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Unable to delete peak')
    } finally {
      setDeletingId(null)
    }
  }

  async function handleRefreshSnapshot(id: number) {
    setRefreshingId(id)
    try {
      await refreshPeakExternal(id).unwrap()
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Unable to sync NPS data')
    } finally {
      setRefreshingId(null)
    }
  }

  async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!searchTerm.trim()) {
      setSearchError('Enter a peak name to search.')
      return
    }
    setSearchError(null)
    try {
      await triggerSearch({ q: searchTerm.trim(), limit: 5 }).unwrap()
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : 'Unable to search peaks right now.')
    }
  }

  async function importExternalPeak(result: ExternalPeakResult) {
    setFormError(null)
    const payload = {
      name: result.name ?? searchTerm.trim(),
      region: result.region ?? undefined,
      grade: undefined,
      description: '',
      elevation_ft: result.elevation_m ? Math.round(result.elevation_m * 3.28084) : null,
      lat: result.lat ?? undefined,
      lon: result.lon ?? undefined,
    }
    try {
      await createPeak(payload).unwrap()
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Unable to import peak')
    }
  }

  return (
    <div className="grid gap-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="font-semibold text-lg">Peaks</h3>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            Import summits from OpenStreetMap, enrich them with elevation + weather data, and keep them
            synced for planning.
          </p>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
          {isRefreshing && hasPeaks && (
            <span className="inline-flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-brand-500 animate-pulse" />
              Refreshing peaks…
            </span>
          )}
          <button type="button" className="btn-ghost text-xs" onClick={() => refetch()}>
            Refetch
          </button>
        </div>
      </div>

      <form className="grid gap-4" onSubmit={handleSubmit}>
        <div className="grid gap-3 sm:grid-cols-2">
          <label className="text-sm grid gap-1">
            <span>Name *</span>
            <input
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="name"
              value={form.name}
              onChange={updateField}
              required
            />
          </label>
          <label className="text-sm grid gap-1">
            <span>Region</span>
            <input
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="region"
              value={form.region}
              onChange={updateField}
            />
          </label>
          <label className="text-sm grid gap-1">
            <span>Grade</span>
            <input
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="grade"
              value={form.grade}
              onChange={updateField}
            />
          </label>
          <label className="text-sm grid gap-1">
            <span>Elevation (ft)</span>
            <input
              type="number"
              inputMode="numeric"
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="elevation_ft"
              value={form.elevation_ft}
              onChange={updateField}
            />
          </label>
          <label className="text-sm grid gap-1">
            <span>Latitude</span>
            <input
              type="number"
              step="any"
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="lat"
              value={form.lat}
              onChange={updateField}
            />
          </label>
          <label className="text-sm grid gap-1">
            <span>Longitude</span>
            <input
              type="number"
              step="any"
              className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
              name="lon"
              value={form.lon}
              onChange={updateField}
            />
          </label>
        </div>
        <label className="text-sm grid gap-1">
          <span>Description / Notes</span>
          <textarea
            className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60 min-h-[90px]"
            name="description"
            value={form.description}
            onChange={updateField}
          />
        </label>

        <div className="flex flex-wrap gap-2">
          <button className="btn-primary" disabled={saving}>
            {editingId ? 'Update Peak' : 'Add Peak'}
          </button>
          {editingId && (
            <button
              type="button"
              className="btn-ghost"
              onClick={resetForm}
              disabled={saving}
            >
              Cancel
            </button>
          )}
        </div>

        {formError && <p className="text-sm text-red-600">{formError}</p>}
        {queryError && (
          <p className="text-sm text-red-600">
            {(queryError as { status?: number })?.status
              ? `Unable to load peaks (status ${(queryError as { status?: number }).status}).`
              : 'Unable to load peaks.'}
          </p>
        )}
      </form>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="text-left text-xs uppercase text-slate-500 dark:text-slate-400 border-b border-slate-200/70 dark:border-slate-800/70">
            <tr>
              <th className="py-2 pr-3 font-semibold">Name</th>
              <th className="py-2 pr-3 font-semibold">Region</th>
              <th className="py-2 pr-3 font-semibold">Grade</th>
              <th className="py-2 pr-3 font-semibold text-right">Elevation</th>
              <th className="py-2 pr-3 font-semibold">External Snapshot</th>
              <th className="py-2"></th>
            </tr>
          </thead>
          <tbody>
            {isInitialLoading ? (
              Array.from({ length: 3 }).map((_, idx) => (
                <tr key={idx} className="animate-pulse border-b border-slate-100 dark:border-slate-800/60">
                  <td className="py-4 pr-3">
                    <div className="h-4 w-32 rounded bg-slate-200/70 dark:bg-slate-800" />
                  </td>
                  <td className="py-4 pr-3">
                    <div className="h-4 w-24 rounded bg-slate-200/70 dark:bg-slate-800" />
                  </td>
                  <td className="py-4 pr-3">
                    <div className="h-4 w-16 rounded bg-slate-200/70 dark:bg-slate-800" />
                  </td>
                  <td className="py-4 pr-3 text-right">
                    <div className="h-4 w-20 rounded bg-slate-200/70 dark:bg-slate-800 ml-auto" />
                  </td>
                  <td className="py-4 pr-3">
                    <div className="h-4 w-40 rounded bg-slate-200/70 dark:bg-slate-800" />
                  </td>
                  <td className="py-4" />
                </tr>
              ))
            ) : !hasPeaks ? (
              <tr>
                <td colSpan={6} className="py-6 text-center text-slate-500">
                  No peaks yet. Add your first objective above.
                </td>
              </tr>
            ) : (
              peaks.map(peak => {
                const snapshotStale =
                  peak.external_retrieved_at &&
                  Date.now() - new Date(peak.external_retrieved_at).getTime() > SNAPSHOT_TTL_MS

                return (
                  <tr key={peak.id} className="border-b border-slate-100 dark:border-slate-800/60">
                    <td className="py-2 pr-3 font-medium">{peak.name}</td>
                    <td className="py-2 pr-3 text-slate-600 dark:text-slate-300">
                      {peak.region || '—'}
                    </td>
                    <td className="py-2 pr-3 text-slate-600 dark:text-slate-300">
                      {peak.grade || '—'}
                    </td>
                    <td className="py-2 pr-3 text-right text-slate-600 dark:text-slate-300">
                      {peak.elevation_ft ? `${peak.elevation_ft.toLocaleString()} ft` : '—'}
                    </td>
                    <td className="py-2 pr-3 text-slate-600 dark:text-slate-300">
                      {peak.external_country ? (
                        <div className="flex flex-col gap-1">
                          <span className="font-medium text-slate-800 dark:text-slate-100">
                            {peak.external_country}{' '}
                            {peak.external_range ? `• ${peak.external_range}` : ''}
                          </span>
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            {peak.external_elevation_m
                              ? `${peak.external_elevation_m.toLocaleString()} m`
                              : '—'}{' '}
                            elevation
                          </span>
                          <span className="text-[11px] text-slate-400">
                            Synced{' '}
                            {peak.external_retrieved_at
                              ? new Date(peak.external_retrieved_at).toLocaleString()
                              : '—'}
                            {snapshotStale ? ' • stale' : ''}
                          </span>
                        </div>
                      ) : (
                        <span className="text-xs text-slate-500">
                          No external snapshot yet. Sync to enrich details.
                        </span>
                      )}
                    </td>
                    <td className="py-2 flex flex-col gap-1 items-end text-sm">
                      <button className="navlink" onClick={() => startEdit(peak)}>
                        Edit
                      </button>
                      <button
                        className="navlink text-red-500 hover:text-red-400"
                        onClick={() => handleDelete(peak.id)}
                        disabled={deletingId === peak.id}
                      >
                        {deletingId === peak.id ? 'Deleting…' : 'Delete'}
                      </button>
                      <button
                        className="navlink text-brand-600 dark:text-brand-300"
                        onClick={() => handleRefreshSnapshot(peak.id)}
                        disabled={refreshingId === peak.id}
                      >
                        {refreshingId === peak.id ? 'Syncing…' : 'Sync OSM'}
                      </button>
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>

      <div className="rounded-2xl border border-dashed border-slate-200/70 dark:border-slate-800/60 p-4 space-y-4 bg-white/50 dark:bg-slate-950/40">
        <div className="flex flex-col gap-1">
          <h4 className="font-semibold text-sm uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Discover Peaks (OpenStreetMap + OpenTopoData)
          </h4>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            Query OpenStreetMap for nearby summits and fill in missing elevation with OpenTopoData, then
            import them directly into your planner.
          </p>
        </div>
        <form className="flex flex-wrap gap-2" onSubmit={handleSearch}>
          <input
            className="flex-1 min-w-[220px] border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60"
            placeholder="Search e.g., Denali"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
          <button className="btn-primary" disabled={searchState.isFetching}>
            {searchState.isFetching ? 'Searching...' : 'Search'}
          </button>
        </form>
        {searchError && <p className="text-sm text-red-600">{searchError}</p>}
        {searchState.error && (
          <p className="text-sm text-red-600">
            {'data' in searchState.error
              ? (searchState.error as { data?: { detail?: string } }).data?.detail ?? 'Unable to search peaks.'
              : 'Unable to search peaks.'}
          </p>
        )}
        <div className="grid gap-3">
          {searchState.isFetching ? (
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, idx) => (
                <div
                  key={idx}
                  className="animate-pulse h-12 rounded-xl bg-slate-100 dark:bg-slate-900/60"
                />
              ))}
            </div>
          ) : searchState.data?.results?.length ? (
            searchState.data.results.map(result => {
              const contextLine =
                [result.range, result.region, result.country]
                  .filter(Boolean)
                  .join(' • ') || '—'

              return (
                <div
                  key={result.osm_id}
                  className="flex flex-col gap-1 rounded-xl border border-slate-200/70 dark:border-slate-800/70 p-3 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <div className="font-medium text-slate-900 dark:text-slate-100">
                      {result.name ?? 'Unnamed peak'}
                    </div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{contextLine}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">
                      {result.elevation_m ? `${result.elevation_m.toLocaleString()} m` : '—'} •{' '}
                      {result.lat != null && result.lon != null
                        ? `${result.lat.toFixed(3)}, ${result.lon.toFixed(3)}`
                        : 'No coords'}
                    </div>
                  </div>
                  <button
                    className="btn-ghost text-sm mt-2 sm:mt-0"
                    onClick={() => importExternalPeak(result)}
                    type="button"
                  >
                    Import
                  </button>
                </div>
              )
            })
          ) : searchState.data && !searchState.isFetching ? (
            <p className="text-sm text-slate-500">No peaks found. Try another query.</p>
          ) : null}
        </div>
      </div>
    </div>
  )
}
