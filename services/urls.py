from django.urls import path
from django.urls.conf import include
from services.models_shared import Customer
from . import views
from rest_framework_nested import routers

router=routers.DefaultRouter()
# router.register()
router.register('customer', views.CustomerViewSet, basename=Customer)
router.register('allcustomers', views.AllCustomersViewSet)



customer_router = routers.NestedDefaultRouter(router , 'customer', lookup='customer')
customer_router.register('customer', views.CustomerViewSet,basename='Customer')
customer_router.register('allcustomers', views.AllCustomersViewSet)



urlpatterns = router.urls + customer_router.urls 


