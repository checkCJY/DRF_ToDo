# Django REST Framework의 ViewSet 기능 import
# → 여러 API 기능(list, retrieve 등)을 하나의 클래스에서 처리할 수 있음
from rest_framework import viewsets

# API 접근 권한 설정 클래스 import
# → 인증된 사용자만 수정 가능, 비로그인 사용자는 읽기만 가능
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# 현재 앱의 모델과 Serializer import
from .models import CollectedReview
from .serializers import CollectedReviewSerializer


# ============================================================
# CollectedReview 데이터 조회용 API ViewSet
# ============================================================
class CollectedReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    데이터 확인용 API ViewSet

    ReadOnlyModelViewSet
    → 읽기 전용 ViewSet
    → 아래 API만 자동 생성됨

    GET /reviews/        : 리뷰 목록 조회 (list)
    GET /reviews/{id}/   : 리뷰 상세 조회 (retrieve)
    """

    # ------------------------------------------------------------
    # 조회할 데이터(QuerySet) 설정
    # ------------------------------------------------------------
    # DB에서 CollectedReview 데이터를 모두 가져오고
    # id 기준 내림차순 정렬 (최신 데이터 먼저)
    queryset = CollectedReview.objects.all().order_by("-id")

    # ------------------------------------------------------------
    # 사용할 Serializer 지정
    # ------------------------------------------------------------
    # 모델 데이터를 JSON 형태로 변환할 때 사용
    serializer_class = CollectedReviewSerializer

    # ------------------------------------------------------------
    # API 접근 권한 설정
    # ------------------------------------------------------------
    # IsAuthenticatedOrReadOnly 의미
    #
    # 비로그인 사용자
    #   → GET 요청만 가능 (조회)
    #
    # 로그인 사용자
    #   → GET / POST / PUT / DELETE 가능
    #
    # 하지만 현재 ViewSet이 ReadOnlyModelViewSet이므로
    # 실제로는 GET 요청(list, retrieve)만 제공됨
    permission_classes = [IsAuthenticatedOrReadOnly]
