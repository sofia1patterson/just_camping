from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^about$', views.about),
    url(r'^destinations$', views.destinations),
    url(r'^lassen$', views.lassen),
    url(r'^butte$', views.butte),
    url(r'^juniper$', views.juniper),
    url(r'^manzanita$', views.manzanita),
    url(r'^booking/(?P<id>\d+)$', views.booking_page),
    url(r'^book/(?P<id>\d+)$', views.booking),
    url(r'^cart/(?P<id>\d+)$', views.cart),
    url(r'^delete$', views.delete),
    url(r'^loginreg$', views.loginreg_page),
    url(r'^booklogin$', views.booking_login),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^user$', views.user),
    url(r'^logout$', views.logout),
]

#  url(r'^cart/(?P<id>\d+)$', views.cart),
