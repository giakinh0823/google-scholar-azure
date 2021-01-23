from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField
from djangoyearlessdate.models import YearField
from partial_date import PartialDateField



# Create your models here.

class KeywordResearch(models.Model):
    keyword= models.CharField(max_length=256)
    quantity = models.IntegerField()
    def __str__(self) -> str:
        return self.keyword

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    title = models.CharField(max_length=2000)
    author = models.CharField(max_length=2000, default=None, blank=True, null=True)
    publication_date = PartialDateField(help_text="YYYY or YYYY-MM or YYYY-MM-DD", default=None, blank=True, null=True)
    journal = models.CharField(max_length=2000, default=None, blank=True, null=True)
    book = models.CharField(max_length=2000, default=None, blank=True, null=True)
    volume = models.IntegerField(default=None, blank=True, null=True)
    issue = models.CharField(max_length=2000,default=None, blank=True, null=True)
    conference = models.CharField(max_length=2000, default=None, blank=True, null=True)
    page = models.CharField(max_length=2000, default=None, blank=True, null=True)
    publisher = models.CharField(max_length=2000, default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    total_citations = models.IntegerField(default=None, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    year = YearField(default=None, blank=True, null=True)
    url = models.URLField(max_length=2000, default=None, blank=True, null=True)
    def __str__(self) -> str:
        return self.title
    


    