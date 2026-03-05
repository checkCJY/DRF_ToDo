from django.db import models


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
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    exp = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
