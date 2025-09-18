from django.db import models
from django.conf import settings
from patients.models import Patient
from django.core.validators import MinValueValidator, MaxValueValidator


class HeartRate(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='heart_rates')
  bpm = models.PositiveSmallIntegerField(validators=[MinValueValidator(20), MaxValueValidator(240)])
  recorded_at = models.DateTimeField()
  recorded_by = models.ForeignKey("app.Model", on_delete=models.SET_NULL, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=False)

  class Meta:
    ordering = ['-recorded_at']
