# # Django REST Framework ViewSet + 감정 분석 API

# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from .models import CollectedReview
# from .serializers import CollectedReviewSerializer, SentimentTextSerializer
# from .services import predict_sentiment
# from django.shortcuts import render

# from celery.result import AsyncResult
# from .tasks import analyze_review_sentiment_by_id, analyze_sentiment_text

# class CollectedReviewViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     리뷰 데이터 조회 및 감정 분석 ViewSet

#     기본 API:
#         GET  /reviews/              리뷰 목록 조회
#         GET  /reviews/{id}/         리뷰 상세 조회

#     커스텀 action:
#         GET  /reviews/{id}/sentiment/   DB 저장 리뷰 감정 분석
#         POST /reviews/sentiment/        직접 입력 텍스트 감정 분석
#     """

#     # 최신 데이터 먼저 반환 (id 내림차순)
#     queryset = CollectedReview.objects.all().order_by("-id")
#     serializer_class = CollectedReviewSerializer

#     # ReadOnlyModelViewSet이므로 실제로는 GET만 허용됨
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     # -------------------------------------------------------
#     # GET /reviews/{id}/sentiment/  — DB 리뷰 감정 분석
#     # -------------------------------------------------------
#     @action(detail=True, methods=["get"], url_path="sentiment")
#     def sentiment(self, request, pk=None):
#         """DB에 저장된 리뷰 텍스트를 HuggingFace 모델로 감정 분석"""
#         obj = self.get_object()

#         if not obj.review:
#             return Response(
#                 {"detail": "review text is empty"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         pred = predict_sentiment(obj.review)

#         return Response(
#             {"id": obj.id, "title": obj.title, "sentiment": pred},
#             status=status.HTTP_200_OK,
#         )

#     # -------------------------------------------------------
#     # POST /reviews/sentiment/  — 텍스트 직접 감정 분석
#     # -------------------------------------------------------
#     @action(
#         detail=False,
#         methods=["post"],
#         url_path="sentiment",
#         permission_classes=[AllowAny],  # 비로그인 사용자도 허용
#     )
#     def sentiment_text(self, request):
#         """
#         사용자가 직접 입력한 텍스트를 감정 분석

#         요청 body: {"text": "이 영화 정말 재미있다"}
#         """
#         serializer = SentimentTextSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         text = serializer.validated_data["text"]
#         pred = predict_sentiment(text)

#         return Response(pred, status=status.HTTP_200_OK)


# # 화면출력용 간단한 함수 생성
# def reviews_page(request):
#     return render(request, "reviews/reviews_page.html")


# Django REST Framework ViewSet + 감정 분석 API

from celery.result import AsyncResult
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CollectedReview
from .serializers import CollectedReviewSerializer, SentimentTextSerializer
from .tasks import analyze_review_sentiment_by_id, analyze_sentiment_text
from django.shortcuts import render


class CollectedReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CollectedReview.objects.all().order_by("-id")
    serializer_class = CollectedReviewSerializer

    """
    Part 17

    DB 리뷰 비동기 분석 시작: job_id 즉시 반환
    POST /api/reviews/collected-reviews/{id}/sentiment-async/
    """

    @action(detail=True, methods=["post"], url_path="sentiment-async")
    def sentiment_async(self, request, pk=None):
        review_id = int(pk)
        task = analyze_review_sentiment_by_id.delay(review_id)

        return Response(
            {"task_id": task.id, "status": "queued"}, status=status.HTTP_202_ACCEPTED
        )

    """
    Part 17

    텍스트 비동기 분석 시작
    POST /api/reviews/collected-reviews/sentiment-async/
    body: {"text": "..."}
    """

    @action(detail=False, methods=["post"], url_path="sentiment-async")
    def sentiment_text_async(self, request):
        serializer = SentimentTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]
        task = analyze_sentiment_text.delay(text)

        return Response(
            {"task_id": task.id, "status": "queued"}, status=status.HTTP_202_ACCEPTED
        )

    """
    Part 17

    결과 조회
    GET /api/reviews/collected-reviews/sentiment-result/{task_id}/
    """

    @action(
        detail=False, methods=["get"], url_path=r"sentiment-result/(?P<task_id>[^/.]+)"
    )
    def sentiment_result(self, request, task_id=None):
        res = AsyncResult(task_id)

        payload = {"task_id": task_id, "state": res.state}

        if res.state == "PENDING":
            return Response(payload, status=status.HTTP_200_OK)

        if res.state == "FAILURE":
            payload["error"] = str(res.result)
            return Response(payload, status=status.HTTP_200_OK)

        if res.state == "SUCCESS":
            payload["result"] = res.result
            return Response(payload, status=status.HTTP_200_OK)

        return Response(payload, status=status.HTTP_200_OK)


# 화면출력용 간단한 함수 생성
def reviews_page(request):
    return render(request, "reviews/reviews_page.html")
