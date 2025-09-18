from django.urls import path
from .views import HeartRateCreateView, HeartRateListView

urlpatterns = [
    path('', HeartRateCreateView.as_view(), name='heartbeats_create'),
    path('list/', HeartRateListView.as_view(), name='heartbeats_list'),
]