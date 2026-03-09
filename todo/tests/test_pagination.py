import pytest
from rest_framework.test import APIClient
from todo.models import Todo

# pytest todo/tests/test_pagination.py -v


# fixture
@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def create_todos(db, user):
    """테스트용 Todo 7개 생성 (PAGE_SIZE=3 기준으로 3페이지 구성)"""
    for i in range(1, 8):
        Todo.objects.create(name=f"Todo {i}", description=f"설명 {i}", user=user)


# 1. 응답 구조 키 검증
@pytest.mark.django_db
def test_pagination_response_keys(client, create_todos):
    """응답에 필수 키가 모두 존재하는지 검증"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    assert response.status_code == 200
    # Step 10: list() 커스텀 응답 구조 기준 (page_size, total_count 없음)
    assert "data" in data
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
    """첫 페이지는 previous가 False이어야 함"""
    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    # Step 10: next/previous가 URL 대신 boolean으로 변경됨
    assert data["previous"] is False
    assert data["next"] is True


@pytest.mark.django_db
def test_pagination_last_page(client, create_todos):
    """마지막 페이지는 next가 False이어야 함"""
    response = client.get("/todo/viewsets/view/?page=1")
    last_page = response.json()["page_count"]

    response = client.get(f"/todo/viewsets/view/?page={last_page}")
    data = response.json()

    # Step 10: next/previous가 URL 대신 boolean으로 변경됨
    assert data["next"] is False
    assert data["previous"] is True


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


# 6. page_count 정확성 검증
@pytest.mark.django_db
def test_pagination_page_count(client, create_todos):
    """page_count가 데이터 수 / page_size(3) 올림 값과 일치하는지 검증"""
    # Step 10: total_count 키 없음 → page_count로 검증
    import math

    response = client.get("/todo/viewsets/view/?page=1")
    data = response.json()

    expected_page_count = math.ceil(Todo.objects.count() / 3)
    assert data["page_count"] == expected_page_count


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
