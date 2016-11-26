# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0011_auto_20161126_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='vend',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vend',
            name='voucher_type',
            field=models.CharField(default='STD', max_length=3, choices=[(b'', b'Select Type'), (b'STD', b'Standard'), (b'INS', b'Instant')]),
            preserve_default=False,
        ),
    ]
