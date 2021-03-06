# -*- coding: utf-8 -*-
import os
from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static-dist")
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, "admin/")
ADMIN_MEDIA_PREFIX = "/static/admin/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static-src"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
    "dajaxice.finders.DajaxiceFinder",
)

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

FIXTURE_DIRS = [os.path.join(BASE_DIR, "fixtures")]

LEGACY_STORAGE_ROOT = None
