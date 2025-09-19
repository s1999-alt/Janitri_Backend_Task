from rest_framework import serializers
from .models import HeartRate


class HeartRateSerializer(serializers.ModelSerializer):
  abnormal = serializers.SerializerMethodField()

  class Meta:
    model = HeartRate
    fields = ['id', 'patient', 'bpm', 'recorded_at', 'created_at', 'recorded_by', 'abnormal']
    read_only_fields = ('created_at','recorded_by')

  def get_abnormal(self, obj):
    return obj.bpm < 60 or obj.bpm > 100