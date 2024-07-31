from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from ..models import Links
from django.shortcuts import get_object_or_404, redirect

def search_links(request):
    query = request.GET.get('query', '')
    if query:
        links = Links.objects.filter(url__icontains=query).values('key', 'url')
    else:
        links = Links.objects.all().values('key', 'url')

    params = {'link': False,'mess': 'Just make sure it\'s a full URL.'}
    params["links"] = list(links)
    return render(request, 'url_shortener/links.html', params)

def update_link(request, key):
    if request.method == 'POST':
        new_url = request.POST.get('url')
        link = get_object_or_404(Links, key=key)
        link.url = new_url
        link.save()
        return redirect('index')

def delete_link(request, key):
    # Ensure the request is a POST request
    if request.method == 'POST':
        # Get the link object or return 404 if not found
        link = get_object_or_404(Links, key=key)
        # Delete the link
        link.delete()
        # Redirect to the index page
        return redirect('index')
    else:
        # If not a POST request, return a 405 Method Not Allowed response
        print('You are not allowed to ',request.method)
        return HttpResponseNotAllowed(['POST'])
