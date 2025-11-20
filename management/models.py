from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from management.validators import validate_file_size
from services.models_shared import Customer

class Manager(models.Model):
    address=models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    oppening_time = models.TimeField()
    closing_time = models.TimeField()   
    discription = models.TextField(null=False,blank=True)
    manager = models.OneToOneField(Manager,on_delete=models.CASCADE )
    average_rating = models.FloatField(default=0)
    
class RestaurantImage(models.Model):
    restaurant= models.ForeignKey(Restaurant , on_delete=models.CASCADE , related_name='re_image')
    image = models.ImageField(upload_to='managment/re_image',validators=[validate_file_size])
    
class FavoriteRestaurant(models.Model):
    like = models.BooleanField(default=True , editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 

class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE , related_name='reservations')
    table_rent=models.FloatField(null= True)
    done = models.BooleanField(default=False)

class Table(models.Model):
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    reservation= models.ForeignKey(Reservation, on_delete=models.CASCADE , null=True , related_name='table')
    table_status = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='table')

class Meal(models.Model):
    TYPE_DESSERT = 'DESSERT'
    TYPE_DRINK = 'DRINK'
    TYPE_MAIN = 'MAIN'
    
    TYPE_CHOICES = [
        (TYPE_DESSERT, 'Dessert'),
        (TYPE_DRINK, 'Drink'),
        (TYPE_MAIN, 'Main'),
    ]    
    name = models.CharField(max_length=255)
    discription = models.TextField(null=False,blank=True)
    average_rating = models.FloatField(default=0)
    type =  models.CharField(max_length = 10 , choices = TYPE_CHOICES , default = TYPE_MAIN)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='meals', null=True)

class MealImage(models.Model):
    meal= models.ForeignKey(Meal , on_delete=models.CASCADE , related_name='meal_image')
    image = models.ImageField(upload_to='managment/meal_image',validators=[validate_file_size])
    
class FavoriteMeal(models.Model):
    like = models.BooleanField(default=True , editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)     

class ReservationItem(models.Model):
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE , related_name= 'items')
    meal= models.ForeignKey(Meal,on_delete=models.CASCADE , null=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)] , null = True)
        
# class TableBill(models.Model):
#     reservation=models.OneToOneField(Reservation,on_delete=models.CASCADE)
#     table_rent=models.DecimalField(max_digits=5, decimal_places=2 , null= True)
#     # additional_thing=models.DecimalField(max_digits=5, decimal_places=2)
class Complaint(models.Model):
    resolve = models.BooleanField(default=False )
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField() 

class RatingRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='rating')
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    rating =models.PositiveIntegerField(choices=((1,'1 star'),(2, '2 stars'), (3 , '3 stars'), (4 , '4 stars'), (5 , '5 stars')))
    
class RatingMeal(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE,related_name='rating')
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    rating =models.PositiveIntegerField(choices=((1,'1 star'),(2, '2 stars'), (3 , '3 stars'), (4 , '4 stars'), (5 , '5 stars')),null=True)


class Order (models.Model):
    STATUS_DONE = 'DONE'
    STATUS_LOADING = 'LOADING'
    STATUS_REFUSED = 'REFUSED'
    STATUS_CHOICES = [
        (STATUS_DONE, 'done'),
        (STATUS_LOADING, 'loading'),
        (STATUS_REFUSED, 'refused'),
    ]  
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant , on_delete = models.CASCADE , related_name = 'orders')
    delivery_rent=models.FloatField(null= True)
    done = models.BooleanField(default=False)

class OrderItem(models.Model):
    meal= models.ForeignKey(Meal,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')

class DeliveryBill(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    delivery_rent=models.DecimalField(max_digits=5, decimal_places=2)
    date=models.DateTimeField(auto_now_add=True)