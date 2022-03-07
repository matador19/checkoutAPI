from email import header
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import phoneSerializer
from .models import phoneNumber
from .models import customer
from .serializers import customerSerializer
import requests
import json
import base64
from rest_framework import viewsets

phone=""

def safaricomauth(request):
    #Customer ID
    customer_key = "P5giKpFolWJzLQAqsLWYPJH7GWdS3X2A"
    # Customer secret
    customer_secret = "70otjSiYQptugMc6"
    # Concatenate customer key and customer secret and use base64 to encode the concatenated string
    credentials = customer_key + ":" + customer_secret
    # Encode with base64
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")
    response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Basic '+credential })
    print(response.text.encode('utf8'))
    return render(request,'safaricom.html',context={'response':response})

def stkpush(request,phone):
    headers = {
    'Authorization': 'Bearer RXXyvoV19mSPnjPn6f1SMpOGrqq8',
     'Content-Type': 'application/json',
    }
    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwMzA3MTM1ODQy",
        "Timestamp": "20220307135842",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708374149,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json=payload)
    return render(request,'stkpush.html',context={'response':response})


def ctob(request):
     headers = {
    'Authorization': 'Bearer Td4CEMwC4WrDstIFl1MgUIcsspTq',
     'Content-Type': 'application/json',
    }


@api_view(['GET'])
def getData(request):
    Customer=customer.objects.all()
    serializer=customerSerializer(Customer,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getphoneNumber(request):
    phonenumber=phoneNumber.objects.all()
    serializer=phoneSerializer(phonenumber,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addcustomer(request):
    serializer=customerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addphone(request):
    serializer=phoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getdetailphoneNumber(request,pk):
    phonenumber=phoneNumber.objects.get(id=pk)
    serializer=phoneSerializer(phonenumber,many=False)
    return Response(serializer.data)





