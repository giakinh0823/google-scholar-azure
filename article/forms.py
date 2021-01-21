from django import forms
from django.forms.fields import MultipleChoiceField
from .models import *
from django.forms import widgets
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name)
        
class ArticleForm(forms.ModelForm):
    class Meta():
        model = Article
        fields = ('title','author','publication_date','journal','book','volume','issue' ,'conference', 'page', 'publisher', 'description','url', 'total_citations') 
        