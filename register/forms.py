from django import forms
from django.contrib.auth.models import User
from django.forms import models
from django.forms import fields
from django.forms.fields import DateField
from .models import UserProfile
from django.forms import widgets
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple




class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password','confirm_password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields= ('name','Affiliation','AreasOfInterest','homepage','EmailForVerification', 'avatar')
        
class CoAuthorForm(forms.ModelForm):
    coAuthor = CustomSelectMultiple(widget=forms.CheckboxSelectMultiple, queryset=UserProfile.objects.all())
    class Meta():
        model = UserProfile
        fields = ('coAuthor',)
        