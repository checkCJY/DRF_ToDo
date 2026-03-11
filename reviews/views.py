# Django REST Framework ViewSet + 감정 분석 API

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CollectedReview
from .serializers import CollectedReviewSerializer, SentimentTextSerializer
from .services import predict_sentiment
from django.shortcuts import render


class CollectedReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    리뷰 데이터 조회 및 감정 분석 ViewSet

    기본 API:
        GET  /reviews/              리뷰 목록 조회
        GET  /reviews/{id}/         리뷰 상세 조회

    커스텀 action:
        GET  /reviews/{id}/sentiment/   DB 저장 리뷰 감정 분석
        POST /reviews/sentiment/        직접 입력 텍스트 감정 분석
    """

    # 최신 데이터 먼저 반환 (id 내림차순)
    queryset = CollectedReview.objects.all().order_by("-id")
    serializer_class = CollectedReviewSerializer

    # ReadOnlyModelViewSet이므로 실제로는 GET만 허용됨
    permission_classes = [IsAuthenticatedOrReadOnly]

    # -------------------------------------------------------
    # GET /reviews/{id}/sentiment/  — DB 리뷰 감정 분석
    # -------------------------------------------------------
    @action(detail=True, methods=["get"], url_path="sentiment")
    def sentiment(self, request, pk=None):
        """DB에 저장된 리뷰 텍스트를 HuggingFace 모델로 감정 분석"""
        obj = self.get_object()

        if not obj.review:
            return Response(
                {"detail": "review text is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        pred = predict_sentiment(obj.review)

        return Response(
            {"id": obj.id, "title": obj.title, "sentiment": pred},
            status=status.HTTP_200_OK,
        )

    # -------------------------------------------------------
    # POST /reviews/sentiment/  — 텍스트 직접 감정 분석
    # -------------------------------------------------------
    @action(
        detail=False,
        methods=["post"],
        url_path="sentiment",
        permission_classes=[AllowAny],  # 비로그인 사용자도 허용
    )
    def sentiment_text(self, request):
        """
        사용자가 직접 입력한 텍스트를 감정 분석

        요청 body: {"text": "이 영화 정말 재미있다"}
        """
        serializer = SentimentTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]
        pred = predict_sentiment(text)

        return Response(pred, status=status.HTTP_200_OK)


# 화면출력용 간단한 함수 생성
def reviews_page(request):
    return render(request, "reviews/reviews_page.html")
