# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_player_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='p1_name',
            field=models.CharField(default='yrfm1929', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='p2_name',
            field=models.CharField(default='Ariel', max_length=255),
            preserve_default=False,
        ),
    ]
