# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0010_vend_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'verbose_name_plural': 'batches'},
        ),
        migrations.AddField(
            model_name='vend',
            name='value',
            field=models.PositiveSmallIntegerField(default=6),
            preserve_default=False,
        ),
    ]
