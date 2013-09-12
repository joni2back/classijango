# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from main.models.user import UserProfile
from main.models.classifieds import Classified

class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified

class UserRegistrationForm(UserCreationForm):
    email = forms.CharField()
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user