from rest_framework import serializers
from core.serializers import UserSerializer , SimpleUserSerializer
from management.models import Meal
from .models_shared import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user','phone','address']

class SimpleCustomerSerializer(serializers.ModelSerializer):
    user=SimpleUserSerializer(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user']


class SimpleMealSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meal
        fields=['id','name','price']


    