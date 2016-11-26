from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from utils import send_report

class Batch(models.Model):

    class Meta:
        verbose_name_plural = 'batches'

    INSTANT = 'INS'
    STANDARD = 'STD'

    TYPE_CHOICES = (
        ('', 'Select Type'),
        (STANDARD, 'Standard'),
        (INSTANT, 'Instant'),
    )

    user = models.ForeignKey(User)
    value = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    voucher_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    is_downloaded = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.date_created.strftime('%B %d %Y, %I:%M%p'), str(self.value), str(self.quantity))

@receiver(post_save, sender=Batch)
def send_generation_report(sender, **kwargs):
    instance = kwargs['instance']

    VOUCHER_TYPE_DICT = {
        'STD': 'Standard',
        'INS': 'Instant'
    }

    username = instance.user.username
    if instance.user.first_name:
        username = instance.user.get_full_name()

    context = {
        'username': username,
        'batch_id': instance.id,
        'voucher_type': VOUCHER_TYPE_DICT[instance.voucher_type],
        'quantity': instance.quantity,
        'value': str(instance.value) + ' GHS',
        'total_value': str(int(instance.value) * int(instance.quantity)) + ' GHS'
    }

    send_report(context)

class Vend(models.Model):
    vendor_id = models.PositiveSmallIntegerField()
    value = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=10)
    date_of_vend = models.DateTimeField(default=timezone.now)

class Common(models.Model):
    class Meta:
        abstract = True

    value = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    sold_to = models.PositiveSmallIntegerField(null=True)
    batch = models.ForeignKey(Batch)
    vend = models.ForeignKey(Vend, null=True)

class VoucherInstant(Common):
    username = models.CharField(max_length=24, unique=True) # e.g.uxuw@spectrawireless.com
    password = models.CharField(max_length=6)

class VoucherStandard(Common):
    UNIT = 'GHS'

    # price choices
    ONE = 1
    TWO = 2
    FIVE = 5
    TEN = 10
    TWENTY = 20

    PRICE_CHOICES = (
        ('', 'Select Price'),
        (ONE, '1 ' + UNIT),
        (TWO, '2 ' + UNIT),
        (FIVE, '5 ' + UNIT),
        (TEN, '10 ' + UNIT),
        (TWENTY, '20 ' + UNIT),
    )

    # quantity choices
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100
    TWO_HUNDRED = 200
    FIVE_HUNDRED = 500

    QUANTITY_CHOICES = (
        ('', 'Select Quantity'),
        (TWENTY, '20'),
        (FIFTY, '50'),
        (HUNDRED, '100'),
        (TWO_HUNDRED, '200'),
        (FIVE_HUNDRED, '500'),
    )

    # Use id as serial number
    pin = models.CharField(max_length=14)

    def __str__(self):
        return '%s %s GHS' % (self.pk, self.value)
