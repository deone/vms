# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0008_auto_20160106_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucherinstant',
            name='vend',
        ),
        migrations.RemoveField(
            model_name='voucherstandard',
            name='vend',
        ),
    ]
