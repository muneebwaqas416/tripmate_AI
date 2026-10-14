from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.tools import get_tools
from app.core.config import settings

_templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "prompts"),
    autoescape=False,
)


def _system_prompt() -> SystemMessage:
    template = _templates.get_template("system.jinja2")
    return SystemMessage(content=template.render(today=date.today().isoformat()))


def build_graph(checkpointer: BaseCheckpointSaver):
    tools = get_tools()
    llm = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key).bind_tools(tools)

    async def assistant(state: MessagesState) -> dict:
        response = await llm.ainvoke([_system_prompt(), *state["messages"]])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    return builder.compile(checkpointer=checkpointer)
