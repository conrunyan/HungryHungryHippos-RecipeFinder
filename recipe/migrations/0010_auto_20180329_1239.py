# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-29 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20180327_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('D', 'Hard')], max_length=1, null=True),
        ),
    ]
