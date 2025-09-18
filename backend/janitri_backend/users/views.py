from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

#uncomment this and comment UserListView, UserCreateView for anyone can register
# class RegisterView(generics.CreateAPIView):
#   queryset = User.objects.all()
#   serializer_class = RegisterSerializer
#   permission_classes = [permissions.AllowAny]



class UserListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAdminUser] # only admins can view all users

class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [permissions.IsAdminUser] # only admins can create doctors/nurses



