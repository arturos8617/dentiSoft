"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import TEMPLATES
from .base import env
import tempfile

# GENERAL
# ------------------------------------------------------------------------------

CELERY_TASK_ALWAYS_EAGER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="FMf98tFc8zeXEGp4EWvDnbbSNuH98rfEkUNSyBIlzTjDRgRkpkarlhmEi5EmH1xW",
)
SITE_DOMAIN = env("DJANGO_SITE_DOMAIN", default="testserver")
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver/"

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = tempfile.mkdtemp(prefix="staticfiles_")

# Your stuff...
# ------------------------------------------------------------------------------
