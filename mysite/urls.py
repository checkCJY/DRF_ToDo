from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("todo/", include("todo.urls")),
    path("interaction/", include("interaction.urls")),  # Part 10
    path("", lambda request: redirect("todo:list")),
    path("", include("accounts.urls")),  # 추가, 회원가입
    path("api/reviews/", include("reviews.urls")),
]

# DEBUG일 때만 media 파일을 /media/ (settings) 로 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
