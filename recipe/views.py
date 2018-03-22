"""Holds the views for the index page."""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Group

def index(request):
	"""Return the base index page for the site."""
	groups = Group.objects.order_by("name")
	context = { "groups" : groups }
	return HttpResponse(render(request, 'recipe/index.html', context))
