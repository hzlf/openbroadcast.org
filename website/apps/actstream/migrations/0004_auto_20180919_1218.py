# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-19 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actstream', '0003_auto_20180919_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='verb',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
