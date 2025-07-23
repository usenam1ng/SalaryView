from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from database.database import create_tables
from routers.router import router as tasks_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    logger.info('База данных готова')
    yield
    logger.info('Выкл')

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)