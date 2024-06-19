from django.urls import path
from . import views
from userauths import views as userauths_views
from store import views as store_views


urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view()),
    path('user/register/',userauths_views.RegisterView.as_view()),

    #Store Endpoints
    path('category/',store_views.CategoryListAPIView.as_view()),
    path('products/',store_views.ProductListAPIView.as_view()),
    #path('products/<int:pk>/',store_views.ProductDetailAPIView.as_view()),
    path('products/<slug>/',store_views.ProductDetailAPIView.as_view()),
]   