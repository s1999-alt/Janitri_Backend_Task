from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Avg, Min, Max
from rest_framework.response import Response
from .models import HeartRate
from .serializers import HeartRateSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filter import HeartRateFilter
from users.permissions import IsAdminOrDoctor
from patients.models import Patient


# view for heartrate creation
class HeartRateCreateView(generics.CreateAPIView):
  serializer_class = HeartRateSerializer

  def get_permissions(self):
     # Only Admin or Doctor can record heart rates
     return [IsAdminOrDoctor()]

  def perform_create(self, serializer):
    serializer.save(recorded_by=self.request.user)

#view for heartrate listing
class HeartRateListView(generics.ListAPIView):
    serializer_class = HeartRateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HeartRateFilter

    def get_queryset(self):
       queryset = HeartRate.objects.all()
       return queryset


class HeartRateSummaryView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
      patient_id = request.query_params.get('patient')
      if not patient_id:
         return Response({"error": "patient parameter is required"}, status=400)
      
      try:
         patient = Patient.objects.get(id=patient_id)
      except Patient.DoesNotExist:
         return Response({"error":"Patient not found"}, status=404)
      

      stats = HeartRate.objects.filter(patient=patient).aggregate(
        min_bpm=Min('bpm'),
        max_bpm=Max('bpm'),
        avg_bpm=Avg('bpm'),
      )

      latest = HeartRate.objects.filter(patient=patient).order_by('-recorded_at').first()

      return Response({
        "patient": patient.id,
        "patient_name": patient.name,
        "min_bpm": stats['min_bpm'],
        "max_bpm": stats['max_bpm'],
        "avg_bpm": stats['avg_bpm'],
        "latest_bpm": latest.bpm if latest else None,
        "total_records": HeartRate.objects.filter(patient=patient).count()
      })

      