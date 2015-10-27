from django.db import models
from django.utils import timezone

class Batch(models.Model):
    value = models.SmallIntegerField()
    quantity = models.SmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    is_downloaded = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.date_created.strftime('%B %d %Y, %I:%M%p'), str(self.value), str(self.quantity))

class Voucher(models.Model):
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
    value = models.SmallIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True) # this can be True or False
    batch = models.ForeignKey(Batch)
