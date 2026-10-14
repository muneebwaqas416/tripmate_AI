import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { ChatHistory, ChatRequest, ChatResponse } from '../types/chat'

export const tripmateApi = createApi({
  reducerPath: 'tripmateApi',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_BASE_URL ?? '/api',
  }),
  tagTypes: ['ChatHistory'],
  endpoints: (builder) => ({
    getHealth: builder.query<{ status: string }, void>({
      query: () => '/health',
    }),
    getChatHistory: builder.query<ChatHistory, string>({
      query: (threadId) => `/chat/${threadId}`,
      providesTags: (_result, _error, threadId) => [{ type: 'ChatHistory', id: threadId }],
    }),
    sendMessage: builder.mutation<ChatResponse, ChatRequest>({
      query: (body) => ({ url: '/chat', method: 'POST', body }),
      invalidatesTags: (result) =>
        result ? [{ type: 'ChatHistory', id: result.thread_id }] : [],
    }),
  }),
})

export const { useGetHealthQuery, useGetChatHistoryQuery, useSendMessageMutation } = tripmateApi
