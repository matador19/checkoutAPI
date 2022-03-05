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

    def __str__(self):
        return self.name