from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^download/(?P<pk>\d+)/$', views.download, name='download'),
    url(r'^generate/$', views.generate, name='generate'),
    url(r'^batches/$', views.BatchList.as_view(), name='batches'),
    url(r'^insert/$', views.insert_stub, name='insert'),
    url(r'^delete/$', views.delete_stub, name='delete'),
    url(r'^redeem/$', views.redeem, name='redeem'),
    url(r'^invalidate/', views.invalidate, name='invalidate'),
]
