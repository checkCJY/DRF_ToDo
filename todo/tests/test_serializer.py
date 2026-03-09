import pytest
from ..serializers import TodoSerializer
from ..models import Todo

# pytest todo/tests/test_serializer.py -v


# 직렬화 필드 목록 검증
@pytest.mark.django_db
def test_serializer_fields(todo):
    """직렬화 결과에 선언한 필드가 모두 포함되는지 검증"""
    serializer = TodoSerializer(todo)
    # Step 10: interaction 앱 추가로 새 필드 포함, completed_at/updated_at 제외
    expected_fields = {
        "id",
        "name",
        "description",
        "complete",
        "exp",
        "image",
        "created_at",
        "user",
        "username",
        "like_count",
        "is_liked",
        "bookmark_count",
        "is_bookmarked",
        "comment_count",
        "is_public",  # Part 12 is_public 추가.
    }
    assert set(serializer.data.keys()) == expected_fields


# read_only_fields 검증
def test_read_only_fields():
    """user, username, like_count 등은 읽기 전용 필드인지 검증"""
    # Step 10: updated_at 필드 제거됨, interaction 관련 필드 read_only 추가
    serializer = TodoSerializer()
    read_only = {name for name, field in serializer.fields.items() if field.read_only}
    assert "user" in read_only
    assert "username" in read_only
    assert "like_count" in read_only
    assert "is_liked" in read_only
    assert "created_at" in read_only


# 유효한 데이터로 is_valid() 통과
@pytest.mark.django_db
def test_valid_data(db):
    """필수 필드가 모두 있는 데이터는 유효성 검사 통과"""
    data = {"name": "공부", "description": "DRF", "complete": False, "exp": 5}
    serializer = TodoSerializer(data=data)
    assert serializer.is_valid()


# 필수 필드(name) 누락 시 is_valid() 실패
@pytest.mark.django_db
def test_missing_required_field(db):
    """name 필드 누락 시 유효성 검사 실패 및 에러 키 포함 검증"""
    data = {"description": "설명만 있음", "complete": False, "exp": 0}
    serializer = TodoSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors


# save()로 실제 객체 생성
@pytest.mark.django_db
def test_create_via_serializer(user):
    """유효한 데이터로 save() 호출 시 DB에 실제 객체가 생성되는지 검증"""
    data = {"name": "새 할일", "exp": 3}
    serializer = TodoSerializer(data=data)
    assert serializer.is_valid()
    todo = serializer.save(user=user)
    assert todo.pk is not None
    assert Todo.objects.filter(pk=todo.pk).exists()
