from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .helpers import get_packages
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

MODEL_VOUCHER_TYPE_MAP = {'INS': VoucherInstant, 'STD': VoucherStandard}

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

@api_view(['POST'])
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

    voucher_type = request.POST['voucher_type']
    value = request.POST['value']

    model = MODEL_VOUCHER_TYPE_MAP[voucher_type]

    # Return a list of one voucher
    voucher_list = model.objects.filter(value=value).exclude(is_valid=False)[:1]
    if not voucher_list:
        return Response({'message': 'Voucher not available.'}, status=404)
    else:
        response = {'serial_no': voucher_list[0].pk}
        if isinstance(voucher_list[0], VoucherInstant):
            response.update({
                'username': voucher_list[0].username,
                'password': voucher_list[0].password
            })
        else:
            response.update({'pin': voucher_list[0].pin})
        return Response(response)

@api_view(['POST'])
def invalidate(request):
    ### Receive voucher id and vendor id. Set voucher.is_valid to False and mark as sold.
    ### Return success message. 

    # Parameters:
    # - voucher_id: string e.g '1', '2'
    # - vendor_id: string e.g '1', '2'
    # Return success message:
    # - {'message': 'Voucher invalidated'}

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
    return Response({'message': 'Voucher invalidated.'})

@api_view(['POST'])
def create_test_user(request):
    ### This function is strictly for testing the API.
    ### Take in a username and create a user.
    ### Return user.

    # Parameters:
    # - username: string
    username = request.POST['username']
    user = User.objects.create_user(username, username, '12345')
    return Response({'username': user.username})

@api_view(['POST'])
def delete_test_user(request):
    username = request.POST['username']
    user = User.objects.get(username=username)
    user.delete()
    return Response({'message': 'Success!'})

@api_view(['POST'])
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

    value = 5
    quantity = 1
    creator = request.POST['creator']
    voucher_type = request.POST['voucher_type']

    user = User.objects.get(username=creator)
    batch = Batch.objects.create(user=user, value=value, quantity=quantity, voucher_type=voucher_type)

    if voucher_type == 'STD':
        pin = request.POST['pin']
        voucher = VoucherStandard.objects.create(pin=pin, value=value, batch=batch)
        return Response({'id': voucher.pk, 'pin': voucher.pin})
    else:
        username = request.POST['username']
        password = request.POST['password']
        voucher = VoucherInstant.objects.create(batch=batch, username=username, password=password, value=value)
        return Response({'id': voucher.pk, 'username': voucher.username})

@api_view(['POST'])
def delete_test_voucher(request):
    """ This function is strictly for testing the API. """
    voucher_type = request.POST['voucher_type']
    pk = request.POST['voucher_id']

    model = MODEL_VOUCHER_TYPE_MAP[voucher_type]

    try:
        voucher = model.objects.get(pk=pk)
    except model.DoesNotExist:
        pass
    else:
        voucher.delete()

    return Response({'message': 'Success!'})

class VoucherValuesList(APIView):
    def get(self, request, format=None):
        voucher_type = request.GET['voucher_type']
        model = MODEL_VOUCHER_TYPE_MAP[voucher_type]
        values = set(a.value for a in model.objects.filter(is_sold=False))
        return Response(values)