from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from patients.models import Patient
from heartbeats.models import HeartRate

User = get_user_model()

class HeartRateTests(APITestCase):
  def setUp(self):
      # Create doctor
      self.doctor = User.objects.create_user(username="doc", password="docpass", role="doctor")
      response = self.client.post(reverse('token_obtain_pair'),
          {"username": "doc", "password": "docpass"}, format="json")
      self.doctor_token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

      # Create patient
      self.patient = Patient.objects.create(name="Charlie", medical_id="PAT100", created_by=self.doctor)

  def test_doctor_can_record_heartbeat(self):
      data = {"patient": self.patient.id, "bpm": 85, "recorded_at": "2025-09-18 10:00:00"}
      response = self.client.post("/api/heartbeats/", data, format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.data['bpm'], 85)
      self.assertEqual(response.data['patient'], self.patient.id)

  def test_nurse_cannot_record_heartbeat(self):
      nurse = User.objects.create_user(username="nina", password="nursepass", role="nurse")
      response = self.client.post(reverse('token_obtain_pair'),
          {"username": "nina", "password": "nursepass"}, format="json")
      nurse_token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {nurse_token}')

      data = {"patient": self.patient.id, "bpm": 90, "recorded_at": "2025-09-18 11:00:00"}
      response = self.client.post("/api/heartbeats/", data, format="json")
      self.assertEqual(response.status_code, 403)

  def test_list_heartbeats(self):
      HeartRate.objects.create(patient=self.patient, bpm=78, recorded_at="2025-09-18 09:00:00", recorded_by=self.doctor)
      response = self.client.get("/api/heartbeats/list/?patient=" + str(self.patient.id))
      self.assertEqual(response.status_code, 200)
      self.assertGreaterEqual(len(response.data['results']), 1)
  
  def test_abnormal_flag_behavior(self):
      r = self.client.post('/api/heartbeats/', {'patient': self.patient.id, 'bpm':59, 'recorded_at':'2025-09-18 10:00:00'}, format='json')
      assert r.status_code == 201
      assert r.data['abnormal'] is True

      r2 = self.client.post('/api/heartbeats/', {'patient': self.patient.id, 'bpm':80, 'recorded_at':'2025-09-18 11:00:00'}, format='json')
      assert r2.status_code == 201
      assert r2.data['abnormal'] is False

  def test_summary_computation(self):
      HeartRate.objects.create(patient=self.patient, bpm=70, recorded_at='2025-09-18 09:00:00', recorded_by=self.doctor)
      HeartRate.objects.create(patient=self.patient, bpm=90, recorded_at='2025-09-18 10:00:00', recorded_by=self.doctor)
      resp = self.client.get(f'/api/heartbeats/summary/?patient={self.patient.id}')
      data = resp.json()
      assert data['min_bpm'] == 70
      assert data['max_bpm'] == 90
      assert abs(data['avg_bpm'] - 80.0) < 0.0001
      assert data['latest_bpm'] == 90
