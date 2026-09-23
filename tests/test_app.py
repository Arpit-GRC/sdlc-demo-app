import pytest
from app import app, _tasks, _next_id


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory store before every test so tests don't leak into each other."""
    _tasks.clear()
    import app as app_module
    app_module._next_id = 1
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_create_task(client):
    resp = client.post("/tasks", json={"title": "Write SETUP.md"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Write SETUP.md"
    assert body["completed"] is False
    assert "id" in body


def test_create_task_missing_title(client):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 400


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_get_task(client):
    created = client.post("/tasks", json={"title": "Task A"}).get_json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Task A"


def test_get_task_not_found(client):
    resp = client.get("/tasks/999")
    assert resp.status_code == 404


def test_update_task_completed(client):
    created = client.post("/tasks", json={"title": "Task A"}).get_json()
    resp = client.patch(f"/tasks/{created['id']}", json={"completed": True})
    assert resp.status_code == 200
    assert resp.get_json()["completed"] is True


def test_update_task_invalid_completed_type(client):
    created = client.post("/tasks", json={"title": "Task A"}).get_json()
    resp = client.patch(f"/tasks/{created['id']}", json={"completed": "yes"})
    assert resp.status_code == 400


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Task A"}).get_json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404
