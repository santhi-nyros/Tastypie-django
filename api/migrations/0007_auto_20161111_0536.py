# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(null=True, upload_to='static/videos'),
        ),
    ]
