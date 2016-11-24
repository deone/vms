from django.contrib import admin

from .models import Batch, Vend

class VendAdmin(admin.ModelAdmin):
    list_display = ('vendor_id', 'phone_number', 'date_of_vend')

class BatchAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'value', 'quantity', 'voucher_type')

admin.site.register(Batch, BatchAdmin)
admin.site.register(Vend, VendAdmin)