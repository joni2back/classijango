# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from main.models.locations import City

class UserProfile(User):
    phone = models.CharField(max_length = 64, blank = True, default = '')
    city = models.ForeignKey(City)
    class Meta:
        app_label = "main"
        db_table = "main_user_profile"


        
