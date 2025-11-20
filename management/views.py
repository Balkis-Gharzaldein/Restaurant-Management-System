from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filters import MealFilter, RestaurantFilter
from .permissions import IsCustomerOrReadOnly, IsManager, IsSuperUser ,IsUser
from .models import Complaint, DeliveryBill, FavoriteMeal, FavoriteRestaurant, Manager, Meal, MealImage, Order, OrderItem, RatingMeal, RatingRestaurant, Reservation, ReservationItem , Restaurant, RestaurantImage, Table
from .serializers import ( AddOrderItemSerializer, AllBillOrderSerializer, AllFavoriteRestaurantSerializer, AllInfoRestaurantSerializer, AllMealSerializer, AllReservationManagerSerializer, AllRestaurantSerializer,ComplaintAdminSerializer, ComplaintSerializer, DelivayRentSerializer, DeliveryBillSerializer, FavoriteMealSerializer, FavoriteRestaurantSerializer, 
                            ManagerSerializer, MealImageSerializer,  MealSerializer, OrderItemSerializer, OrderSerializer, RatingMealSerializer, RatingRestaurantSerializer,  ReservationSerializer, RestaurantImageSerializer,
                            RestaurantSerializer,SimpleMealSerializer, SimpleRestaurantSerializer, SimpleTableSerializer, TableSerializer, UpdateOrderItemSerializer,
                            UpdateTableSerializer , ReservationItemSerializer , SelectReservationSerializer  , AddTableRentSerializer , AllBillSerializer )
from rest_framework import status

class ManagerViewSet(ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class=ManagerSerializer
    permission_classes=[IsManager]
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        return Manager.objects.filter(user=self.request.user)
    @action(detail=False ,methods=['GET','PUT','DELETE'])
    def me(self,request):
        (manager,create )= Manager.objects.get_or_create(user_id=self.request.user.id)
        if request.method =='GET' :
            serializer=ManagerSerializer(manager)
            return Response(serializer.data)
        elif request.method =='PUT':
            serializer = ManagerSerializer(manager,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class AllManagersViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Manager.objects.all()
    serializer_class=ManagerSerializer
    permission_classes=[IsSuperUser]
# ------------------------------------------------------------------------------
#   Restaurant
# ------------------------------------------------------------------------------
class RestaurantViewSet(ModelViewSet):  
    serializer_class = RestaurantSerializer
    permission_classes = [IsManager]
    def get_queryset(self):
        return Restaurant.objects.filter(manager=self.request.user.manager)
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user.manager)

class RestaurantImageViewSet(ModelViewSet):
    serializer_class = RestaurantImageSerializer
    permission_classes =[IsManager]
    def get_serializer_context(self):
        return {'restaurant_id':self.kwargs['restaurant_pk']}
    def get_queryset(self):
        return RestaurantImage.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])        

class SimbleRestaurantViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):  
    queryset=Restaurant.objects.all()
    permission_classes =[IsUser]
    serializer_class = SimpleRestaurantSerializer        

class AllRestaurantViewSet(ListModelMixin,GenericViewSet):
    queryset=Restaurant.objects.all()
    serializer_class=AllRestaurantSerializer
    # permission_classes=[IsUser]       
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = RestaurantFilter
    search_fields = ['name']
    ordering_fields = ['average_rating']

class AllInfoRestaurantViewSet(ListModelMixin,GenericViewSet):
    queryset=Restaurant.objects.all()
    serializer_class=AllInfoRestaurantSerializer
    # permission_classes=[IsSuperUser]       
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
class FavoriteRestaurantViewSet(ModelViewSet):
    serializer_class = FavoriteRestaurantSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer
        context['restaurant_id'] = self.kwargs['simplerestaurant_pk']
        return context
    def get_queryset(self):
        return FavoriteRestaurant.objects.filter(customer=self.request.user.customer)

class AllFavoriteRestaurantViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    # queryset = FavoriteRestaurant.objects.all()
    serializer_class = AllFavoriteRestaurantSerializer
    def get_queryset(self):
        return FavoriteRestaurant.objects.filter(customer=self.request.user.customer)
    
class RatingRestaurantViewSet(ModelViewSet):
    serializer_class=RatingRestaurantSerializer
    permission_classes = [IsUser]
    def get_queryset(self):
        return RatingRestaurant.objects.filter(restaurant_id = self.kwargs['simplerestaurant_pk'])
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer.id
        context['restaurant_id'] = self.kwargs['simplerestaurant_pk']
        return context
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
class TableViewSet(ModelViewSet):
    permission_classes =[IsManager]
    def get_queryset(self):
        manager = self.request.user.manager
        restaurant_id = self.kwargs.get('restaurant_pk')
        return Table.objects.filter(restaurant__manager=manager, restaurant_id=restaurant_id) 
    def get_serializer_context(self):
        return {'restaurant_id':self.kwargs['restaurant_pk']}  
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SimpleTableSerializer
        if self.request.method == 'PATCH':
            return UpdateTableSerializer
        return TableSerializer
    # def get_serializer_context(self):
    #     return {'restaurant_id': self.kwargs['restaurant_pk']}


class SimpleTableViewSet(ModelViewSet):
    http_method_names = ['get', 'patch']
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateTableSerializer
        return TableSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['reservation_id'] = self.kwargs['reservation_pk']
        return context
    def get_queryset(self):
        restaurant_id = self.kwargs['simplerestaurant_pk']
        queryset = Table.objects.filter(restaurant_id=restaurant_id, table_status=False)
        return queryset
    def update(self, request, *args, **kwargs):
        reservation_id = self.kwargs['reservation_pk']
        instance = self.get_object()
        instance.reservation_id = reservation_id
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    filter_backends = [SearchFilter]
    search_fields = ['capacity']
