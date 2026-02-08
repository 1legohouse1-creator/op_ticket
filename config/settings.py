from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t*7-brg)c2--9e8tkeqe4%=3=5v9=)r_puck9(%(0blrskko7r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['115.68.224.229','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "jazzmin",  # 관리자 페이지 테마
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tickets",  # op_ticket App
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '1legohouse1$default',          # 'Your databases'에 표시된 이름
        'USER': '1legohouse1',                  # 사용자 이름
        'PASSWORD': '!123456789!', # <--- 여기에 직접 입력
        'HOST': '1legohouse1.mysql.pythonanywhere-services.com', # Host address
        'PORT': '3306',                          # 기본 포트
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# 모든 정적 파일을 'staticfiles' 라는 이름의 폴더에 모으라고 지시합니다.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    # 페이지 탭에 표시될 제목
    "site_title": "OP 티켓 관리자",

    # 로그인 화면과 왼쪽 상단에 표시될 헤더
    "site_header": "OP 티켓 관리",

    # 로고를 사용할 경우 (이미지 파일 경로)
    # "site_logo": "path/to/your/logo.png",

    # 로그인 화면 상단에 표시될 문구
    "welcome_sign": "OP 준비 티켓 관리자 페이지에 오신 것을 환영합니다.",

    # 저작권 문구
    "copyright": "Your Hospital Name or Team",

    # 왼쪽 사이드바에 표시될 앱 순서 및 아이콘 설정
    "order_with_respect_to": ["auth", "tickets", "tickets.Ticket", "tickets.Precaution"],

    # 앱 별 아이콘 설정 (Font Awesome 아이콘 클래스 사용)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "tickets.Ticket": "fas fa-clipboard-list",
        "tickets.Precaution": "fas fa-exclamation-triangle",
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# settings.py 맨 아래 수정

# 1. 로그인이 안 된 사람은 '일반 로그인 페이지'로 보냅니다. (admin 아님!)
LOGIN_URL = '/accounts/login/'

# 2. 로그인 성공 시 메인 화면으로 이동
LOGIN_REDIRECT_URL = '/'

# 3. 로그아웃 시 다시 로그인 화면으로 이동
LOGOUT_REDIRECT_URL = '/accounts/login/'
