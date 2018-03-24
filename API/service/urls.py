# -*- coding=utf-8 -*-

# Implemented by Eduardo Machado

from django.conf.urls import url
from rest_framework import routers

from .views import ServerListView, ServerView, DataView

urlpatterns = [
    # Server List
    url(r'^servers/$', ServerListView.as_view()),

    # Server datail
    url(r'^servers/new$', ServerView.as_view()),
    url(r'^servers/(?P<server_name>.+)/$', ServerView.as_view()),
    url(r'^servers/(?P<server_name>.+)/activation', ServerView.as_view()),
    url(r'^servers/(?P<server_name>.+)/(?P<attribute>.+)/(?P<period>.+)/(?P<spacing>.+)$', DataView.as_view()),
]
