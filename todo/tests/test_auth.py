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

    def test_other_user_cannot_look(self, api_client, client):
        login_res = api_client.get("/me/")
        notlogin_res = client.get("/me/")

        assert login_res.status_code == 200
        assert notlogin_res.status_code == 401


@pytest.mark.django_db
class TestTodoOwnership:
    def test_unauthenticated_list(self, client):
        res = client.get(reverse("todo:todo-list"))

        # IsAuthenticated 설정으로 비인증 사용자는 401
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
        # assert res.status_code == 403
        assert res.status_code == 401

    def test_authenticated_list_shows_all(self, api_client, todo, another_user_todo):
        res = api_client.get(reverse("todo:todo-list"))
        assert res.status_code == 200
        ids = [item["id"] for item in res.data["data"]]
        # Step 10: queryset이 전체 공개로 변경되어 다른 유저 Todo도 보임
        assert todo.id in ids
        assert another_user_todo.id in ids

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

    def test_can_access_other_user_todo(self, api_client, another_user_todo):
        # Step 10: queryset 전체 공개로 변경되어 다른 유저 Todo 조회 가능
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.get(url)
        assert res.status_code == 200

    def test_can_update_other_user_todo(self, api_client, another_user_todo):
        # Step 10: queryset 전체 공개로 변경되어 다른 유저 Todo 수정 가능
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.patch(url, {"name": "수정시도"})
        assert res.status_code == 403  # 수정 ViewSet의 인증때문에 200에서 수정.

    def test_can_delete_other_user_todo(self, api_client, another_user_todo):
        # Step 10: queryset 전체 공개로 변경되어 다른 유저 Todo 삭제 가능
        url = reverse("todo:todo-detail", kwargs={"pk": another_user_todo.pk})
        res = api_client.delete(url)
        assert res.status_code == 403  # 수정 ViewSet의 인증때문에 200에서 수정.
