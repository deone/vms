# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0004_auto_20151027_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='is_downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
