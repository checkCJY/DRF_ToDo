import pytest
from django.urls import reverse

"""
DRF DefaultRouter 자동 생성 URL 이름 (basename="todo")
todo:todo-list         → GET  /todo/viewsets/view/         (목록 조회)
todo:todo-list         → POST /todo/viewsets/view/         (생성)
todo:todo-detail       → GET  /todo/viewsets/view/{pk}/   (단일 조회)
todo:todo-detail       → PATCH /todo/viewsets/view/{pk}/  (부분 수정)
todo:todo-detail       → DELETE /todo/viewsets/view/{pk}/ (삭제)

accounts URL
api-signup  → POST /api/signup/  (회원가입)
api-login   → POST /api/login/   (로그인)
api-logout  → POST /api/logout/  (로그아웃)
"""


@pytest.mark.django_db
class TestAuth:
    def test_signup_success(self, client):
        res = client.post(
            "/api/signup/",
            {
                "username": "newuser",
                "password": "pass1234",
                "password2": "pass1234",
            },
            content_type="application/json",
        )
        assert res.status_code == 201

    def test_signup_duplicate_username(self, client, user):
        res = client.post(
            "/api/signup/",
            {
                "username": "testuser",
                "password": "pass1234",
                "password2": "pass1234",
            },
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_signup_password_mismatch(self, client):
        res = client.post(
            "/api/signup/",
            {
                "username": "newuser",
                "password": "pass1234",
                "password2": "wrongpass",
            },
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_login_success(self, client, user):
        res = client.post(
            "/api/login/",
            {
                "username": "testuser",
                "password": "testpass",
            },
            content_type="application/json",
        )
        assert res.status_code == 200

    def test_logout_success(self, api_client):
        res = api_client.post("/api/logout/")
        assert res.status_code == 200


@pytest.mark.django_db
class TestTodoOwnership:
    def test_unauthenticated_list(self, client):
        res = client.get(reverse("todo:todo-list"))
        
        # 세션방식 인증 없으면 403
        # JWT는 인증없으면 401
        #assert res.status_code == 403
        assert res.status_code == 401

    def test_unauthenticated_create(self, client):
        res = client.post(
            reverse("todo:todo-list"),
            {
                "name": "테스트",
                "exp": 0,
            },
        )
        
        # 세션방식 인증 없으면 403
        # JWT는 인증없으면 401
        #assert res.status_code == 403
        assert res.status_code == 401

    def test_authenticated_list_only_mine(self, api_client, todo, another_user_todo):
        res = api_client.get(reverse("todo:todo-list"))
        assert res.status_code == 200
        ids = [item["id"] for item in res.data["data"]]
        assert todo.id in ids
        assert another_user_todo.id not in ids

    def test_create_auto_assign_user(self, api_client, user):
        res = api_client.post(
            reverse("todo:todo-list"),
            {
                "name": "자동유저주입",
                "exp": 0,
            },
        )
        assert res.status_code == 201
        assert res.data["user"] == user.id

    def test_cannot_access_other_user_todo(self, api_client, another_user_todo):
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.get(url)
        assert res.status_code == 404

    def test_cannot_update_other_user_todo(self, api_client, another_user_todo):
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.patch(url, {"name": "수정시도"})
        assert res.status_code == 404

    def test_cannot_delete_other_user_todo(self, api_client, another_user_todo):
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.delete(url)
        assert res.status_code == 404
