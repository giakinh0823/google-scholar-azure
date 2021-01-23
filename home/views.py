from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render

from article.models import Article
from Scholar.getDataScholar import data_scrap,data_profile
from register.models import UserProfile
from asgiref.sync import sync_to_async

import time



# Create your views here.


# import pyodbc 
    

def home(request):
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-EF058DF;DATABASE=dataScholar;Trusted_Connection=yes;')

    # cursor = cnxn.cursor()
    # cursor.execute('SELECT * FROM Article')
    # i=0
    # for row in cursor:
    #     i+=1
    #     if i>=104:
    #         article = Article(user = User.objects.get(id=3), title = row[2],author=row[3], publication_date=row[4], journal=row[5], conference=row[9], total_citations= row[13])
    #         print(article)
    #         article.save()
    
    # str = 'acdefghijklmnopqrstuvwxyz'
    #    
    # for x in str:
    #     data_profile('https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors='+x)
    return render(request, 'home/index.html')   