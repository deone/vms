# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(max_length=14)),
                ('value', models.SmallIntegerField()),
                ('date_created', models.DateTimeField()),
                ('expiry_date', models.DateTimeField()),
            ],
        ),
    ]
