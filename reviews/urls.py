from django.urls import path
from .views import CollectedReviewViewSet, reviews_page

from rest_framework.routers import DefaultRouter
# → CollectedReview 데이터를 조회하는 API ViewSet

# DefaultRouter → ViewSet을 등록하면 자동으로 REST API URL을 생성
router = DefaultRouter()


"""
ViewSet 등록

router.register()       → 특정 URL 경로에 ViewSet을 연결하는 함수
r"collected-reviews"    → API 기본 URL 경로
                        → 예: /collected-reviews/
CollectedReviewViewSet  → 해당 URL에서 실행될 ViewSet 클래스
basename                → URL 이름을 만들 때 사용하는 기본 이름
"""
router.register(
    r"collected-reviews", CollectedReviewViewSet, basename="collected-reviews"
)

"""
    Django URL 패턴 생성
    router.urls
    → Router가 자동으로 생성한 URL 패턴 목록
    이 값을 urlpatterns에 연결하면 아래 API가 자동으로 생성됩니다.
"""

urlpatterns = [
    path("page/", reviews_page, name="reviews-page"),
]

urlpatterns += router.urls