class MealViewSet(ModelViewSet):
    serializer_class=MealSerializer
    permission_classes =[IsManager]
    def get_queryset(self):
        manager = self.request.user.manager
        restaurant_id = self.kwargs.get('restaurant_pk')
        return Meal.objects.filter(restaurant__manager=manager, restaurant_id=restaurant_id) 
    def get_serializer_context(self):
        return {'restaurant_id':self.kwargs['restaurant_pk']}

class SimbleMealViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):  
    serializer_class = SimpleMealSerializer
    def get_queryset(self):
        return Meal.objects.filter(restaurant_id=self.kwargs['simplerestaurant_pk'])
    permission_classes =[IsUser]
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
class MealImageViewSet(ModelViewSet):
    serializer_class = MealImageSerializer
    permission_classes =[IsManager]
    def get_serializer_context(self):
        return {'meal_id':self.kwargs['meal_pk']}
    def get_queryset(self):
        return MealImage.objects.filter(meal_id=self.kwargs['meal_pk'])

class AllMealViewSet(ListModelMixin,GenericViewSet):
    # queryset=Meal.objects.all()
    serializer_class=AllMealSerializer
    permission_classes=[IsManager]  
    def get_queryset(self):
        return Meal.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])   
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = MealFilter
    search_fields = ['name', 'price','type']
    ordering_fields = ['average_rating']

class AllMealTopViewSet(ListModelMixin,GenericViewSet):
    queryset=Meal.objects.all()
    serializer_class=AllMealSerializer
    permission_classes=[IsUser]   
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = MealFilter
    search_fields = ['name', 'price','type']
    ordering_fields = ['average_rating']
class FavoriteMealViewSet(ModelViewSet):
    queryset = FavoriteMeal.objects.all()
    serializer_class = FavoriteMealSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer
        context['meal_id'] = self.kwargs['simplemeal_pk']
        return context

class RatingMealViewSet(ModelViewSet):
    serializer_class=RatingMealSerializer
    permission_classes = [IsUser]
    def get_queryset(self):
        return RatingMeal.objects.filter(meal_id = self.kwargs['simplemeal_pk'])
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer.id
        context['meal_id'] = self.kwargs['simplemeal_pk']
        return context
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
class ReservationViewSet (CreateModelMixin ,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    # queryset=Reservation.objects.all()
    serializer_class= ReservationSerializer
    def get_queryset(self):
        return Reservation.objects.filter(restaurant=self.kwargs['simplerestaurant_pk'],customer=self.request.user.customer)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer
        context['restaurant_id'] = self.kwargs['simplerestaurant_pk']
        return context
    
    
class AllReservationCustomerViewSet (ListModelMixin,RetrieveModelMixin,GenericViewSet):
    # queryset=Reservation.objects.all()
    permission_classes = [IsCustomerOrReadOnly,IsUser]

    serializer_class= ReservationSerializer
    def get_queryset(self):
        return Reservation.objects.filter(customer=self.request.user.customer)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_id'] = self.request.user.customer
        return context
    
    
class AllReservationManagerViewSet (ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):
    permission_classes = [IsManager]
    def get_queryset(self):
        manager = self.request.user.manager
        return Reservation.objects.filter(restaurant__manager=manager) 
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AddTableRentSerializer
        return AllReservationManagerSerializer
class CreateTableBillViewSet(ModelViewSet):
    queryset = ReservationItem.objects.all()
    serializer_class = ReservationItemSerializer
    def get_serializer_context(self):
        return {'reservation_id': self.kwargs['allreservationformanager_pk']} 
    def get_queryset(self):
        return ReservationItem.objects.filter(reservation_id=self.kwargs['allreservationformanager_pk'])
 

class AllBillViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class =AllBillSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        manager = manager=self.request.user.manager
        queryset = Reservation.objects.filter(done=True)
        if manager:
            queryset = queryset.filter(restaurant__manager_id=manager)
        return queryset

class SelectReservationViewSet(ListModelMixin , GenericViewSet) :
    queryset = Reservation.objects.all()
    serializer_class = SelectReservationSerializer    
class ComplaintViewSet(CreateModelMixin,GenericViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer      
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class ComplaintAdminViewSet(ListModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintAdminSerializer      
    # permission_classes=[IsSuperUser]  

class OrderViewSet(CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # queryset=Order.objects.prefetch_related('items__meal').all()
    serializer_class= OrderSerializer    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurant_id'] = self.kwargs['simplerestaurant_pk']
        return context

class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderItemSerializer
        return OrderItemSerializer
    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_pk']}
    def get_queryset(self):
        return OrderItem.objects \
                .filter(order_id=self.kwargs['order_pk']) \
                .select_related('meal') 

class AllOrderViewSet(UpdateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # serializer_class= OrderSerializer    
    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user.customer)
    permission_classes = [IsManager]
    def get_queryset(self):
        manager = self.request.user.manager
        return Order.objects.filter(restaurant__manager=manager) 
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DelivayRentSerializer
        return OrderSerializer

class AllBillOrderViewSet(ListModelMixin ,RetrieveModelMixin, GenericViewSet):
    serializer_class =AllBillOrderSerializer
    permission_classes = [IsManager]
    def get_queryset(self):
        manager = manager=self.request.user.manager
        queryset = Order.objects.filter(done=True)
        if manager:
            queryset = queryset.filter(restaurant__manager_id=manager)
        return queryset