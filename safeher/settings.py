"""
Django settings for SafeHer.

Anything that differs between a laptop and Render is read from the environment, so
the same code runs in both places. Defaults are the *safe* (production) ones: if a
variable is missing we fail closed rather than silently serving with DEBUG on.

For local development, copy .env.example to .env — `manage.py runserver` reads it.
"""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env for local runs. On Render the variables are already in the environment,
# so this is a no-op there — and it never overrides a real environment variable.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env", override=False)
except ImportError:
    pass


def env_bool(name, default=False):
    return os.environ.get(name, "1" if default else "0").strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", False)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY is not set. Render generates one automatically via "
            "render.yaml; locally, put one in .env (see .env.example)."
        )
    SECRET_KEY = "insecure-development-key-do-not-use-in-production"

# Render injects RENDER_EXTERNAL_HOSTNAME with the service's real hostname, so the
# app works on the free *.onrender.com URL without anyone editing settings. localhost
# stays allowed so health checks and local runs aren't rejected by the host check.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"] + env_list("DJANGO_ALLOWED_HOSTS")
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
if DEBUG:
    ALLOWED_HOSTS.append("*")

# Render terminates HTTPS at its edge and forwards plain HTTP to Gunicorn, so without
# this Django thinks every request is insecure — which breaks secure cookies and turns
# SECURE_SSL_REDIRECT into a redirect loop. Same header the ngrok and Cloudflare
# tunnels set during development.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Django needs a full origin (with scheme) to trust a cross-origin POST. The dev
# tunnel wildcards stay because those hostnames change on every restart.
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS") + [
    "https://*.onrender.com",
    "https://*.ngrok-free.app", "https://*.ngrok-free.dev",
    "https://*.ngrok.io", "https://*.ngrok.app", "https://*.trycloudflare.com",
]
for _host in env_list("DJANGO_ALLOWED_HOSTS"):
    if _host in ("*", "localhost", "127.0.0.1") or _host.startswith("."):
        continue
    CSRF_TRUSTED_ORIGINS += ["https://" + _host, "http://" + _host]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "corsheaders","rest_framework","rest_framework.authtoken","accounts","experiences","moods","buddies",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves /static/ (and the admin's CSS) straight from the app process.
    # Render gives free instances no CDN or separate web server, so without this the
    # admin renders unstyled and the PWA icons 404.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The React Native app's fetch calls aren't subject to browser CORS on a real phone,
# so production doesn't need this open — only `expo start --web` does, which is a
# development scenario. Set CORS_ALLOW_ALL=1 to point Expo web at the deployed API.
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL", DEBUG)
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS")
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + ["ngrok-skip-browser-warning"]

ROOT_URLCONF = "safeher.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "safeher.wsgi.application"

# SQLite locally, Postgres on Render. This isn't a preference — Render's filesystem is
# wiped on every deploy and restart, so a SQLite file there would lose every signup.
# DATABASE_URL is wired to the managed database automatically by render.yaml.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", BASE_DIR / "db.sqlite3"),
    }
}
if os.environ.get("DATABASE_URL"):
    import dj_database_url

    # conn_max_age keeps connections open between requests instead of paying a TCP +
    # TLS handshake on every single one, which matters on a free instance.
    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)

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
if not DEBUG:
    # Drop the browsable HTML API in production: it renders a full page (and drags in
    # the template stack) for every API response, which is pure overhead here since
    # only the PWA and the mobile app ever call these endpoints.
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    # Hashed filenames plus pre-compressed variants, so WhiteNoise serves them with a
    # far-future cache header and never re-compresses at request time.
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Production hardening (all no-ops while DEBUG is on) --------------------
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
# Render's health check reaches the container over plain HTTP, so redirecting it to
# https would make every deploy look unhealthy and roll back.
SECURE_REDIRECT_EXEMPT = [r"^healthz/?$"]
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
# HSTS is deliberately off: it's a browser-cached promise that is hard to undo, and
# you may still move off the *.onrender.com domain. Set it to 2592000 once you're on
# your own domain and happy with it.
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0

# Logs go to stdout, which is where Render's dashboard log viewer reads from.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "{levelname} {asctime} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
}
