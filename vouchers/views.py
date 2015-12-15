from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import GenerateVoucherForm
from .models import *
from .helpers import write_batch, zeropad

@login_required
def generate(request):
    context = {}
    if request.method == "POST":
        form = GenerateVoucherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vouchers generated successfully.')
            return redirect('vouchers:generate')
    else:
        form = GenerateVoucherForm()

    context.update({'form': form})
    return render(request, 'vouchers/generate.html', context)

class BatchList(ListView):
    template_name = 'vouchers/batch_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BatchList, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        batches = Batch.objects.all()
        return render(request, self.template_name, {'batches': batches})

def file_generator(_file):
    with open(_file.name, 'r') as f:
        for line in f:
            yield line

@ensure_csrf_cookie
def values(request):
    response = {}
    values = set(a.value for a in Voucher.objects.filter(is_sold=False))
    response.update({'code': 200, 'results': list(values)})
    return JsonResponse(response)

@login_required
def download(request, pk):
    batch = Batch.objects.get(pk=pk)
    _file, file_name = write_batch(batch)

    batch.is_downloaded = True
    batch.save()

    response = HttpResponse(file_generator(_file), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response

@ensure_csrf_cookie
def fetch(request):
    response = {}
    if request.method == 'POST':
        vendor_id = request.POST['vendor_id']
        value = request.POST['value']
        quantity = request.POST['quantity']
        vouchers = Voucher.objects.filter(value=value).exclude(is_sold=True)[:quantity]

        voucher_list = []
        for v in vouchers:
            Vend.objects.create(vendor_id=vendor_id, voucher=v)
            voucher_list.append([zeropad(v.pk), v.pin])
            v.is_sold = True
            v.save()
        response.update({'code': 200, 'results': voucher_list})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def redeem(request):
    response = {}

    if request.method == 'POST':
        pin = request.POST['pin']
        try:
            voucher = Voucher.objects.get(pin=pin)
        except Voucher.DoesNotExist:
            response.update({'code': 404, 'message': 'Voucher does not exist.'})
        else:
            if voucher.is_sold:
                if not voucher.is_valid:
                    response.update({'code': 500, 'message': 'Voucher has been used.'})
                else:
                    response.update({'code': 200, 'value': voucher.value, 'serial_number': voucher.pk})
            else:
                response.update({'code': 500, 'message': 'You cannot use this voucher. It has not been sold.'})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def invalidate(request):
    response = {}

    if request.method == 'POST':
        pk = request.POST['id']
        voucher = Voucher.objects.get(pk=pk)
        voucher.is_valid = False
        voucher.save()
        response.update({'code': 200})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def insert_stub(request):
    """ This function is strictly for testing the API. """
    response = {}
    if request.method == 'POST':
        pin = request.POST['pin']
        value = 5

        batch = Batch.objects.create(value=value, quantity=1, is_sold=True)
        voucher = Voucher.objects.create(pin=pin, value=value, batch=batch)
        response.update({'code': 200, 'id': voucher.pk, 'pin': voucher.pin})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def delete_stub(request):
    """ This function is strictly for testing the API. """
    response = {}
    if request.method == 'POST':
        pin = request.POST['pin']
        voucher = Voucher.objects.get(pin=pin)
        voucher.batch.delete()
        voucher.delete()
        response.update({'code': 200})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)
