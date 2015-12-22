from django.test import TestCase

from ..forms import GenerateInstantVoucherForm

class GenerateInstantVoucherFormTest(TestCase):
    """ We should ideally create a test package for this. This means we would have to create an insert function in billing. """

    def setUp(self):
        self.data = {'package': 1, 'quantity': 20}

    def test_save(self):
        form = GenerateInstantVoucherForm(self.data)
        form.is_valid()
        batch = form.save()
        self.assertEqual(batch.voucherinstant_set.count(), 20)
