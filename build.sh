#!/usr/bin/env bash
# Render runs this on every deploy, before starting the web process.
# Invoked as `sh build.sh` from render.yaml so it works regardless of the file's
# executable bit, which Git on Windows does not reliably preserve.
set -o errexit

pip install --no-cache-dir -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Idempotent (update_or_create), so re-running it on each deploy just refreshes the
# valley data rather than duplicating it. Set SEED_PLACES=0 to skip.
if [ "${SEED_PLACES:-1}" = "1" ]; then
  python manage.py seed_valley_places
fi

# Free instances have no shell access, so the admin account has to be created here.
# Set these three in the Render dashboard, deploy once, then remove the password var.
# `|| true` because the command fails on the second deploy, when the user exists —
# that is expected and must not fail the whole build.
if [ -n "${DJANGO_SUPERUSER_PHONE:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  python manage.py createsuperuser --no-input \
    --phone "$DJANGO_SUPERUSER_PHONE" \
    --first_name "${DJANGO_SUPERUSER_FIRST_NAME:-Admin}" || true
fi
