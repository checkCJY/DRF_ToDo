from django.conf import settings
from django.db import models


class TodoLike(models.Model):
    """
    Todo 좋아요 모델
    user        : 좋아요를 누른 사용자
    todo        : 좋아요 대상 Todo
    created_at  : 좋아요 생성 시간
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 현재 프로젝트에서 사용하는 User 모델
        on_delete=models.CASCADE,  # 사용자가 삭제되면 좋아요도 함께 삭제
    )

    todo = models.ForeignKey(
        "todo.Todo",  # 기존 todo 앱 모델 참조
        on_delete=models.CASCADE,
        related_name="likes",  # Todo 객체에서 todo.likes 로 접근 가능
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 좋아요 생성 시간

    class Meta:
        """동일한 user + todo 조합은 한 번만 허용"""

        unique_together = ("user", "todo")


class TodoBookmark(models.Model):
    """
    Todo 북마크 모델
    user            : 북마크를 등록한 사용자
    todo            : 북마크 대상 Todo
    created_at      : 북마크 생성 시간
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """동일 사용자 + Todo 조합 중복 방지"""

        unique_together = ("user", "todo")


class TodoComment(models.Model):
    """
    Todo 댓글 모델

    user            : 댓글 작성 사용자
    todo            : 댓글이 달린 Todo
    content         : 댓글 내용
    created_at      : 댓글 작성 시간
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
