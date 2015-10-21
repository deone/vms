from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': AuthenticationForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
]
