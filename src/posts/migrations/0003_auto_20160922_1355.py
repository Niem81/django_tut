# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-22 13:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2016, 9, 22, 13, 55, 53, 75629, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
