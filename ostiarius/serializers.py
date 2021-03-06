from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'S_N', 'asset_no', 'item_name', 'maintenance_mode', 'present', 'map_status']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['asset_no','date','time','item_id','notified']
