from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/graduation-check/', include('graduation_check.urls')),
]
