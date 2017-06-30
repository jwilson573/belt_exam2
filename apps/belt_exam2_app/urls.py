from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='login_page'),
    url(r'^success$', views.success, name='poking_page'),
    url(r'^create_user$', views.create_user),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login),
    url(r'^poke/(?P<id>\d+$)', views.poke)
]
