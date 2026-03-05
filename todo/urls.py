from django.urls import path
from .views.templates_views import TodoListView, TodoCreateView, TodoDetailView
from .views.api_views import TodoListAPI, TodoCreateAPI, TodoRetrieveAPI

app_name = "todo"

urlpatterns = [
    # path("list/", views.todo_list, name="todo_List"), # 첫 테스트용
    # HTML 렌더링 뷰
    path("list/", TodoListView.as_view(), name="list"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    # api DRF / JSON 응답 뷰
    path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
]
