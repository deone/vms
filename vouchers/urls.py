from django.conf.urls import include, url

from . import views
from .forms import GenerateStandardVoucherForm, GenerateInstantVoucherForm

urlpatterns = [
    url(r'^download/(?P<pk>\d+)/$', views.download, name='download'),
    url(r'^generate/standard$', views.generate,
      {
        'template': 'vouchers/generate_standard.html',
        'voucher_form': GenerateStandardVoucherForm,
        'redirect_to': 'vouchers:generate-standard',
      },
      name='generate-standard'),
    url(r'^generate/instant$', views.generate,
      {
        'template': 'vouchers/generate_instant.html',
        'voucher_form': GenerateInstantVoucherForm,
        'redirect_to': 'vouchers:generate-instant',
      },
      name='generate-instant'),
    url(r'^batches/$', views.BatchList.as_view(), name='batches'),
    url(r'^insert/$', views.insert_stub, name='insert'),
    url(r'^delete/$', views.delete_stub, name='delete'),
    url(r'^redeem/$', views.redeem, name='redeem'),
    url(r'^invalidate/', views.invalidate, name='invalidate'),
    url(r'^fetch/', views.fetch_vouchers, name='fetch_vouchers'),
    url(r'^values/', views.voucher_values, name='voucher_values'),
]
