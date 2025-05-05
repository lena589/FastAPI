import pytest
from fastapi.testclient import TestClient
from main import app, lifespan
import asyncio

client = TestClient(app)

def test_lifespan():
    async def run():
        async with lifespan(app):
            pass
    asyncio.run(run())

def test_main_app():
    response = client.get("/api/users/")
    assert response.status_code in (200, 404)

def test_create_user():
    response = client.post(
        "/api/users/",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert isinstance(response.json()["user_id"], int)

def test_get_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    if users:
        assert "id" in users[0]
        assert "username" in users[0]

def test_delete_user():
    user = client.post(
        "/api/users/",
        data={"username": "todelete", "password": "pass"}
    ).json()
    user_id = user["user_id"]
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_create_category():
    response = client.post(
        "/api/categories/",
        data={"name": "testcategory"}
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert isinstance(response.json()["category_id"], int)

def test_get_categories():
    response = client.get("/api/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    if categories:
        assert "id" in categories[0]
        assert "name" in categories[0]

def test_delete_category():
    category = client.post(
        "/api/categories/",
        data={"name": "todelete"}
    ).json()
    category_id = category["category_id"]
    response = client.delete(f"/api/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_create_task():
    user = client.post(
        "/api/users/",
        data={"username": "taskuser", "password": "pass"}
    ).json()
    category = client.post(
        "/api/categories/",
        data={"name": "taskcategory"}
    ).json()
    response = client.post(
        "/api/tasks/",
        data={
            "title": "testtask",
            "user_id": user["user_id"],
            "category_id": category["category_id"],
            "description": "test description"
        }
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert isinstance(response.json()["task_id"], int)

def test_get_tasks():
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    if tasks:
        assert "id" in tasks[0]
        assert "title" in tasks[0]
        assert "user_id" in tasks[0]

def test_filter_tasks_by_category():
    user = client.post(
        "/api/users/",
        data={"username": "filteruser", "password": "pass"}
    ).json()
    category = client.post(
        "/api/categories/",
        data={"name": "filtercategory"}
    ).json()
    task = client.post(
        "/api/tasks/",
        data={
            "title": "filtertask",
            "user_id": user["user_id"],
            "category_id": category["category_id"],
            "description": "filter description"
        }
    ).json()
    response = client.get(
        "/api/tasks/",
        params={"category_ids": [category["category_id"]]}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    assert tasks[0]["category_id"] == category["category_id"]

def test_update_task():
    user = client.post(
        "/api/users/",
        data={"username": "updateuser", "password": "pass"}
    ).json()
    task = client.post(
        "/api/tasks/",
        data={
            "title": "update_task",
            "user_id": user["user_id"],
            "description": "old description"
        }
    ).json()
    response = client.put(
        f"/api/tasks/{task['task_id']}",
        data={"title": "updated_title", "description": "new description"}
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_delete_task():
    user = client.post(
        "/api/users/",
        data={"username": "deleteuser", "password": "pass"}
    ).json()
    task = client.post(
        "/api/tasks/",
        data={
            "title": "deletetask",
            "user_id": user["user_id"]
        }
    ).json()
    response = client.delete(f"/api/tasks/{task['task_id']}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_delete_nonexistent():
    response = client.delete("/api/users/999999")
    assert response.status_code == 200
    assert response.json()["ok"] is False

    response = client.delete("/api/categories/999999")
    assert response.status_code == 200
    assert response.json()["ok"] is False

    response = client.delete("/api/tasks/999999")
    assert response.status_code == 200
    assert response.json()["ok"] is False
