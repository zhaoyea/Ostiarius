# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostiarius', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='maintenance_mode',
            field=models.BooleanField(default=False),
        ),
    ]
