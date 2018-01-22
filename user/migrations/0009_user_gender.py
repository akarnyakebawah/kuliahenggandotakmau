# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-13 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_add picture field'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('other', 'Other'), ('male', 'Male'), ('female', 'Female')], default='other', max_length=16, verbose_name='gender'),
        ),
    ]
