# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user = models.ForeignKey(User, unique=True)
    phone = models.CharField(max_length=255, blank=True, default='')
    COUNTRIES = (
        ('ar','Arg'),
        ('es','Esp'),
        ('br','Bra'),
    )
    color = models.CharField(max_length=255, choices=COUNTRIES, default='red').contribute_to_class(User, "country")