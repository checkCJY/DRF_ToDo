# ============================================================
# reviews/tests/test_reviews_async.py
# Celery 비동기 감정 분석 테스트
#
# 테스트 전략:
# - Celery task 는 .delay() 없이 직접 호출해서 테스트
#   (실제 broker/worker 없이도 동작)
# - predict_sentiment 는 mock 처리
# - AsyncResult 는 mock 처리 (Redis 없이 테스트)
# ============================================================

import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

from reviews.models import CollectedReview
from reviews.tasks import analyze_review_sentiment_by_id, analyze_sentiment_text


# ============================================================
# 공통 Fixture
# ============================================================


@pytest.fixture
def client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def review(db):
    return CollectedReview.objects.create(
        title="테스트 영화 리뷰",
        review="이 영화 진짜 재밌었어요!",
        doc_id="test-doc-001",
    )


@pytest.fixture
def review_empty(db):
    return CollectedReview.objects.create(
        title="빈 리뷰",
        review="",
        doc_id="test-doc-002",
    )


@pytest.fixture
def mock_predict():
    """predict_sentiment mock fixture"""
    mock_result = {
        "model": "blockenters/finetuned-nsmc-sentiment",
        "label_raw": "LABEL_1",
        "label": "positive",
        "score": 0.9383,
    }
    with patch("reviews.tasks.predict_sentiment", return_value=mock_result) as m:
        yield m


# ============================================================
# 1. tasks.py — analyze_review_sentiment_by_id 테스트
# .delay() 없이 직접 호출 (unit test)
# ============================================================


@pytest.mark.django_db
class TestAnalyzeReviewSentimentById:
    def test_returns_ok_status_with_valid_review(self, review, mock_predict):
        """정상 리뷰 id → status: ok + sentiment 포함"""
        result = analyze_review_sentiment_by_id(review.id)

        assert result["status"] == "ok"
        assert result["review_id"] == review.id
        assert result["title"] == review.title
        assert "sentiment" in result

    def test_predict_called_with_review_text(self, review, mock_predict):
        """predict_sentiment 에 리뷰 텍스트가 전달되는지 확인"""
        analyze_review_sentiment_by_id(review.id)
        mock_predict.assert_called_once_with(review.review)

    def test_returns_error_for_nonexistent_id(self, db, mock_predict):
        """존재하지 않는 id → status: error"""
        result = analyze_review_sentiment_by_id(99999)

        assert result["status"] == "error"
        assert result["detail"] == "review not found"
        assert result["review_id"] == 99999

    def test_returns_error_for_empty_review_text(self, review_empty, mock_predict):
        """빈 review 텍스트 → status: error"""
        result = analyze_review_sentiment_by_id(review_empty.id)

        assert result["status"] == "error"
        assert result["detail"] == "review text is empty"

    def test_predict_not_called_when_review_empty(self, review_empty, mock_predict):
        """빈 텍스트일 때 predict_sentiment 호출 안 됨"""
        analyze_review_sentiment_by_id(review_empty.id)
        mock_predict.assert_not_called()


# ============================================================
# 2. tasks.py — analyze_sentiment_text 테스트
# ============================================================


class TestAnalyzeSentimentText:
    def test_returns_ok_status_with_valid_text(self, mock_predict):
        """정상 텍스트 → status: ok + sentiment 포함"""
        result = analyze_sentiment_text("이 영화 진짜 재밌었어요!")

        assert result["status"] == "ok"
        assert "sentiment" in result

    def test_predict_called_with_correct_text(self, mock_predict):
        """predict_sentiment 에 입력 텍스트가 전달되는지 확인"""
        analyze_sentiment_text("재밌는 영화")
        mock_predict.assert_called_once_with("재밌는 영화")

    def test_returns_error_for_empty_text(self, mock_predict):
        """빈 텍스트 → status: error"""
        result = analyze_sentiment_text("")

        assert result["status"] == "error"
        assert result["detail"] == "text is empty"

    def test_returns_error_for_whitespace_only(self, mock_predict):
        """공백만 있는 텍스트 → strip() 후 빈 문자열이므로 error"""
        result = analyze_sentiment_text("   ")

        assert result["status"] == "error"
        assert result["detail"] == "text is empty"

    def test_predict_not_called_when_text_empty(self, mock_predict):
        """빈 텍스트일 때 predict_sentiment 호출 안 됨"""
        analyze_sentiment_text("")
        mock_predict.assert_not_called()


# ============================================================
# 3. views.py — POST /{id}/sentiment-async/ 테스트
# ============================================================


