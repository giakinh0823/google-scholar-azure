from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from .filters import *
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


import nltk
nltk.download('stopwords') #if cant not run please remove comment in here
nltk.download('punkt') #if cant not run please remove comment in here
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag


# Create your views here.


def article(request):
    articles = Article.objects.all() 
    if request.GET:
        # articlesFilter = ArticleFilter(request.GET, queryset=articles)
        # articles= articlesFilter.qs
        try:
            getTitle = request.GET['search']
        except:
            getTitle = None 
        if getTitle:
            articles = Article.objects.filter(Q(title__icontains=request.GET['search']) | Q(author__icontains=request.GET['search']))
        
        if getTitle and articles:
            title = str(articles[0]).lower()
            title = title.strip()
            
            text_tokens = nltk.word_tokenize(title)
            text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
            text_tokens = pos_tag(text_tokens) 
            title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS','DT',':',')','(','.',',')]
            if getTitle:
                keywords = str(request.GET['search']).strip()
                text_tokens = nltk.word_tokenize(keywords)
                text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
                text_tokens = pos_tag(text_tokens) 
                keywords = [x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT',':',')','(','.',',') and x.lower() in title]
            
                for keyword in keywords:
                    try:
                        keywordResearch = KeywordResearch.objects.get(keyword = keyword.lower())
                    except KeywordResearch.DoesNotExist:
                        keywordResearch = None
                    if keywordResearch:
                        keywordResearch.quantity += 1
                        keywordResearch.save()
                    else:
                        keywordResearch = KeywordResearch(keyword = keyword.lower(), quantity = 1)
                        keywordResearch.save()
        paginator = Paginator(articles, 15)
        pageNumber = request.GET.get('page',1)
        try:
            articles = paginator.page(pageNumber)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return render(request, 'article/article.html', {'articles': articles, })
    paginator = Paginator(articles, 15)
    pageNumber = request.GET.get('page',1)
    try:
        articles = paginator.page(pageNumber)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'article/article.html', {'articles': articles})

@login_required
def createarticle(request):
    if request.method == "POST":
        form_article = ArticleForm(data=request.POST)
        if form_article.is_valid():
            article = form_article.save(commit=False)
            article.user = request.user
            article.save()
        else:
            raise forms.ValidationError("wrong format")
    return render(request, 'article/articlecreate.html', {'articleForm': ArticleForm()})


def keywordresearch(request):
    labels = []
    data = []
    queryset = KeywordResearch.objects.order_by('-quantity')[:20]
    for keyword in queryset:
        labels.append(keyword.keyword)
        data.append(keyword.quantity)
    return render(request, 'article/keywordresearch.html', {'labels': labels, 'data': data})
