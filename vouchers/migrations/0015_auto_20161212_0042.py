# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0014_auto_20161212_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucherinstant',
            name='value',
            field=models.DecimalField(max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='voucherstandard',
            name='value',
            field=models.DecimalField(max_digits=4, decimal_places=2),
        ),
    ]
