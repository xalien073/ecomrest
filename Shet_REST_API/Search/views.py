from rest_framework import viewsets
from E_Store .models import Product
from E_Store .serializers import ProductSer
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class SearchPagination(PageNumberPagination):
    page_size = 5

class Search(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSer
    filter_backends = [SearchFilter]
    search_fields = ['product_name', 'description', 'category__name',
                     'brand__name']
    pagination_class = SearchPagination