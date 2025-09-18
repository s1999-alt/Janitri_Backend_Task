from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from patients.models import Patient

User = get_user_model()

class PatientTests(APITestCase):
  def setUp(self):
      # Create doctor user
      self.doctor = User.objects.create_user(username="doc", password="docpass", role="doctor")
      response = self.client.post(reverse('token_obtain_pair'),
          {"username": "doc", "password": "docpass"}, format="json")
      self.doctor_token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

  def test_doctor_can_create_patient(self):
      """Doctors can add patients"""
      data = {
          "name": "Alice",
          "age": 30,
          "gender": "F",
          "medical_id": "PAT001"
      }
      response = self.client.post("/api/patients/", data, format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.data['name'], "Alice")
      self.assertEqual(response.data['created_by'], self.doctor.id)

  def test_nurse_cannot_create_patient(self):
      """Nurses should not be allowed to add patients"""
      # Create nurse
      nurse = User.objects.create_user(username="nina", password="nursepass", role="nurse")
      response = self.client.post(reverse('token_obtain_pair'),
          {"username": "nina", "password": "nursepass"}, format="json")
      nurse_token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {nurse_token}')

      data = {"name": "Bob", "age": 40, "gender": "M", "medical_id": "PAT002"}
      response = self.client.post("/api/patients/", data, format="json")
      self.assertEqual(response.status_code, 403)

  def test_list_patients(self):
      """All authenticated roles can view patient list"""
      Patient.objects.create(name="Test Patient", medical_id="PAT003", created_by=self.doctor)
      response = self.client.get("/api/patients/")
      self.assertEqual(response.status_code, 200)
      self.assertGreaterEqual(len(response.data['results']), 1)