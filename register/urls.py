from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'register'

urlpatterns = [
    path('signup/', views.signup, name ='signup'),
    path('login/', views.loginuser, name ='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/addArticle/', views.addArticle, name='addArticle'),
    path('profile/searchCoauthor/', views.searchCoauthor, name='searchCoauthor'),
    path('listprofile/', views.listprofile, name='listprofile'),
    path('<int:profile_pk>/profiledetail/', views.profiledetail, name ="profiledetail"),
    
    #update data
    path('profile/updateData/', views.updateData, name='updateData'),
    path('profile/updateArticle/', views.updateArticle, name='updateArticle'),
]
urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)