# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0007_auto_20160103_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucherinstant',
            name='username',
            field=models.CharField(unique=True, max_length=24),
        ),
    ]
