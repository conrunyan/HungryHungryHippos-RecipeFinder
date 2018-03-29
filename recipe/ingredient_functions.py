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
    user_persistent_ingredients = PersistentIngredient.objects.filter(user=user)
    saved_ingredients = Ingredient.objects.filter(id__in=user_persistent_ingredients.values('ingredient_id'))

    ingredients_to_delete = saved_ingredients.difference(submitted_ingredients)
    ingredients_to_add = submitted_ingredients.difference(saved_ingredients)

    ingredients_to_delete.delete()
    for ingredient in ingredients_to_add:
        PersistentIngredient.objects.create(user=user, ingredient=ingredient)
