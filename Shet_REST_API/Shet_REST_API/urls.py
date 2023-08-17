from tkinter.font import names
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from E_Store .views import ProductVS, Contact, StarRatingVS, GetReviews
from UserProfile .views import UserProfileVS, SignUp, LogIn, LogOut, GetCSRF
from Cart .views import CartVS, AddForLaterVS, MoveToCartVS
from Orders .views import AddressVS, GetAddresses, OrderVS, PlaceOrderVS, GetOrders, ProductOrderedVS
from Search .views import Search

router = routers.DefaultRouter()
router.register(r'user-profile', UserProfileVS)
router.register(r'cart', CartVS, basename="Cart")
router.register(r'add-for-later', AddForLaterVS, basename="AddForLater")
router.register(r'move-to-cart', MoveToCartVS, basename="MoveToCartVS")
router.register(r'products', ProductVS)
router.register(r'contact-us', Contact)
router.register(r'address', AddressVS)
router.register(r'product-ordered', ProductOrderedVS)
router.register(r'orders', OrderVS)
router.register(r'place-order', PlaceOrderVS, basename='PlaceOrder')
# router.register(r'order-updates', OrderUpdate)
router.register(r'star-ratings', StarRatingVS)
router.register(r'search', Search)

urlpatterns = [
    path('', include(router.urls)),
    path('get-csrf', GetCSRF, name='GetCSRF'),
    path('sign-up', SignUp, name='SignUp'),
    path('log-in', LogIn, name='LogIn'),
    path('log-out', LogOut, name='LogOut'),
    path('get-orders/<str:Customer>', GetOrders, name='GetOrders'),
    path('get-addresses/<str:Customer>', GetAddresses, name='GetAddresses'),
    path('product-reviews/<int:Product>', GetReviews, name='GetReviews'),
    path('admin/', admin.site.urls),
    #SocialAuth
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
