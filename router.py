from typing import List, Optional
from fastapi import APIRouter, Form, Query

from scheme import User, UserId, Category, CategoryId, Task, TaskId
from repository import UserRepository, CategoryRepository, TaskRepository

router = APIRouter(
    prefix="/api",
    tags=["API"]
)

"""Модуль router.py содержит роутеры FastAPI для работы с пользователями, категориями и задачами."""

@router.post("/users/", response_model=UserId)
async def create_user(
    username: str = Form(...),
    password: str = Form(...)
):
    """Создаёт нового пользователя."""
    user_id = await UserRepository.create_user_form(username, password)
    return {"ok": True, "user_id": user_id}

@router.get("/users/", response_model=List[User])
async def get_users():
    """Возвращает список всех пользователей."""
    users = await UserRepository.get_users()
    return users

@router.delete("/users/{user_id}", response_model=UserId)
async def delete_user(user_id: int):
    """Удаляет пользователя по его идентификатору."""
    deleted = await UserRepository.delete_user(user_id)
    return {"ok": deleted, "user_id": user_id}

@router.post("/categories/", response_model=CategoryId)
async def create_category(
    name: str = Form(...)
):
    """Создаёт новую категорию."""
    category_id = await CategoryRepository.create_category_form(name)
    return {"ok": True, "category_id": category_id}

@router.get("/categories/", response_model=List[Category])
async def get_categories():
    """Возвращает список всех категорий."""
    categories = await CategoryRepository.get_categories()
    return categories

@router.delete("/categories/{category_id}", response_model=CategoryId)
async def delete_category(category_id: int):
    """Удаляет категорию по её идентификатору."""
    deleted = await CategoryRepository.delete_category(category_id)
    return {"ok": deleted, "category_id": category_id}

@router.post("/tasks/", response_model=TaskId)
async def create_task(
    title: str = Form(...),
    user_id: int = Form(...),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None)
):
    """Создаёт новую задачу."""
    task_id = await TaskRepository.create_task_form(title, user_id, category_id, description)
    return {"ok": True, "task_id": task_id}

@router.get("/tasks/", response_model=List[Task])
async def get_tasks(
    category_ids: Optional[List[int]] = Query(None)
):
    """Возвращает список задач, с возможностью фильтрации по категориям."""
    tasks = await TaskRepository.get_tasks(category_ids)
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskId)
async def update_task(
    task_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None)
):
    """Обновляет задачу по её идентификатору."""
    updated = await TaskRepository.update_task_form(task_id, title, description, category_id)
    return {"ok": updated, "task_id": task_id}

@router.delete("/tasks/{task_id}", response_model=TaskId)
async def delete_task(task_id: int):
    """Удаляет задачу по её идентификатору."""
    deleted = await TaskRepository.delete_task(task_id)
    return {"ok": deleted, "task_id": task_id}
