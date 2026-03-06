import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from todo.models import Todo
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def another_user(db):
    return User.objects.create_user(username="anotheruser", password="testpass")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def todo(db, user):
    return Todo.objects.create(
        name="운동",
        description="스쿼트 50회",
        exp=10,
        user=user,
    )


@pytest.fixture
def another_user_todo(db, another_user):
    return Todo.objects.create(
        name="다른유저 Todo",
        description="다른유저 설명",
        exp=5,
        user=another_user,
    )


# 수정
# @pytest.fixture
# def image_file():
#     return SimpleUploadedFile(
#         name="test.jpg",
#         content=b"\x47\x49\x46\x38\x39\x61",  # 최소 바이트
#         content_type="image/jpeg",
#     )

"""
image_file fixture 에서 넣은 바이트가 실제 유효한 이미지 데이터가 아닌상태
Django의 ImageField가 Pillow로 검증할 때 이미지 파일이 아니라고 거부해서 테스트오류

해결방법 : image_file 픽스처를 유효한 최소 GIF 바이트로 수정해야 한다.
"""


@pytest.fixture
def image_file():
    return SimpleUploadedFile(
        name="test.gif",
        content=(
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00"
            b"\x00\xff\x00\x2c\x00\x00\x00\x00\x01\x00"
            b"\x01\x00\x00\x02\x00\x3b"
        ),
        content_type="image/gif",
    )
