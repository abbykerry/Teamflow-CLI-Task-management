import os
import json
import tempfile
import pytest

from services import user_service, project_service, task_service
from models.user import User
from models.project import Project
from models.task import Task

# helper fixtures to isolate file data
@ pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Ensure services read/write from a temporary data directory."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    # also reset internal paths if they were computed at import time
    user_service.DATA_DIR = data_dir
    user_service.USERS_FILE = data_dir / "users.json"
    project_service.DATA_DIR = data_dir
    project_service.PROJECTS_FILE = data_dir / "projects.json"
    task_service.DATA_DIR = data_dir
    task_service.TASKS_FILE = data_dir / "tasks.json"
    yield


def test_create_and_load_user():
    # initially no users
    assert user_service.load_users() == []

    u1 = user_service.create_user("alice", "pwdhash", "admin")
    assert isinstance(u1, User)
    assert u1.username == "alice"
    assert u1.role == "admin"

    # saving occurs inside create_user, so file should now exist
    assert user_service.USERS_FILE.exists()
    users = user_service.load_users()
    assert len(users) == 1
    assert users[0].username == "alice"

    # duplicate username should raise
    with pytest.raises(ValueError):
        user_service.create_user("alice", "pwd2", "user")


def test_project_lifecycle():
    u = user_service.create_user("bob", "x", "user")
    p = project_service.create_project("proj1", "desc", u.id)
    assert isinstance(p, Project)
    assert p.name == "proj1"
    assert p.owner_id == u.id

    # load should return same
    loaded = project_service.load_projects()
    assert len(loaded) == 1
    assert loaded[0].name == "proj1"

    # create another, id auto increments
    p2 = project_service.create_project("proj2", "", u.id)
    assert p2.id == p.id + 1


def test_task_lifecycle():
    u = user_service.create_user("carol", "h", "user")
    p = project_service.create_project("proj", "desc", u.id)
    t = task_service.create_task(p.id, "t1", "", u.id)
    assert isinstance(t, Task)
    assert t.project_id == p.id
    assert t.title == "t1"
    assert t.assigned_to == u.id

    all_tasks = task_service.load_tasks()
    assert len(all_tasks) == 1

    # unassigned allowed
    t2 = task_service.create_task(p.id, "t2", "", None)
    assert t2.assigned_to is None


def test_update_task_assignment():
    """Tasks can be reassigned using the service helper"""
    u1 = user_service.create_user("ed", "a", "user")
    u2 = user_service.create_user("frank", "b", "user")
    p = project_service.create_project("proj", "desc", u1.id)
    t = task_service.create_task(p.id, "reassignable", "", u1.id)
    assert t.assigned_to == u1.id

    # perform reassignment
    updated = task_service.update_task_assignment(t.id, u2.id)
    assert updated.assigned_to == u2.id
    # check persisted in storage
    all_tasks = task_service.load_tasks()
    assert any(task.id == t.id and task.assigned_to == u2.id for task in all_tasks)

    # invalid task should raise
    with pytest.raises(ValueError):
        task_service.update_task_assignment(9999, u2.id)


# extra safety: verify JSON data structure matches expectations

def test_user_file_json_format():
    user_service.create_user("dan", "a", "user")
    txt = user_service.USERS_FILE.read_text()
    data = json.loads(txt)
    assert isinstance(data, list)
    assert "username" in data[0]


# ensure load functions handle malformed json gracefully

def test_load_malformed(monkeypatch, tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not json")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    user_service.DATA_DIR = tmp_path
    user_service.USERS_FILE = bad_file
    # should not raise, just return []
    assert user_service.load_users() == []
