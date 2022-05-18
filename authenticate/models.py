from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator ,MinValueValidator

User=get_user_model()

Tag=(
        ('grocery','grocery'),
        ('fruits','fruits'),
        ('vegetables','vegetables'),
        ('hindustan uniliver','hindustan uniliver'),
    )
class List(models.Model):
    listno=models.AutoField(primary_key=True)
    listname = models.CharField(max_length=500,blank=True)
    leads = models.CharField(max_length=500)
    generationDate=models.DateField(auto_now_add=True , editable=False,blank=True)
    list_owner=models.ForeignKey(User, on_delete=models.CASCADE)
    scrapingurl = models.CharField(max_length=500)
    last_updated=models.DateField(auto_now=True,editable=False,blank=True)
    def __str__(self):
	    return self.listname
        
class Team(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    def __str__(self):
        return self.user.username
    

class Leadlist(models.Model):
    leadChoice=(
        ('lead','lead'),
        ('contact made','contact made'),
        ('signed up','signed up'),
        ('closed lost','closed lost'),
        ('closed won','closed won'),
    )
    listname = models.ForeignKey(List, on_delete=models.CASCADE,blank=True)
    generationDate=models.DateField(auto_now_add=True,editable=False)
    list_owner=models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    team=models.ManyToManyField(Team,blank=True)
    last_updated=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    lead_id=models.AutoField(primary_key=True)
    notes=models.CharField(max_length=500,blank=True)
    phones=models.CharField(max_length=200 ,null=True,blank=True)
    email=models.EmailField(unique=False,blank=True)
    address=models.CharField(max_length=500,blank=True)
    whatsapp_url=models.URLField(blank=True)
    reviews=models.FloatField(null=True,blank=True ,validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    tags=models.CharField(choices=Tag,blank=True,max_length=100)
    lead_status=models.CharField(choices=leadChoice ,max_length=100,blank=True)
    
    def __str__(self):
	    return self.name

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)