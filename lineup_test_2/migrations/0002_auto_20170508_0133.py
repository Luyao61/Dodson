# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-08 05:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup_test_2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eyewitnessstimuli',
            name='statementOnly',
            field=models.TextField(default='not initialized', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='StatementType',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='birth_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='comments',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='device',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='race',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='answer',
            field=models.IntegerField(choices=[(0, 0), (20, 20), (40, 40), (60, 60), (80, 80), (100, 100)], null=True),
        ),
    ]
