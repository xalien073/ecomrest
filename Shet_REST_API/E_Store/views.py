from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product, Contact, StarRating
from .serializers import ProductSer, ContactSer, StarRatingSer, ReviewsSerializer
from django.http import JsonResponse
# Create your views here.
class ProductVS(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSer
    lookup_field = 'slug'

class Contact(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Contact.objects.all()
    serializer_class = ContactSer
   
class StarRatingVS(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = StarRating.objects.all()
    serializer_class = StarRatingSer
   
def GetReviews(request, Product):
    Reviews = StarRating.objects.filter(product=Product).order_by("-timeStamp")
    serializer = ReviewsSerializer(Reviews, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)
