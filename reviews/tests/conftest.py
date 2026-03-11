import pytest
from django.contrib.auth.models import User
from django.db import connection
from rest_framework.test import APIClient


# ============================================================
# unmanaged 모델(stg_movie_reviews) 테스트 DB 생성
# managed=False 이므로 Django가 테이블을 자동 생성하지 않음
# session 범위로 한 번만 생성
# ============================================================


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        from reviews.models import CollectedReview

        CollectedReview._meta.managed = True
        with connection.schema_editor() as editor:
            try:
                editor.create_model(CollectedReview)
            except Exception:
                pass  # 이미 존재하면 무시
        CollectedReview._meta.managed = False


# ============================================================
# 인증된 클라이언트 fixture
# DEFAULT_PERMISSION_CLASSES = IsAuthenticated 이므로
# 테스트에서 force_authenticate 필요
# ============================================================


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client
