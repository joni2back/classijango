# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from main.models.user import UserProfile
from main.models.classifieds import Classified, ClassifiedCategory
from main.models.locations import Country, Province, City


class AddClassifiedForm(ModelForm):
    city = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'autocomplete': 'off'}))
    city_id = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'type': 'hidden'}))
    class Meta:
        model = Classified
        fields = (
            'title', 'content', 'category', 'type', 'currency', 'price',
            'contact_name', 'contact_email',  
            'contact_phone', 'contact_address', 'google_map', 
            'image_1', 'image_2', 'image_3',
        )
    
    def __init__OLD(self, *args, **kwargs):
        super(AddClassifiedForm, self).__init__(*args, **kwargs)
        self.fields['categodry'].empty_label = u'---------'

class DeleteClassifiedForm(ModelForm):
    class Meta:
        model = Classified
        fields = ()

class EditProfileForm(ModelForm):
    city = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'autocomplete': 'off'}))
    city_id = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'type': 'hidden'}))
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', )

class UserRegistrationForm(UserCreationForm):
    email = forms.CharField()
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Passwords don\'t match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and UserProfile.objects.filter(email = email).count():
            raise forms.ValidationError(u'This email address is already registered')
        return email

    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password1'])

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SerarchForm(forms.Form):
    category = forms.ModelChoiceField(queryset = ClassifiedCategory.objects.all())
    search = forms.CharField(max_length = 100)

class AdvancedSerarchForm(forms.Form):
    search = forms.CharField(max_length = 100)
    category = forms.ModelChoiceField(queryset = ClassifiedCategory.objects.all())
    city = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'autocomplete': 'off'}))
    city_id = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'type': 'hidden'}))
    price_min = forms.CharField(max_length = 100)
    price_max = forms.CharField(max_length = 100)
    currency = forms.ChoiceField(choices = Classified.CLASSIFIED_CURRENCIES)
