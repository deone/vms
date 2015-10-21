from django.db import models

class Voucher(models.Model):
    # Use id as serial number
    pin = models.CharField(max_length=14)
    value = models.SmallIntegerField()
    date_created = models.DateTimeField()
    expiry_date = models.DateTimeField()
