from django.conf.urls import include, url

from .import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
