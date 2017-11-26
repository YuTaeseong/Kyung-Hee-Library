#-*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.do_you_sign_up, name='library_page_header'),
    url(r'^sign_up/$', views.library_sign_up, name='library_sign_up'),
    url(r'^service/$', views.service, name='service'),
    url(r'^ajax/serverTotoken/$', views.save_token, name='save_token'),
]