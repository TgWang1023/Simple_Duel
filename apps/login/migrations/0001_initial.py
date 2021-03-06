# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p1_health', models.IntegerField()),
                ('p2_health', models.IntegerField()),
                ('p1_frz', models.BooleanField()),
                ('p2_frz', models.BooleanField()),
                ('p1_brn', models.BooleanField()),
                ('p2_brn', models.BooleanField()),
                ('p1_pos', models.BooleanField()),
                ('p2_pos', models.BooleanField()),
                ('battleground', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('pass_hs', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('role', models.IntegerField()),
                ('friends', models.ManyToManyField(related_name='_player_friends_+', to='login.Player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='login.Game')),
            ],
        ),
    ]
