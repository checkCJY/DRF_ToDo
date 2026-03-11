from rest_framework import serializers
from .models import CollectedReview


# CollectedReview 데이터를 API용으로 변환하는 Serializer
class CollectedReviewSerializer(serializers.ModelSerializer):
    # Serializer 설정 클래스
    class Meta:
        # 어떤 Django 모델을 기반으로 Serializer를 만들지 지정
        model = CollectedReview

        # API에서 사용할 필드 목록 지정
        # → 모델의 필드 중 아래 항목만 JSON으로 변환됨
        fields = [
            "id",  # DB 기본 키 (Primary Key)
            "title",  # 리뷰 제목
            "review",  # 리뷰 본문
            "doc_id",  # 중복 방지용 문서 ID
            "collected_at",  # 데이터 수집 시각
        ]
