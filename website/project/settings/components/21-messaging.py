# -*- coding: utf-8 -*-
import os
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab

BASE_DIR = getattr(settings, "BASE_DIR")
DEBUG = getattr(settings, "DEBUG")


################################################################################
# messaging
################################################################################

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_CONFIRMATION_DAYS = 5
EMAIL_DEBUG = DEBUG
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"


################################################################################
# celery / rabbitmq
################################################################################
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_ACCEPT_CONTENT = ["pickle", "json"]


# base broker url - used for task servers
BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/openbroadcast.org"
PLAYOUT_BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/openbroadcast.org/playout"

CELERY_IMPORTS = (
    "importer.util.importer_tools",
    "base.pypo.gateway",
    # 'djcelery_email.tasks',
    #'media_asset.tasks',
    #'search.tasks',
)

CELERY_ROUTES = {
    "importer.models.import_task": {
        "queue": "import"
    },  # NOTE: assign import task to single-instance worker
    "importer.models.identify_task": {"queue": "process"},
    "importer.util.importer_tools.mb_complete_media_task": {"queue": "complete"},
    # TODO: check if completion tasks have to run on single-concurency instance
    "importer.util.importer_tools.mb_complete_release_task": {"queue": "complete"},
    "importer.util.importer_tools.mb_complete_artist_task": {"queue": "complete"},
    "alibrary.models.generate_media_versions_task": {"queue": "convert"},
    "alibrary.models.create_waveform_image": {"queue": "convert"},
    "media_asset.tasks.process_assets_for_media": {"queue": "convert"},
    "media_asset.models.process_waveform": {"queue": "grapher"},
    "media_asset.models.process_format": {"queue": "convert"},
    "media_asset.process_waveform": {"queue": "grapher"},
    "media_asset.process_format": {"queue": "convert"},
    "media_asset.tasks.process_waveform": {"queue": "grapher"},
    "media_asset.tasks.process_format": {"queue": "convert"},
    "exporter.models.process_task": {"queue": "export"},
    "search.signals.handle_save_task": {"queue": "index"},
    #'search.tasks.update_index': {'queue': 'index'},
}

CELERYBEAT_SCHEDULE = {
    "exporter-cleanup": {
        "task": "exporter.models.cleanup_exports",
        "schedule": timedelta(seconds=660),
    },
    "importer-cleanup": {
        "task": "importer.models.reset_hanging_files",
        "schedule": timedelta(seconds=300),
    },
    "asset-cleanup": {
        "task": "media_asset.models.clean_assets",
        "schedule": timedelta(hours=24),
    },
    # 'update-search-index': {
    #     'task': 'search.tasks.update_index',
    #     'schedule': crontab(minute='*'),
    # },
}

CELERY_EMAIL_TASK_CONFIG = {"queue": "celery", "rate_limit": "50/m"}


ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = "search.signals.CelerySignalProcessor"

"""
using django pushy
"""
# TODO: refactor settings in a way of:
# PUSHY_REGISTER_MODELS =
# PUSHY_REDIS_HOST =
# etc.
PUSHY_SETTINGS = {
    "MODELS": (
        "alibrary.playlist",
        "alibrary.media",
        "importer.import",
        "importer.importfile",
        "abcast.emission",
        "exporter.export",
        "abcast.channel",
    ),
    "SOCKET_SERVER": "//localhost:8888/",
    "CHANNEL_PREFIX": "pushy_",
    "DEBUG": DEBUG,
}
