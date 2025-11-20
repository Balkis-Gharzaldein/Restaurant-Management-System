from django.urls import include, path
from . import views
from .views import  RefreshTokenView
from django.urls import path
from rest_framework_nested import routers


router=routers.DefaultRouter()

router.register('alluser', views.AllUserViewSet,basename='alluser')
urlpatterns = [    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('', include(router.urls)),
]
