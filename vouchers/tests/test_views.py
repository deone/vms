from django.test import (
    TestCase, Client, RequestFactory
)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

from ..forms import GenerateStandardVoucherForm
from ..views import generate
from ..models import Batch, VoucherStandard
from ..helpers import generate_standard_vouchers

import json
import os

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

    def test_generate_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:generate_standard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], GenerateStandardVoucherForm))
        self.assertTemplateUsed(response, 'vouchers/generate_standard.html')

    def test_generate_post(self):
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
            voucher_form=GenerateStandardVoucherForm, redirect_to='vouchers:generate_standard')
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Vouchers generated successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('vouchers:generate_standard'))

    def test_batch_list_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:batches'))
        self.assertTrue('batches' in response.context)
        self.assertTemplateUsed(response, 'vouchers/batch_list.html')

    def test_download(self):
        price = 1
        quantity = 5
        batch = Batch.objects.create(value=price, quantity=quantity)
        generate_standard_vouchers(price, quantity, batch)

        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:download', kwargs={'pk': batch.pk}))

        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertNotEqual(response.content, '')

class APITests(TestCase):

    def setUp(self):
        # Create stub
        self.c = Client()
        self.data = {'pin': 12345678901234}
        self.voucher = json.loads(self.c.post(reverse('vouchers:insert'), data=self.data).content)

    def check_response(self, response):
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
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
        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)

    def test_redeem_voucher_does_not_exist(self):
        response = self.c.post(reverse('vouchers:redeem'), data={'pin': 12345678901231})
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 404)

    def test_redeem_used_voucher(self):
        # Invalidate
        self.c.post(reverse('vouchers:invalidate'), data={'id': self.voucher['id']})

        # Test
        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 500)

    def test_redeem_unsold_voucher(self):
        voucher = VoucherStandard.objects.get(pk=self.voucher['id'])
        voucher.is_sold = False
        voucher.save()

        response = self.c.post(reverse('vouchers:redeem'), data=self.data)
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 500)
        self.assertEqual(value['message'], 'You cannot use this voucher. It has not been sold.')

    def tearDown(self):
        # Delete stub
        self.c.post(reverse('vouchers:delete'), data=self.data)

class VoucherFetchTests(TestCase):

    def setUp(self):
        self.c = Client()

        batch_one = Batch.objects.create(value=1, quantity=1, voucher_type='STD')
        batch_two = Batch.objects.create(value=2, quantity=1, voucher_type='STD')
        batch_five = Batch.objects.create(value=5, quantity=1, voucher_type='STD')

        voucher_one = VoucherStandard.objects.create(pin='12345678901235', value=1, batch=batch_one)
        voucher_two = VoucherStandard.objects.create(pin='12345678901236', value=2, batch=batch_two)
        voucher_three = VoucherStandard.objects.create(pin='12345678901238', value=2, batch=batch_two)
        voucher_five = VoucherStandard.objects.create(pin='12345678901237', value=5, batch=batch_five)

    def test_fetch_vouchers_post(self):
        response = self.c.post(reverse('vouchers:fetch_vouchers'), data={'vendor_id': 2, 'quantity': 2, 'value': 2})
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'][0][1], '12345678901236')
        self.assertEqual(value['results'][1][1], '12345678901238')

    def test_fetch_vouchers_get(self):
        response = self.c.get(reverse('vouchers:fetch_vouchers'))
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['status'], 'ok')

    def test_fetch_voucher_values(self):
        response = self.c.get(reverse('vouchers:fetch_voucher_values'))
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)
        self.assertEqual(value['results'], [1, 2, 5])
