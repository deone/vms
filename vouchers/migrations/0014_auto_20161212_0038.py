# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0013_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='value',
            field=models.DecimalField(max_digits=4, decimal_places=2),
        ),
    ]
