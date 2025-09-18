from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsDoctorOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class PatientListCreateView(generics.ListCreateAPIView):
  queryset = Patient.objects.all().order_by('-created_at')
  serializer_class = PatientSerializer
  permission_classes = [IsDoctorOrReadOnly]
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_fields = ['medical_id','gender']
  search_fields = ['name','medical_id']
  ordering_fields = ['created_at','name']


  def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)


class PatientRetrieveView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]



