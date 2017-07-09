from django.db import models
from datetime import datetime


class Item(models.Model):
    asset_no = models.CharField(max_length=10)
    item_name = models.CharField(max_length=1000)
    maintenance_mode = models.BooleanField(default=False)
    present = models.BooleanField(default=True)
    map_status = models.BooleanField(default=False)

    def __str__(self):
        return self.asset_no + ' - ' + self.item_name


class Alert(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    photo = models.CharField(max_length=1000)

    def __str__(self):
        return self.item.asset_no


class Maintenance(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    asset_no = models.CharField(max_length=10)
    lecturer = models.CharField(max_length=100)
    date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.asset_no


class Mapping(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    uid = models.CharField(max_length=20)
    asset_no = models.CharField(max_length=10)

    def __str__(self):
        return self.uid + '-' + self.asset_no
