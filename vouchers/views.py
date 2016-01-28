from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import *
from .helpers import write_batch, zeropad, get_packages
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

@login_required
def generate(request, template=None, voucher_form=None, redirect_to=None):
    context = {}
    if request.method == "POST":
        if voucher_form == GenerateInstantVoucherForm:
            form = voucher_form(request.POST, packages=get_packages())
        else:
            form = voucher_form(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Vouchers generated successfully.')
            return redirect(redirect_to)
    else:
        if voucher_form == GenerateInstantVoucherForm:
            form = voucher_form(packages=get_packages())
        else:
            form = voucher_form()

    context.update({'form': form})
    return render(request, template, context)

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
def sell(request):
    response = {}
    if request.method == 'POST':
        pin = request.POST['pin']
        voucher = VoucherStandard.objects.get(pin=pin)
        voucher.is_sold = True
        voucher.save()
        voucher.__dict__.pop("_state")
        voucher.__dict__.pop("date_created")
        response.update({'code': 200, 'result': voucher.__dict__})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def fetch_voucher_values(request):
    voucher_type = request.GET['voucher_type']
    response = {}

    if voucher_type == 'STD':
        values = set(a.value for a in VoucherStandard.objects.filter(is_sold=False))
    elif voucher_type == 'INS':
        values = set(a.value for a in VoucherInstant.objects.filter(is_sold=False))

    response.update({'code': 200, 'results': list(values)})
    return JsonResponse(response)

@login_required
def download(request, pk):
    batch = Batch.objects.get(pk=pk)
    _file, file_name = write_batch(batch)

    batch.is_downloaded = True
    batch.save()

    response = HttpResponse(file_generator(_file), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response

@ensure_csrf_cookie
def fetch_vouchers(request):
    response = {}
    if request.method == 'POST':
        vendor_id = request.POST['vendor_id']
        voucher_type = request.POST['voucher_type']
        value = request.POST['value']
        quantity = request.POST['quantity']

        # - create a vend entry.
        vend = Vend.objects.create(vendor_id=vendor_id)

        # - fetch vouchers based on voucher_type.
        if voucher_type == 'STD':
            vouchers = VoucherStandard.objects.filter(value=value).exclude(is_sold=True)[:quantity]
        elif voucher_type == 'INS':
            vouchers = VoucherInstant.objects.filter(value=value).exclude(is_sold=True)[:quantity]

        voucher_list = []
        for v in vouchers:
            if isinstance(v, VoucherStandard):
                voucher_list.append([zeropad(v.pk), v.pin])
            elif isinstance(v, VoucherInstant):
                voucher_list.append([zeropad(v.pk), v.username, v.password])

            # - set each voucher entry is_sold=True, sold_to=vendor_id and vend=vend.
            v.is_sold = True
            v.sold_to = vendor_id
            v.vend = vend
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
            voucher = VoucherStandard.objects.get(pin=pin)
        except VoucherStandard.DoesNotExist:
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
        voucher = VoucherStandard.objects.get(pk=pk)
        voucher.is_sold = True # We are adding this for testing purposes. Normally, a voucher that has to be invalidated would have been sold.
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
        voucher_type = request.POST['voucher_type']
        value = 5

        batch = Batch.objects.create(value=value, quantity=1, voucher_type=voucher_type)

        if voucher_type=='STD':
            pin = request.POST['pin']
            voucher = VoucherStandard.objects.create(pin=pin, value=value, batch=batch)
            response.update({'code': 200, 'id': voucher.pk, 'pin': voucher.pin})
        elif voucher_type=='INS':
            username = request.POST['username']
            password = request.POST['password']
            voucher = VoucherInstant.objects.create(batch=batch, username=username, password=password, value=value)
            response.update({'code': 200, 'id': voucher.pk, 'username': voucher.username})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def delete_stub(request):
    """ This function is strictly for testing the API. """
    response = {}
    if request.method == 'POST':
        voucher_type = request.POST['voucher_type']
        pk = request.POST['voucher_id']

        if voucher_type == 'INS':
            voucher = VoucherInstant.objects.get(pk=pk)
        elif voucher_type == 'STD':
            voucher = VoucherStandard.objects.get(pk=pk)

        voucher.batch.delete()
        voucher.delete()
        response.update({'code': 200})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)
