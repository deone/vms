from django.conf import settings

import random
import string

from .models import Voucher

def generate_vouchers(price, quantity, batch):
    chars = string.digits
    for i in range(int(quantity)):
        pin = ''.join(random.choice(chars) for _ in range(settings.PIN_LENGTH))
        Voucher.objects.create(pin=pin, value=price, batch=batch)

    return True

def zeropad(num):
    num = str(num)
    return ('0' * (10 - len(num))) + num

def write_batch(batch):
    file_name = batch.date_created.strftime('%d-%m-%Y_%I:%M') + '_' + str(batch.value) + 'GHS.csv'
    _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name
    vouchers = Voucher.objects.filter(batch=batch)

    for v in vouchers:
        with open(_file, 'a') as f:
            f.write(zeropad(v.pk) + ',' + v.pin + '\n')

    return (f, file_name)
