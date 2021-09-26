from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

from . import views


app_name = 'entries'
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', views.index, name='index'),
    url(
        r'^(?P<slug>[-\w]+)/(?P<path>.*)$',
        views.serve_attachment,
        name='serve_attachment'
    ),
]
