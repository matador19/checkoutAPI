from rest_framework import serializers
from .models import phoneNumber
from .models import customer

class customerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = customer
        fields = ('id' , 'first_Name', 'last_Name','email','street_Address','country','city','phone','postal_Address')

class phoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = phoneNumber
        fields = ('id','phonenumber')