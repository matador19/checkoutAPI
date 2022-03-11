from audioop import reverse
from email import header
from multiprocessing import context
from time import sleep, time
from urllib import response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import cartSerializer, phoneSerializer,mpesarespSerializer,mpesaExprSucSerializer
from .models import cart, phoneNumber,CheckoutRequestID, mpesaExprSuc,mpesaresp
from .models import customer
from .serializers import customerSerializer, CheckoutRequestIDSerializer
import requests
import json
import base64
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import ast





def stkpush(request,phone,cost):
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
    response=response.json()
    token=response['access_token']
    headers = {
    'Authorization': 'Bearer '+token,
     'Content-Type': 'application/json',
    }
    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwMzA3MTM1ODQy",
        "Timestamp": "20220307135842",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": cost,
        "PartyA": 254720163490,
        "PartyB": 174379,
        "PhoneNumber": phone,
        #change here
        "CallBackURL": "https://e8cc-41-90-115-26.ngrok.io/webhook",
        "AccountReference": "E-commerce X",
        "TransactionDesc": "Payment of products XYZ" 
    }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json=payload)
    response=json.loads(response.text)
    CheckoutRequestID={'CheckoutRequestID':response['CheckoutRequestID']}
    serializer=CheckoutRequestIDSerializer(data=CheckoutRequestID)
    if serializer.is_valid():
        #print('done')
        serializer.save()
    return redirect('http://localhost:3000/')



def ctob(request):
     headers = {
    'Authorization': 'Bearer GGpTTKefnsdsOrWAsQLPql2fJSTr',
     'Content-Type': 'application/json',
    }

#get customer json
@api_view(['GET'])
def getData(request):
    Customer=customer.objects.all()
    serializer=customerSerializer(Customer,many=True)
    return Response(serializer.data)

#get phonenumber json --- not used for now
@api_view(['GET'])
def getphoneNumber(request):
    phonenumber=phoneNumber.objects.all()
    serializer=phoneSerializer(phonenumber,many=True)
    return Response(serializer.data)

#add customer json
@api_view(['POST'])
def addcustomer(request):
    serializer=customerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#add phone json  ---- not used now
@api_view(['POST'])
def addphone(request):
    serializer=phoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#get detail phone number by id json --- not used now
@api_view(['GET'])
def getdetailphoneNumber(request,pk):
    phonenumber=phoneNumber.objects.get(id=pk)
    serializer=phoneSerializer(phonenumber,many=False)
    return Response(serializer.data)

#get cart json
@api_view(['GET'])
def getcart(request):
    carts=cart.objects.all()
    serializer=cartSerializer(carts,many=True)
    return Response(serializer.data)

#add cart json
@api_view(['POST'])
def addcart(request):
    serializer=cartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

request_desc=""
#mpesa response
@api_view(['POST'])
@csrf_exempt
def webhook(request):
        #json_data = json.loads(str(request.body, encoding='utf-8'))
    if request.method =='POST':
        json_data=request.body
        json_data = json.loads(json_data)
        request_desc=json_data['Body']['stkCallback']['ResultDesc']
        if request_desc=='Request cancelled by user':
            json_data_declined=json_data['Body']['stkCallback']
            serializer=mpesarespSerializer(data=json_data_declined)
            #print(json_data_declined)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        elif request_desc=='The service request is processed successfully.':
            json_data_accepted=json_data['Body']['stkCallback']['CallbackMetadata']['Item']
            json_data_CheckoutRequestID= json_data['Body']['stkCallback']['CheckoutRequestID']
            json_data_accepted_processed={
                'PhoneNumber':json_data_accepted[4]['Value'],
                'Amount':json_data_accepted[0]['Value'],
                'TransactionDate':json_data_accepted[3]['Value'],
                'MpesaReceiptNumber':json_data_accepted[1]['Value'],
                'CheckoutRequestID': json_data_CheckoutRequestID
            }
           # print(json_data_accepted_processed)
            serializer=mpesaExprSucSerializer(data=json_data_accepted_processed)
            if serializer.is_valid():
                print('true')
                serializer.save()
            return Response(serializer.data)

        
def checkpayment(request):
    CheckoutID= CheckoutRequestID.objects.values('CheckoutRequestID')
    PassedCheckoutID=mpesaExprSuc.objects.values('CheckoutRequestID')
    Transcode=mpesaExprSuc.objects.values('MpesaReceiptNumber')
    Amount=mpesaExprSuc.objects.values('Amount')
    phone=mpesaExprSuc.objects.values('PhoneNumber')
    FailedCheckoutID=mpesaresp.objects.values('CheckoutRequestID')
    A=len(CheckoutID)
    B=len(PassedCheckoutID)
    C=len(FailedCheckoutID)
    D=len(Transcode)
    E=len(Amount)
    F=len(phone)
   # print(CheckoutID[A-1]['CheckoutRequestID'])
    #print(PassedCheckoutID[B-1]['CheckoutRequestID'])
    #print(FailedCheckoutID[C-1]['CheckoutRequestID'])
    context={
        'CheckoutID':CheckoutID[A-1]['CheckoutRequestID'],
        'PassedCheckoutID':PassedCheckoutID[B-1]['CheckoutRequestID'],
        'FailedCheckoutID':FailedCheckoutID[C-1]['CheckoutRequestID'],
        'code':Transcode[D-1]['MpesaReceiptNumber'],
        'Amount':Amount[E-1]['Amount'],
        'phone':phone[F-1]['PhoneNumber']
    }
    failedcontext={
        'CheckoutID':CheckoutID[A-1]['CheckoutRequestID'],
        'PassedCheckoutID':PassedCheckoutID[B-1]['CheckoutRequestID'],
        'FailedCheckoutID':FailedCheckoutID[C-1]['CheckoutRequestID'],
        'code': None,
        'Amount': None,
        'phone': None
    }

    if CheckoutID[A-1]==FailedCheckoutID[C-1]:
        return JsonResponse(failedcontext)
    elif CheckoutID[A-1]==PassedCheckoutID[B-1]:
        return JsonResponse(context)
     #   return render(request,'passed.html',context)
    else:
        return JsonResponse(failedcontext)


       

        
        
        




