import django_filters
from .models import HeartRate


class HeartRateFilter(django_filters.FilterSet):
  from_date = django_filters.IsoDateTimeFilter(field_name="recorded_at", lookup_expr='gte')
  to_date = django_filters.IsoDateTimeFilter(field_name="recorded_at", lookup_expr='lte')

  class Meta:
    model = HeartRate
    fields = ['patient', 'from_date', 'to_date']