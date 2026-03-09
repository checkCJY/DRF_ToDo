from rest_framework import serializers
from .models import TodoLike, TodoBookmark, TodoComment


class TodoLikeSerializer(serializers.ModelSerializer):
    """Todo 좋아요 Serializer"""

    class Meta:
        model = TodoLike
        fields = "__all__"


class TodoBookmarkSerializer(serializers.ModelSerializer):
    """Todo 북마크 Serializer"""

    class Meta:
        model = TodoBookmark
        fields = "__all__"


# Todo 댓글 Serializer


class TodoCommentSerializer(serializers.ModelSerializer):
    """Todo 댓글 Serializer"""

    # username 필드를 추가
    username = serializers.CharField(
        source="user.username",  # user 모델의 username 값을 가져옴
        read_only=True,  # 클라이언트가 수정할 수 없음 (조회용)
    )

    class Meta:
        model = TodoComment

        # API에서 사용할 필드 목록
        fields = [
            "id",  # 댓글 id
            "todo",  # 어떤 Todo에 달린 댓글인지
            "user",  # 댓글 작성자
            "username",  # 작성자 username (추가 필드)
            "content",  # 댓글 내용
            "created_at",  # 작성 시간
        ]

        # 읽기 전용 필드
        read_only_fields = ["user"]
