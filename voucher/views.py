from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import GenerateVoucherForm

# Create your views here.
# This is where we generate, download and redeem PINs.
@login_required
def generate(request):
    context = {}
    if request.method == "POST":
        form = GenerateVoucherForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = GenerateVoucherForm()

    context.update({'form': form})
    return render(request, 'voucher/generate.html', context)
