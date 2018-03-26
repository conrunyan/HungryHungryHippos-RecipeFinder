"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.html import escape
from django.contrib.admin.views.decorators import staff_member_required
from urllib.error import URLError
from scraper import parse
from .errors import UnknownWebsiteError, RecipeParsingError

@staff_member_required(login_url='login')
def scrape_site(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    site_url = escape(request.GET.get('url', ''))

    results = {'valid': 'false', 'source_url': site_url}

    try:
        parse_results = parse(site_url)

        # Perform union of results
        results = {**results, **parse_results}

        results['valid'] = 'true'
    except (ValueError, URLError):
        results['error'] = 'invalid url'
    except UnknownWebsiteError as e:
        results['error'] = str(e)
    except RecipeParsingError as e:
        results['error'] = str(e)

    return JsonResponse(results)

@staff_member_required(login_url='login')
def scrape_and_save(request):
    """Parse a url and save it to the database."""
    return JsonResponse({})
