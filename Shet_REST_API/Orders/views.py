from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Shipping_Address, Order, ProductOrdered
from .serializers import ShippingAddressSer, OrderSer, GetOrderSer, ProductOrderedSer
from Cart.cart import Cart
# Create your views here.
class AddressVS(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Shipping_Address.objects.all()
    serializer_class = ShippingAddressSer

@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])    
def GetAddresses(request, Customer):
    Customer = Customer
    Addresses = Shipping_Address.objects.filter(User_id=Customer)
    serializer = ShippingAddressSer(Addresses, many=True)
    return JsonResponse(serializer.data, safe=False)    

class ProductOrderedVS(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = ProductOrdered.objects.all()
    serializer_class = ProductOrderedSer

class OrderVS(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Order.objects.all()
    serializer_class = OrderSer

class PlaceOrderVS(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]#, )
    permission_classes = (IsAuthenticated, )
    def create(self, request):
        cart = Cart(request)
        cart.PlaceOrder(request)
        return HttpResponse('success')


@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])    
def GetOrders(request, Customer):
    Customer = Customer
    Orders = Order.objects.filter(Customer_id=Customer).order_by("-Order_Id")
    serializer = GetOrderSer(Orders, context={'request': request}, many=True)
    return JsonResponse(serializer.data, safe=False)    
   