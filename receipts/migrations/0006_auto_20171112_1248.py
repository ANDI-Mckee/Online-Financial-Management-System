# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0005_auto_20171112_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='notes',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
