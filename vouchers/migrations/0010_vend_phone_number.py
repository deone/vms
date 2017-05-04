# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0009_batch_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vend',
            name='phone_number',
            field=models.CharField(default='0231802940', max_length=10),
            preserve_default=False,
        ),
    ]
