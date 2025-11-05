/* eslint-disable @typescript-eslint/no-explicit-any */
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
const baseUrl = import.meta.env.PROD ? '/api/' : 'http://localhost:8000/api/'
export const portfolioApi = createApi({
  reducerPath: 'portfolioApi',
  baseQuery: fetchBaseQuery({
    baseUrl,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('access')
      if (token) headers.set('authorization', `Bearer ${token}`)
      return headers
    }
  }),
  tagTypes: ['Board','Column','Card','Plan','Workout','Metric','Product','Order'],
  endpoints: (b) => ({
    login: b.mutation<{access:string;refresh:string}, {username:string;password:string}>({ query: (body) => ({ url: 'auth/token/', method: 'POST', body }) }),
    me: b.query<any, void>({ query: () => 'accounts/me/' }),
    boards: b.query<any[], void>({ query: () => 'tracker/boards/' }),
    createBoard: b.mutation<any, Partial<any>>({ query: (body) => ({ url: 'tracker/boards/', method: 'POST', body }) }),
    moveCard: b.mutation<any, {id:number; column:number; position:number}>({ query: ({id, ...body}) => ({ url: `tracker/cards/${id}/move/`, method: 'POST', body }) }),
    generatePlan: b.mutation<any, {name:string;start_date:string;weeks:number}>({ query: (body) => ({ url: 'training/plans/generate/', method: 'POST', body }) }),
    products: b.query<any[], void>({ query: () => 'shop/products/' }),
    createOrder: b.mutation<any, {items:{product_id:number;quantity:number}[]}>({
      query: (body) => ({ url: 'shop/orders/', method: 'POST', body })
    }),
    payOrder: b.mutation<any, {id:number; token?:string}>({ query: ({id, ...body}) => ({ url: `shop/orders/${id}/pay/`, method: 'POST', body }) }),
  })
})
export const {
  useLoginMutation, useMeQuery, useBoardsQuery, useCreateBoardMutation,
  useMoveCardMutation, useGeneratePlanMutation, useProductsQuery,
  useCreateOrderMutation, usePayOrderMutation
} = portfolioApi
