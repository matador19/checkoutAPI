from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import customerSerializer
from .models import customer


@api_view(['GET'])
def getData(request):
    Customer=customer.objects.all()
    serializer=customerSerializer(Customer,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addcustomer(request):
    serializer=customerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)