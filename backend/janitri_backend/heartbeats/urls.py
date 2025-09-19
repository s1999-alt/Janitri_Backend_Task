from django.urls import path
from .views import HeartRateCreateView, HeartRateListView, HeartRateSummaryView

urlpatterns = [
    path('', HeartRateCreateView.as_view(), name='heartbeats_create'),
    path('list/', HeartRateListView.as_view(), name='heartbeats_list'),
    path('summary/', HeartRateSummaryView.as_view(), name='heart_rate_summary'),
]