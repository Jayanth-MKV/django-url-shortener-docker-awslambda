from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Links

# Home page
# def index(request):
# 	params = {'link': False,'mess': 'Just make sure it\'s a full URL.'}
# 	all_links = Links.objects.all()
# 	params["all_links"] = all_links
# 	return render(request, 'url_shortener/index.html', params)
def index(request):
	query = request.GET.get('searchterm', '')
	params = {'link': False,'mess': 'Just make sure it\'s a full URL.'}

	if query:
		links = Links.objects.filter(url__icontains=query).values('key', 'url')
	else:
		links = Links.objects.all().values('key', 'url')

	params["all_links"] = list(links)
	# context = {'links': list(links)}
	return render(request, 'url_shortener/index.html', params)
	# return render(request, 'index.html', params)