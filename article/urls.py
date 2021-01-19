from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='article'

urlpatterns = [
    path('article/', views.article, name='article'),
    path('createarticle/', views.createarticle, name = 'createarticle'),
    path('keywordresearch/', views.keywordresearch, name = 'keywordresearch'),
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
