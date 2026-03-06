from rest_framework.serializers import ModelSerializer
from .models import Todo


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        # 학습 단계예서는 아래코드 사용해도 상관없음.
        # fields = "__all__" # 모델의 모든 필드를 자동으로 직렬화합니다.
        read_only_fields = ["created_at", "updated_at"]  # 읽기만 가능

        # 습관적으로 아래코드 사용하는걸 추천
        fields = [
            "id",  # 추가 __all__은 자동으로 생성된 ID 캐치하지만, fields 에서 추가로 확인
            "name",
            "description",
            "complete",
            "exp",
            "completed_at",
            "created_at",
            "updated_at",
            "image",
        ]

        # 모든 필드를 기본 포함시키고 → 특정 필드만 제외하고 싶을 때
        # 신규 필드 추가시 노출될 가능성이 있음
        # exclude = ["created_at", "updated_at"]
