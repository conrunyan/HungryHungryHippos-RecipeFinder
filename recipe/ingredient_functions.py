"""Holds functions to do with the ingredients."""

from .models import Ingredient
from accounts.models import PersistentIngredient

def get_ingredient_obj(name):
    """Try to get the ingredient object associate with this name.

    Matches the name exactly, ignoring case. Return None if the ingredient does not exist.
    """
    try:
        return Ingredient.objects.get(name__iexact=name)
    except:
        return None

def get_ingredient_objs(names):
    """Try to get the ingredient objects associate with the names.

    Matches each name exactly, ignoring case. Set object to None if the ingredient does not exist.
    Return a set of ingredient objects.
    """
    results = {}

    for name in names:
        obj = get_ingredient_obj(name)
        if obj:
            results.append(obj)

    return results

def save_ingredients_to_user(user, ingredients):
    """Update the user's persistent ingredients.

    If an ingredient in the database is not found in 'ingredients', then it is removed from the database.
    """
    submitted_ingredients = Ingredient.objects.filter(name__in=ingredients)
    saved_ingredients = get_ingredient_objs_of_user(user)

    ingredients_to_delete = saved_ingredients.difference(submitted_ingredients)
    ingredients_to_add = submitted_ingredients.difference(saved_ingredients)

    for ingredient in ingredients_to_delete:
        PersistentIngredient.objects.get(ingredient=ingredient).delete()
    for ingredient in ingredients_to_add:
        PersistentIngredient.objects.create(user=user, ingredient=ingredient)

def get_ingredient_objs_of_user(user):
    """Return a QuerySet of Ingredients that are saved by the user."""
    user_persistent_ingredients = PersistentIngredient.objects.filter(user=user)
    return Ingredient.objects.filter(id__in=user_persistent_ingredients.values('ingredient_id'))

def get_ingredient_names(ingredients):
    """Return a list of ingredient names from a queryset."""
    return list(ingredients.values_list('name', flat=True))
