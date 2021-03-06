# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.apps import AppConfig


class ActstreamConfig(AppConfig):
    name = "actstream"
    verbose_name = "Actstream"

    def ready(self):
        from .models import setup_generic_relations

        setup_generic_relations()
