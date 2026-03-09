import pytest
from rest_framework.test import APIClient
from ..models import Todo
from django.urls import reverse


# 실행 명령어
# pytest todo/tests/test_viewset_crud.py

# ViewSet API 기본 URL 상수
BASE_URL = "/todo/viewsets/view/"


@pytest.fixture
def client(user):
    """인증된 DRF 전용 API 테스트 클라이언트 생성"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ViewSet CRUD 검증 테스트 함수들


@pytest.mark.django_db
def test_list(client, todo):
    """목록 조회 검증 (페이지네이션 응답 구조, 최소 1개 이상의 데이터 반환)"""
    res = client.get(BASE_URL)

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, dict)
    assert "data" in data
    assert len(data["data"]) >= 1


@pytest.mark.django_db
def test_create(client, todo):
    """새로운 Todo 데이터 생성 및 DB 반영 검증"""
    payload = {
        "name": "공부",
        "description": "DRF",
        "complete": False,
        "exp": 5,
    }

    res = client.post(BASE_URL, payload, format="json")

    assert res.status_code in (200, 201)
    # fixture에서 1개 생성 + 여기서 1개 생성 = 총 2개여야 함
    assert Todo.objects.count() == 2


@pytest.mark.django_db
def test_retrieve(client, todo):
    """특정 Todo ID 상세 조회 시 정확한 데이터 반환 검증"""
    res = client.get(f"{BASE_URL}{todo.id}/")

    assert res.status_code == 200
    assert res.json()["name"] == "운동"


@pytest.mark.django_db
def test_partial_update_patch(client, todo):
    """Todo 부분 수정(PATCH) 성공 및 실제 DB 값 변경 검증"""
    payload = {"name": "운동(수정)"}

    res = client.patch(f"{BASE_URL}{todo.id}/", payload, format="json")

    assert res.status_code == 200

    todo.refresh_from_db()
    assert todo.name == "운동(수정)"


@pytest.mark.django_db
def test_destroy_delete(client, todo):
    """Todo 삭제 성공 및 DB에서 완전히 제거되었는지 검증"""
    res = client.delete(f"{BASE_URL}{todo.id}/")

    assert res.status_code in (200, 204)
    assert not Todo.objects.filter(id=todo.id).exists()


@pytest.mark.django_db
def test_not_found_returns_404(client):
    """존재하지 않는 엉뚱한 ID 요청 시 404 에러 반환 검증"""
    res = client.get(f"{BASE_URL}999999/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_full_update_put(client, todo):
    """Todo 전체 수정(PUT) 성공 및 실제 DB 값 변경 검증"""
    payload = {
        "name": "수영",
        "description": "접영 30분",
        "complete": True,
        "exp": 20,
    }

    res = client.put(f"{BASE_URL}{todo.id}/", payload, format="json")

    assert res.status_code == 200

    todo.refresh_from_db()
    assert todo.name == "수영"
    assert todo.description == "접영 30분"
    assert todo.complete is True
    assert todo.exp == 20


# Part 12: is_public=False 글은 작성자 본인만 보이는지 검증
@pytest.mark.django_db
def test_private_todo_visibility(api_client, private_todo, another_private_todo):
    """본인의 비공개 Todo는 보이고, 다른 유저의 비공개 Todo는 보이지 않아야 함"""
    res = api_client.get(reverse("todo:todo-list"))
    assert res.status_code == 200
    ids = [item["id"] for item in res.data["data"]]
    # 본인의 비공개 Todo는 보임
    assert private_todo.id in ids
    # 다른 유저의 비공개 Todo는 보이지 않음
    assert another_private_todo.id not in ids
