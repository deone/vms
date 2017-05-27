from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VMSAuthenticationForm

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': VMSAuthenticationForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^vouchers/', include('vouchers.urls', namespace="vouchers")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
