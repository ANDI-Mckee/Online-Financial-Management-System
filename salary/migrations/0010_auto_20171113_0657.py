# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0009_salary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='date',
            field=models.DateField(),
        ),
    ]
