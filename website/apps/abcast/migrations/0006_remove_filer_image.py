# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-06-11 11:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0005_auto_20160819_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jingleset',
            name='main_image',
        ),
        migrations.RemoveField(
            model_name='station',
            name='main_image',
        ),
    ]