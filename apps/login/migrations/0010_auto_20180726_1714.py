# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20180726_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='create',
        ),
        migrations.RemoveField(
            model_name='player',
            name='games',
        ),
        migrations.RemoveField(
            model_name='player',
            name='join',
        ),
        migrations.AddField(
            model_name='game',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='create', to='login.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='joiner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='join', to='login.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='games', to='login.Player'),
        ),
    ]