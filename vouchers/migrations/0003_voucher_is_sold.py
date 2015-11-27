# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0002_vend'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
