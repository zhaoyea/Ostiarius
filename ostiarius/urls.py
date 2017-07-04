from django.conf.urls import url
from . import views

app_name = 'ostiarius'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<present_id>[0-9]+)/$', views.present, name='present'),
    url(r'^assets/$', views.assets, name='assets'),
    url(r'^asset_list/$', views.asset_list, name='asset_list'),
]
