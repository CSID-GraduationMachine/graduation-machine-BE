from .services.graduation_check_service import GraduationCheckService
from rest_framework import views, response
from django.http import JsonResponse

class GraduationCheckAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        year = self.request.query_params.get('year')
        tech = self.request.query_params.get('tech')
        excel_file = request.FILES.get('file')

        if not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'error': 'File is not xlsx format'}, status=400)
        
        return response.Response({"success": True, "data": GraduationCheckService().check_graduation(year, tech, excel_file), "error": None})