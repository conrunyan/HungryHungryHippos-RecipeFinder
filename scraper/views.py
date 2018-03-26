"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.html import escape
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from urllib.error import URLError
from scraper import parse
from .errors import UnknownWebsiteError, RecipeParsingError

# Create your views here.
@login_required
def scrape(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    if not request.user.is_staff:
        raise PermissionDenied

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
