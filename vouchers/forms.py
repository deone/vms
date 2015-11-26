from django import forms

from .models import Voucher, Batch
from .helpers import generate_vouchers

class GenerateVoucherForm(forms.Form):
    price = forms.ChoiceField(label='Price', choices=Voucher.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.ChoiceField(label='Quantity', choices=Voucher.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self):
        price = self.cleaned_data['price']
        quantity = self.cleaned_data['quantity']

        batch = Batch.objects.create(value=price, quantity=quantity)
        generate_vouchers(price, quantity, batch)
