# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 18:40
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_auto_20180131_0820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from='name', primary_key=True, serialize=False, unique=True),
        ),
    ]
