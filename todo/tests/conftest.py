import pytest
from django.contrib.auth.models import User
from todo.models import Todo


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def todo(db, user):
    return Todo.objects.create(
        name="운동",
        description="스쿼트 50회",
        exp=10,
        user=user,
    )
