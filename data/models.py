from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_icon = models.URLField()
    item_sell_price = models.IntegerField()
    item_buy_price = models.IntegerField()
    selected = models.BooleanField(default="false")
