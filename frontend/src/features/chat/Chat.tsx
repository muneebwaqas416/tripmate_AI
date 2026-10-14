import { skipToken } from '@reduxjs/toolkit/query'
import { useEffect, useRef, useState, type FormEvent } from 'react'
import { useGetChatHistoryQuery, useSendMessageMutation } from '../../app/api'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import type { ChatMessage } from '../../types/chat'
import { newConversation, setThreadId } from './chatSlice'

const SUGGESTIONS = [
  'Plan a 5-day trip to Tokyo in spring',
  'Which airports serve Istanbul?',
  'Weekend getaway ideas from London under £300',
]

export default function Chat() {
  const dispatch = useAppDispatch()
  const threadId = useAppSelector((state) => state.chat.threadId)
  const { data: history } = useGetChatHistoryQuery(threadId ?? skipToken)
  const [sendMessage, { isLoading, error }] = useSendMessageMutation()
  const [input, setInput] = useState('')
  const [pending, setPending] = useState<ChatMessage | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const messages: ChatMessage[] = [
    ...(threadId ? (history?.messages ?? []) : []),
    ...(pending ? [pending] : []),
  ]

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages.length, isLoading])

  const submit = async (text: string) => {
    const message = text.trim()
    if (!message || isLoading) return
    setInput('')
    setPending({ role: 'user', content: message })
    try {
      const res = await sendMessage({ message, thread_id: threadId }).unwrap()
      if (res.thread_id !== threadId) dispatch(setThreadId(res.thread_id))
    } catch {
      setInput(message)
    } finally {
      setPending(null)
    }
  }

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    void submit(input)
  }

  return (
    <div className="chat">
      <header className="chat__header">
        <h1>✈️ TripMate AI</h1>
        <button type="button" onClick={() => dispatch(newConversation())} disabled={isLoading}>
          New trip
        </button>
      </header>

      <main className="chat__messages">
        {messages.length === 0 && (
          <div className="chat__empty">
            <p>Where would you like to go? Ask me to plan your next trip.</p>
            <div className="chat__suggestions">
              {SUGGESTIONS.map((s) => (
                <button key={s} type="button" onClick={() => void submit(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble bubble--${m.role}`}>
            {m.content}
          </div>
        ))}
        {isLoading && <div className="bubble bubble--assistant bubble--typing">Planning…</div>}
        {error && !isLoading && (
          <div className="chat__error">Something went wrong. Please try again.</div>
        )}
        <div ref={bottomRef} />
      </main>

      <form className="chat__input" onSubmit={onSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about destinations, flights, itineraries…"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}
