# Django 기본 인증 유틸리티
#   - authenticate : 아이디/비밀번호로 사용자 인증 (실패 시 None 반환)
#   - login        : 인증된 사용자를 세션에 저장 (JWT에서 사용 안함)
#   - logout       : 현재 세션을 삭제하여 로그아웃 처리
from django.contrib.auth import logout

# DRF 핵심 컴포넌트
from rest_framework.views import APIView  # CBV 기반 API 뷰의 베이스 클래스
from rest_framework.response import Response  # JSON 직렬화된 HTTP 응답 객체
from rest_framework import status  # HTTP 상태 코드 상수 모음 (예: status.HTTP_200_OK)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)  # 인증 없이 누구나 접근 허용하는 권한 클래스

# 로컬 Serializer
from .serializers import SignupSerializer  # 회원가입 입력 데이터 검증 및 유저 생성


class SignupAPIView(APIView):
    """
    회원가입 API

    로그인하지 않은 사용자도 접근 가능 (AllowAny)
    JWT/세션과 무관하게 그대로 사용 가능하다.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """POST 요청으로 신규 사용자를 생성하고 201 응답을 반환한다."""

        # 요청 데이터를 Serializer에 전달 후 검증
        # raise_exception=True → 검증 실패 시 자동으로 400 에러 응답 반환
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 검증 완료 후 사용자 생성
        serializer.save()

        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


# JWT 부터 SessionLoginAPIView가 필요 없다.
# - /api/login/ 은 accounts/urls.py에서 TokenObtainPairView가 처리 (JWT 발급)
# - 따라서 authenticate/login 로직 제거

# class SessionLoginAPIView(APIView):
#     """
#     세션 로그인 API

#     로그인하지 않은 사용자도 접근 가능 (AllowAny)

#     """

#     permission_classes = [AllowAny]

#     def post(self, request):
#         """POST 요청으로 인증성공시 200 | 인증실패시 400"""

#         # 요청 데이터에서 username, password 추출
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")

#         # 사용자 인증
#         # username / password가 맞는지 확인
#         user = authenticate(request, username=username, password=password)

#         # 인증 실패
#         if not user:
#             return Response(
#                 {"detail": "아이디/비밀번호가 올바르지 않습니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # 인증 성공 → 세션 로그인 처리
#         login(request, user)

#         # 로그인 성공 응답
#         return Response({"detail": "로그인 성공"}, status=status.HTTP_200_OK)


class SessionLogoutAPIView(APIView):
    """
    세션 로그아웃 API
    - JWT 환경에서 '로그아웃'은 보통 프론트에서 토큰 삭제로 처리합니다.
    - 그래도 혹시 남아있을 수 있는 세션을 logout(request)로 정리해줍니다.
    """
    permission_classes = [IsAuthenticated]

    # POST 요청 처리
    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃"}, status=status.HTTP_200_OK)
