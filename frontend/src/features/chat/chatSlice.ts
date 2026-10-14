import { createSlice, type PayloadAction } from '@reduxjs/toolkit'

const STORAGE_KEY = 'tripmate.threadId'

const readThreadId = (): string | null => {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

const writeThreadId = (threadId: string | null) => {
  try {
    if (threadId) localStorage.setItem(STORAGE_KEY, threadId)
    else localStorage.removeItem(STORAGE_KEY)
  } catch {
    // storage unavailable (private mode etc.) — thread just won't persist
  }
}

interface ChatState {
  threadId: string | null
}

const initialState: ChatState = { threadId: readThreadId() }

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    setThreadId(state, action: PayloadAction<string>) {
      state.threadId = action.payload
      writeThreadId(action.payload)
    },
    newConversation(state) {
      state.threadId = null
      writeThreadId(null)
    },
  },
})

export const { setThreadId, newConversation } = chatSlice.actions
export default chatSlice.reducer
