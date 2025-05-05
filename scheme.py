from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """Базовая схема пользователя."""
    username: str

class UserCreate(UserBase):
    """Схема для создания пользователя (с паролем)."""
    password: str

class User(UserBase):
    """Схема пользователя с ID."""
    id: int

class CategoryBase(BaseModel):
    """Базовая схема категории."""
    name: str

class CategoryCreate(CategoryBase):
    """Схема для создания категории."""
    pass

class Category(CategoryBase):
    """Схема категории с ID."""
    id: int

class TaskBase(BaseModel):
    """Базовая схема задачи."""
    title: str
    description: Optional[str] = None
    user_id: int
    category_id: Optional[int] = None

class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    pass

class Task(TaskBase):
    """Схема задачи с ID."""
    id: int

class TaskUpdate(BaseModel):
    """Схема для обновления задачи."""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class TaskId(BaseModel):
    """Схема с ID задачи и статусом операции."""
    ok: bool = True
    task_id: int

class CategoryId(BaseModel):
    """Схема с ID категории и статусом операции."""
    ok: bool = True
    category_id: int

class UserId(BaseModel):
    """Схема с ID пользователя и статусом операции."""
    ok: bool = True
    user_id: int
