from  .models import *
from django import forms


from  django_filters import DateFilter, CharFilter
import django_filters

class ProfileFilter(django_filters.FilterSet):
    name = CharFilter(field_name = "name", lookup_expr="icontains")
    class Meta():
        model = UserProfile
        fields = ('name',)