from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import GenerateVoucherForm
from .models import Voucher, Batch
from .helpers import write_batch

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

class BatchList(ListView):
    template_name = 'voucher/batch_list.html'

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

@login_required
def download(request, pk):
    batch = Batch.objects.get(pk=pk)
    _file, file_name = write_batch(batch)

    batch.is_downloaded = True
    batch.save()

    response = HttpResponse(file_generator(_file), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response

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
