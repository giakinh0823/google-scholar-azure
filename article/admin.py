from django.contrib import admin
from .models import *
# Register your models here.

    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','user','title',] 
    readonly_fields =('id',)
    list_per_page = 15
    search_fields = ('id',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(KeywordResearch)


