from django.conf import settings
from django.http import JsonResponse

from django.conf import settings

DEBUG = settings.DEBUG

class APIKeyMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        if request.method == "OPTIONS":

            return self.get_response(request)

        public_paths = ['/admin']
        public_add = ['/api/v1/', '/api/v1/schema', '/api/v1/schema/swagger-ui/']

        if DEBUG:

            public_paths.extend(public_add)

        if any(request.path.startswith(p) for p in public_paths):

            return self.get_response(request)

        api_key = request.headers.get('X-API-Key')

        if not api_key:

            return JsonResponse(
                {'error': 'Acesso negado: API Key não fornecida'},
                status=403
            )

        if api_key != settings.API_KEY:
            
            return JsonResponse(
                {'error': 'Acesso negado: API Key inválida'},
                status=403
            )

        return self.get_response(request)
