from rest_framework import serializers
from .models import CollectedReview


class CollectedReviewSerializer(serializers.ModelSerializer):
    """CollectedReview 데이터를 API용으로 변환하는 Serializer 설정 클래스"""

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


class SentimentTextSerializer(serializers.Serializer):
    """
    감정 분석 API에서 사용자가 직접 텍스트를 POST로 보낼 때
    입력 데이터 검증(validation)을 수행하는 Serializer

    예시 요청

    POST /api/sentiment/

    {
        "text": "이 영화 정말 재미있다"
    }
    """

    # 분석할 텍스트 필드
    text = serializers.CharField(
        allow_blank=False,  # 반드시 내용이 있어야 함
        max_length=5000,  # 너무 긴 텍스트 입력 방지 (서버 보호 목적)
    )
