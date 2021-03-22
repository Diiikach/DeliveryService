from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def create_couriers(request):
    pass


@require_http_methods(['PATCH', 'GET'])
def get_courier(request):
    pass

