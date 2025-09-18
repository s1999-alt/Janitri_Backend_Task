from django.urls import path
from .views import RegisterView, UserListView, UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),

    path('', UserListView.as_view(), name='users_list'),
    path('create/', UserCreateView.as_view, name='user_create'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
