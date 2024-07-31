from django.shortcuts import render
from ..models import Links

import re
import base64, os


def generate_key(length: int = 16) -> str:
    """
    Generates a random string encoded in Base64 URL-safe format.

    Args:
    - length (int): The desired length of the random bytes before encoding.

    Returns:
    - str: A random string encoded in Base64 URL-safe format.
    """
	
    # Generate random bytes of specified length
    random_bytes = os.urandom(length)
	
    # Encode these bytes into a Base64 URL-safe string and remove any '=' padding
    random_string = base64.urlsafe_b64encode(random_bytes).decode().rstrip('=')

    return random_string



def is_valid_url(url):
	url_pattern = re.compile(
		r'^(https?:\/\/)?'  # optional scheme
		r'((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|'  # domain
		r'((\d{1,3}\.){3}\d{1,3}))'  # or ip
		r'(\:\d+)?(\/[-a-z\d%_.~+]*)*'  # optional port and path
		r'(\?[;&a-z\d%_.~+=-]*)?'  # optional query string
		r'(\#[-a-z\d_]*)?$', re.IGNORECASE)  # optional fragment
	return re.match(url_pattern, url) is not None


# Creating a new URL shortened key
def createLink(request):
	url = request.GET.get('url')
	try:
		key = Links.objects.get(url = url).key
		params = {'link': True , 'key': key}
		all_links = Links.objects.all()
		params["all_links"] = all_links
	except:
		if (is_valid_url(url)):
			key = generate_key(3)
			Links(key = key , url = url).save()
			params = {'link': True , 'key': key}
		else:
			params = {'link': False, 'snuck': True}
	all_links = Links.objects.all()
	params["all_links"] = all_links
	return render(request, 'url_shortener/index.html', params)
