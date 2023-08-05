# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-05 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kalabash_contacts', '0004_auto_20181005_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
        migrations.AlterField(
            model_name='contact',
            name='addressbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kalabash_contacts.AddressBook'),
        ),
    ]
