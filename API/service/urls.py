# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from django.conf.urls import url
from rest_framework import routers

from .views import ServerListView, ServerCreateView, ServerActivationView, ServerView, DataView

urlpatterns = [
    url(r'^servers/create/', ServerCreateView.as_view()),
    url(r'^servers/activation/', ServerActivationView.as_view()),
    url(r'^servers/', ServerListView.as_view()),
    url(r'^servers/(?P<server_name>.+)/$', ServerView.as_view()),
    url(r'^servers/(?P<server_name>.+)/(?P<attribute>.+)/(?P<period>.+)/(?P<spacing>.+)$', DataView.as_view()),
]
