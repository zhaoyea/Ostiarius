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
    url(r'^detail/overdue/$', views.overdue, name='overdue'),
    url(r'^assets/$', views.assets, name='assets'),
    url(r'^maintenance/$', views.maintenancePage, name='maintenancePage'),
    url(r'^alert/$', views.alertPage, name='alertPage'),
    url(r'^assets/updateItems$', views.update_items, name='update_items'),
    url(r'^assets/addItems$', views.add_items, name='add_items'),
    url(r'^assets/delete/(?P<item_id>[0-9]+)/$', views.delete_items, name='delete_items'),
    url(r'^maintenance/insertMaintenance$', views.new_maintenance, name='new_maintenance'),
    url(r'^maintenance/updateMaintenance$', views.update_maintenance, name='update_maintenance'),
    url(r'^console/$', views.console, name='console'),
    url(r'^camera/$', views.camera, name='camera'),
    url(r'^indexLineChart/$', views.indexLineChart, name='indexLineChart'),
    url(r'^alert_report/(?P<alert_id>[0-9]+)/$', views.alert_report, name='alert_report'),

    url(r'^jsonData/$', views.jsonData, name='jsonData'),
    url(r'^jsonData/blankTable$', views.blank_table, name='blank_table'),
    url(r'^GETrequest/$', views.GETrequest, name='GETrequest'),
    url(r'^POSTassets/$', views.POSTassets, name='POSTassets'),
    url(r'^asset_list/$', views.asset_list, name='asset_list'),
    url(r'^push_notifi/$', views.push_notifi, name='push_notifi'),
    url(r'^push_alert/$', views.push_alert, name='push_alert'),
    url(r'^piStatus/$', views.piStatus, name='piStatus'),


]
