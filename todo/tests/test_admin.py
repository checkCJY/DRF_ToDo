import pytest
from django.contrib import admin as django_admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import Client
from ..models import Todo
from ..admin import TodoAdmin

# pytest todo/tests/test_admin.py -v


@pytest.fixture
def admin_client(db):
    """superuser 로 로그인된 Django 테스트 클라이언트"""
    User.objects.create_superuser(
        username="admin", password="password", email="admin@test.com"
    )
    client = Client()
    client.login(username="admin", password="password")
    return client


# Todo가 admin site에 등록되어 있는지 검증
def test_todo_registered_in_admin():
    """Todo 모델이 admin site에 등록되어 있는지 검증"""
    assert Todo in django_admin.site._registry


# list_display 필드 검증
def test_list_display():
    """TodoAdmin의 list_display에 __str__, created_at, updated_at 포함 검증"""
    site = AdminSite()
    todo_admin = TodoAdmin(Todo, site)
    assert "__str__" in todo_admin.list_display
    assert "created_at" in todo_admin.list_display
    assert "updated_at" in todo_admin.list_display


# admin changelist 페이지 200 응답 검증
@pytest.mark.django_db
def test_admin_changelist(admin_client):
    """admin Todo 목록 페이지 GET 요청 시 200 응답 검증"""
    res = admin_client.get("/admin/todo/todo/")
    assert res.status_code == 200
