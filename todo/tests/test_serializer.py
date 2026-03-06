import pytest
from ..serializers import TodoSerializer
from ..models import Todo

# pytest todo/tests/test_serializer.py -v


@pytest.fixture
def todo(db):
    return Todo.objects.create(name="운동", description="스쿼트 50회", exp=10)


# 직렬화 필드 목록 검증
@pytest.mark.django_db
def test_serializer_fields(todo):
    """직렬화 결과에 선언한 8개 필드가 모두 포함되는지 검증"""
    serializer = TodoSerializer(todo)
    expected_fields = {
        "id",
        "name",
        "description",
        "complete",
        "exp",
        "completed_at",
        "created_at",
        "updated_at",
        "image",  # 모델 필드 추가로 인해 테스트코드 필드 추가.
    }
    assert set(serializer.data.keys()) == expected_fields


# read_only_fields 검증
def test_read_only_fields():
    """created_at, updated_at 은 읽기 전용 필드인지 검증"""
    serializer = TodoSerializer()
    read_only = {name for name, field in serializer.fields.items() if field.read_only}
    assert "created_at" in read_only
    assert "updated_at" in read_only


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
def test_create_via_serializer(db):
    """유효한 데이터로 save() 호출 시 DB에 실제 객체가 생성되는지 검증"""
    data = {"name": "새 할일", "exp": 3}
    serializer = TodoSerializer(data=data)
    assert serializer.is_valid()
    todo = serializer.save()
    assert todo.pk is not None
    assert Todo.objects.filter(pk=todo.pk).exists()
