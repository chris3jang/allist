# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-01 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.AddField(
            model_name='list',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='_list_children_+', to='lists.List'),
        ),
    ]