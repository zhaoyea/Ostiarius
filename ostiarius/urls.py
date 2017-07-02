from django.conf.urls import url
from . import views

app_name = 'ostiarius'

urlpatterns = [
    #/index/
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^history/$', views.history, name='history'),

]