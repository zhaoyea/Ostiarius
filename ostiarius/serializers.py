from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'asset_no', 'item_name', 'present', 'map_status']