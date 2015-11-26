# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_id', models.PositiveSmallIntegerField()),
                ('date_of_vend', models.DateTimeField(default=django.utils.timezone.now)),
                ('voucher', models.ForeignKey(to='vouchers.Voucher')),
            ],
        ),
    ]
