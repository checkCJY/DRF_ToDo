from django.contrib import admin
from .models import CollectedReview

"""
Django Admin에 CollectedReview 모델 등록
@admin.register()
→ 해당 모델을 Django 관리자 페이지에 등록하는 데코레이터
→ admin.site.register() 대신 간단히 사용 가능
"""


@admin.register(CollectedReview)
class CollectedReviewAdmin(admin.ModelAdmin):
    """
    관리자 목록 화면에서 표시할 컬럼 설정
    id           : 데이터 기본 키
    title        : 리뷰 제목
    doc_id       : 중복 방지용 문서 ID
    collected_at : 데이터 수집 시각
    """

    list_display = ("id", "title", "doc_id", "collected_at")

    """
    관리자 페이지 검색 기능 설정
    title  : 제목 기준 검색 / review : 본문 기준 검색
    """
    search_fields = ("title", "review")
