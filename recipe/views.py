"""Holds the views for the index page."""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Recipe, RecipeIngredient

def index(request):
	"""Return the base index page for the site."""
	groups = Group.objects.order_by("name")
	ingredientsAreSelected = False
	context = { "groups" : groups , "ingredientsAreSelected" : ingredientsAreSelected}
	return HttpResponse(render(request, 'recipe/index.html', context))

def recipe_full_view(request, id):
    current_recipe = Recipe.objects.get(id = id)
    ingredients = RecipeIngredient.objects.filter(recipe = current_recipe)
    context = {'current_recipe' : current_recipe, 'ingredients' : ingredients}
    return HttpResponse(render(request, 'recipe/recipe_full_view.html', context))
