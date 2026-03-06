from django.views.generic import TemplateView

"""
해당 템플릿을 렌더링해서 보여달라는 TemplateView
별도 로직이 필요 없을 때 가장 단순한 CBV
GET 요청을 받으면 templates_name 에 지정된 파일을 렌더링해서 반환

나중에 로그인 상태면 redirect 로직이 필요해지면 get() 오버라이드.
현재는 화면만 띄우는 용도이므로 이렇게 설정
"""


class SignupPageView(TemplateView):
    template_name = "accounts/signup.html"


class LoginPageView(TemplateView):
    template_name = "accounts/login.html"
