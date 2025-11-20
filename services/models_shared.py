from django.db import models
from django.conf import settings
class Customer(models.Model):
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=30,null=False,blank=False)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)