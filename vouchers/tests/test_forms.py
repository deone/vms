from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from ..forms import GenerateInstantVoucherForm
from ..helpers import send_api_request, get_packages

class GenerateInstantVoucherFormTest(TestCase):

    def setUp(self):
        response = send_api_request(settings.PACKAGE_INSERT_URL,
            data={'package_type': 'Daily', 'volume': '3', 'speed': '1.5', 'price': 4})
        self.package = response['result']
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        self.data = {'package': self.package['id'], 'quantity': 20}

    def test_save(self):
        form = GenerateInstantVoucherForm(self.data, packages=get_packages(), user=self.user)
        form.is_valid()
        batch = form.save()
        self.assertEqual(batch.voucherinstant_set.count(), 20)

    def tearDown(self):
        send_api_request(settings.PACKAGE_DELETE_URL, data={'package_id': self.package['id']})
