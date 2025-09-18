from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
  def setUp(self):
    # Create an admin user for authentication
    self.admin = User.objects.create_superuser(
        username="admin",
        password="adminpass",
        email="admin@example.com"
    )
    # Get JWT token for admin
    response = self.client.post(reverse('token_obtain_pair'),
        {"username": "admin", "password": "adminpass"},
        format="json"
    )
    self.admin_token = response.data['access']
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

  def test_admin_can_create_doctor(self):
    """Admin should be able to create a doctor user"""
    data = {
        "username": "drsmith",
        "email": "drsmith@example.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!",
        "first_name": "John",
        "last_name": "Smith",
        "role": "doctor"
    }
    response = self.client.post("/api/users/create/", data, format="json")
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['role'], "doctor")

  def test_non_admin_cannot_create_user(self):
    """Doctors/Nurses should NOT be able to create users"""
    # Create a doctor manually
    doctor = User.objects.create_user(username="doc", password="docpass", role="doctor")
    response = self.client.post(reverse('token_obtain_pair'),
        {"username": "doc", "password": "docpass"}, format="json")
    token = response.data['access']

    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    data = {
        "username": "nurse1",
        "email": "nurse@example.com",
        "password": "Nurse123!",
        "password2": "Nurse123!",
        "role": "nurse"
    }
    response = self.client.post("/api/users/create/", data, format="json")
    self.assertEqual(response.status_code, 403)  # Forbidden
