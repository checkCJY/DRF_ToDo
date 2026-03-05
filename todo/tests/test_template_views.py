import pytest
from django.test import Client
from ..models import Todo

# pytest todo/tests/test_template_views.py -v


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def todo(db):
    return Todo.objects.create(name="운동", description="스쿼트 50회", exp=10)


# ── TodoListView ──────────────────────────────────────────────


@pytest.mark.django_db
def test_list_view_status(client):
    """목록 페이지 GET 요청 시 200 응답 검증"""
    res = client.get("/todo/list/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_list_view_template(client):
    """목록 페이지에 올바른 템플릿이 사용되는지 검증"""
    res = client.get("/todo/list/")
    assert "todo/list.html" in [t.name for t in res.templates]


@pytest.mark.django_db
def test_list_view_context(client, todo):
    """context에 'todos' 키가 존재하고 생성한 todo가 포함되는지 검증"""
    res = client.get("/todo/list/")
    assert "todos" in res.context
    assert todo in res.context["todos"]


# ── TodoCreateView ────────────────────────────────────────────


@pytest.mark.django_db
def test_create_view_get(client):
    """생성 페이지 GET 요청 시 200 응답 검증"""
    res = client.get("/todo/create/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_create_view_post(client, db):
    """유효한 POST 제출 후 redirect 및 DB 저장 검증"""
    payload = {"name": "공부", "description": "DRF", "complete": False, "exp": 5}
    res = client.post("/todo/create/", payload)
    assert res.status_code == 302
    assert Todo.objects.filter(name="공부").exists()


# ── TodoDetailView ────────────────────────────────────────────


@pytest.mark.django_db
def test_detail_view_status(client, todo):
    """상세 페이지 GET 요청 시 200 응답 검증"""
    res = client.get(f"/todo/detail/{todo.id}/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_detail_view_context(client, todo):
    """context에 'todo' 키가 존재하고 올바른 데이터를 담는지 검증"""
    res = client.get(f"/todo/detail/{todo.id}/")
    assert "todo" in res.context
    assert res.context["todo"].name == "운동"


@pytest.mark.django_db
def test_detail_view_not_found(client):
    """존재하지 않는 pk 요청 시 404 응답 검증"""
    res = client.get("/todo/detail/999999/")
    assert res.status_code == 404


# ── TodoUpdateView ────────────────────────────────────────────


@pytest.mark.django_db
def test_update_view_get(client, todo):
    """수정 페이지 GET 요청 시 200 응답 검증"""
    res = client.get(f"/todo/update/{todo.id}/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_update_view_post(client, todo):
    """유효한 POST 제출 후 redirect 및 DB 값 변경 검증"""
    payload = {
        "name": "운동(수정)",
        "description": "수정된 설명",
        "complete": True,
        "exp": 20,
    }
    res = client.post(f"/todo/update/{todo.id}/", payload)
    assert res.status_code == 302
    todo.refresh_from_db()
    assert todo.name == "운동(수정)"
