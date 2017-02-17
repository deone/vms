from django.conf.urls import include, url

from . import views
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

urlpatterns = [
    url(r'^download/(?P<pk>\d+)/$', views.download, name='download'),
    url(r'^sell/$', views.sell, name='sell'),
    url(r'^generate/standard/$', views.generate,
    {
        'template': 'vouchers/generate_standard.html',
        'voucher_form': GenerateStandardVoucherForm,
        'redirect_to': 'vouchers:generate_standard',
    },
    name='generate_standard'),
    url(r'^generate/instant/$', views.generate,
    {
        'template': 'vouchers/generate_instant.html',
        'voucher_form': GenerateInstantVoucherForm,
        'redirect_to': 'vouchers:generate_instant',
    },
    name='generate_instant'),
    url(r'^batches/$', views.BatchList.as_view(), name='batches'),
    url(r'^insert/$', views.insert_stub, name='insert'),
    url(r'^delete/$', views.delete_stub, name='delete'),
    url(r'^redeem/$', views.redeem, name='redeem'),
    url(r'^invalidate/$', views.invalidate, name='invalidate'),
    url(r'^get/$', views.get_voucher, name='get_voucher'),
    url(r'^values/$', views.fetch_voucher_values, name='fetch_voucher_values'),
]