from django.shortcuts import render
from ..models import Links



# Requesting URL corresponding a key
def getURL(request , key):
	try:
		obj = Links.objects.get(key = key)
		return render(request, 'url_shortener/middle.html', {'seconds': 5, 'url': obj.url})
	except:
		return render(request, 'url_shortener/index.html', {'link': False, 'mess': 'Sorry, I couldn\'t find it.'})
