"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.html import escape
from django.contrib.admin.views.decorators import staff_member_required
from urllib.error import URLError
from scraper import parse, get_batch
from .errors import UnknownWebsiteError, RecipeParsingError
from ._utils import htmlify_list
from recipe.models import Ingredient, Recipe, Appliance, Group, RecipeIngredient

def _scrape(url):
    site_url = escape(url)

    results = {'valid': 'False', 'source_url': site_url}

    try:
        parse_results = parse(site_url)

        # Perform union of results
        results = {**results, **parse_results}

        results['valid'] = 'True'
    except (ValueError, URLError):
        results['error'] = 'invalid url'
    except (KeyError, AttributeError) as e:
        results['error'] = 'parsing error: {}'.format(e)
    except UnknownWebsiteError as e:
        results['error'] = str(e)
    except RecipeParsingError as e:
        results['error'] = str(e)

    return results

def _scrape_and_save(url, user):
    results = _scrape(url)
    if results['valid'] != 'True':
        return 'Error in parsing site: {}'.format(results['error'])

    source_url = results['source_url']
    if Recipe.objects.filter(source_url__contains=source_url):
        return 'This url has already been parsed'

    title = results['title']
    summary = results['summary']
    instructions = htmlify_list(results['instructions'])
    image_url = results['image_url']
    time = results['time']
    if time:
        time = int(time)
    else:
        time = None
    ingredients = results['ingredients']
    appliances = results['appliances']

    recipe = Recipe.objects.create(title=title, summary=summary, instructions=instructions,
        image_url=image_url, time=time, source_url=source_url, user=user, is_private=False)

    recipe.appliances.add(*get_appliance_objects(appliances))
    add_ingredient_objects(ingredients, recipe)

    return 'Recipe saved'

@staff_member_required(login_url='login')
def scrape_batch(request, start, end):
    """Scrape and save a batch of recipes based on passed parameters."""
    start = int(start)
    end = int(end)
    if start > end:
        return HttpResponse('Start must be less than end')

    site_url = escape(request.GET.get('url', ''))
    results = []

    try:
        site_list = get_batch(site_url, start, end)

        for site in site_list:
            results.append(_scrape_and_save(site, request.user) + " --- " + site)
    except (URLError) as e:
        return HttpResponse('Invalid url: ' + str(e))
    # except (KeyError, ValueError) as e:
    #     return HttpResponse('Key or Value error: ' + str(e))
    except UnknownWebsiteError as e:
        return HttpResponse('Unknown website: ' + str(e))

    return HttpResponse('Successfully added batch<br/>' + htmlify_list(results))

@staff_member_required(login_url='login')
def scrape_and_display(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    return JsonResponse(_scrape(escape(request.GET.get('url', ''))))

@staff_member_required(login_url='login')
def scrape_and_save(request):
    """Parse a url and save it to the database."""
    return HttpResponse(_scrape_and_save(escape(request.GET.get('url', '')), request.user))

def get_appliance_objects(appliances):
    """Turn a string of appliances into appliance objects and create them if they don't exist."""
    results = []
    for appliance in appliances:
        appliance = appliance.lower()
        obj = Appliance.objects.filter(name__iexact=appliance)
        if obj:
            results.append(obj.first())
        else:
            results.append(Appliance.objects.create(name=appliance))
    return results

def add_ingredient_objects(ingredients, recipe):
    """Turn a list of json objects into Ingredient and RecipeIngredient and create if they don't exist."""
    # Get an uncategorized group
    UNCATEGORIZED_NAME = 'uncategorized'
    group = Group.objects.filter(name__iexact=UNCATEGORIZED_NAME)
    if group:
        group = group.first()
    else:
        group = Group.objects.create(name=UNCATEGORIZED_NAME)

    # Create Ingredients if they don't exist and add them to recipe ingredients
    results = []
    for obj in ingredients:
        name = obj['ingredient'].lower()
        ingredient_filter = Ingredient.objects.filter(name__iexact=name)
        ingredient = None
        if ingredient_filter:
            ingredient = ingredient_filter.first()
        else:
            ingredient = Ingredient.objects.create(name=name, group=group)

        amount = obj['amount']
        unit = obj['unit']

        if not amount:
            amount = None
        if not unit:
            unit = None

        results.append(RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=amount, unit=unit))
    return results
