import uuid

from fastapi import APIRouter, HTTPException, Request
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from app.schemas.chat import ChatHistory, ChatMessage, ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


def _to_chat_message(message: BaseMessage) -> ChatMessage | None:
    """Convert LangChain messages to API messages, skipping tool calls/results."""
    if isinstance(message, HumanMessage):
        return ChatMessage(role="user", content=message.text)
    if isinstance(message, AIMessage) and message.text:
        return ChatMessage(role="assistant", content=message.text)
    return None


@router.post("", response_model=ChatResponse)
async def send_message(payload: ChatRequest, request: Request) -> ChatResponse:
    graph = request.app.state.graph
    thread_id = payload.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    try:
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=payload.message)]}, config=config
        )
    except Exception as exc:  # surface LLM/tool failures as a clean API error
        raise HTTPException(status_code=502, detail=f"Agent error: {exc}") from exc

    reply = _to_chat_message(result["messages"][-1])
    if reply is None:
        raise HTTPException(status_code=502, detail="Agent returned an empty reply")
    return ChatResponse(thread_id=thread_id, reply=reply)


@router.get("/{thread_id}", response_model=ChatHistory)
async def get_history(thread_id: str, request: Request) -> ChatHistory:
    graph = request.app.state.graph
    state = await graph.aget_state({"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", []) if state and state.values else []
    converted = [m for m in (_to_chat_message(msg) for msg in messages) if m]
    return ChatHistory(thread_id=thread_id, messages=converted)
