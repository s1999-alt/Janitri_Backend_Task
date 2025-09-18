from django.urls import path
from .views import PatientListCreateView, PatientRetrieveView



urlpatterns = [
  path('', PatientListCreateView.as_view(), name='patients_list_create'),
  path('<int:pk>/', PatientRetrieveView.as_view(), name='patient_detail'),
]
