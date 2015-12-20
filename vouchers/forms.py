from django import forms

from .models import Voucher, Batch
from .helpers import generate_vouchers

class Common(forms.Form):
    quantity = forms.ChoiceField(label='Quantity', choices=Voucher.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class GenerateStandardVoucherForm(Common):
    price = forms.ChoiceField(label='Price', choices=Voucher.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self):
        price = self.cleaned_data['price']
        quantity = self.cleaned_data['quantity']

        batch = Batch.objects.create(value=price, quantity=quantity)
        generate_vouchers(price, quantity, batch)

class GenerateInstantVoucherForm(Common):
    package = forms.CharField(label='Package', widget=forms.TextInput({'class': 'form-control'}))
