import pytest
from rest_framework.test import APIClient
from ..models import Todo

# 실행 명령어
# pytest todo/tests/test_viewset_crud.py

# ViewSet API 기본 URL 상수
BASE_URL = "/todo/viewsets/view/"

# Fixtures: 테스트용 공통 객체 및 데이터 세팅


@pytest.fixture
def client():
    """DRF 전용 API 테스트 클라이언트 생성"""
    return APIClient()


@pytest.fixture
def todo(db):
    """테스트용 기본 Todo 데이터 1개 생성 (DB 접근 허용)"""
    return Todo.objects.create(
        name="운동",
        description="스쿼트 50회",
        complete=False,
        exp=10,
    )


# ViewSet CRUD 검증 테스트 함수들


@pytest.mark.django_db
def test_list(client, todo):
    """목록 조회 검증 (최소 1개 이상의 리스트 반환)"""
    res = client.get(BASE_URL)

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1


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
