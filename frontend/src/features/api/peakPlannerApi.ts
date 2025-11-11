import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''

export type Peak = {
  id: number
  name: string
  region: string
  grade: string
  elevation_ft: number | null
  prominence_ft: number | null
  lat: number | null
  lon: number | null
  description: string
  external_source?: string | null
  external_id?: string | null
  external_country?: string | null
  external_range?: string | null
  external_elevation_m?: number | null
  external_prominence_m?: number | null
  external_retrieved_at?: string | null
  external_payload?: Record<string, unknown> | null
  created_at: string
  updated_at: string
}

export type ExternalPeakResult = {
  osm_id: string
  name: string | null
  lat: number | null
  lon: number | null
  elevation_m: number | null
  country: string | null
  region: string | null
  range: string | null
  retrieved_at: string | null
}

export type PeakPayload = {
  name: string
  region?: string
  grade?: string
  elevation_ft?: number | null
  lat?: number | null
  lon?: number | null
  description?: string
}

type PeakSnapshotResponse = {
  peak: Peak
  snapshot: {
    source: string | null
    external_id: string | null
    country: string | null
    range: string | null
    elevation_m: number | null
    prominence_m: number | null
    retrieved_at: string | null
    payload?: Record<string, unknown> | null
  } | null
  from_cache: boolean
}

type PeakSearchResponse = {
  results: ExternalPeakResult[]
}

const API_PREFIX = API_BASE_URL || ''

export const peakPlannerApi = createApi({
  reducerPath: 'peakPlannerApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_PREFIX,
    prepareHeaders: (headers) => {
      headers.set('Accept', 'application/json')
      return headers
    },
  }),
  tagTypes: ['Peak', 'PeakExternal'],
  endpoints: (builder) => ({
    listPeaks: builder.query<Peak[], void>({
      query: () => '/api/peak-planner/peaks/',
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: 'Peak' as const, id })),
              { type: 'Peak' as const, id: 'LIST' },
            ]
          : [{ type: 'Peak' as const, id: 'LIST' }],
      keepUnusedDataFor: 1800,
    }),
    createPeak: builder.mutation<Peak, PeakPayload>({
      query: (body) => ({
        url: '/api/peak-planner/peaks/',
        method: 'POST',
        body,
      }),
      invalidatesTags: [{ type: 'Peak', id: 'LIST' }],
    }),
    updatePeak: builder.mutation<Peak, { id: number; body: PeakPayload }>({
      query: ({ id, body }) => ({
        url: `/api/peak-planner/peaks/${id}/`,
        method: 'PUT',
        body,
      }),
      invalidatesTags: (result, error, arg) => [
        { type: 'Peak', id: arg.id },
        { type: 'Peak', id: 'LIST' },
        { type: 'PeakExternal', id: arg.id },
      ],
    }),
    deletePeak: builder.mutation<void, number>({
      query: (id) => ({
        url: `/api/peak-planner/peaks/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: (result, error, id) => [
        { type: 'Peak', id },
        { type: 'Peak', id: 'LIST' },
      ],
    }),
    refreshPeakExternal: builder.mutation<PeakSnapshotResponse, number>({
      query: (id) => ({
        url: `/api/peak-planner/peaks/${id}/osm/refresh/`,
        method: 'POST',
      }),
      invalidatesTags: (result, error, id) => [
        { type: 'PeakExternal', id },
        { type: 'Peak', id },
        { type: 'Peak', id: 'LIST' },
      ],
    }),
    searchGlobalPeaks: builder.query<
      PeakSearchResponse,
      { q: string; lat?: number; lon?: number; limit?: number }
    >({
      query: ({ q, lat, lon, limit = 5 }) => ({
        url: '/api/peak-planner/peaks/osm/search/',
        params: { q, lat, lon, limit },
      }),
      keepUnusedDataFor: 600,
    }),
  }),
})

export const {
  useListPeaksQuery,
  useCreatePeakMutation,
  useUpdatePeakMutation,
  useDeletePeakMutation,
  useRefreshPeakExternalMutation,
  useLazySearchGlobalPeaksQuery,
} = peakPlannerApi
