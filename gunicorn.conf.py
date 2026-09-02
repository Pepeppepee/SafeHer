"""
Gunicorn tuning for a Render free instance (512MB RAM, 0.1 CPU).

The usual advice (2 * CPU + 1 workers) would start several processes, each holding
its own copy of Django at roughly 70-90MB resident — which does not fit. Instead we
run a single worker with threads: this app is I/O-bound (database reads, template
rendering), so threads absorb concurrent requests at almost no memory cost.

That leaves roughly 400MB of headroom on a free instance. If you later upgrade to a
paid plan, raise WEB_CONCURRENCY to 2 rather than adding more threads.
"""
import os

# Render tells the app which port to listen on; 8000 is the local default.
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")

# WEB_CONCURRENCY is Render's own convention for worker count, so setting it in the
# dashboard works without touching this file.
workers = int(os.environ.get("WEB_CONCURRENCY", "1"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
worker_class = "gthread"

# Load Django once before forking so the interpreter, settings, URL conf and compiled
# templates are shared rather than duplicated per worker.
preload_app = True

# Recycle workers periodically so any slow leak is bounded instead of growing until
# the instance is OOM-killed. The jitter avoids restarting everything in lockstep.
max_requests = 500
max_requests_jitter = 50

# Free instances sleep after inactivity and are slow to wake, so the first request
# after a cold start needs a generous timeout.
timeout = 120
graceful_timeout = 30
keepalive = 5

accesslog = "-" if os.environ.get("GUNICORN_ACCESS_LOG", "1") == "1" else None
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
