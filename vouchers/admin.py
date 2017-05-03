from django.contrib import admin

from .models import Batch

class BatchAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'value', 'quantity', 'voucher_type')

admin.site.register(Batch, BatchAdmin)