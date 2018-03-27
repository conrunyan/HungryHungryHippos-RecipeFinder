"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.html import escape
from django.contrib.admin.views.decorators import staff_member_required
from urllib.error import URLError
from scraper import parse
from .errors import UnknownWebsiteError, RecipeParsingError
from ._utils import htmlify_list
from recipe.models import Ingredient, Recipe, Appliance, Group, RecipeIngredient

def _scrape(request):
    site_url = escape(request.GET.get('url', ''))

    results = {'valid': 'False', 'source_url': site_url}

    try:
        parse_results = parse(site_url)

        # Perform union of results
        results = {**results, **parse_results}

        results['valid'] = 'True'
    except (ValueError, URLError):
        results['error'] = 'invalid url'
    except UnknownWebsiteError as e:
        results['error'] = str(e)
    except RecipeParsingError as e:
        results['error'] = str(e)

    return results


@staff_member_required(login_url='login')
def scrape_and_display(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    return JsonResponse(_scrape(request))

@staff_member_required(login_url='login')
def scrape_and_save(request):
    """Parse a url and save it to the database."""
    results = _scrape(request)

    if results['valid'] != 'True':
        return HttpResponse('Error in parsing site.')

    source_url = results['source_url']
    if Recipe.objects.filter(source_url__contains=source_url):
        return HttpResponse('This url has already been parsed')

    title = results['title']
    summary = results['summary']
    instructions = htmlify_list(results['instructions'])
    image_url = results['image_url']
    time = results['time']
    if time:
        time = int(time)
    ingredients = results['ingredients']
    appliances = results['appliances']

    user = request.user

    recipe = Recipe.objects.create(title=title, summary=summary, instructions=instructions,
        image_url=image_url, time=time, source_url=source_url, user=user, is_private=False)

    recipe.appliances.add(*get_appliance_objects(appliances))
    add_ingredient_objects(ingredients, recipe)

    return HttpResponse('Recipe saved')

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
