from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny

from userauths.models import User,Profile
from userauths.serializer import MyTokenObtainPairSerializer, RegisterSerializer,ProfileSerializer


# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_objects(self):
        user_id = self.kwargs["user_id"]
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)

        return profile

