# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 00:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20180726_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='create',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='login.Game'),
        ),
        migrations.AlterField(
            model_name='player',
            name='join',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joiner', to='login.Game'),
        ),
    ]