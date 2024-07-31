from django.http import JsonResponse
from ..models import Links
import random

def random_link(request):
    links = Links.objects.all()
    if links:
        random_link = random.choice(links).url
        return JsonResponse({'link': random_link})
    return JsonResponse({'link': None})