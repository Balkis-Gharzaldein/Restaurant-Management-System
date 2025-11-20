from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin , ListModelMixin
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models_shared import Customer
from .permissions import IsCustomerOrReadOnly, IsSuperUser 
from .serializers import  CustomerSerializer


class CustomerViewSet(ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class=CustomerSerializer
    permission_classes=[IsCustomerOrReadOnly]
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    # prevent the customer
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
    @action(detail=False ,methods=['GET','PUT'])
    def me(self,request):
        # prevent the user 
        (customer,create )= Customer.objects.get_or_create(user_id=request.user.id)
        if request.method =='GET' :
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method =='PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class AllCustomersViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Customer.objects.select_related('user').all()
    serializer_class=CustomerSerializer
    permission_classes=[IsSuperUser]
    

