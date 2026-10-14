import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from app.agent.graph import build_graph
from app.api.routes import chat, health
from app.core.config import settings

logger = logging.getLogger("tripmate")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.database_url:
        async with AsyncConnectionPool(
            conninfo=settings.database_url,
            max_size=10,
            kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
        ) as pool:
            checkpointer = AsyncPostgresSaver(pool)
            await checkpointer.setup()
            app.state.graph = build_graph(checkpointer)
            logger.info("Using Postgres checkpointer")
            yield
    else:
        logger.warning("DATABASE_URL not set; using in-memory checkpointer")
        app.state.graph = build_graph(InMemorySaver())
        yield


app = FastAPI(title="TripMate AI", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
