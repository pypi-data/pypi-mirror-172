# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 17:34
from __future__ import unicode_literals

from django.db import migrations, models


def set_path(apps, schema_editor):
    """Set path."""
    UserCalendar = apps.get_model("kalabash_radicale", "UserCalendar")
    for calendar in UserCalendar.objects.select_related("mailbox__domain"):
        calendar._path = "{}@{}/{}".format(
            calendar.mailbox.address, calendar.mailbox.domain.name,
            calendar.name
        )
        calendar.save()
    SharedCalendar = apps.get_model("kalabash_radicale", "SharedCalendar")
    for calendar in SharedCalendar.objects.select_related("domain"):
        calendar._path = "{}/{}".format(
            calendar.domain.name, calendar.name)
        calendar.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('kalabash_radicale', '0002_auto_20170831_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedcalendar',
            name='_path',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercalendar',
            name='_path',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.RunPython(set_path, backwards),
    ]
