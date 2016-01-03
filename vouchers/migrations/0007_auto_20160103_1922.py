# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0006_auto_20160103_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucherinstant',
            name='sold_to',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='voucherstandard',
            name='sold_to',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
