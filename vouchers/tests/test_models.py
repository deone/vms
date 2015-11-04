from django.test import TestCase

from ..models import Batch, Voucher

class VoucherModelsTests(TestCase):

    def setUp(self):
        self.batch = Batch.objects.create(value=2, quantity=5)

    def test_batch__str__(self):
        self.assertTrue(self.batch.__str__().endswith('2 5'))

    def test_voucher__str__(self):
        voucher = Voucher.objects.create(pin=12345678901234, value=2, batch=self.batch)
        self.assertTrue(voucher.__str__().endswith('2 GHS'))
