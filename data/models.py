from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_icon = models.URLField()
    item_sell_price = models.IntegerField()
    item_buy_price = models.IntegerField()
    selected = models.BooleanField(default="false")
    item_api_id = models.CharField(max_length=20, blank=True)

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    result = models.ForeignKey('Item')
    result_quantity = models.IntegerField(default=0)

class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='ingredients')
    item = models.ForeignKey('Item')
    quantity = models.IntegerField()
