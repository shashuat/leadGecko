from authenticate.models import Leadlist ,List
from rest_framework import serializers

class AuthenticateCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=List
        fields=("listname",'list_owner',"leads",'scrapingurl')
class AuthenticateListSerializers(serializers.ModelSerializer):
    listname=serializers.StringRelatedField()
    list_owner=serializers.StringRelatedField()
    class Meta:
        model=List
        fields=("listname",'list_owner',"leads","generationDate","last_updated")


class AuthenticateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Leadlist
        fields=("listname",'list_owner','team','generationDate',"last_updated",'notes','lead_id','name','phones','email','address','whatsapp_url','reviews','tags','lead_status')

class AuthenticateUpdateSerializers(serializers.ModelSerializer):
    listname=serializers.StringRelatedField()
    list_owner=serializers.StringRelatedField()
    class Meta:
        model=Leadlist
        fields=("listname",'list_owner','team','generationDate',"last_updated",'notes','lead_id','name','phones','email','address','whatsapp_url','reviews','tags','lead_status')