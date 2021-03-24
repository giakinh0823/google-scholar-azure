import asyncio
from time import time
from django.http.response import HttpResponse, JsonResponse
from article.models import Article
from article.views import article
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileForm , UserForm, CoAuthorForm
from .filters import *
from .models import *
from article.forms import ArticleForm
from article.models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


#update data

from article.models import Article
from Scholar.getDataScholar import data_scrap,data_profile
from register.models import UserProfile
from asgiref.sync import sync_to_async
import asyncio

import nltk
nltk.download('stopwords') #if can't not run please remove comment in here
nltk.download('punkt') #if can't not run please remove comment in here
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag


# Create your views here.


#is_authenticated
@user_passes_test(lambda u: u.is_anonymous, login_url='home:index')
def signup(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if request.POST['password']==request.POST['confirm_password']:
            if user_form.is_valid() and profile_form.is_valid():
                user= user_form.save() 
                user.set_password(user.password) 
                user.save()
                profile= profile_form.save(commit=False)
                profile.user = user
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                profile.save()
                login(request, user)
                request.session['user'] = { 'image': profile.avatar.url}
                return redirect('home:index')
            else:
                return render(request, 'register/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'error': "Wrong fomat"})
        else:
            return render(request, 'register/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'error': "Password Wrong"})
    else:
        user_form = UserForm()
        profile_form= UserProfileForm()
    return render(request, 'register/signup.html', {'user_form': user_form, 'profile_form': profile_form})

@user_passes_test(lambda u: u.is_anonymous, login_url='home:index')
def loginuser(request):
    if request.method == "GET":
        return render(request, 'register/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'register/login.html', {'form': AuthenticationForm(), 'error': "username or password wrong"})
        else: 
            login(request, user)
            profile = UserProfile.objects.get(user = user)
            request.session['user'] = { 'image': profile.avatar.url }
            return redirect('home:index')
        
@login_required
def logoutuser(request):
    logout(request)
    return redirect('home:index')


def getCitations(articles):
    articlelist=articles
    labels = []
    data = []
    totalCitations=0
    totalCitationsSince=0
    if articlelist:
        articlelist = articlelist.order_by('-year')
        index = 0
        while not articlelist[index].year:
            index+=1
        if index==len(articlelist)-1:
            max=0
        else:
            max = int(articlelist[0].year)
        index =len(articlelist)-1
        while not articlelist[index].year:
            index-=1
        if index==0:
            min=0
        else:
            min = int(articlelist[index].year)
        for x in range(min, max+1):
            labels.append(x)
            cyted = 0 
            for article in articlelist:
                if article.year:
                    if x == int(article.year):
                        if article.total_citations:
                            cyted += int(article.total_citations)
                            totalCitations+=int(article.total_citations)
                            if x>=2016:
                                totalCitationsSince+=int(article.total_citations)
            data.append(cyted)
    return  labels, data, totalCitations, totalCitationsSince


def getWordCloud(articles):
    listarticle=articles
    labeltitle = []
    datatitle = []
    for item in listarticle:
            text_tokens = nltk.word_tokenize(str(item.title))
            text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
            text_tokens = pos_tag(text_tokens) 
            title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT', 'VBD','CD', '.', ',',':', ')', '(' )]
            
            for word in title:
                try:
                    index = labeltitle.index(word.lower())
                except:
                    index = None
                if index:
                    datatitle[index]+=1
                else:
                    labeltitle.append(word.lower())
                    datatitle.append(1)
    lis = [(datatitle[i], labeltitle[i]) for i in range(len(datatitle))]
    datatitle.sort()
    labeltitle = [x[1] for i in range(len(datatitle)) for x in lis if x[0] == i]
    # datatitle, labeltitle = zip(*sorted(zip(datatitle, labeltitle)))
    datatitle=datatitle[::-1] #reverse list
    labeltitle=labeltitle[::-1] #reverse list
    return labeltitle, datatitle
    

def setCoAuthor(request, profile):
     if request.is_ajax():
        idAuthor = request.POST.get('id')
        author = UserProfile.objects.get(id = idAuthor) #id coAuthor
        try: 
           checkCoauthor =CoAuthor.objects.get(coAuthor= author)
        except:
            checkCoauthor=None
        if checkCoauthor:
            checkCoauthor.delete()
        else:
            newCoAuthor = CoAuthor(author = profile, coAuthor= author)
            newCoAuthor.save()
        coauthorlist = CoAuthor.objects.filter(author = profile)
        profile = []
        for author in coauthorlist:
            profile.append(author.coAuthor)
        return coauthorlist

@login_required
def profile(request):
        
    profile = UserProfile.objects.get(user = request.user)
    profilelist = UserProfile.objects.all()
    articles = Article.objects.filter(user = request.user)
    authorlist = CoAuthor.objects.filter(author = profile)
    
    #set-co-Author
    if request.is_ajax():
        coauthorlist = setCoAuthor(request, profile)
        return render(request, 'register/listcoAuthorProfile.html', {'authorlist':coauthorlist})
        
    
    #co-Author
    coAuthors = []
    for author in authorlist:
        coAuthors.append(author.coAuthor.id)
        
    #set-map
    labels, data, totalCitations, totalCitationsSince = getCitations(articles)
    labeltitle, datatitle = getWordCloud(articles)
        
    #page
    paginator = Paginator(articles, 15)
    pageNumber = request.GET.get('page',1)
    try:
        articles = paginator.page(pageNumber)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    return render(request, 'register/profile.html', {'profile': profile, 'articles': articles, 'labels': labels, 'data': data,'labeltitle':labeltitle[:100],'datatitle':datatitle[:100] ,'CoAuthorForm': CoAuthorForm(), 'profilelist': profilelist, 'coAuthorList': coAuthors, 'articleForm': ArticleForm(), 'authorlist': authorlist, 'totalCitations': totalCitations, 'totalCitationsSince': totalCitationsSince})

def findProfile(request):
    listprofile=[]
    listprofile = UserProfile.objects.all()
    if request.GET:
        profileFilter = []
        profileFilter = ProfileFilter(request.GET, queryset=listprofile)
        listprofile= profileFilter.qs
        paginator = Paginator(listprofile, 15)
        pageNumber = request.GET.get('page',1)
        try:
            listprofile = paginator.page(pageNumber)
        except PageNotAnInteger:
            listprofile = paginator.page(1)
        except EmptyPage:
            listprofile = paginator.page(paginator.num_pages)
        return listprofile
    
    paginator = Paginator(listprofile, 15)
    pageNumber = request.GET.get('page',1)
    try:
        listprofile = paginator.page(pageNumber)
    except PageNotAnInteger:
        listprofile = paginator.page(1)
    except EmptyPage:
        listprofile = paginator.page(paginator.num_pages)
    return listprofile, request

# async def viewArticle(request,listprofile ):
#     print("1")
#     return render(request, 'register/listprofile.html', {'listprofile': listprofile, 'profileFilter': ProfileFilter()})

def listprofile(request):
    listprofile = []
    listprofile = findProfile(request)
    return render(request, 'register/listprofile.html', {'listprofile': listprofile, 'profileFilter': ProfileFilter()})


def profiledetail(request, profile_pk):
    labels = []
    data = []
    labeltitle = []
    datatitle = []
    profile = UserProfile.objects.get(id = profile_pk)
    articlelist = Article.objects.filter(user = profile.user)
    listarticle = articlelist
    for item in listarticle:
        text_tokens = nltk.word_tokenize(str(item.title))
        text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
        text_tokens = pos_tag(text_tokens) 
        title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT', 'VBD','CD', '.', ',',':', ')', '(' )]
            
        for word in title:
            try:
                index = labeltitle.index(word.lower())
            except:
                index = None
            if index:
                datatitle[index]+=1
            else:
                labeltitle.append(word.lower())
                datatitle.append(1)
    lis = [(datatitle[i], labeltitle[i]) for i in range(len(datatitle))]
    datatitle.sort()
    labeltitle = [x[1] for i in range(len(datatitle)) for x in lis if x[0] == i]
    # datatitle, labeltitle = zip(*sorted(zip(datatitle, labeltitle)))
    datatitle=datatitle[::-1] #reverse list
    labeltitle=labeltitle[::-1] #reverse list
    totalCitations=0
    totalCitationsSince=0
    if articlelist:
        articlelist = articlelist.order_by('-year')
        index = 0
        while not articlelist[index].year:
            index+=1
        if index==len(articlelist)-1:
            max=0
        else:
            max = int(articlelist[0].year)
        index =len(articlelist)-1
        while not articlelist[index].year:
            index-=1
        if index==0:
            min=0
        else:
            min = int(articlelist[index].year)
        for x in range(min, max+1):
            labels.append(x)
            cyted = 0 
            for article in articlelist:
                if article.year:
                    if x == int(article.year):
                        if article.total_citations:
                            cyted += int(article.total_citations)
                            totalCitations+=int(article.total_citations)
                            if x>=2016:
                                totalCitationsSince+=int(article.total_citations)
            data.append(cyted)
            
        articlelist = Article.objects.filter(user = profile.user)
    articles = Article.objects.filter(user = profile.user)
    authorlist = CoAuthor.objects.filter(author = profile)
    paginator = Paginator(articles, 15)
    pageNumber = request.GET.get('page',1)
    try:
        articles = paginator.page(pageNumber)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'register/profiledetail.html', {'profile': profile, 'articles': articles, 'labels': labels,'data': data,'labeltitle':labeltitle[:100], 'datatitle':datatitle[:100],  'authorlist': authorlist, 'totalCitations': totalCitations, 'totalCitationsSince': totalCitationsSince})

def searchCoauthor(request):
    profile = UserProfile.objects.get(user = request.user)
    if request.is_ajax:
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
        else:
            search_text = ''
        coAuthorList = UserProfile.objects.filter(name__contains=search_text)
        authorlist = CoAuthor.objects.filter(author = profile)
        coAuthors = []
        for item in authorlist:
            coAuthors.append(item.coAuthor.id)
        return render(request, 'register/coauthorlist.html', {'profilelist': coAuthorList, 'coAuthorList': coAuthors })
    
@login_required
def addArticle(request):
    if request.is_ajax():
        form_article = ArticleForm(request.POST)
        if form_article.is_valid():
            article = form_article.save(commit=False)
            article.user = request.user
            article.year = int(str(article.publication_date)[:4])
            article.save()
        else:
            raise forms.ValidationError("wrong format")
        return JsonResponse({"ok": "ok"})
    
    
    

def getdataProfile(request):
    if request.is_ajax():
        az = 'fpt+university'
        # str = 'fpt+university'
        profiles = UserProfile.objects.all();
        page = len(profiles)
        while page % 10 !=0:
            page -= 1
        number = str(page) 
        data_profile('https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors='+ az +'&astart='+number)
    

def getdataArticle(request):
    if request.is_ajax():
        profiles = UserProfile.objects.all()
        for profile in profiles:
            print("Update article profile: "+ profile.name)
            if 'scholar.google.com' in str(profile.homepage):
                data_scrap(profile.homepage, profile.user)

def updateData(request):
    getdataProfile(request)
    return redirect('register:profile')

def updateArticle(request):
    getdataArticle(request)
    return redirect('register:profile')

    
    

