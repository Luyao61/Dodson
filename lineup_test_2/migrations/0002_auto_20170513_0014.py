# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup_test_2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
