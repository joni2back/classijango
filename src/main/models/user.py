from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	receives_new_posting_notices = models.BooleanField()
	receives_newsletter = models.BooleanField()
	address = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = USStateField(blank=True)
	zipcode = models.CharField(max_length=10, blank=True)
	phone = PhoneNumberField(blank=True, default='')
