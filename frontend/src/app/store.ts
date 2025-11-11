import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'

import { peakPlannerApi } from '@/features/api/peakPlannerApi'

export const store = configureStore({
  reducer: {
    [peakPlannerApi.reducerPath]: peakPlannerApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(peakPlannerApi.middleware),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

setupListeners(store.dispatch)
