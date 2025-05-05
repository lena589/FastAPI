"""Модуль для работы с базой данных и определения моделей SQLAlchemy."""

from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass

class UserOrm(Model):
    """Модель пользователя."""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    tasks: Mapped[list["TaskOrm"]] = relationship(back_populates="user")

class CategoryOrm(Model):
    """Модель категории задачи."""
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    tasks: Mapped[list["TaskOrm"]] = relationship(back_populates="category")

class TaskOrm(Model):
    """Модель задачи."""
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserOrm"] = relationship(back_populates="tasks")
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[Optional["CategoryOrm"]] = relationship(back_populates="tasks")

async def create_tables():
    """Создает все таблицы в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    """Удаляет все таблицы из базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
