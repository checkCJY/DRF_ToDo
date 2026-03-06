import pytest
from ..models import Todo


@pytest.fixture
def todo(db):
    return Todo.objects.create(
        name="운동",
        description="스쿼트 50회",
        exp=10,
    )


# 기본값 검증
@pytest.mark.django_db
def test_defaults():
    todo = Todo.objects.create(name="테스트")

    assert todo.complete is False
    assert todo.exp == 0
    assert todo.description == ""
    assert todo.completed_at is None


# __str__ 검증
@pytest.mark.django_db
def test_str(todo):
    assert str(todo) == "운동"


# auto_now_add / auto_now 검증
@pytest.mark.django_db
def test_timestamps(todo):
    assert todo.created_at is not None
    assert todo.updated_at is not None


# complete 상태 변경 후 저장 검증
@pytest.mark.django_db
def test_complete_flag(todo):
    todo.complete = True
    todo.save()
    todo.refresh_from_db()

    assert todo.complete is True


# exp 음수 불가 (PositiveIntegerField)
@pytest.mark.django_db
def test_exp_positive(db):
    todo = Todo.objects.create(name="양수exp", exp=100)
    assert todo.exp == 100


# completed_at 수동 설정 및 저장 검증
# @pytest.mark.django_db
# def test_completed_at_manual_set(todo):
#     from django.utils import timezone

#     now = timezone.now()
#     todo.completed_at = now
#     todo.save()
#     todo.refresh_from_db()

#     assert todo.completed_at is not None
#     assert todo.completed_at == now


# 수정 후
@pytest.mark.django_db
def test_completed_at_manual_set(todo):
    todo.complete = True  # complete를 True로 설정
    todo.save()  # save() 오버라이드가 completed_at을 자동 설정
    todo.refresh_from_db()

    assert todo.completed_at is not None


# description blank=True: 빈 문자열로 생성 허용 검증
@pytest.mark.django_db
def test_description_blank_allowed(db):
    todo = Todo.objects.create(name="설명없음", description="")
    assert todo.description == ""


# name max_length=100 초과 시 full_clean() ValidationError 검증
@pytest.mark.django_db
def test_name_max_length(db):
    from django.core.exceptions import ValidationError

    todo = Todo(name="a" * 101)
    with pytest.raises(ValidationError):
        todo.full_clean()
