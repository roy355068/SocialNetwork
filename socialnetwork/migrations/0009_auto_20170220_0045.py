# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0008_auto_20170220_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='socialnetwork.Profile'),
        ),
    ]