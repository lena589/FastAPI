"""Основной модуль запуска FastAPI-приложения."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as api_router

@asynccontextmanager
async def lifespan(app_instance: FastAPI):

    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
