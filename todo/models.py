from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Todo(models.Model):
    """
    투두리스트 항목을 나타내는 모델.

    name        : 할 일의 제목 (최대 100자)
    description : 할 일에 대한 상세 설명 (선택 입력)
    complete    : 완료 여부 (기본값: 미완료)
    exp         : 완료 시 획득하는 경험치 (기본값: 0)
    completed_at: 완료된 시각 (미완료 상태일 때는 null)
    created_at  : 항목이 처음 생성된 시각 (자동 기록)
    updated_at  : 항목이 마지막으로 수정된 시각 (자동 갱신)
    image       : 해당 할 일에 관련한 이미지파일 (추가되었으므로, serializers.py 필드 수정)
    user        : 기본 장고의 user 이용 (ForeignKey, on_delete=models.CASCADE)
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    exp = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="todo_images/", blank=True, null=True)
    # 추가
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Todo가 저장될 때 complete 상태에 따라 completed_at을 자동으로 관리

        완료 여부(True) 일 때 완료 시간이 없으면 자동저장
        완료 여부(False) 일 때 완료 시간 있으면 취소로 판단 후 시간제거
        """

        if self.complete and self.completed_at is None:
            self.completed_at = timezone.now()

        if not self.complete and self.completed_at is not None:
            self.completed_at = None

        # 부모 모델(Model)의 원래 save() 오버라이딩 (DB 실제저장)
        # super()가 없을 경우 커스텀 저장만 적용되므로, 실제로 저장 안됨
        super().save(*args, **kwargs)
