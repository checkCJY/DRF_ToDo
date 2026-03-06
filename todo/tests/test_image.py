import pytest
from django.urls import reverse

"""
DRF DefaultRouter 자동 생성 URL 이름 (basename="todo")
todo:todo-list         → GET  /todo/viewsets/view/         (목록 조회)
todo:todo-list         → POST /todo/viewsets/view/         (생성)
todo:todo-detail       → GET  /todo/viewsets/view/{pk}/   (단일 조회)
todo:todo-detail       → PUT  /todo/viewsets/view/{pk}/   (전체 수정)
todo:todo-detail       → PATCH /todo/viewsets/view/{pk}/  (부분 수정)
todo:todo-detail       → DELETE /todo/viewsets/view/{pk}/ (삭제)
"""


@pytest.mark.django_db
class TestTodoImage:
    def test_create_todo_with_image(self, api_client, image_file):
        url = reverse("todo:todo-list")
        data = {
            "name": "이미지 테스트",
            "description": "설명",
            "exp": 0,
            "image": image_file,
        }
        res = api_client.post(url, data, format="multipart")
        assert res.status_code == 201
        assert res.data["image"] is not None

    def test_create_todo_without_image(self, api_client):
        url = reverse("todo:todo-list")
        data = {
            "name": "이미지 없는 Todo",
            "description": "설명",
            "exp": 0,
        }
        res = api_client.post(url, data, format="multipart")
        assert res.status_code == 201
        assert res.data["image"] is None

    def test_update_todo_with_image(self, api_client, todo, image_file):
        url = reverse("todo:todo-detail", kwargs={"pk": todo.pk})
        data = {"image": image_file}
        res = api_client.patch(url, data, format="multipart")
        assert res.status_code == 200
        assert res.data["image"] is not None

    def test_completed_at_set_when_complete_true(self, todo):
        todo.complete = True
        todo.save()
        todo.refresh_from_db()
        assert todo.completed_at is not None

    def test_completed_at_cleared_when_complete_false(self, todo):
        todo.complete = True
        todo.save()
        todo.complete = False
        todo.save()
        todo.refresh_from_db()
        assert todo.completed_at is None
