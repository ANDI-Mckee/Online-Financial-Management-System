# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 00:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_staff_is_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='workplace',
        ),
    ]
