"""Holds the views for the index page."""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Ingredient

def index(request):
	"""Return the base index page for the site."""
	ingredients = Ingredient.objects.all();
	context = { "ingredients": ingredients }
	return HttpResponse(render(request, 'recipe/index.html', context))
