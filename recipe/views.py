"""Holds the views for the index page."""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Group, Recipe, RecipeIngredient
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def index(request):
	"""Return the base index page for the site."""
	groups = Group.objects.order_by("name")
	ingredientsAreSelected = False
	context = { "groups" : groups , "ingredientsAreSelected" : ingredientsAreSelected}
	return HttpResponse(render(request, 'recipe/index.html', context))

@login_required
def recipe_full_view(request, id):
	current_recipe = get_object_or_404(Recipe, id = id)
	if current_recipe.user != request.user:
		raise PermissionDenied
	ingredients = RecipeIngredient.objects.filter(recipe = current_recipe)
	context = {'current_recipe' : current_recipe, 'ingredients' : ingredients}
	return HttpResponse(render(request, 'recipe/recipe_full_view.html', context))
