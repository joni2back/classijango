# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser

class UserProfile(User):
    phone = models.CharField(max_length=64, blank=True, default='')

    class Meta:
        app_label = "main"
        db_table = "main_user_profile"


        
