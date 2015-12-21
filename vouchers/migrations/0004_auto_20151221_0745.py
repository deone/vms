# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0003_voucher_is_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherInstant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_sold', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=24)),
                ('password', models.CharField(max_length=6)),
                ('batch', models.ForeignKey(to='vouchers.Batch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VoucherStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_sold', models.BooleanField(default=False)),
                ('pin', models.CharField(max_length=14)),
                ('batch', models.ForeignKey(to='vouchers.Batch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='batch',
        ),
        migrations.AlterField(
            model_name='vend',
            name='voucher',
            field=models.ForeignKey(to='vouchers.VoucherStandard'),
        ),
        migrations.DeleteModel(
            name='Voucher',
        ),
    ]
