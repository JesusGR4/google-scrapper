# -*- coding: utf-8 -*-
from django.db import models

class PlaceInfo(models.Model):
    website = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=150, null=True)
    rating = models.DecimalField(null=True, decimal_places=2, max_digits=3)
    international_phone_number = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=300, null=True)
    place_id = models.CharField(max_length=150, unique=True)
    web_status = models.CharField(max_length=150,)
