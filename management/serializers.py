from rest_framework import serializers
from core.serializers import UserSerializer
from services.models_shared import Customer
from services.serializers import CustomerSerializer , SimpleCustomerSerializer
from .models import  Complaint, DeliveryBill, Order, OrderItem,ReservationItem  ,FavoriteMeal, FavoriteRestaurant, Manager, MealImage, RatingRestaurant, RatingMeal, Reservation , Restaurant, Table , Meal,RestaurantImage 
from statistics import mean
class ManagerSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Manager
        fields=['id','user','phone','address']
        
class RestaurantImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        restaurant_id = self.context['restaurant_id']
        return RestaurantImage.objects.create(restaurant_id=restaurant_id , **validated_data)
    class Meta:
        model = RestaurantImage
        fields = ['id','image']
        
class TableSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['reservation_id'] = self.context['reservation_id']
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return Table.objects.create(**validated_data)
    class Meta:
        model=Table
        fields = ['id', 'capacity', 'table_status']

class SimpleTableSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        restaurant_id=self.context['restaurant_id']
        return Table.objects.create(restaurant_id=restaurant_id,**validated_data)
    class Meta:
        model=Table
        fields = ['id', 'capacity', 'table_status']


class UpdateTableSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return Table.objects.create(**validated_data)
    class Meta:
        model = Table
        fields = ['table_status']
class JustTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id']
    # def validate(self, attrs):
    #     table_status = attrs.get('table_status')
    #     if table_status == 1:
    #         raise serializers.ValidationError("Sorry the table is reserved")
    #     elif table_status == 0:
    #         reservation_id = self.instance.reservation_id
    #         if reservation_id is not None:
    #             raise serializers.ValidationError("الطاولة محجوزة بالفعل.")
    #     return attrs
class RatingRestaurantSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['restaurant_id'] = self.context['restaurant_id']
        validated_data['customer_id'] = self.context['customer_id']
        return RatingRestaurant.objects.create(**validated_data)
    class Meta:
        model = RatingMeal
        fields = ['id','rating']  
class RestaurantSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)
    re_image = RestaurantImageSerializer(many = True,read_only=True)
    table = TableSerializer(many = True , read_only = True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'phone', 'email', 'oppening_time', 'closing_time','discription','manager','re_image','table','average_rating']
    def create(self, validated_data):
        validated_data['manager'] = Manager.objects.get(user=self.context['request'].user)
        restaurant = Restaurant.objects.create(**validated_data)
        return restaurant

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    re_image = RestaurantImageSerializer(many = True,read_only=True)
    avg_rate = serializers.SerializerMethodField()
    def get_avg_rate(self, restaurant):
        ratings = restaurant.rating.all()
        if ratings:
            avg_rating = mean([item.rating for item in ratings])
            restaurant.average_rating = avg_rating
            restaurant.save()
            return avg_rating
        return 0
    class Meta:
        model=Restaurant
        fields=['id','name','phone','oppening_time', 'closing_time','discription','re_image','avg_rate'] 
    
class AllRestaurantSerializer(serializers.ModelSerializer):
    re_image = RestaurantImageSerializer(many = True,read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name','re_image','average_rating']

class AllRestaurantSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']

class AllInfoRestaurantSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name','phone','email','manager']      

class MealImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        meal_id = self.context['meal_id']
        return MealImage.objects.create(meal_id=meal_id , **validated_data)
    class Meta:
        model = MealImage
        fields = ['id','image']
        
class RatingMealSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['meal_id'] = self.context['meal_id']
        validated_data['customer_id'] = self.context['customer_id']
        return RatingMeal.objects.create(**validated_data)
    class Meta:
        model = RatingMeal
        fields = ['id','rating']  

class MealSerializer(serializers.ModelSerializer):
    meal_image = MealImageSerializer(many = True,read_only=True)
    class Meta:
        model = Meal
        fields = ['id', 'name', 'discription','type','price','meal_image']
    def create(self, validated_data):
        restaurant_id=self.context['restaurant_id']
        return Meal.objects.create(restaurant_id=restaurant_id,**validated_data)

class SimpleMealSerializer(serializers.ModelSerializer):
    meal_image = MealImageSerializer(many=True, read_only=True)
    avg_rate = serializers.SerializerMethodField() 
    def get_avg_rate(self, meal):
        ratings = meal.rating.all()
        if ratings:
            avg_rating = mean([item.rating for item in ratings])
            meal.average_rating = avg_rating
            meal.save()
            return avg_rating
        return 0
    class Meta:
        model = Meal
        fields = ['id', 'name', 'discription', 'type', 'price', 'meal_image','avg_rate']
            
class AllMealSerializer(serializers.ModelSerializer):
    meal_image = MealImageSerializer(many = True,read_only=True)
    class Meta:
        model = Meal
        fields = ['id', 'name','meal_image','average_rating']

class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    restaurant = AllRestaurantSerializer(read_only=True)
    def create(self, validated_data):
        validated_data['customer'] = Customer.objects.get(user=self.context['request'].user)
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return FavoriteRestaurant.objects.create(**validated_data)
    class Meta:
        model = FavoriteRestaurant
        fields = ('id', 'like', 'customer','restaurant')
        
class AllFavoriteRestaurantSerializer(serializers.ModelSerializer):
    restaurant = AllRestaurantSerializer(read_only=True)
    class Meta:
        model = FavoriteRestaurant
        fields = ('id', 'like','restaurant')

class FavoriteMealSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    def create(self, validated_data):
        validated_data['customer'] = Customer.objects.get(user=self.context['request'].user)
        validated_data['meal_id'] = self.context['meal_id']
        return FavoriteMeal.objects.create(**validated_data)
    class Meta:
        model = FavoriteMeal
        fields = ('id', 'like', 'customer')

class ReservationSerializer(serializers.ModelSerializer):
    table = JustTableSerializer(read_only=True,many=True)
    # customer=CustomerSerializer(read_only=True)
    restaurant=AllRestaurantSerializer2(read_only=True)
    def create(self, validated_data):
        validated_data['customer'] = Customer.objects.get(user=self.context['request'].user)
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return Reservation.objects.create(**validated_data)
    class Meta:
        model=Reservation
        fields=['id','restaurant','date','time','notes','table']

class AllReservationManagerSerializer(serializers.ModelSerializer):
    customer= SimpleCustomerSerializer()
    class Meta:
        model = Reservation
        fields= [ 'id' ,'date','time', 'customer','table']
class AddTableRentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Reservation
        fields = ['table_rent' , 'done']
class ReservationItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta :
        model = ReservationItem
        fields = [ 'id' ,'meal' , 'quantity' , 'total_price']
    def create(self, validated_data):
        reservation_id=self.context['reservation_id']
        return ReservationItem.objects.create(reservation_id=reservation_id , **validated_data)    
    def get_total_price(self , reservation_item):
        return reservation_item.quantity * reservation_item.meal.price 

class SelectReservationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Reservation
        fields = [ 'id' , 'customer', 'table' ]    

class GetReservationItemsSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many = True )
    class Meta:
        model = Reservation
        fields = [ 'id' , 'items'  ]       
