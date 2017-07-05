from django.db import models
from datetime import datetime

# Create your models here.
class Item(models.Model):
    asset_no = models.CharField(max_length=10)
    item_name = models.CharField(max_length=1000)
    present = models.BooleanField(default=True)
    photo = models.CharField(max_length=1000, default=None)

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
    asset_no = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField()
    returnDate = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.asset_no.asset_no