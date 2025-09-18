from rest_framework import generics
from .models import HeartRate
from .serializers import HeartRateSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filter import HeartRateFilter
from users.permissions import IsAdminOrDoctor


class HeartRateCreateView(generics.CreateAPIView):
  serializer_class = HeartRateSerializer

  def get_permissions(self):
     # Only Admin or Doctor can record heart rates
     return [IsAdminOrDoctor()]

  def perform_create(self, serializer):
    serializer.save(recorded_by=self.request.user)


class HeartRateListView(generics.ListAPIView):
    serializer_class = HeartRateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HeartRateFilter

    def get_queryset(self):
       queryset = HeartRate.objects.all()
       return queryset
