"""Provides utility functions for scraping."""

from recipe.models import Ingredient, Recipe, Appliance, Group, RecipeIngredient
from .errors import UnknownWebsiteError, RecipeParsingError
from urllib.error import URLError
from .scraper_functions import parse, get_batch
from .string_utils import htmlify_list
from threading import Lock

_save_lock = Lock()

def scrape_to_json(url):
    """Scrape a url for a recipe."""
    site_url = url

    results = {'valid': 'False', 'source_url': site_url}

    try:
        parse_results = parse(site_url)

        # Perform union of results
        results = {**results, **parse_results}

        results['valid'] = 'True'
    except (ValueError, URLError) as e:
        results['error'] = 'invalid url: {}'.format(e)
    except (KeyError, AttributeError) as e:
        results['error'] = 'parsing error: {}'.format(e)
    except UnknownWebsiteError as e:
        results['error'] = str(e)
    except RecipeParsingError as e:
        results['error'] = str(e)

    return results

def save(json, user):
    """Save a json recipe to the database."""
    global _save_lock

    if json['valid'] != 'True':
        raise RecipeParsingError('Error in parsing site: {}'.format(json['error']))

    source_url = json['source_url']
    if Recipe.objects.filter(source_url__contains=source_url):
        raise RecipeParsingError('This url has already been parsed')

    title = json['title']
    summary = json['summary']

    if Recipe.objects.filter(title__iexact=title,summary=summary):
        raise RecipeParsingError('A recipe very similar to this has already been parsed: {0}'.format(title))

    instructions = htmlify_list(json['instructions'])
    image_url = json['image_url']
    time = json['time']
    if time:
        time = int(time)
    else:
        time = None
    ingredients = json['ingredients']
    appliances = json['appliances']

    _save_lock.acquire()
    recipe = Recipe.objects.create(title=title, summary=summary, instructions=instructions,
        image_url=image_url, time=time, source_url=source_url, user=user, is_private=False)

    recipe.appliances.add(*_get_appliance_objects(appliances))
    _add_ingredient_objects(ingredients, recipe)
    _save_lock.release()

    return 'Recipe saved'

def scrape_and_save(url, user):
    """Scrape a recipe from a url and then save it to the database."""
    results = scrape_to_json(url)
    return save(results, user)

def _get_appliance_objects(appliances):
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

def _add_ingredient_objects(ingredients, recipe):
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
