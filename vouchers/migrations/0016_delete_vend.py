# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0015_auto_20161212_0042'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vend',
        ),
    ]
