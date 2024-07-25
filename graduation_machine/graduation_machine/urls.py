from django.urls import path, include
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def preflight_options(request, *args, **kwargs):
    response = JsonResponse({"message": "CORS preflight options successful."})
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE, PATCH'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

schema_view = get_schema_view(
   openapi.Info(
      title="graduation_machine API",
      default_version='v1',
      description="graduation_machine API 문서",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@graduation.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url='https://dongguk-cse-graduationcheck.site/',
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('graduation_check.urls')),
]

urlpatterns += [
    path('api/v1/<path:path>', preflight_options),
]
