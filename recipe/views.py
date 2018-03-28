from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from .models import Recipe, RecipeIngredient, Ingredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet


def index(request):
    """Return the base index page for the site."""
    ingredients = Ingredient.objects.all()
    context = {"ingredients": ingredients}
    return HttpResponse(render(request, 'recipe/index.html', context))


def add_private_recipe(request):
    if(request.method == 'POST'):
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            for ingredient_form in formset:
                if(ingredient_form.has_changed()):
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()
            return redirect('recipe:index')

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {'form': form,
               'formset': formset}
    return HttpResponse(render(request, 'recipe/add_private_recipe.html', context))
