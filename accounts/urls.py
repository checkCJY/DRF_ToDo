from django.urls import path
from .views import SignupAPIView, SessionLogoutAPIView
from .views_page import LoginPageView, SignupPageView


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT


# app 네임은 왜 사용을 안할까? 템플릿 사용을 아직 안해서?

urlpatterns = [
    # API
    path("api/signup/", SignupAPIView.as_view(), name="api-signup"),
    # JWT 로그인(토큰 발급): access + refresh 반환
    path("api/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"
    ),  # access 만료 시 refresh로 재발급
    path("api/logout/", SessionLogoutAPIView.as_view(), name="api-logout"),
    # Pages
    path("signup-page/", SignupPageView.as_view(), name="page-signup"),
    path("login/", LoginPageView.as_view(), name="page-login"),
    # JWT 사용으로 인해 미사용코드
    # path("api/login/", SessionLoginAPIView.as_view(), name="api-login"),
]
