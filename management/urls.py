from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()
# router.register()
router.register('manager', views.ManagerViewSet,basename='manager')
router.register('allmanagers', views.AllManagersViewSet,basename='allmanager')
router.register('restaurant',views.RestaurantViewSet ,basename='restaurant')
router.register('simplerestaurant',views.SimbleRestaurantViewSet,basename='Simple_Restaurant')
router.register('allrestaurant', views.AllRestaurantViewSet,basename='allrestaurant')
router.register('allinforestaurant', views.AllInfoRestaurantViewSet,basename='allinforestaurant')
router.register('likerestaurant', views.AllFavoriteRestaurantViewSet, basename='likerestaurant')
router.register('allreservationforcustomer', views.AllReservationCustomerViewSet,basename='allreservationcustomer')
router.register('allreservationformanager', views.AllReservationManagerViewSet,basename='allreservationmanager')
router.register('allbill', views.AllBillViewSet,basename='allbill')
router.register('allorder', views.AllOrderViewSet,basename='allorder')
router.register('allorderbill', views.AllBillOrderViewSet,basename='allorderbill')
router.register('alltopmeal', views.AllMealTopViewSet,basename='alltopmeal')



router.register('complaint', views.ComplaintViewSet,basename='complaint')
router.register('complaintadmin', views.ComplaintAdminViewSet,basename='complaintadmin')


manager_router = routers.NestedDefaultRouter(router , 'manager', lookup='manager')
manager_router.register('manager', views.ManagerViewSet,basename='manager')
manager_router.register('allmanagers', views.AllManagersViewSet,basename='allmanager')

restaurant_router = routers.NestedDefaultRouter(router , 'restaurant', lookup='restaurant')
restaurant_router.register('restaurant', views.RestaurantViewSet,basename='restaurant')
restaurant_router.register('restaurantimage', views.RestaurantImageViewSet,basename='restaurant_Image')
restaurant_router.register('table', views.TableViewSet,basename='Table')
restaurant_router.register('meal',views.MealViewSet,basename='meal')
restaurant_router.register('image', views.MealImageViewSet,basename='Meal_Image')
restaurant_router.register('allmeal', views.AllMealViewSet,basename='allmeal')


meal_router = routers.NestedDefaultRouter(restaurant_router, 'meal', lookup='meal')
meal_router.register('image', views.MealImageViewSet, basename='meal-image')

simplerestaurant_router = routers.NestedDefaultRouter(router, 'simplerestaurant', lookup='simplerestaurant')
simplerestaurant_router.register('simplerestaurant', views.SimbleRestaurantViewSet,basename='simplerestaurant')
simplerestaurant_router.register('likerestaurant', views.FavoriteRestaurantViewSet, basename='likerestaurant')
simplerestaurant_router.register('simplemeal',views.SimbleMealViewSet,basename='simplemeal')
simplerestaurant_router.register('reservation', views.ReservationViewSet, basename='reservation')
simplerestaurant_router.register('ratingrestaurant', views.RatingRestaurantViewSet, basename='ratingrestaurant')
simplerestaurant_router.register('order', views.OrderViewSet, basename='order')


simplemeal_router = routers.NestedDefaultRouter(simplerestaurant_router, 'simplemeal', lookup='simplemeal')
simplemeal_router.register('likemeal', views.FavoriteMealViewSet, basename='likemeal')
simplemeal_router.register('ratingmeal', views.RatingMealViewSet, basename='ratingmeal')

reservation_router = routers.NestedDefaultRouter(simplerestaurant_router, 'reservation', lookup='reservation')
reservation_router.register('simpletable', views.SimpleTableViewSet,basename='simpletable')
# reservation_router.register('billitem' , views.CreateTableBillViewSet , basename='billitem')

order_router = routers.NestedDefaultRouter(simplerestaurant_router , 'order', lookup='order')
order_router.register('order', views.OrderViewSet, basename='order')
order_router.register('orderitem', views.OrderItemViewSet,basename='orderitem')

reservationmanager_router = routers.NestedDefaultRouter(router , 'allreservationformanager' , lookup='allreservationformanager')
reservationmanager_router.register('allreservationformanager', views.AllReservationManagerViewSet,basename='allreservationmanager')
reservationmanager_router.register('addtablemeal', views.CreateTableBillViewSet, basename='addtablemeal')


urlpatterns = (router.urls + manager_router.urls +restaurant_router.urls  
                +meal_router.urls + simplerestaurant_router.urls
                + simplemeal_router.urls + reservation_router.urls+ 
                order_router.urls + reservationmanager_router.urls)


