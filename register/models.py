from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #mối quan hệ một một
    name = models.CharField(max_length=256)
    Affiliation = models.CharField(max_length=256)
    AreasOfInterest = models.CharField(max_length=256, default=None, blank=True, null=True)
    EmailForVerification  = models.CharField(max_length=256, default=None, blank=True, null=True)
    homepage  = models.URLField(blank=True) #blank=true có nghĩa là để trống không cần điền vẫn ok
    avatar = models.ImageField(upload_to='images', blank=True) 
    def __str__(self) -> str:
        return self.user.username
    
    
class CoAuthor(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="author")
    coAuthor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="coauthor")
    
    
    

