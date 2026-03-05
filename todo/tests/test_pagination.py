import pytest
from rest_framework.test import APIClient
from todo.models import Todo

# pytest todo/tests/test_pagination.py -v


# fixture
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_todos(db):
    """테스트용 Todo 7개 생성 (PAGE_SIZE=3 기준으로 3페이지 구성)"""
    for i in range(1, 8):
        Todo.objects.create(name=f"Todo {i}", description=f"설명 {i}")


# 1. 응답 구조 키 검증
@pytest.mark.django_db
def test_pagination_response_keys(client, create_todos):
    """응답에 필수 키가 모두 존재하는지 검증"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    assert response.status_code == 200
    assert "data" in data
    assert "page_size" in data
    assert "total_count" in data
    assert "page_count" in data
    assert "current_page" in data
    assert "next" in data
    assert "previous" in data


# 2. PAGE_SIZE 개수 검증
@pytest.mark.django_db
def test_pagination_page_size(client, create_todos):
    """1페이지 응답 데이터가 PAGE_SIZE(3)개인지 검증"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    assert len(data["data"]) == 3


# 3. next / previous URL 검증
@pytest.mark.django_db
def test_pagination_first_page(client, create_todos):
    """첫 페이지는 previous가 null이어야 함"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    assert data["previous"] is None
    assert data["next"] is not None


@pytest.mark.django_db
def test_pagination_last_page(client, create_todos):
    """마지막 페이지는 next가 null이어야 함"""
    response = client.get("/todo/viewsets/view/?page=1")
    last_page = response.json()["page_count"]

    response = client.get(f"/todo/viewsets/view/?page={last_page}")
    data = response.json()

    assert data["next"] is None
    assert data["previous"] is not None


# 4. page_size 쿼리 파라미터 동작 검증
@pytest.mark.django_db
def test_pagination_custom_page_size(client, create_todos):
    """?page_size=5 요청 시 5개 반환 검증"""
    response = client.get("/todo/viewsets/view/?page=1&page_size=5")
    data = response.json()

    assert len(data["data"]) == 5


# 5. 범위 초과 페이지 요청
@pytest.mark.django_db
def test_pagination_out_of_range(client, create_todos):
    """존재하지 않는 페이지 요청 시 404 반환 검증"""
    response = client.get("/todo/viewsets/view/?page=999")

    assert response.status_code == 404


# 6. total_count 정확성 검증
@pytest.mark.django_db
def test_pagination_total_count(client, create_todos):
    """total_count가 실제 DB 데이터 수와 일치하는지 검증"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    assert data["total_count"] == Todo.objects.count()


# 7. page_size=all 파라미터 동작 검증
@pytest.mark.django_db
def test_pagination_page_size_all(client, create_todos):
    """?page_size=all 요청 시 전체 데이터가 반환되는지 검증"""
    response = client.get("/todo/viewsets/view/?page=1&page_size=all")
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == Todo.objects.count()


# 8. 유효하지 않은 page_size 값 입력 시 기본값 fallback 검증
@pytest.mark.django_db
def test_pagination_invalid_page_size_fallback(client, create_todos):
    """?page_size=abc 처럼 숫자가 아닌 값 입력 시 기본 PAGE_SIZE(3)으로 동작하는지 검증"""
    response = client.get("/todo/viewsets/view/?page=1&page_size=abc")
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 3
