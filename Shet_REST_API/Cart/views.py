from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .cart import Cart

# Create your views here.   
class CartVS(viewsets.ViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    def list(self, request):
            cart = Cart(request)
            return JsonResponse(cart.cart, safe=False)

    def create(self, request):
        cart = Cart(request)
        cart.add(request, request.data['id'])
        return HttpResponse('success')
        
    def partial_update(self, request, pk):
        cart = Cart(request)
        cart.update(int(pk), request)
        return HttpResponse('success')
    
    def destroy(self, request, pk=id):
        cart = Cart(request)
        cart.delete(int(pk))
        return HttpResponse('success')

class AddForLaterVS(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        cart = Cart(request)
        cart.AddForLater(request, request.data['id'])
        return HttpResponse('success')

class MoveToCartVS(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        cart = Cart(request)
        cart.MoveToCart(request, request.data['id'])
        return HttpResponse('success')

    def destroy(self, request, pk=id):
        cart = Cart(request)
        cart.DeleteForLater(int(pk))
        return HttpResponse('success')     
               