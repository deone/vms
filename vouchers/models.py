from django.db import models
from django.utils import timezone

class Batch(models.Model):
    INSTANT = 'INS'
    STANDARD = 'STD'

    TYPE_CHOICES = (
        ('', 'Select Type'),
        (STANDARD, 'Standard'),
        (INSTANT, 'Instant'),
    )

    value = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    voucher_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    is_downloaded = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.date_created.strftime('%B %d %Y, %I:%M%p'), str(self.value), str(self.quantity))

class Vend(models.Model):
    vendor_id = models.PositiveSmallIntegerField()
    date_of_vend = models.DateTimeField(default=timezone.now)

class Common(models.Model):
    class Meta:
        abstract = True

    value = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    sold_to = models.PositiveSmallIntegerField()
    batch = models.ForeignKey(Batch)
    vend = models.ForeignKey(Vend, null=True)

class VoucherInstant(Common):
    username = models.CharField(max_length=24) # e.g.uxuw@spectrawireless.com
    password = models.CharField(max_length=6)

class VoucherStandard(Common):
    UNIT = 'GHS'

    # price choices
    ONE = 1
    TWO = 2
    FIVE = 5

    PRICE_CHOICES = (
        ('', 'Select Price'),
        (ONE, '1 ' + UNIT),
        (TWO, '2 ' + UNIT),
        (FIVE, '5 ' + UNIT),
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
