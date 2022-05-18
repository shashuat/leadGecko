from django.shortcuts import render ,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin
from django.views.generic import ListView ,CreateView , View
from .models import Leadlist ,List
from django.contrib.auth.mixins import LoginRequiredMixin
from . import justdial_scrapper
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# Create your views here.
def Loginapi(request):
    if request.method=='POST':
        uname=request.POST['username']
        psswd=request.POST['password']
        user=authenticate(username=uname,password=psswd)
        if user is not None:
            authlogin(request,user)
            return HttpResponseRedirect('/home/')
    return render(request,'index.html')

def home(request):
    user = request.user
    if not user.is_authenticated:
        return render(request,'index.html')
    return render(request,"home.html")


def order(request):
    user=request.user
    if not user.is_authenticated:
        return render(request,'index.html')
    return render(request,'tables.html')

class leadList(LoginRequiredMixin,CreateView):
    model = Leadlist
    template_name = 'tables.html'
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leads'] = Leadlist.objects.filter(listname=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        user=self.request.user
        if request.method == "POST":
            listname=List.objects.get(pk=self.kwargs.get('pk'))
            name=request.POST['name']
            listowner=user
            notes=request.POST['notes']
            phones=request.POST['phones']
            email=request.POST['email']
            address=request.POST['address']
            whatsapp_url=request.POST['whatsapp_url']
            reviews=request.POST['reviews']
            tags=request.POST['tg']
            lead_status=request.POST['ls']
            if user is not None:
                data=Leadlist(listname=listname,name=name,list_owner=listowner,notes=notes,phones=phones,email=email,address=address,whatsapp_url=whatsapp_url,reviews=reviews,tags=tags,lead_status=lead_status)
                data.save()
                return render(request,'tables.html',{'leads':Leadlist.objects.filter(listname=self.kwargs.get('pk'))})


def listGet(request):
    user=request.user
    if request.method == "POST":
        leads=request.POST['leads']
        namel=request.POST['name']
        scrurl=request.POST['scrapingurl']
        user=user
        if user is not None:
            data=List(list_owner=user,listname=namel,leads=leads,scrapingurl=scrurl)
            data.save()
            list=List.objects.filter(list_owner=user)
            catalogs_scrapper=justdial_scrapper.CatalogsScrapper(browser=webdriver.Chrome(options=justdial_scrapper.option, service=justdial_scrapper.service), filename='links.txt', count=10,dataId='authenticate_leadlist')
            error=catalogs_scrapper.getLinksData(pageUrl=scrurl, option=justdial_scrapper.option, service=justdial_scrapper.service)
            return render(request,"homev2.html",{'list':list})
    else:
        list=List.objects.filter(list_owner=user)
    return render(request,"homev2.html",{'list':list})
