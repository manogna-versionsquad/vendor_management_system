from django.urls import path
from . import views
from userauths import views as userauths_views
from store import views as store_views
from customer import views as customer_views

urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view()),
    path('user/register/',userauths_views.RegisterView.as_view()),
    path('user/profile/<user_id>/',userauths_views.ProfileView.as_view()),
    #Store Endpoints
    path('category/',store_views.CategoryListAPIView.as_view()),
    path('products/',store_views.ProductListAPIView.as_view()),
    #path('products/<int:pk>/',store_views.ProductDetailAPIView.as_view()),
    path('products/<slug>/',store_views.ProductDetailAPIView.as_view()),
    path('cart-list/<str:cart_id>/<int:user_id>/',store_views.CartListView.as_view()),
    path('cart-list/<str:cart_id>/',store_views.CartListView.as_view()),
    path('cart-detail/<str:cart_id>/',store_views.CartDetailView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/<int:user_id>/',store_views.CartItemDeleteAPIView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/',store_views.CartItemDeleteAPIView.as_view()),
    path('checkout/<order_oid>/',store_views.CheckoutView.as_view()),
    path('reviews/<product_id>/',store_views.ReviewListAPIView.as_view()),
    path('search/',store_views.SearchProductAPIView.as_view()), 

    #Payment Endpoints


    # Customer Endpoints
    path("customer/orders/<user_id>/",customer_views.OrdersAPIView.as_view()),
    path("customer/orders/<user_id>/<order_oid>/",customer_views.OrderDetailAPIView.as_view()),


]   