# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-05 12:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kalabash_contacts', '0002_auto_20180124_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sync_token', models.TextField(blank=True)),
                ('last_sync', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('_path', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='uid',
            field=models.CharField(max_length=100, null=True, unique=True, db_index=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='etag',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='addressbook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kalabash_contacts.AddressBook'),
        ),
    ]
