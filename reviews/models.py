from django.db import models


class CollectedReview(models.Model):
    """
    크롤링으로 수집된 영화 리뷰 데이터를 표현하는 Django Model
    id              : 기본 Primary Key
    title           : 리뷰 제목 -> 블로그 글 본문 저장
    doc_id          : 문서 고유 ID  -> 크롤링 URL을 SHA1 해시로 만든 값
    collected_at    : 데이터 수집 시각 -> 크롤링 파이프라인에서 언제 수집했는지 기록
    """

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    review = models.TextField()
    doc_id = models.CharField(
        max_length=255,
        null=True,  # DB에 NULL 허용
        blank=True,  # Django form에서도 비워둘 수 있음
    )
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # 실제 PostgreSQL 테이블 이름 지정
        # → Django 기본 이름(app_model)이 아닌
        #   기존 데이터 파이프라인 테이블을 그대로 사용
        db_table = "stg_movie_reviews"

        # managed=False
        # → Django가 이 테이블을 생성/삭제/마이그레이션하지 않음
        # → 이미 PostgreSQL에 존재하는 테이블을 읽기용으로 연결
        managed = False

    # Django Admin / Shell 출력용 문자열
    def __str__(self):
        return self.title
