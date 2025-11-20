from django_filters.rest_framework import FilterSet
from .models import Meal , Restaurant

class MealFilter(FilterSet):
    class Meta:
        model = Meal
        fields ={
            'name' : ['exact'],
            'price' : ['gt','lt']
        }
        
class RestaurantFilter(FilterSet):
    class Meta:
        model = Restaurant
        fields ={
            'name' : ['exact'],
            'oppening_time' : ['gt','lt']
        }        
