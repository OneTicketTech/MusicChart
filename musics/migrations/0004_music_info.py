# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0003_auto_20160414_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='info',
            field=models.CharField(default=b'', max_length=250),
        ),
    ]
