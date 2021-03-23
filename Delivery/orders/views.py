from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse


@require_http_methods(['GET'])
def create_orders(request):
    return HttpResponse(content='{"maria": 21}', content_type='application/json', status=201)


@require_http_methods(['POST'])
def assign_orders(reqeust):
    pass


@require_http_methods(['POST'])
def complete_order(request):
    pass
