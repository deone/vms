# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0005_auto_20151027_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='quantity',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='batch',
            name='value',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='value',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
