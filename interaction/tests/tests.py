import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from todo.models import Todo
from interaction.models import TodoLike, TodoBookmark, TodoComment

User = get_user_model()


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def user(db):
    # 기본 테스트 유저
    return User.objects.create_user(username="testuser", password="pass1234")


@pytest.fixture
def another_user(db):
    # 다른 유저 (다중 유저 카운트 테스트용)
    return User.objects.create_user(username="another", password="pass1234")


@pytest.fixture
def api_client(user):
    # 기본 유저로 인증된 API 클라이언트
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def todo(db, user):
    # 기본 유저 소유의 테스트 Todo
    return Todo.objects.create(user=user, name="테스트 Todo", description="테스트")


# ============================================================
# TodoLike — ViewSet @action 테스트
# ============================================================


class TestTodoLike:
    def test_like_on(self, api_client, todo):
        """좋아요 ON — liked=True, like_count=1"""
        url = reverse("todo:todo-like", kwargs={"pk": todo.pk})
        res = api_client.post(url)

        assert res.status_code == 200
        assert res.data["liked"] is True
        assert res.data["like_count"] == 1

    def test_like_off(self, api_client, todo, user):
        """좋아요가 이미 있으면 OFF — liked=False, like_count=0"""
        # 미리 좋아요 생성해두고 토글
        TodoLike.objects.create(user=user, todo=todo)

        url = reverse("todo:todo-like", kwargs={"pk": todo.pk})
        res = api_client.post(url)

        assert res.status_code == 200
        assert res.data["liked"] is False
        assert res.data["like_count"] == 0

    def test_like_toggle_on_off_on(self, api_client, todo):
        """좋아요 ON → OFF → ON 연속 토글"""
        url = reverse("todo:todo-like", kwargs={"pk": todo.pk})

        res = api_client.post(url)
        assert res.data["liked"] is True

        res = api_client.post(url)
        assert res.data["liked"] is False

        res = api_client.post(url)
        assert res.data["liked"] is True

    def test_like_unique_together(self, db, user, todo):
        """같은 user + todo 조합은 DB에 한 번만 저장됨 (unique_together 제약)"""
        TodoLike.objects.create(user=user, todo=todo)

        with pytest.raises(Exception):
            TodoLike.objects.create(user=user, todo=todo)

    def test_like_count_multiple_users(self, db, user, another_user, todo):
        """여러 유저가 좋아요 누르면 like_count가 정확히 누적됨"""
        TodoLike.objects.create(user=user, todo=todo)
        TodoLike.objects.create(user=another_user, todo=todo)

        # DB 기준 직접 검증
        assert TodoLike.objects.filter(todo=todo).count() == 2

    def test_like_cascade_on_todo_delete(self, db, user, todo):
        """Todo 삭제 시 연결된 좋아요도 함께 삭제됨 (CASCADE)"""
        TodoLike.objects.create(user=user, todo=todo)
        todo_id = todo.pk  # 삭제 전에 pk 저장
        todo.delete()

        assert TodoLike.objects.filter(todo_id=todo_id).count() == 0

    def test_like_unauthenticated(self, db, todo):
        """비인증 요청 → 401"""
        client = APIClient()
        url = reverse("todo:todo-like", kwargs={"pk": todo.pk})
        res = client.post(url)

        assert res.status_code == 401


# ============================================================
# TodoBookmark — ViewSet @action 테스트
# ============================================================


class TestTodoBookmark:
    def test_bookmark_on(self, api_client, todo):
        """북마크 ON — bookmarked=True, bookmark_count=1"""
        url = reverse("todo:todo-bookmark", kwargs={"pk": todo.pk})
        res = api_client.post(url)

        assert res.status_code == 200
        assert res.data["bookmarked"] is True
        assert res.data["bookmark_count"] == 1

    def test_bookmark_off(self, api_client, todo, user):
        """북마크가 이미 있으면 OFF — bookmarked=False, bookmark_count=0"""
        TodoBookmark.objects.create(user=user, todo=todo)

        url = reverse("todo:todo-bookmark", kwargs={"pk": todo.pk})
        res = api_client.post(url)

        assert res.status_code == 200
        assert res.data["bookmarked"] is False
        assert res.data["bookmark_count"] == 0

    def test_bookmark_toggle_on_off_on(self, api_client, todo):
        """북마크 ON → OFF → ON 연속 토글"""
        url = reverse("todo:todo-bookmark", kwargs={"pk": todo.pk})

        res = api_client.post(url)
        assert res.data["bookmarked"] is True

        res = api_client.post(url)
        assert res.data["bookmarked"] is False

        res = api_client.post(url)
        assert res.data["bookmarked"] is True

    def test_bookmark_unique_together(self, db, user, todo):
        """같은 user + todo 조합은 DB에 한 번만 저장됨 (unique_together 제약)"""
        TodoBookmark.objects.create(user=user, todo=todo)

        with pytest.raises(Exception):
            TodoBookmark.objects.create(user=user, todo=todo)

    def test_bookmark_count_multiple_users(self, db, user, another_user, todo):
        """여러 유저가 북마크하면 bookmark_count가 정확히 누적됨"""
        TodoBookmark.objects.create(user=user, todo=todo)
        TodoBookmark.objects.create(user=another_user, todo=todo)

        assert TodoBookmark.objects.filter(todo=todo).count() == 2

    def test_bookmark_cascade_on_todo_delete(self, db, user, todo):
        """Todo 삭제 시 연결된 북마크도 함께 삭제됨 (CASCADE)"""
        TodoBookmark.objects.create(user=user, todo=todo)
        todo_id = todo.pk  # 삭제 전에 pk 저장
        todo.delete()

        assert TodoBookmark.objects.filter(todo_id=todo_id).count() == 0

    def test_bookmark_unauthenticated(self, db, todo):
        """비인증 요청 → 401"""
        client = APIClient()
        url = reverse("todo:todo-bookmark", kwargs={"pk": todo.pk})
        res = client.post(url)

        assert res.status_code == 401