class TableBillSerializer(serializers.ModelSerializer) :
    items = ReservationItemSerializer(many = True )
    table = SimpleTableSerializer(many=True)
    class Meta:
        model = Reservation
        fields = [ 'id' , 'items' , 'table_rent' ,'table']   

class ComplaintSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Complaint
        fields = ['id', 'message','user']
        
class ComplaintAdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Complaint
        fields = ('id', 'resolve','message','user')

class OrderItemSerializer(serializers.ModelSerializer):
    meal=SimpleMealSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self , order_item):
        return order_item.quantity * order_item.meal.price 
    class Meta:
        model=OrderItem
        fields=['id','meal','quantity','total_price'] 

class AddOrderItemSerializer(serializers.ModelSerializer):
    meal_id = serializers.IntegerField()
    def validate_meal_id(self, value):
        if not Meal.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Meal With The Given Value')
        return value 
    def save(self, **kwargs):
        order_id = self.context['order_id']
        meal_id = self.validated_data['meal_id']
        quantity = self.validated_data['quantity']
        try:
            order_item = OrderItem.objects.get(order_id=order_id,meal_id=meal_id)
            order_item.quantity += quantity
            order_item.save()
            self.instance = order_item
        except OrderItem.DoesNotExist:
            self.instance = OrderItem.objects.create(order_id=order_id , **self.validated_data)
        return self.instance 
    class Meta:
        model = OrderItem
        fields = ['id', 'meal_id','quantity']

class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']  

class OrderSerializer(serializers.ModelSerializer):
    items= OrderItemSerializer(many = True , read_only = True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self , order):
        return sum([item.quantity * item.meal.price for item in order.items.all()])
    class Meta:
        model=Order 
        fields=['id','items','total_price']        
    def create(self, validated_data):
        validated_data['customer'] = Customer.objects.get(user=self.context['request'].user)
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return Order.objects.create(**validated_data)
class DelivayRentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Order
        fields= [ 'delivery_rent', 'done']
class BillItemsSerializer(serializers.ModelSerializer):
    items= OrderItemSerializer(many = True , read_only = True ) 
    class Meta:
        model=Order
        fields = ['id','items']
        
class DeliveryBillSerializer(serializers.ModelSerializer):
    order=BillItemsSerializer(read_only=True)
    class Meta:
        model= DeliveryBill
        fields=['id','date','delivery_rent','order']
    
    def create(self, validated_data):
        order_id=self.context['order_id']
        return DeliveryBill.objects.create(order_id=order_id , **validated_data)

class AllBillSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    items = ReservationItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    def get_total_price(self, reservation):
        return sum([item.quantity * item.meal.price for item in reservation.items.all()])
    def get_total(self, reservation):
        total_price = self.get_total_price(reservation)
        table_rent = reservation.table_rent
        total = total_price + table_rent
        return total
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'items', 'table_rent', 'total_price', 'total']

class AllBillOrderSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total_price(self, order):
        return sum([item.quantity * item.meal.price for item in order.items.all()])

    def get_total(self, order):
        total_price = self.get_total_price(order)
        delivery_rent = order.delivery_rent
        total = total_price + delivery_rent
        return total

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'delivery_rent', 'total_price', 'total']
