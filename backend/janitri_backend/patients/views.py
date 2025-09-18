from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminOrDoctor
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


#view for patient creation
class PatientListCreateView(generics.ListCreateAPIView):
  queryset = Patient.objects.all().order_by('-created_at')
  serializer_class = PatientSerializer
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_fields = ['medical_id','gender']
  search_fields = ['name','medical_id']
  ordering_fields = ['created_at','name']

  def get_permissions(self):
     if self.request.method == 'POST':
        return [IsAdminOrDoctor()]
     return [IsAuthenticated()]

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)

#view for get the patient
class PatientRetrieveView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]