# ============================================================
# TodoComment — ViewSet @action 테스트
# ============================================================


class TestTodoComment:
    def test_comment_create(self, api_client, todo):
        """댓글 등록 정상 — comment_count=1, username 반환"""
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})
        res = api_client.post(url, {"content": "테스트 댓글"})

        assert res.status_code == 200
        assert res.data["comment_count"] == 1
        assert res.data["username"] == "testuser"

    def test_comment_empty_content(self, api_client, todo):
        """빈 content → 400"""
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})
        res = api_client.post(url, {"content": ""})

        assert res.status_code == 400

    def test_comment_whitespace_content(self, api_client, todo):
        """공백만 있는 content → strip 후 빈 문자열이므로 400"""
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})
        res = api_client.post(url, {"content": "   "})

        assert res.status_code == 400

    def test_comment_multiple(self, api_client, todo):
        """댓글 여러 개 등록 시 comment_count 정확히 누적"""
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})

        api_client.post(url, {"content": "첫 번째"})
        res = api_client.post(url, {"content": "두 번째"})

        assert res.data["comment_count"] == 2

    def test_comment_saved_to_db(self, api_client, todo):
        """댓글 등록 후 DB에 실제로 저장되는지 검증"""
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})
        api_client.post(url, {"content": "DB 저장 확인"})

        assert TodoComment.objects.filter(todo=todo).count() == 1
        assert TodoComment.objects.get(todo=todo).content == "DB 저장 확인"

    def test_comment_cascade_on_todo_delete(self, db, user, todo):
        """Todo 삭제 시 연결된 댓글도 함께 삭제됨 (CASCADE)"""
        TodoComment.objects.create(user=user, todo=todo, content="삭제 테스트")
        todo_id = todo.pk  # 삭제 전에 pk 저장
        todo.delete()

        assert TodoComment.objects.filter(todo_id=todo_id).count() == 0

    def test_comment_unauthenticated(self, db, todo):
        """비인증 요청 → 401"""
        client = APIClient()
        url = reverse("todo:todo-comments", kwargs={"pk": todo.pk})
        res = client.post(url, {"content": "테스트"})

        assert res.status_code == 401


# ============================================================
# interaction 앱 독립 API 테스트
# (/interaction/like/, /interaction/bookmark/, /interaction/comment/)
# ============================================================


class TestInteractionAPI:
    def test_interaction_like(self, api_client, todo):
        """interaction 앱 독립 좋아요 API 정상 동작"""
        url = f"/interaction/like/{todo.pk}/"
        res = api_client.post(url)

        assert res.status_code == 200
        assert "liked" in res.data
        assert "like_count" in res.data

    def test_interaction_bookmark(self, api_client, todo):
        """interaction 앱 독립 북마크 API 정상 동작"""
        url = f"/interaction/bookmark/{todo.pk}/"
        res = api_client.post(url)

        assert res.status_code == 200
        assert "bookmarked" in res.data
        assert "bookmark_count" in res.data

    def test_interaction_comment(self, api_client, todo):
        """interaction 앱 독립 댓글 등록 API 정상 동작"""
        url = f"/interaction/comment/{todo.pk}/"
        res = api_client.post(url, {"content": "interaction API 테스트"})

        assert res.status_code == 200

    def test_interaction_comment_list(self, db, user, todo):
        """댓글 목록 API — 인증 필요"""
        # 댓글 미리 생성
        TodoComment.objects.create(user=user, todo=todo, content="목록 테스트")

        client = APIClient()  # 비인증 클라이언트
        url = f"/interaction/comment/{todo.pk}/list/"
        res = client.get(url)

        assert res.status_code == 401

    def test_interaction_unauthenticated(self, db, todo):
        """interaction 독립 API — 비인증 요청 → 401"""
        client = APIClient()

        assert client.post(f"/interaction/like/{todo.pk}/").status_code == 401
        assert client.post(f"/interaction/bookmark/{todo.pk}/").status_code == 401
        assert (
            client.post(
                f"/interaction/comment/{todo.pk}/", {"content": "test"}
            ).status_code
            == 401
        )
