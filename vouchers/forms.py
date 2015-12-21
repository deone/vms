from django import forms
from django.conf import settings

from .models import VoucherStandard, Batch
from .helpers import generate_standard_vouchers, generate_instant_vouchers

import requests

def get_packages():
    lst = [('', 'Select Package')]
    packages = requests.get(settings.PACKAGES_URL).json()
    for p in packages['results']:
        lst.append(p)
    return lst

class Common(forms.Form):
    quantity = forms.ChoiceField(label='Quantity',
        choices=VoucherStandard.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class GenerateStandardVoucherForm(Common):
    price = forms.ChoiceField(label='Price',
        choices=VoucherStandard.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self):
        price = self.cleaned_data['price']
        quantity = self.cleaned_data['quantity']

        batch = Batch.objects.create(value=price, quantity=quantity, voucher_type='STD')
        generate_standard_vouchers(price, quantity, batch)

class GenerateInstantVoucherForm(Common):
    package = forms.ChoiceField(label='Package', choices=get_packages(), widget=forms.Select({'class': 'form-control'}))

    def save(self):
        package_id = self.cleaned_data['package']
        quantity = self.cleaned_data['quantity']

        packages_dict = dict(get_packages())
        price = packages_dict[int(package_id)].split(' ')[3]

        batch = Batch.objects.create(value=price, quantity=quantity, voucher_type='INS')
        generate_instant_vouchers(price, quantity, batch)

        # This is where we insert generated username, password into radius database - Radcheck. Also insert package.
