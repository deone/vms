from django.test import (
    TestCase, Client, RequestFactory
)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

from ..forms import GenerateVoucherForm
from ..views import generate
from ..models import Batch
from ..helpers import generate_vouchers

import json

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

    def test_generate_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:generate'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], GenerateVoucherForm))
        self.assertTemplateUsed(response, 'vouchers/generate.html')

    def test_generate_post(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})

        factory = RequestFactory()
        session = SessionMiddleware()

        request = factory.post(reverse('vouchers:generate'), data={'price': '1', 'quantity': '20'})
        request.user = self.user

        session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = generate(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Vouchers generated successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('vouchers:generate'))

    def test_batch_list_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:batches'))
        self.assertTrue('batches' in response.context)
        self.assertTemplateUsed(response, 'vouchers/batch_list.html')

    def test_download(self):
        price = 1
        quantity = 5
        batch = Batch.objects.create(value=price, quantity=quantity)
        generate_vouchers(price, quantity, batch)

        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vouchers:download', kwargs={'pk': batch.pk}))

        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('0000000002' in response.content)

    def test_redeem_get(self):
        response = self.c.get(reverse('vouchers:redeem'))
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['status'], 'ok')

    def test_redeem_post(self):
        data = {'pin': 12345678901234}

        # Create stub
        self.c.post(reverse('vouchers:insert'), data=data)

        # Write tests
        response = self.c.post(reverse('vouchers:redeem'), data=data)
        value = json.loads(response.content)

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(value['code'], 200)

        # Delete stub
        self.c.post(reverse('vouchers:delete'), data=data)
