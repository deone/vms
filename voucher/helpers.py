from django.utils import timezone
from django.conf import settings

import random
import string

from .models import Voucher

def generate_vouchers(price, quantity, batch):
    chars = string.digits
    for i in range(int(quantity)):
        pin = ''.join(random.choice(chars) for _ in range(settings.PIN_LENGTH))
        Voucher.objects.create(pin=pin, value=price, date_created=timezone.now(), batch=batch)
