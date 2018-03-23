"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.html import escape
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError

# Create your views here.
def scrape(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    site_url = escape(request.GET.get('url', ''))

    if site_url == '':
        return JsonResponse({'error':'no url specified'})

    try:
        content = urlopen(site_url).read()
        soup = BeautifulSoup(content, "html.parser")
    except (ValueError, URLError) as e:
        return JsonResponse({'error':'invalid url'})

    return JsonResponse({'success':site_url})
