# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-07 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0009_auto_20171206_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='parent', to='lists.List'),
        ),
    ]