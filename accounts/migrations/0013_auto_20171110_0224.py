# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20171110_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='age',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='staff',
            name='full_name',
            field=models.CharField(max_length=30),
        ),
    ]
