import pytest
from rest_framework.test import APIClient
from ..models import Todo

# Fixtures - 테스트에서 공통으로 사용하는 데이터/객체


@pytest.fixture
def client():
    # DRF 전용 테스트 클라이언트
    return APIClient()


@pytest.fixture
def todo(db):
    # 테스트용 기본 Todo 1개 생성
    # → retrieve / update / delete 테스트에서 사용
    return Todo.objects.create(
        name="운동",
        description="스쿼트 50회",
        complete=False,
        exp=10,
    )


# Todo API CRUD 동작을 검증하는 테스트 함수들


# 목록 조회 테스트 (GET /list/)
@pytest.mark.django_db
def test_list(client):
    res = client.get("/todo/api/list/")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


# 생성 테스트 (POST /create/)
@pytest.mark.django_db
def test_create(client):
    payload = {
        "name": "공부",
        "description": "DRF",
        "complete": False,
        "exp": 5,
    }

    res = client.post("/todo/api/create/", payload, format="json")

    assert res.status_code == 201
    # setUp에서 생성한 1개 없이 시작 → 새로 생성 1개만 존재
    assert Todo.objects.count() == 1


# 상세 조회 테스트 (GET /retrieve/<pk>/)
@pytest.mark.django_db
def test_retrieve(client, todo):
    res = client.get(f"/todo/api/retrieve/{todo.id}/")

    assert res.status_code == 200
    assert res.json()["name"] == "운동"


# 수정 테스트 (PATCH /update/<pk>/)
@pytest.mark.django_db
def test_update_patch(client, todo):
    payload = {"name": "운동(수정)"}

    res = client.patch(f"/todo/api/update/{todo.id}/", payload, format="json")

    assert res.status_code == 200

    # DB에서 다시 불러와서 실제 값이 변경되었는지 확인
    todo.refresh_from_db()
    assert todo.name == "운동(수정)"


# 삭제 테스트 (DELETE /delete/<pk>/)
@pytest.mark.django_db
def test_delete(client, todo):
    res = client.delete(f"/todo/api/delete/{todo.id}/")

    assert res.status_code == 204
    assert not Todo.objects.filter(id=todo.id).exists()


# 존재하지 않는 데이터 요청 시 404 테스트
@pytest.mark.django_db
def test_not_found_returns_404(client):
    res = client.get("/todo/api/retrieve/999999/")

    assert res.status_code == 404
