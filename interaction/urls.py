from django.urls import path
from .views import (
    TodoLikeToggleAPIView,
    TodoBookmarkToggleAPIView,
    TodoCommentCreateAPIView,
    TodoCommentListAPIView,
)

# app_name 생략
# 장고에서는 app_name 으로 HTML 연결했는데, DRF에서는?
# 그런데, app_name 설정한 DRF 파일도 있었는데 흠.. 왜 여기선 안했을까

"""
POST /interaction/like/3/
POST /interaction/bookmark/3/
POST /interaction/comment/3/
GET /interaction/comment/3/list/
"""

urlpatterns = [
    path("like/<int:todo_id>/", TodoLikeToggleAPIView.as_view()),
    path("bookmark/<int:todo_id>/", TodoBookmarkToggleAPIView.as_view()),
    path("comment/<int:todo_id>/", TodoCommentCreateAPIView.as_view()),
    path("comment/<int:todo_id>/list/", TodoCommentListAPIView.as_view()),
]
