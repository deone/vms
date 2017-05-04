from django import forms
from django.conf import settings

from .models import VoucherStandard, Batch
from .helpers import (
    generate_standard_vouchers, generate_instant_vouchers, get_packages
)

class Common(forms.Form):
    quantity = forms.ChoiceField(label='Quantity',
        choices=VoucherStandard.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class GenerateStandardVoucherForm(Common):
    price = forms.ChoiceField(label='Price',
        choices=VoucherStandard.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GenerateStandardVoucherForm, self).__init__(*args, **kwargs)

    def save(self):
        price = self.cleaned_data['price']
        quantity = self.cleaned_data['quantity']

        batch = Batch.objects.create(user=self.user, value=price, quantity=quantity, voucher_type='STD')
        generate_standard_vouchers(price, quantity, batch)

        return batch

class GenerateInstantVoucherForm(Common):

    def __init__(self, *args, **kwargs):
        packages = kwargs.pop('packages', None)
        self.user = kwargs.pop('user', None)
        super(GenerateInstantVoucherForm, self).__init__(*args, **kwargs)
        self.fields['package'] = forms.ChoiceField(label='Package', choices=packages, widget=forms.Select({'class': 'form-control'}))

    def save(self):
        package_id = self.cleaned_data['package']
        quantity = self.cleaned_data['quantity']

        packages_dict = dict(get_packages())
        price = packages_dict[int(package_id)].split(' ')[3]
        
        batch = Batch.objects.create(user=self.user, value=price, quantity=quantity, voucher_type='INS')
        generate_instant_vouchers(price, quantity, batch, package_id)

        return batch