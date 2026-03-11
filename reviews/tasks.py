from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import CollectedReview
from .services import predict_sentiment


# ============================================================
# Task 1: DB 리뷰 ID로 감정 분석
# ============================================================


@shared_task(bind=True)
def analyze_review_sentiment_by_id(self, review_id: int) -> dict:
    """
    DB에서 리뷰를 조회한 뒤 AI 감정 분석 결과를 반환합니다.

    bind=True: self를 통해 retry, request 등 Task 컨텍스트에 접근 가능
    """
    # 1) 리뷰 조회
    try:
        obj = CollectedReview.objects.get(id=review_id)
    except ObjectDoesNotExist:
        return {"status": "error", "detail": "review not found", "review_id": review_id}

    # 2) 텍스트 정제 — None 또는 공백만 있는 경우 에러 반환
    text = (obj.review or "").strip()
    if not text:
        return {
            "status": "error",
            "detail": "review text is empty",
            "review_id": review_id,
        }

    # 3) HuggingFace 모델로 감정 분석 수행
    pred = predict_sentiment(text)

    return {
        "status": "ok",
        "review_id": obj.id,
        "title": obj.title,
        "sentiment": pred,
    }


# ============================================================
# Task 2: 텍스트 직접 입력으로 감정 분석
# ============================================================


@shared_task(bind=True)
def analyze_sentiment_text(self, text: str) -> dict:
    """
    사용자가 전달한 텍스트를 직접 감정 분석합니다.
    """
    # 1) 텍스트 정제 — None 또는 공백만 있는 경우 에러 반환
    text = (text or "").strip()
    if not text:
        return {"status": "error", "detail": "text is empty"}

    # 2) HuggingFace 모델로 감정 분석 수행
    pred = predict_sentiment(text)

    return {"status": "ok", "sentiment": pred}
