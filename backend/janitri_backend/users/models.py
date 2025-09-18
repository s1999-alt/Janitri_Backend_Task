from django.db import models
from django.contrib.auth. models import AbstractUser
from .manager import UserManager



class User(AbstractUser):
  ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse'),
  )
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='doctor')
  objects = UserManager()

  def __str__(self):
    return f"{self.username} ({self.role})"
  


