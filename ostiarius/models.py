from django.db import models
from datetime import datetime


class Item(models.Model):
    S_N = models.IntegerField()
    asset_no = models.CharField(max_length=10)
    item_name = models.CharField(max_length=1000)
    maintenance_mode = models.BooleanField(default=False)
    present = models.BooleanField(default=True)
    map_status = models.BooleanField(default=False)

    def __str__(self):
        return self.asset_no + ' - ' + self.item_name


class Alert(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    asset_no = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    photo = models.TextField()
    admin_message = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.item.asset_no


class Maintenance(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    asset_no = models.CharField(max_length=10)
    staff_name = models.CharField(max_length=100)
    date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.asset_no


class Mapping(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    uid = models.CharField(max_length=20)
    asset_no = models.CharField(max_length=10)

    def __str__(self):
        return self.uid + '-' + self.asset_no


class Staff(models.Model):
    staff_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)

    def __str__(self):
        return self.staff_name

class Pilog(models.Model):
    pi_sn = models.IntegerField()
    temp_status = models.DecimalField(max_digits=3, decimal_places=1)
    camera_status = models.BooleanField(default=0)
    arm_usage = models.IntegerField()
    gpu_usage = models.IntegerField()
    logdate = models.DateField()
    logtime = models.TimeField()

    def __str__(self):
        return self.pi_sn