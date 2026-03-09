# from rest_framework.serializers import ModelSerializer
# from .models import Todo


# # API 요청 데이터를 모델 객체로 변환하는 변환기
# class TodoSerializer(ModelSerializer):
#     class Meta:
#         model = Todo
#         # 학습 단계예서는 아래코드 사용해도 상관없음.
#         # fields = "__all__" # 모델의 모든 필드를 자동으로 직렬화합니다.

#         # 서버가 채워야 하는 값은 클라이언트가 건드리지 못하게 한다.
#         read_only_fields = ["created_at", "updated_at", "user"]  # 읽기만 가능

#         # 습관적으로 아래코드 사용하는걸 추천
#         fields = [
#             "id",  # 추가 __all__은 자동으로 생성된 ID 캐치하지만, fields 에서 추가로 확인
#             "name",
#             "description",
#             "complete",
#             "exp",
#             "completed_at",
#             "created_at",
#             "updated_at",
#             "image",
#             "user",
#         ]

#         # 모든 필드를 기본 포함시키고 → 특정 필드만 제외하고 싶을 때
#         # 신규 필드 추가시 노출될 가능성이 있음
#         # exclude = ["created_at", "updated_at"]


from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Todo
from interaction.models import TodoLike, TodoBookmark, TodoComment


class TodoSerializer(ModelSerializer):
    """
    Todo 모델 직렬화 Serializer.

    역할:
        1. Todo 모델 데이터를 JSON으로 변환
        2. 좋아요 수 / 북마크 수 / 댓글 수 계산
        3. 현재 로그인 사용자 기준으로 is_liked / is_bookmarked 판단

    로그인 사용자 기반 필드(is_liked, is_bookmarked)를 사용하려면
    view에서 context를 반드시 전달해야 합니다.
        serializer = TodoSerializer(..., context={"request": request})
    """

    # user FK에서 username만 꺼내서 노출 (읽기 전용)
    username = serializers.CharField(source="user.username", read_only=True)

    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    bookmark_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = [
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "image",
            "created_at",
            "user",
            "username",
            "like_count",
            "is_liked",
            "bookmark_count",
            "is_bookmarked",
            "comment_count",
            # "is_public",
        ]
        read_only_fields = ["user"]

    def _user(self):
        """
        현재 로그인 사용자 반환.

        Serializer는 request를 직접 접근할 수 없으므로
        context["request"]를 통해 간접 접근합니다.
        비로그인 상태이면 None을 반환합니다.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user
        return None

    def get_like_count(self, obj):
        """해당 Todo의 좋아요 수를 반환합니다."""
        return TodoLike.objects.filter(todo=obj).count()

    def get_is_liked(self, obj):
        """
        현재 로그인 사용자의 좋아요 여부를 반환합니다.

        비로그인 상태이면 False를 반환합니다.
        """
        user = self._user()
        if not user:
            return False
        return TodoLike.objects.filter(todo=obj, user=user).exists()

    def get_bookmark_count(self, obj):
        """해당 Todo의 북마크 수를 반환합니다."""
        return TodoBookmark.objects.filter(todo=obj).count()

    def get_is_bookmarked(self, obj):
        """
        현재 로그인 사용자의 북마크 여부를 반환합니다.

        비로그인 상태이면 False를 반환합니다.
        """
        user = self._user()
        if not user:
            return False
        return TodoBookmark.objects.filter(todo=obj, user=user).exists()

    def get_comment_count(self, obj):
        """해당 Todo의 댓글 수를 반환합니다."""
        return TodoComment.objects.filter(todo=obj).count()
