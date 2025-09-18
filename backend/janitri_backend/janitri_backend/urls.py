from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/heartbeats/', include('heartbeats.urls')),
]
