from contextvars import Token

from requests import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .serializers import AllUserSerializer
from .models import User

from .permissions import  IsSuperUser 
# Create your views here.
class RefreshTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
class AllUserViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=User.objects.all()
    serializer_class=AllUserSerializer
    # permission_classes=[IsSuperUser]
    filter_backends = [SearchFilter]
    search_fields = ['username']