from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "change-me-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]
# Needed to test through a tunnel (ngrok, Cloudflare Tunnel, etc.): the tunnel terminates
# HTTPS and forwards plain HTTP to this dev server, so without SECURE_PROXY_SSL_HEADER
# Django thinks every request is insecure — and without CSRF_TRUSTED_ORIGINS it doesn't
# trust the tunnel's https:// origin either, so every POST 403s with "Origin checking failed."
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app", "https://*.ngrok-free.dev",
    "https://*.ngrok.io", "https://*.ngrok.app", "https://*.trycloudflare.com",
]
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "corsheaders","rest_framework","rest_framework.authtoken","accounts","experiences","moods","buddies",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# The React Native app's fetch calls aren't subject to browser CORS on a real phone,
# but testing it via `expo start --web` runs it in an actual browser, which is. Same
# permissive posture as ALLOWED_HOSTS/DEBUG above — fine for dev, not for production.
CORS_ALLOW_ALL_ORIGINS = True
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + ["ngrok-skip-browser-warning"]
ROOT_URLCONF = "safeher.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "safeher.wsgi.application"
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR / "db.sqlite3"}}
AUTH_USER_MODEL = "accounts.User"
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # SessionAuthentication keeps the existing web app working (cookies + CSRF);
    # TokenAuthentication is what the React Native app uses — no cookies/CSRF in a
    # mobile app, so it authenticates every request with a bearer token instead.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
