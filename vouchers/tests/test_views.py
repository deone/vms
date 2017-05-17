from django.test import (
    TestCase, Client, RequestFactory
)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.conf import settings

from .. import forms
from ..views import generate
from ..models import Batch, VoucherStandard, VoucherInstant
from ..helpers import generate_standard_vouchers, send_api_request

import json
import os

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

    def test_generate_standard_vouchers_GET(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:generate_standard'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], forms.GenerateStandardVoucherForm))
        self.assertTemplateUsed(response, 'vouchers/generate_standard.html')

    def test_generate_instant_vouchers_GET(self):
        # Create package - we don't need this since this is a get request.
        """ response = send_api_request(settings.PACKAGE_INSERT_URL,
            data={'package_type': 'Daily', 'volume': '3', 'speed': '1.5', 'price': 4})
        package = response['result'] """

        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:generate_instant'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], forms.GenerateInstantVoucherForm))
        self.assertTemplateUsed(response, 'vouchers/generate_instant.html')

        # Delete package
        # send_api_request(settings.PACKAGE_DELETE_URL, data={'package_id': package['id']})

    # Refactor these
    def test_generate_standard_vouchers_POST(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})

        factory = RequestFactory()
        session = SessionMiddleware()

        request = factory.post(reverse('vouchers:generate_standard'), data={'price': '2', 'quantity': '20'})
        request.user = self.user

        session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = generate(request, template='vouchers/generate_standard.html',
            voucher_form=forms.GenerateStandardVoucherForm, redirect_to='vouchers:generate_standard')
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Vouchers generated successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('vouchers:generate_standard'))

    def test_generate_instant_vouchers_POST(self):
        # Create package
        response = send_api_request(settings.PACKAGE_INSERT_URL,
            data={'package_type': 'Daily', 'volume': '3', 'speed': '1.5', 'price': 4})
        package = response['result']

        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})

        factory = RequestFactory()
        session = SessionMiddleware()

        request = factory.post(reverse('vouchers:generate_instant'), data={'package': package['id'], 'quantity': '20'})
        request.user = self.user

        session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = generate(request, template='vouchers/generate_instant.html',
            voucher_form=forms.GenerateInstantVoucherForm, redirect_to='vouchers:generate_instant')
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Vouchers generated successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('vouchers:generate_instant'))

        # Delete package
        send_api_request(settings.PACKAGE_DELETE_URL, data={'package_id': package['id']})
    ########

    def test_batch_list_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:batches'))
        self.assertTrue('batches' in response.context)
        self.assertTemplateUsed(response, 'vouchers/batch_list.html')

class APITests(TestCase):

    def setUp(self):
        # Create test voucher
        self.c = Client()

        self.user_data = {'username': 'z@z.com'}
        self.user = json.loads(self.c.post(reverse('vouchers:create_test_user'), data=self.user_data).content)

        # Standard
        std_voucher_data = {'creator': self.user['username'], 'pin': '12345678901234', 'voucher_type': 'STD'}
        self.std_voucher = json.loads(self.c.post(reverse('vouchers:create_test_voucher'), data=std_voucher_data).content)

        # Instant
        ins_voucher_data = {'creator': self.user['username'], 'username': 'a@pty.gh', 'password': 'CTYB', 'voucher_type': 'INS'}
        self.ins_voucher = json.loads(self.c.post(reverse('vouchers:create_test_voucher'), data=ins_voucher_data).content)

    def check_response(self, response):
        value = json.loads(response.content)
        self.assertEqual(value['status'], 'ok')

    def test_invalidate(self):
        response = self.c.get(reverse('vouchers:invalidate'))
        self.check_response(response)

        # Invalidate standard voucher
        response = self.c.post(reverse('vouchers:invalidate'), data={
            'voucher_id': self.std_voucher['id'],
            'vendor_id': '1',
            'voucher_type': 'STD'
        })
        value = json.loads(response.content)
        self.assertEqual(value['message'], 'Voucher invalidated.')

        # Invalidate instant voucher
        response = self.c.post(reverse('vouchers:invalidate'), data={
            'voucher_id': self.ins_voucher['id'],
            'vendor_id': '1',
            'voucher_type': 'INS'
        })

    def test_create_test_voucher(self):
        response = self.c.get(reverse('vouchers:create_test_user'))
        self.check_response(response)

        response = self.c.get(reverse('vouchers:create_test_voucher'))
        self.check_response(response)

        std_voucher = VoucherStandard.objects.get(pin='12345678901234')
        ins_voucher = VoucherInstant.objects.get(username='a@pty.gh')

        self.assertEqual(std_voucher.batch.user.username, self.user['username'])
        self.assertEqual(ins_voucher.batch.user.username, self.user['username'])

    def test_delete_test_voucher(self):
        response = self.c.get(reverse('vouchers:delete_test_voucher'))
        self.check_response(response)

        # Delete standard voucher
        response = json.loads(self.c.post(reverse('vouchers:delete_test_voucher'), data={
            'voucher_id': self.std_voucher['id'],
            'voucher_type': 'STD'
        }).content)
        self.assertEqual(response['message'], 'Success!')

        response = json.loads(self.c.post(reverse('vouchers:delete_test_voucher'), data={
            'voucher_id': self.ins_voucher['id'],
            'voucher_type': 'INS'
        }).content)
        self.assertEqual(response['message'], 'Success!')

        response = self.c.get(reverse('vouchers:delete_test_user'))
        self.check_response(response)

    def tearDown(self):
        # Delete test voucher
        self.c.post(reverse('vouchers:delete_test_voucher'), data={'voucher_id': self.std_voucher['id'], 'voucher_type': 'STD'})
        self.c.post(reverse('vouchers:delete_test_voucher'), data={'voucher_id': self.ins_voucher['id'], 'voucher_type': 'INS'})
        self.c.post(reverse('vouchers:delete_test_user'), data={'username': self.user['username']})

class VoucherGetTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

        self.batch_one = Batch.objects.create(user=self.user, value=1, quantity=1, voucher_type='STD')
        self.batch_two = Batch.objects.create(user=self.user, value=2, quantity=1, voucher_type='STD')
        self.batch_five = Batch.objects.create(user=self.user, value=5, quantity=1, voucher_type='STD')

        voucher_one = VoucherStandard.objects.create(pin='12345678901235', value=1, batch=self.batch_one)
        voucher_two = VoucherStandard.objects.create(pin='12345678901236', value=2, batch=self.batch_two)
        voucher_three = VoucherStandard.objects.create(pin='12345678901238', value=2, batch=self.batch_two)
        voucher_five = VoucherStandard.objects.create(pin='12345678901237', value=5, batch=self.batch_five)

        self.batch_one_ins = Batch.objects.create(user=self.user, value=2, quantity=2, voucher_type='INS')

        voucher_one_ins = VoucherInstant.objects.create(username='a@a.com', password='12345', value=2, batch=self.batch_one_ins)
        voucher_two_ins = VoucherInstant.objects.create(username='b@b.com', password='12345', value=2, batch=self.batch_one_ins)

    def test_get_standard_voucher_post(self):
        response = self.c.post(reverse('vouchers:get_voucher'),
            data={'value': 2, 'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(value['pin'], '12345678901236')
        self.assertTrue('serial_no' in value)

    def test_get_instant_voucher_post(self):
        response = self.c.post(reverse('vouchers:get_voucher'),
            data={'value': 2, 'voucher_type': 'INS'})
        value = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(value['username'], 'a@a.com')
        self.assertEqual(value['password'], '12345')
        self.assertTrue('serial_no' in value)

    def test_get_voucher_voucher_not_available(self):
        # Delete vouchers
        self.batch_one.delete()
        self.batch_two.delete()
        self.batch_five.delete()
        self.batch_one_ins.delete()

        response = self.c.post(reverse('vouchers:get_voucher'),
            data={'value': 2, 'voucher_type': 'INS'})
        value = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(value, {'message': 'Voucher not available.', 'code': 'voucher-unavailable'})

    def test_get_voucher_get(self):
        response = self.c.get(reverse('vouchers:get_voucher'), {'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(value['status'], 'ok')

    def test_fetch_standard_voucher_values(self):
        response = self.c.get(reverse('vouchers:fetch_voucher_values'), {'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'], ['1.00', '2.00', '5.00'])

    def test_fetch_instant_voucher_values(self):
        response = self.c.get(reverse('vouchers:fetch_voucher_values'), {'voucher_type': 'INS'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'], ['2.00'])

class InstantVoucherTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        self.response = self.c.post(reverse('vouchers:create_test_voucher'),
            data={'creator': self.user.username, 'voucher_type': 'INS', 'username': 'a@a.com', 'password': '12345'})
        self.voucher = json.loads(self.response.content)

    def test_create_test_voucher(self):
        self.assertEqual(self.voucher['username'], 'a@a.com')

    def test_delete_test_voucher(self):
        response = self.c.post(reverse('vouchers:delete_test_voucher'),
            data={'voucher_type': 'INS', 'voucher_id': self.voucher['id']})
        value = json.loads(response.content)

        self.assertEqual(value['message'], 'Success!')