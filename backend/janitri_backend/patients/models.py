from django.db import models
from django.conf import settings

class Patient(models.Model):
  GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
    ('O','Other')
  )
  name = models.CharField(max_length=225)
  age = models.PositiveIntegerField(null=True, blank=True)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
  medical_id = models.CharField(max_length=100, unique=True)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='patients')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} ({self.medical_id})"
  



