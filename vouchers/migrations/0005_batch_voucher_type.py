# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0004_auto_20151221_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='voucher_type',
            field=models.CharField(default='STD', max_length=3, choices=[(b'', b'Select Type'), (b'STD', b'Standard'), (b'INS', b'Instant')]),
            preserve_default=False,
        ),
    ]
