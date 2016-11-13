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

        request = factory.post(reverse('vouchers:generate_standard'), data={'price': '1', 'quantity': '20'})
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

    def test_download(self):
        price = 1
        quantity = 5
        batch = Batch.objects.create(user=self.user, value=price, quantity=quantity, voucher_type='STD')
        generate_standard_vouchers(price, quantity, batch)

        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:download', kwargs={'pk': batch.pk}))

        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertNotEqual(response.content, '')

class APITests(TestCase):

    def setUp(self):
        # Create stub
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        self.data = {'user': self.user, 'pin': '12345678901234', 'voucher_type': 'STD'}
        self.voucher = json.loads(self.c.post(reverse('vouchers:insert'), data=self.data).content)

    def check_response(self, response):
        value = json.loads(response.content)

        self.assertEqual(value['status'], 'ok')

    def test_redeem_get(self):
        response = self.c.get(reverse('vouchers:redeem'))
        self.check_response(response)

    def test_invalidate_get(self):
        response = self.c.get(reverse('vouchers:invalidate'))
        self.check_response(response)

    def test_insert_stub_get(self):
        response = self.c.get(reverse('vouchers:insert'))
        self.check_response(response)

    def test_delete_stub_get(self):
        response = self.c.get(reverse('vouchers:delete'))
        self.check_response(response)

    def test_redeem_post(self):
        # Write tests
        voucher = VoucherStandard.objects.get(pin=self.data['pin'])
        voucher.is_sold = True
        voucher.save()

        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)

    def test_redeem_voucher_does_not_exist(self):
        response = self.c.post(reverse('vouchers:redeem'), data={'pin': 12345678901231})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 404)

    def test_redeem_used_voucher(self):
        # Invalidate
        self.c.post(reverse('vouchers:invalidate'), data={'id': self.voucher['id']})

        # Test
        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(value['code'], 500)

    def test_redeem_unsold_voucher(self):
        voucher = VoucherStandard.objects.get(pk=self.voucher['id'])
        voucher.is_sold = False
        voucher.save()

        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(value['code'], 500)
        self.assertEqual(value['message'], 'You cannot use this voucher. It has not been sold.')

    def tearDown(self):
        # Delete stub
        self.c.post(reverse('vouchers:delete'), data={'voucher_id': self.voucher['id'], 'voucher_type': 'STD'})

class VoucherFetchTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

        batch_one = Batch.objects.create(user=self.user, value=1, quantity=1, voucher_type='STD')
        batch_two = Batch.objects.create(user=self.user, value=2, quantity=1, voucher_type='STD')
        batch_five = Batch.objects.create(user=self.user, value=5, quantity=1, voucher_type='STD')

        voucher_one = VoucherStandard.objects.create(pin='12345678901235', value=1, batch=batch_one)
        voucher_two = VoucherStandard.objects.create(pin='12345678901236', value=2, batch=batch_two)
        voucher_three = VoucherStandard.objects.create(pin='12345678901238', value=2, batch=batch_two)
        voucher_five = VoucherStandard.objects.create(pin='12345678901237', value=5, batch=batch_five)

        batch_one_ins = Batch.objects.create(user=self.user, value=2, quantity=2, voucher_type='INS')

        voucher_one_ins = VoucherInstant.objects.create(username='a@a.com', password='12345', value=2, batch=batch_one_ins)
        voucher_two_ins = VoucherInstant.objects.create(username='b@b.com', password='12345', value=2, batch=batch_one_ins)

    def test_fetch_standard_vouchers_post(self):
        response = self.c.post(reverse('vouchers:fetch_vouchers'),
            data={'vendor_id': 2, 'quantity': 2, 'value': 2, 'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'][0][1], '12345678901236')
        self.assertEqual(value['results'][1][1], '12345678901238')

    def test_fetch_instant_vouchers_post(self):
        response = self.c.post(reverse('vouchers:fetch_vouchers'),
            data={'vendor_id': 2, 'quantity': 2, 'value': 2, 'voucher_type': 'INS'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'][0][1], 'a@a.com')
        self.assertEqual(value['results'][1][1], 'b@b.com')

    def test_fetch_vouchers_get(self):
        response = self.c.get(reverse('vouchers:fetch_vouchers'), {'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(value['status'], 'ok')

    def test_fetch_standard_voucher_values(self):
        response = self.c.get(reverse('vouchers:fetch_voucher_values'), {'voucher_type': 'STD'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'], [1, 2, 5])

    def test_fetch_instant_voucher_values(self):
        response = self.c.get(reverse('vouchers:fetch_voucher_values'), {'voucher_type': 'INS'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'], [2])

    def test_sell_get(self):
        response = self.c.get(reverse('vouchers:sell'))
        value = json.loads(response.content)

        self.assertEqual(value['status'], 'ok')

    def test_sell_post(self):
        response = self.c.post(reverse('vouchers:sell'), data={'pin': '12345678901236'})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
        self.assertTrue(value['result']['is_sold'])

class InstantVoucherTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.response = self.c.post(reverse('vouchers:insert'),
            data={'voucher_type': 'INS', 'username': 'a@a.com', 'password': '12345'})
        self.voucher = json.loads(self.response.content)

    def test_insert_stub(self):
        self.assertEqual(self.voucher['code'], 200)
        self.assertEqual(self.voucher['username'], 'a@a.com')

    def test_delete_stub(self):
        response = self.c.post(reverse('vouchers:delete'),
            data={'voucher_type': 'INS', 'voucher_id': self.voucher['id']})
        value = json.loads(response.content)

        self.assertEqual(value['code'], 200)
