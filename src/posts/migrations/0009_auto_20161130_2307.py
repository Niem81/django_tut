# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_post_classif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_topic',
            field=models.CharField(choices=[('TC', 'Tecnologia'), ('PR', 'Programacion'), ('IN', 'Innovacion'), ('OT', 'Others')], max_length=2),
        ),
    ]
