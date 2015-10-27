from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import GenerateVoucherForm
from .models import Voucher

# This is where we generate, download and redeem PINs.

@login_required
def dashboard(request):
    return render(request, 'voucher/dashboard.html')

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

@login_required
def download(request):
    pass

@csrf_protect
@ensure_csrf_cookie
def redeem(request):
    response = {}

    if request.method == 'POST':
        pin = request.POST['payload']
        try:
            obj = Voucher.objects.get(pin=pin)
        except Voucher.DoesNotExist:
            response.update({'code': 404})
        else:
            if not obj.is_valid:
                response.update({'code': 0})
            else:
                response.update({'code': 200, 'value': obj.value, 'serial_number': obj.pk})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@csrf_protect
@ensure_csrf_cookie
def invalidate(request):
    response = {}

    if request.method == 'POST':
        pk = request.POST['payload']
        obj = Voucher.objects.get(pk=pk)
        obj.is_valid = False
        obj.save()
        response.update({'code': 200})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)
