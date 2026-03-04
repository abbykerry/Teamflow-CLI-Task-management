import pytest
from io import StringIO
import sys

from auth.session import Session
from cli import task_cli, project_cli, menu
from services import user_service, project_service, task_service


@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("DATA_DIR", str(data_dir))

    user_service.DATA_DIR = data_dir
    user_service.USERS_FILE = data_dir / "users.json"
    project_service.DATA_DIR = data_dir
    project_service.PROJECTS_FILE = data_dir / "projects.json"
    task_service.DATA_DIR = data_dir
    task_service.TASKS_FILE = data_dir / "tasks.json"
    yield


def capture_output(func, *args, **kwargs):
    """Helper that captures stdout of a callable."""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_view_all_tasks_table(monkeypatch):
    admin = user_service.create_user("admin", "x", "admin")
    user = user_service.create_user("user", "x", "user")
    p = project_service.create_project("proj", "", admin.id)
    task_service.create_task(p.id, "task1", "", user.id)
    task_service.create_task(p.id, "task2", "", None)

    session = Session()
    session.current_user = admin

    out = capture_output(task_cli.view_all_tasks_action, session)
    assert "ALL TASKS" in out
    assert "task1" in out
    assert "Unassigned" in out


def test_reassign_task_via_cli(monkeypatch):
    admin = user_service.create_user("admin", "x", "admin")
    u1 = user_service.create_user("u1", "x", "user")
    u2 = user_service.create_user("u2", "x", "user")
    p = project_service.create_project("proj", "", admin.id)
    t = task_service.create_task(p.id, "todo", "", u1.id)

    session = Session()
    session.current_user = admin

    # simulate menu interactions: first show tasks list, then choose task id, then assign to u2
    inputs = iter([str(t.id), str(u2.id)])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))

    out = capture_output(task_cli.reassign_task_action, session)
    assert "reassigned to" in out
    assert u2.username in out
    tasks = task_service.load_tasks()
    assert any(tt.id == t.id and tt.assigned_to == u2.id for tt in tasks)


def test_project_dashboard_table(monkeypatch):
    admin = user_service.create_user("admin", "x", "admin")
    user = user_service.create_user("joe", "x", "user")
    p = project_service.create_project("proj", "desc", admin.id)
    task_service.create_task(p.id, "t1", "", user.id)

    session = Session()
    session.current_user = admin

    # make the projects_menu return "3" (view dashboard) then "5" (back)
    choices = iter(["3", "5"])
    monkeypatch.setattr(menu, "projects_menu", lambda: next(choices))

    out = capture_output(project_cli.handle_project_actions, session)
    assert "PROJECT DASHBOARD" in out
    assert "t1" in out


def test_create_task_unassigned_cli(monkeypatch):
    """Admin can create a task without immediately assigning a user."""
    admin = user_service.create_user("admin", "x", "admin")
    p = project_service.create_project("proj", "desc", admin.id)

    session = Session()
    session.current_user = admin
    inputs = iter([str(p.id), "n", "some task title"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))

    out = capture_output(task_cli.create_task_action, session)
    assert "created successfully" in out
    tasks = task_service.load_tasks()
    assert len(tasks) == 1
    assert tasks[0].assigned_to is None


# ensure that tables work without rich (ascii fallback)
def test_display_table_fallback(monkeypatch, capsys):
    from utils import table_utils
    monkeypatch.setattr(table_utils, "_RICH_AVAILABLE", False)
    headers = ["A", "B"]
    rows = [["one", "two"], ["three", "four"]]
    table_utils.display_table("TITLE", headers, rows)
    captured = capsys.readouterr()
    assert "TITLE" in captured.out
    assert "+" in captured.out  # ascii sep
    assert "one" in captured.out
