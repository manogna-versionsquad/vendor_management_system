from django.shortcuts import render
from userauths.models import User
from django.conf import settings
from store.models import Tax,Product,Coupon,CartOrderItem,CartOrder,Category,Cart,Notification,Review
from store.serializers import ProductSerializer,CategorySerializer,CartSerializer,CartOrderSerializer,CouponSerializer,ReviewSerializer

from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from decimal import Decimal

#import stripe

#stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def send_notification(user=None,vendor=None,order=None,order_item=None):
    Notification.objects.create(
        user=user,
        vendor=vendor,
        order=order,
        order_item=order_item
    )

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailAPIView(generics.RetrieveAPIView):
    #queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug=slug)

class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer 
    permission_classes = [AllowAny]

    def create(self,request):
        payload = request.data
        product_id = payload['product_id']
        user_id = payload['user_id']
        qty = payload['qty']
        price = payload['price']
        shipping_amountcountry = payload['shipping_amountcountry']
        country = payload['country']
        size = payload['size']
        color = payload['color']
        cart_id = payload['cart_id']

        product = Product.objects.get(id=product_id)
        #user = User.objects.get(id=user_id)
        if user_id != "undefined":
            user = User.objects.get(id=user_id)
        else:
            user = None

        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100

        else:
            tax_rate = 0
        cart = Cart.objects.filter(cart_id = cart_id,product=product).first()

        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage = 20/100
            cart.service_fee = service_fee_percentage * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()

            return Response ({"message": "Cart Updated Successfully"},status=status.HTTP_200_OK)
        
        else:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage = 20/100
            cart.service_fee = service_fee_percentage * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()

            return Response ({"message": "Cart Updated Successfully"},status=status.HTTP_201_CREATED)
        
            
class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user,cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user,cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset
    
    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()

        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        for cart_item in queryset:
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += float(self.calculate_total(cart_item))

        
        data = {
            'shipping':total_shipping,
            'tax':total_tax,
            'service_fee':total_service_fee,
            'sub_total':total_sub_total,
            'total':total_total,
        }

        return Response(data)
    
    
    def calculate_shipping(self,cart_item):
        return cart_item.shipping_amount
    
    def calculate_tax(self,cart_item):
        return cart_item.tax_fee
    
    def calculate_service_fee(self,cart_item):
        return cart_item.service_fee
    
    def calculate_sub_total(self,cart_item):
        return cart_item.sub_total
    
    def calculate_total(self,cart_item):
        return cart_item.total

class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = "cart_id"

    def get_objects(self):
        cart_id = self.kwargs["cart_id"]
        item_id = self.kwargs["item_id"]
        user_id = self.kwargs("user_id")

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id,cart_id=cart_id,user=user)
        else:
            cart = Cart.objects.get(id=item_id,cart_id=cart_id)

        return cart

class CreateCartOrderAPIView(generics.CreateAPIView):
    serilaizer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = [AllowAny]

    def create(self,request):
        payload = request.data

        full_name = payload['full_name']
        email = payload['email']
        mobile = payload['mobile']
        address = payload['address']
        city = payload['city']
        state = payload['state']
        country = payload['country']
        cart_id = payload['cart_id']
        user_id = payload['user_id']

        if user_id != 0:
            user = User.objects.get(id=user_id)

        else:
            user=None
        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_service_fee = Decimal(0.00)
        total_sub_total = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = CartOrder.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            country=country,
        )

        for c in cart_items:
            CartOrderItem.objects.create(
                    order = order,
                    product = c.product,
                    vendor = c.vendor,
                    qty = c.qty,
                    color = c.color ,
                    size = c.size,
                    price = c.price,
                    sub_total = c.sub_total,
                    shipping_amount = c.shipping_amount,
                    service_fee= c.service_fee,
                    tax_fee = c.tax_fee,
                    total = c.total,
                    initial_total = c.total

            )

            total_shipping += Decimal(c.shipping_amount)
            total_tax += Decimal(c.tax_fee)
            total_service_fee += Decimal(c.service_fee)
            total_sub_total += Decimal(c.sub_total)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)
            
            order.vendor.add(c.product.vendor)

        order.sub_total = total_sub_total
        order.shipping_amount = total_shipping
        order.tax_fee = total_tax
        order.service_fee = total_service_fee
        order.initial_total = total_initial_total
        order.total = total_total

        order.save()

        return Response({"message":"Order Created Succesfully","order_oid":order.oid},status=status.HTTP_201_CREATED)

class CheckoutView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    lookup_field = "order_oid"

    def get_object(self):
        order_oid = self.kwargs['order_oid']
        order = CartOrder.objects.get(oid=order_oid)
        return order
    
class CouponAPIView(generics.CreateAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = [AllowAny]

    def create(self,request):
        payload = request.data

        order_oid = payload['order_oid']
        coupon_code = payload['coupon_code']

        order = CartOrder.objects.get(oid=order_oid)
        coupon = Coupon.objects.get(code=coupon_code)

        if coupon:
            order_items = CartOrderItem.objects.filter(order=order,vendor=coupon.vendor)
            if order_items:
                for i in order_items:
                    if not coupon in i.coupon.all():
                        discount = i.total * coupon.discount / 100
                        
                        i.total -= discount
                        i.sub_total -= discount
                        i.coupon.add(coupon)
                        i.saved += discount 

                        order.total -= discount
                        order.sub_total -= discount
                        order.saved += discount

                        i.save()
                        order.save()

                        return Response({"message":"Coupon Activated"},status=status.HTTP_200_OK)
                    else:
                        return Response({"message":"Coupon Already Activated"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Coupon Already Activated"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Coupon Does not Exists"},status=status.HTTP_200_OK)         


class StripeCheckoutView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]          
    queryset = CartOrder.objects.all()

    def create(self):
        order_oid = self.kwargs['order_oid']
        order = CartOrder.objects.get(oid=order_oid)

        if not order:
            return Response({"message":"Order Not Found"},status=status.HTTP_404_NOT_FOUND)


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_query(self):
        product_id = self.kwargs['product_id']

        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)

        return reviews
    
    def create(self,request,*args,**kwargs):
        payload = request.data

        user_id = payload['user_id']
        product_id = payload['product_id']
        rating = payload['rating']
        review = payload['review']
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            review=review
        )

        return Response({"message":"Review Created Successfully"},status=status.HTTP_200_OK)
    
class SearchProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

   # def get_query(self):
     #   query = self.request.GET.get("query")
      #  products = Product.objects.filter(status="published",title__icontains=query)
      #  return products
    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            products = Product.objects.filter(status="published", title__icontains=query)
        else:
            products = Product.objects.filter(status="published")
        return products
