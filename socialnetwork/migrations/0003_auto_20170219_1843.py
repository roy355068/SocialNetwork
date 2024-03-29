# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 23:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=430),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
