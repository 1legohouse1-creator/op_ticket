"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include # include를 import 합니다.
from django.views.generic import RedirectView   # # 페이지 리디렉션 모듈
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),

    # 최상위 경로('/')로 접속 시 '/tickets/'로 자동 이동(리디렉션) ---
    path('', RedirectView.as_view(url='/tickets/', permanent=True)),

    # 'admin/'로 시작하는 URL은 admin이 처리하도록 추가 ---
    path('admin/', admin.site.urls),

    # 'tickets/'로 시작하는 모든 URL은 tickets 앱의 urls.py 파일에서 처리하도록 위임 ---
    path('tickets/', include('tickets.urls')),

    # 'ckeditor/'로 시작하는 URL을 ckeditor_uploader가 처리하도록 추가 ---
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# --- [추가] 개발 환경에서 미디어 파일(이미지 등)을 서빙하기 위한 설정 ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)