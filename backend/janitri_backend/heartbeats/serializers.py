from rest_framework import serializers
from .models import HeartRate


class HeartRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = HeartRate
    fields = '__all__'
    read_only_fields = ('created_at','recorded_by')