# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-06-11 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import uuid



def concat_uuid(apps, schema_editor):

    qs = apps.get_model('abcast', 'Channel')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    qs = apps.get_model('abcast', 'Emission')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    qs = apps.get_model('abcast', 'Jingle')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    qs = apps.get_model('abcast', 'JingleSet')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    qs = apps.get_model('abcast', 'OnAirItem')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    qs = apps.get_model('abcast', 'Station')
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0007_refactored_to_model_image'),
    ]

    operations = [
        migrations.RunPython(concat_uuid),

        migrations.AlterModelOptions(
            name='daypartset',
            options={'ordering': ('time_start',), 'verbose_name': 'Daypart set', 'verbose_name_plural': 'Daypart sets'},
        ),
        migrations.RemoveField(
            model_name='daypart',
            name='created',
        ),
        migrations.RemoveField(
            model_name='daypart',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='daypart',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='daypartset',
            name='created',
        ),
        migrations.RemoveField(
            model_name='daypartset',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='daypartset',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='role',
            name='created',
        ),
        migrations.RemoveField(
            model_name='role',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='role',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='channel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='emission',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='emission',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='emission',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='jingle',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='jingle',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='jingle',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='jingleset',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='jingleset',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='jingleset',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='onairitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='onairitem',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='onairitem',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),

    ]