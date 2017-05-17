from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError

from .models import *
from .helpers import get_packages
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

@login_required
def generate(request, template=None, voucher_form=None, redirect_to=None):
    context = {}
    if request.method == "POST":
        if voucher_form == GenerateInstantVoucherForm:
            form = voucher_form(request.POST, packages=get_packages(), user=request.user)
        else:
            form = voucher_form(request.POST, user=request.user)

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

@ensure_csrf_cookie
def get(request):
    ### Receive voucher type and value. Return one voucher that isn't sold.
    ### Return 404 status and error message if voucher isn't found

    # Parameters:
    # - value: string e.g '1', '2'
    # - voucher_type: either 'STD' or 'INS'
    # Return voucher:
    # - {'pin': '12345678901234'}
    # or error:
    # - {'message': 'Voucher not available.'}, HTTP status: 500

    if request.method == 'POST':
        voucher_type = request.POST['voucher_type']
        value = request.POST['value']

        model_class_map = {'INS': VoucherInstant, 'STD': VoucherStandard}
        model = model_class_map[voucher_type]

        # Return a list of one voucher
        voucher_list = model.objects.filter(value=value).exclude(is_valid=False)[:1]
        if not voucher_list:
            return JsonResponse({'message': 'Voucher not available.', 'code': 'voucher-unavailable'}, status=404)
        else:
            response = {'serial_no': voucher_list[0].pk}
            if isinstance(voucher_list[0], VoucherInstant):
                response.update({
                    'username': voucher_list[0].username,
                    'password': voucher_list[0].password
                })
            else:
                response.update({'pin': voucher_list[0].pin})
            return JsonResponse(response)

    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
def invalidate(request):
    ### Receive voucher id and vendor id. Set voucher.is_valid to False and mark as sold.
    ### Return success message. 

    # Parameters:
    # - voucher_id: string e.g '1', '2'
    # - vendor_id: string e.g '1', '2'
    # Return success message:
    # - {'message': 'Voucher invalidated'}

    if request.method == 'POST':
        voucher_type = request.POST['voucher_type']
        voucher_id = request.POST['voucher_id']
        vendor_id = request.POST['vendor_id']

        if voucher_type == 'STD':
            voucher = VoucherStandard.objects.get(pk=voucher_id)
        else:
            voucher = VoucherInstant.objects.get(pk=voucher_id)

        voucher.is_sold = True # We are adding this for testing purposes. Normally, a voucher that has to be invalidated would have been sold.
        voucher.is_valid = False
        voucher.sold_to = vendor_id

        voucher.save()
        return JsonResponse({'message': 'Voucher invalidated.'})

    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
def create_test_user(request):
    ### This function is strictly for testing the API.
    ### Take in a username and create a user.
    ### Return user.

    # Parameters:
    # - username: string
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.create_user(username, username, '12345')
        return JsonResponse({'username': user.username})

    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
def delete_test_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username=username)
        user.delete()
        return JsonResponse({'message': 'Success!'})

    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
def create_test_voucher(request):
    ### This function is strictly for testing the API.
    ### Take in voucher creator username, voucher type, username and password
    ### for instant vouchers and pin for standard vouchers
    ### Create a batch and a voucher.
    ### Return voucher.

    # Parameters:
    # - creator: string
    # - voucher type: e.g. 'STD', 'INS'
    # - username: string
    # - password: string
    # - pin: string
    # Return voucher object

    if request.method == 'POST':
        value = 5
        quantity = 1
        creator = request.POST['creator']
        voucher_type = request.POST['voucher_type']

        user = User.objects.get(username=creator)
        batch = Batch.objects.create(user=user, value=value, quantity=quantity, voucher_type=voucher_type)

        if voucher_type == 'STD':
            pin = request.POST['pin']
            voucher = VoucherStandard.objects.create(pin=pin, value=value, batch=batch)
            return JsonResponse({'id': voucher.pk, 'pin': voucher.pin})
        else:
            username = request.POST['username']
            password = request.POST['password']
            voucher = VoucherInstant.objects.create(batch=batch, username=username, password=password, value=value)
            return JsonResponse({'id': voucher.pk, 'username': voucher.username})

    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
def delete_test_voucher(request):
    """ This function is strictly for testing the API. """
    if request.method == 'POST':
        voucher_type = request.POST['voucher_type']
        pk = request.POST['voucher_id']

        model = VoucherStandard
        if voucher_type == 'INS':
            model = VoucherInstant

        try:
            voucher = model.objects.get(pk=pk)
        except model.DoesNotExist:
            pass
        else:
            voucher.delete()

        return JsonResponse({'message': 'Success!'})

    return JsonResponse({'status': 'ok'})