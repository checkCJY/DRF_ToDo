from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings


class CustomPageNumberPagination(PageNumberPagination):
    """사용자 정의 페이지네이션 클래스"""

    # 기본 페이지 사이즈 설정 settings.py의 REST_FRAMEWORK["PAGE_SIZE"] 값을 사용
    default_page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 3)

    def paginate_queryset(self, queryset, request, view=None):
        """페이지네이션 적용 전 QuerySet 처리"""
        # URL 파라미터에서 page_size 값을 가져옴
        page_size = request.query_params.get("page_size", self.default_page_size)

        # page_size=all 이면 모든 데이터를 반환
        if page_size == "all":
            self.page_size = len(queryset)

        else:
            try:
                # page_size를 정수로 변환
                self.page_size = int(page_size)

            except ValueError:
                # 숫자가 아닌 값이 들어오면 기본값 사용
                self.page_size = self.default_page_size

        # DRF 기본 paginate_queryset 기능 실행
        return super().paginate_queryset(queryset, request, view)

    # 페이지네이션 응답 구조 정의

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    ("page_size", len(data)),
                    ("total_count", self.page.paginator.count),
                    ("page_count", self.page.paginator.num_pages),
                    ("current_page", self.page.number),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                ]
            )
        )


"""
1. 현재 페이지의 데이터 목록
2. 현재 페이지에 포함된 데이터 개수
3. 전체 데이터 개수
4. 전체 페이지 수
5. 현재 페이지 번호
6. 다음 페이지 URL
7. 이전 페이지 URL
"""
