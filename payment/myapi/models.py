from django.db import models

class customer(models.Model):
    first_Name = models.CharField(max_length=60)
    last_Name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    street_Address = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    phone = models.CharField(max_length=60)
    postal_Address = models.CharField(max_length=60)

class phoneNumber(models.Model):
    phonenumber=models.CharField(max_length=50)

class cart(models.Model):
    item=models.CharField(max_length=50)
    desc=models.CharField(max_length=60)
    price=models.IntegerField()

class mpesaresp(models.Model):
    MerchantRequestID=models.CharField(max_length=50,null=True)
    CheckoutRequestID=models.CharField(max_length=50,null=True)
    ResultDesc=models.CharField(max_length=50,null=True)
    ResultCode=models.IntegerField(null=True)

class mpesaExprSuc(models.Model):
    PhoneNumber=models.BigIntegerField(null=True)
    Amount = models.FloatField(null=True)
    TransactionDate= models.BigIntegerField(null=True)
    MpesaReceiptNumber= models.CharField(max_length=50,null=True)


    
    
    def __str__(self):
        return self.name