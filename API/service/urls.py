# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from django.conf.urls import url
from rest_framework import routers

from .views import ServerListView, ServerCreateView, ServerActivationView, ServerGetView, ServerDeleteView, DataView

"""
    pgRealTSD
"""
urlpatterns = [
    url(r'^servers/create/', ServerCreateView.as_view()),
    url(r'^servers/activation/', ServerActivationView.as_view()),
    url(r'^servers/list/', ServerListView.as_view()),
    url(r'^servers/get/', ServerGetView.as_view()),
    url(r'^servers/delete/(?P<name>[0-9a-zA-Z]+)/$', ServerDeleteView.as_view()),
    url(r'^servers/data/', DataView.as_view()),
]
