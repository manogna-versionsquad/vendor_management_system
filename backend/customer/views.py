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
#import requests

#stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class OrdersAPIView(generics.ListAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        orders = CartOrder.objects.filter(buyer=user,payment_status="paid")
        return orders
    

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        order_oid = self.kwargs['order_oid']
        user = User.objects.get(id=user_id)
        order = CartOrder.objects.get(buyer=user,oid=order_oid,payment_status="paid")

        return order
    

