from django.conf import settings

from .models import VoucherStandard, VoucherInstant

import random
import string

def generate_instant_vouchers():
    pass

def generate_standard_vouchers(price, quantity, batch):
    chars = string.digits
    for i in range(int(quantity)):
        pin = ''.join(random.choice(chars) for _ in range(settings.PIN_LENGTH))
        VoucherStandard.objects.create(pin=pin, value=price, batch=batch)

    return True

def zeropad(num):
    num = str(num)
    return ('0' * (10 - len(num))) + num

def write_batch(batch):
    file_name = batch.date_created.strftime('%d-%m-%Y_%I:%M') + '_' + str(batch.value) + 'GHS.csv'
    _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name
    vouchers = VoucherStandard.objects.filter(batch=batch)

    f = write_vouchers(vouchers, _file)

    return (f, file_name)

def write_vouchers(voucher_list, _file):
    for v in voucher_list:
        with open(_file, 'a') as f:
            f.write(zeropad(v.pk) + ',' + v.pin + '\n')

    return f
