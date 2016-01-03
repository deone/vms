# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0005_batch_voucher_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vend',
            name='voucher',
        ),
        migrations.AddField(
            model_name='voucherinstant',
            name='sold_to',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voucherinstant',
            name='vend',
            field=models.ForeignKey(to='vouchers.Vend', null=True),
        ),
        migrations.AddField(
            model_name='voucherstandard',
            name='sold_to',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voucherstandard',
            name='vend',
            field=models.ForeignKey(to='vouchers.Vend', null=True),
        ),
    ]
