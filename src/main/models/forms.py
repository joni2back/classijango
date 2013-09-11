# -*- coding: utf-8 -*-
from django.forms import ModelForm
from main.models.classifieds import Classified
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models.user import UserProfile

class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified

class UserRegistrationForm(UserCreationForm):
	email = forms.CharField()
	#todo review this, add specified fields here not all
	class Meta:
		model = UserProfile