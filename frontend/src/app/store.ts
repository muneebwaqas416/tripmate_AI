import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import chatReducer from '../features/chat/chatSlice'
import { tripmateApi } from './api'

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    [tripmateApi.reducerPath]: tripmateApi.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(tripmateApi.middleware),
})

setupListeners(store.dispatch)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
