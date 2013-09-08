from django.forms import ModelForm
from main.models.classifieds import Classified
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified
		fields = [
			'title', 'content', 'category', 'status', 'type', 
			'currency', 'expires', 'price', 'phone', 'google_map',
			'image_1', 'image_2', 'image_3', 
		];


class UserCreationForms(UserCreationForm):
	overrideOf_UserCreationForm = forms.CharField()