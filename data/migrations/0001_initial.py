# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_icon', models.URLField()),
                ('item_sell_price', models.IntegerField()),
                ('item_buy_price', models.IntegerField()),
            ],
        ),
    ]