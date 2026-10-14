export type ChatRole = 'user' | 'assistant'

export interface ChatMessage {
  role: ChatRole
  content: string
}

export interface ChatRequest {
  message: string
  thread_id?: string | null
}

export interface ChatResponse {
  thread_id: string
  reply: ChatMessage
}

export interface ChatHistory {
  thread_id: string
  messages: ChatMessage[]
}
