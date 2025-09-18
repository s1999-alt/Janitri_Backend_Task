from django.db import models
from django.contrib.auth. models import AbstractUser



class User(AbstractUser):
  ROLE_CHOICES = (
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse'),
    ('admin', 'Admin'),
  )
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='doctor')

  def __str__(self):
    return f"{self.username} ({self.role})"
  


