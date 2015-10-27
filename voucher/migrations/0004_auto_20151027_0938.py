# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0003_voucher_is_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField()),
                ('quantity', models.SmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='voucher',
            name='batch',
            field=models.ForeignKey(default=1, to='voucher.Batch'),
            preserve_default=False,
        ),
    ]
