from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import GenerateVoucherForm
from .models import Voucher

# This is where we generate, download and redeem PINs.
@login_required
def generate(request):
    context = {}
    if request.method == "POST":
        form = GenerateVoucherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vouchers generated successfully.')
    else:
        form = GenerateVoucherForm()

    context.update({'form': form})
    return render(request, 'voucher/generate.html', context)

@csrf_protect
@ensure_csrf_cookie
def redeem(request):
    response = {}

    if request.method == 'POST':
        pin = request.POST['pin']
        obj = Voucher.objects.get(pin=pin)
        if obj:
            response.update({'code': 200, 'value': obj.value})
        else:
            response.update({'code': 404})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)
