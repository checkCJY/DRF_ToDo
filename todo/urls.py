from django.urls import path, include
from .views.templates_views import (
    TodoListView,
    TodoCreateView,
    TodoDetailView,
    TodoUpdateView,
)

# viewsets 사용으로 주석처리
# from .views.api_views import (
#     TodoListAPI,
#     TodoCreateAPI,
#     TodoRetrieveAPI,
#     TodoUpdateAPI,
#     TodoDeleteAPI,
# )
from .views.api_views import TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("view", TodoViewSet, basename="todo")

app_name = "todo"


"""
DRF DefaultRouter 자동 생성 URL 이름 (basename="todo")
todo:todo-list         → GET  /todo/viewsets/view/         (목록 조회)
todo:todo-list         → POST /todo/viewsets/view/         (생성)
todo:todo-detail       → GET  /todo/viewsets/view/{pk}/   (단일 조회)
todo:todo-detail       → PUT  /todo/viewsets/view/{pk}/   (전체 수정)
todo:todo-detail       → PATCH /todo/viewsets/view/{pk}/  (부분 수정)
todo:todo-detail       → DELETE /todo/viewsets/view/{pk}/ (삭제)
"""

urlpatterns = [
    # path("list/", views.todo_list, name="todo_List"), # 첫 테스트용
    # HTML 렌더링 뷰
    path("list/", TodoListView.as_view(), name="list"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_Update"),
    # api DRF / JSON 응답 뷰
    # viewsets 으로 인해 사용안함
    # path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    # path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    # path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
    # path("api/update/<int:pk>/", TodoUpdateAPI.as_view(), name="todo_api_update"),
    # path("api/delete/<int:pk>/", TodoDeleteAPI.as_view(), name="todo_api_delete"),
    # Viewsets CRUD를 하나로 통일
    # 127.0.0.1:8000/todo/viewsets/view/
    path("viewsets/", include(router.urls)),
]
