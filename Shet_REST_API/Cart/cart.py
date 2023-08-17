from django.conf import settings
from E_Store.models import Product
from E_Store.serializers import ProductSer
from Orders .models import ProductOrdered, Order


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                'subtotal': 0, 'products': [], 'forLater': []}

        self.cart = cart
        self.cart['subtotal'] = self.subtotal()

    # def __iter__(self):
    #     product_ids = self.cart.keys()
    #     product_clean_ids = []
    #     for p in product_ids:
    #         product_clean_ids.append(p)
    #         self.cart[str[p]['product']] = Product.objects.get(pk=p)

    #     for item in self.cart.values():
    #         yield item
    #     print(product_clean_ids)

    def add(self, request, id):
        product = Product.objects.get(pk=id)
        serializer = ProductSer(product, context={'request': request})
        self.cart['products'].append(
            {'product': serializer.data, 'qty': 1, 'ProductSubtotal': float(product.price)})
        self.save()

    def update(self, id, request):
        for p in self.cart['products']:
            if p['product']['product_id'] == id:
                p.update(
                    {'qty': request.data['qty'], 'ProductSubtotal': float(request.data['total'])})
                self.save()

    def delete(self, id):
        for p in self.cart['products']:
            if p['product']['product_id'] == id:
                self.cart['products'].remove(p)
                self.save()

    def AddForLater(self, request, id):
        product = Product.objects.get(pk=id)
        serializer = ProductSer(product, context={'request': request})
        self.cart['forLater'].append({'product': serializer.data, 'qty': 1, 'ProductSubtotal': float(product.price)})
        self.delete(id)
        print('id', id)

    def MoveToCart(self, request, id):
        for p in self.cart['forLater']:
            if p['product']['product_id'] == id:
                self.cart['forLater'].remove(p)
        self.add(request, id)
        print('id', id)

    def DeleteForLater(self, id):
        for p in self.cart['forLater']:
            if p['product']['product_id'] == id:
                self.cart['forLater'].remove(p)
                self.save()     

    def subtotal(self):
        return sum(float(product['ProductSubtotal']) for product in self.cart['products'])    

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def PlaceOrder(self, request):
        print(request.user)
        Products = []
        for p in self.cart['products']:
            product = Product.objects.get(product_id=p['product']['product_id'])
            print('P',product)
            PurchasedProduct = ProductOrdered(Product=product, Qty=p['qty'], ProductSubtotal=p['ProductSubtotal'])
            PurchasedProduct.save()
            Products.append(PurchasedProduct)
            print('O',PurchasedProduct.id)
        print(Products)
        NewOrder = Order(Customer=request.user,
        Orders=Products, Subtotal=self.cart['subtotal'], 
        Address=1)
        NewOrder.save()
        print(NewOrder.Order_Id)

    def clear(self):
        self.cart['products'].clear()
        self.cart['subtotal'] = 0
        self.session.modified = True                
