# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='selected',
            field=models.BooleanField(default='false'),
        ),
    ]