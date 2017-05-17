from django.conf.urls import include, url

from . import views
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

urlpatterns = [
    url(r'^download/(?P<pk>\d+)/$', views.download, name='download'),
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
    url(r'^create_test_user$', views.create_test_user, name='create_test_user'),
    url(r'^create_test_voucher$', views.create_test_voucher, name='create_test_voucher'),
    url(r'^delete_test_user$', views.delete_test_user, name='delete_test_user'),
    url(r'^delete_test_voucher$', views.delete_test_voucher, name='delete_test_voucher'),
    url(r'^invalidate$', views.invalidate, name='invalidate'),
    url(r'^get$', views.get, name='get_voucher'),
    url(r'^values/$', views.fetch_voucher_values, name='fetch_voucher_values'),
]