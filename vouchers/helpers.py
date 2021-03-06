from django.conf import settings

from .models import VoucherStandard, VoucherInstant

import random
import string

import requests

def get_packages():
    lst = [('', 'Select Package')]
    packages = requests.get(settings.PACKAGES_URL).json()
    for p in packages['results']:
        lst.append(p)
    return lst

def send_api_request(url, data):
    get_response = requests.get(url)
    post_response = requests.post(
          url,
          data=data,
          headers={"X-CSRFToken": get_response.cookies['csrftoken']},
          cookies=get_response.cookies
        )

    return post_response.json()

def id_generator(size=6, chars=string.ascii_uppercase.replace('O', '') + string.digits.replace('0', '')):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_instant_vouchers(price, quantity, batch, package_id):
    for i in range(int(quantity)):
        username = id_generator(size=settings.USERNAME_LENGTH, chars=string.ascii_lowercase) + '@' + settings.DOMAIN
        password = id_generator(size=settings.PASSWORD_LENGTH)
        VoucherInstant.objects.create(username=username, password=password, value=price, batch=batch)

        send_api_request(settings.INSTANT_VOUCHER_INSERT_URL,
            {'username': username, 'password': password, 'package_id': package_id})

    return True

def generate_standard_vouchers(price, quantity, batch):
    chars = string.digits
    for i in range(int(quantity)):
        pin = ''.join(random.choice(chars) for _ in range(settings.PIN_LENGTH))
        VoucherStandard.objects.create(pin=pin, value=price, batch=batch)

    return True