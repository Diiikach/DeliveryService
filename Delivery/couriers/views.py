from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from couriers.services import logic


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def create_couriers(request):
    json, status_code = logic.import_couriers(request.body)
    return HttpResponse(content=json, status=status_code, content_type='application/json',)


@require_http_methods(['PATCH', 'GET'])
def get_courier(request):
    pass

