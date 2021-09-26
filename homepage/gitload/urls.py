from django.conf.urls import url

from . import views


app_name = 'gitload'
urlpatterns = [
    url(r'trigger/', views.trigger_gitload, name='trigger'),
]
