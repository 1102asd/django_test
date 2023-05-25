# flake8: noqa
from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # in memory
    }
}
LANGUAGE_CODE = "en-us"

CELERY_BROKER_URL = "memory://"
CELERY_TASK_ALWAYS_EAGER = True
SHOW_SWAGGER_DOCS = True
