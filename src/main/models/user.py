# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

class UserProfile(User):
    phone = models.CharField(max_length=255, blank=True, default='')
    COUNTRIES = (
        ('ar','Arg'),
        ('es','Esp'),
        ('br','Bra'),
    )
    
    country = models.CharField(max_length=255, choices=COUNTRIES, default='ar')

    class Meta:
        app_label = "main"
        db_table = "main_user_info"