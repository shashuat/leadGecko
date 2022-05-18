from django.shortcuts import render
from .serializers import AuthenticateSerializers ,AuthenticateCreateSerializers, AuthenticateListSerializers , AuthenticateUpdateSerializers
from authenticate.models import Leadlist , List
from rest_framework.generics import ListAPIView , CreateAPIView ,RetrieveAPIView , RetrieveUpdateDestroyAPIView , RetrieveDestroyAPIView ,ListCreateAPIView
from rest_framework.authentication import TokenAuthentication,SessionAuthentication , BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter

class LeadsList(CreateAPIView):
    queryset=Leadlist.objects.all()
    serializer_class=AuthenticateSerializers
    authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        user=self.request.user
        return Leadlist.objects.filter(list_owner=user)

class LeadsgetList(ListAPIView):
    queryset=Leadlist.objects.all()
    serializer_class=AuthenticateUpdateSerializers
    authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    filter_backends=[SearchFilter]
    search_fields=['lead_id']
    def get_queryset(self):
        user=self.request.user
        return Leadlist.objects.filter(team=user.id)

class UpdateList(RetrieveUpdateDestroyAPIView):
    queryset=Leadlist.objects.all()
    serializer_class=AuthenticateUpdateSerializers
    authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        user=self.request.user
        return Leadlist.objects.filter(list_owner=user)

class CreateList(CreateAPIView):
    queryset=List.objects.all()
    serializer_class=AuthenticateCreateSerializers
    authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]

class Listget(ListAPIView):
    queryset=List.objects.all()
    serializer_class=AuthenticateListSerializers
    authentication_classes=[SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    filter_backends=[SearchFilter]
    search_fields=['listname']
    def get_queryset(self):
        user=self.request.user
        return List.objects.filter(list_owner=user)