from django.conf.urls import url
from . import views

app_name = 'ostiarius'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^detail/present/$', views.present, name='present'),
    url(r'^detail/alert/$', views.alert, name='alert'),
    url(r'^detail/maintenance/$', views.maintenance, name='maintenance'),
    url(r'^assets/$', views.assets, name='assets'),
    url(r'^maintenance/$', views.maintenancePage, name='maintenancePage'),
    url(r'^alert/$', views.alertPage, name='alertPage'),
    url(r'^assets/updateItems$', views.update_items, name='update_items'),
    url(r'^assets/addItems$', views.add_items, name='add_items'),
    url(r'^assets/delete/(?P<item_id>[0-9]+)/$', views.delete_items, name='delete_items'),
    url(r'^maintenance/insertMaintenance$', views.new_maintenance, name='new_maintenance'),
    url(r'^maintenance/updateMaintenance$', views.update_maintenance, name='update_maintenance'),
    url(r'^jsonData/$', views.jsonData, name='jsonData'),
    url(r'^GETrequest/$', views.GETrequest, name='GETrequest'),
    url(r'^POSTassets/$', views.POSTassets, name='POSTassets'),
    # url(r'^POSTalerts/$', views.POSTalerts, name='POSTalerts'),
    url(r'^jsonData/blankTable$', views.blankTable, name='blankTable'),
    url(r'^asset_list/$', views.asset_list, name='asset_list'),
]
