# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-01 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moldyreviews', '0003_auto_20161128_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='movie_year',
            field=models.CharField(default=2016, max_length=4),
            preserve_default=False,
        ),
    ]
