# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveSmallIntegerField()),
                ('quantity', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_downloaded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(max_length=14)),
                ('value', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_valid', models.BooleanField(default=True)),
                ('batch', models.ForeignKey(to='vouchers.Batch')),
            ],
        ),
    ]
