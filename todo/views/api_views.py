from rest_framework import viewsets  # viewsets 사용을 위해 추가
from ..models import Todo
from ..serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from todo.pagination import CustomPageNumberPagination

# Django 앱 간 상대경로 Improt는 동작하지 않기에 절대경로로 작성
from interaction.models import TodoLike, TodoBookmark, TodoComment
from rest_framework.decorators import action  # Part 10 추가
from rest_framework.response import Response

from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


# Todo 목록 페이지네이션 설정
class TodoListPagination(CustomPageNumberPagination):
    """
    page_size=              : 한 페이지에 기본적으로 보여줄 데이터 개수
    page_size_query_param   : URL 쿼리 파라미터로 페이지 크기 변경 가능
    max_page_size           : 사용자가 설정할 수 있는 최대 페이지 크기 제한
    """

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50


class TodoViewSet(viewsets.ModelViewSet):
    """
    Todo CRUD ViewSet.

    ModelViewSet이 아래 액션을 자동 생성합니다.
        GET    /todos/        → list
        POST   /todos/        → create
        GET    /todos/{id}/   → retrieve
        PUT    /todos/{id}/   → update
        DELETE /todos/{id}/   → destroy
        PATCH  /todoss/{id}/  → parital_update (현재 사용안함)

    기본 permission은 AllowAny(목록·상세는 비인증 허용).
    좋아요·북마크·댓글 액션은 IsAuthenticated 필요.
    """

    serializer_class = TodoSerializer
    # permission_classes = [AllowAny]  # 목록·상세는 비인증 허용
    # update, delete 오버라이딩을 위해서 수정
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user  # 현재 로그인한 사용자
        check_user = self.request.user.is_authenticated
        # 비로그인이면 Q(is_public=True) 만 실행
        if not check_user:
            return Todo.objects.filter(Q(is_public=True)).order_by("-created_at")
        # 로그인이면 Q(is_public=True) | Q(user=user) 실행
        else:
            return Todo.objects.filter(Q(is_public=True) | Q(user=user)).order_by(
                "-created_at"
            )

    def list(self, request, *args, **kwargs):
        """
        Todo 목록 API (페이지네이션 응답 커스터마이징).

        기본 DRF list 응답 대신 아래 구조로 반환합니다.
            {
                "data": [...],
                "current_page": 1,
                "page_count": 5,
                "next": true,
                "previous": false
            }
        JS 프론트엔드에서 페이지네이션 UI를 쉽게 처리하기 위한 구조입니다.
        """
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)

        # pagination이 있는 경우
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return Response(
                {
                    "data": serializer.data,
                    "current_page": int(request.query_params.get("page", 1)),
                    "page_count": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link() is not None,
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )

        # pagination이 없는 경우
        serializer = self.get_serializer(qs, many=True, context={"request": request})
        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        좋아요 토글 API.

        POST /todo/viewsets/view/<id>/like/

        - 좋아요 없으면 생성(ON), 있으면 삭제(OFF) — get_or_create 패턴
        - 응답: {"liked": bool, "like_count": int}
        """
        todo = self.get_object()
        user = request.user
        # 좋아요 존재 확인
        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        if created:
            liked = True
        else:
            obj.delete()
            liked = False

        like_count = TodoLike.objects.filter(todo=todo).count()
        return Response({"liked": liked, "like_count": like_count})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        """
        북마크 토글 API.

        POST /todo/viewsets/view/<id>/bookmark/

        - 북마크 없으면 생성(ON), 있으면 삭제(OFF) — like()와 동일한 구조
        - 응답: {"bookmarked": bool, "bookmark_count": int}
        """
        todo = self.get_object()
        user = request.user
        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        if created:
            bookmarked = True
        else:
            obj.delete()
            bookmarked = False

        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()
        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        """
        댓글 등록 API.

        POST /todo/viewsets/view/<id>/comments/

        요청 body:
            {"content": "댓글 내용"}

        - content가 비어있으면 400 반환
        - 응답: {"comment_count": int}
        """
        todo = self.get_object()
        user = request.user
        content = (request.data.get("content") or "").strip()

        if not content:
            return Response({"detail": "content is required"}, status=400)

        TodoComment.objects.create(todo=todo, user=user, content=content)
        comment_count = TodoComment.objects.filter(todo=todo).count()
        return Response(
            {
                "comment_count": comment_count,
                "username": user.username,
            }
        )

    def perform_create(self, serializer):
        #
        if not self.request.user.is_authenticated:
            from rest_framework.exceptions import NotAuthenticated

            raise NotAuthenticated()
        serializer.save(user=self.request.user, is_public=True)