@pytest.mark.django_db
class TestSentimentAsyncByIdAction:
    def test_returns_202_with_task_id(self, client, review):
        """정상 요청 → 202 + task_id, status 반환"""
        mock_task = MagicMock()
        mock_task.id = "test-task-uuid-001"

        with patch("reviews.views.analyze_review_sentiment_by_id") as mock_fn:
            mock_fn.delay.return_value = mock_task
            res = client.post(
                f"/api/reviews/collected-reviews/{review.id}/sentiment-async/"
            )

        assert res.status_code == 202
        data = res.json()
        assert data["task_id"] == "test-task-uuid-001"
        assert data["status"] == "queued"

    def test_delay_called_with_review_id(self, client, review):
        """.delay() 에 review_id 가 전달되는지 확인"""
        mock_task = MagicMock()
        mock_task.id = "test-task-uuid-001"

        with patch("reviews.views.analyze_review_sentiment_by_id") as mock_fn:
            mock_fn.delay.return_value = mock_task
            client.post(f"/api/reviews/collected-reviews/{review.id}/sentiment-async/")

        mock_fn.delay.assert_called_once_with(review.id)


# ============================================================
# 4. views.py — POST /sentiment-async/ 텍스트 비동기 테스트
# ============================================================


@pytest.mark.django_db
class TestSentimentTextAsyncAction:
    ENDPOINT = "/api/reviews/collected-reviews/sentiment-async/"

    def test_returns_202_with_task_id(self, client):
        """정상 텍스트 → 202 + task_id 반환"""
        mock_task = MagicMock()
        mock_task.id = "test-task-uuid-002"

        with patch("reviews.views.analyze_sentiment_text") as mock_fn:
            mock_fn.delay.return_value = mock_task
            res = client.post(self.ENDPOINT, {"text": "재밌는 영화"}, format="json")

        assert res.status_code == 202
        assert res.json()["task_id"] == "test-task-uuid-002"
        assert res.json()["status"] == "queued"

    def test_returns_400_for_blank_text(self, client):
        """빈 텍스트 → serializer 검증 실패 → 400"""
        with patch("reviews.views.analyze_sentiment_text"):
            res = client.post(self.ENDPOINT, {"text": ""}, format="json")

        assert res.status_code == 400

    def test_delay_called_with_correct_text(self, client):
        """.delay() 에 입력 텍스트가 전달되는지 확인"""
        mock_task = MagicMock()
        mock_task.id = "test-task-uuid-002"
        text = "재밌는 영화"

        with patch("reviews.views.analyze_sentiment_text") as mock_fn:
            mock_fn.delay.return_value = mock_task
            client.post(self.ENDPOINT, {"text": text}, format="json")

        mock_fn.delay.assert_called_once_with(text)


# ============================================================
# 5. views.py — GET /sentiment-result/{task_id}/ 테스트
# AsyncResult mock 처리
# ============================================================


@pytest.mark.django_db
class TestSentimentResultAction:
    def _url(self, task_id):
        return f"/api/reviews/collected-reviews/sentiment-result/{task_id}/"

    def test_returns_pending_state(self, client):
        """PENDING 상태 → 200 + state: PENDING"""
        with patch("reviews.views.AsyncResult") as mock_async:
            mock_async.return_value.state = "PENDING"

            res = client.get(self._url("test-task-001"))

        assert res.status_code == 200
        assert res.json()["state"] == "PENDING"

    def test_returns_success_state_with_result(self, client):
        """SUCCESS 상태 → 200 + state: SUCCESS + result 포함"""
        mock_result = {
            "status": "ok",
            "sentiment": {"label": "positive", "score": 0.93},
        }

        with patch("reviews.views.AsyncResult") as mock_async:
            mock_async.return_value.state = "SUCCESS"
            mock_async.return_value.result = mock_result

            res = client.get(self._url("test-task-001"))

        data = res.json()
        assert res.status_code == 200
        assert data["state"] == "SUCCESS"
        assert data["result"] == mock_result

    def test_returns_failure_state_with_error(self, client):
        """FAILURE 상태 → 200 + state: FAILURE + error 포함"""
        with patch("reviews.views.AsyncResult") as mock_async:
            mock_async.return_value.state = "FAILURE"
            mock_async.return_value.result = Exception("모델 추론 실패")

            res = client.get(self._url("test-task-001"))

        data = res.json()
        assert res.status_code == 200
        assert data["state"] == "FAILURE"
        assert "error" in data

    def test_task_id_in_response(self, client):
        """응답에 task_id 가 포함되어야 함"""
        with patch("reviews.views.AsyncResult") as mock_async:
            mock_async.return_value.state = "PENDING"

            res = client.get(self._url("test-task-001"))

        assert res.json()["task_id"] == "test-task-001"
