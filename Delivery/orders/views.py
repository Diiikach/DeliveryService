from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.services import logic


@csrf_exempt
@require_http_methods(['POST'])
def create_orders(request):
    content, status_code = logic.import_orders(request.body)
    return HttpResponse(status=status_code, content=content, content_type='application/json')


@csrf_exempt
@require_http_methods(['POST'])
def assign_orders(reqeust):
    content, status_code = logic.assign_orders(reqeust.body)
    return HttpResponse(status=status_code, content=content, content_type='application/json')


@csrf_exempt
@require_http_methods(['POST'])
def complete_order(request):
    pass
