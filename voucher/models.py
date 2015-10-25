from django.db import models

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
    date_created = models.DateTimeField()
