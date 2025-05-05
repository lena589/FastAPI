from typing import List, Optional
from sqlalchemy import select

from database import new_session, UserOrm, CategoryOrm, TaskOrm
from scheme import User, Category, Task

class UserRepository:
    @classmethod
    async def create_user_form(cls, username: str, password: str) -> int:
        async with new_session() as session:
            user = UserOrm(username=username, password=password)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_users(cls) -> List[User]:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_schemas = [
                User.model_validate({
                    "id": user_model.id,
                    "username": user_model.username
                }) for user_model in user_models
            ]
            return user_schemas

    @classmethod
    async def delete_user(cls, user_id: int) -> bool:
        async with new_session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                return False
            await session.delete(user)
            await session.commit()
            return True

class CategoryRepository:
    @classmethod
    async def create_category_form(cls, name: str) -> int:
        async with new_session() as session:
            category = CategoryOrm(name=name)
            session.add(category)
            await session.flush()
            await session.commit()
            return category.id

    @classmethod
    async def get_categories(cls) -> List[Category]:
        async with new_session() as session:
            query = select(CategoryOrm)
            result = await session.execute(query)
            category_models = result.scalars().all()
            category_schemas = [
                Category.model_validate({
                    "id": category_model.id,
                    "name": category_model.name
                }) for category_model in category_models
            ]
            return category_schemas

    @classmethod
    async def delete_category(cls, category_id: int) -> bool:
        async with new_session() as session:
            category = await session.get(CategoryOrm, category_id)
            if not category:
                return False
            await session.delete(category)
            await session.commit()
            return True

class TaskRepository:
    @classmethod
    async def create_task_form(cls, title: str, user_id: int, category_id: Optional[int] = None, description: Optional[str] = None) -> int:
        async with new_session() as session:
            task = TaskOrm(title=title, user_id=user_id, category_id=category_id, description=description)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_tasks(cls, category_ids: Optional[List[int]] = None) -> List[Task]:
        async with new_session() as session:
            query = select(TaskOrm)
            if category_ids is not None and len(category_ids) > 0:
                query = query.where(TaskOrm.category_id.in_(category_ids))
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [
                Task.model_validate({
                    "id": task_model.id,
                    "title": task_model.title,
                    "description": task_model.description,
                    "user_id": task_model.user_id,
                    "category_id": task_model.category_id
                }) for task_model in task_models
            ]
            return task_schemas

    @classmethod
    async def update_task_form(cls, task_id: int, title: Optional[str] = None, description: Optional[str] = None, category_id: Optional[int] = None) -> bool:
        async with new_session() as session:
            task = await session.get(TaskOrm, task_id)
            if not task:
                return False
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if category_id is not None:
                task.category_id = category_id
            await session.commit()
            return True

    @classmethod
    async def delete_task(cls, task_id: int) -> bool:
        async with new_session() as session:
            task = await session.get(TaskOrm, task_id)
            if not task:
                return False
            await session.delete(task)
            await session.commit()
            return True
