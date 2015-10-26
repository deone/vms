# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0002_remove_voucher_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
