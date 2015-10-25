from django import forms

from .models import Voucher

class GenerateVoucherForm(forms.Form):
    price = forms.ChoiceField(label='Price', choices=Voucher.PRICE_CHOICES)
    quantity = forms.ChoiceField(label='Quantity', choices=Voucher.QUANTITY_CHOICES)
