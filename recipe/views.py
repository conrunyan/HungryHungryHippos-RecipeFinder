from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet


def index(request):
    context = {}
    return HttpResponse(render(request, 'recipe/index.html', context))


def add_private_recipe(request):
    inlineformset = RecipeIngredientFormSet()
    if(request.method == 'POST'):
        form = RecipeForm(request.POST)
        formset = RecipeIngredientForm(request.POST)

        if formset.is_valid():
            if form.is_valid():
                recipe = form.save(commit=False)
                for form in formset:
                    form.save()
                    recipe.ingredient.add(form)

                return redirect('recipe:index')

    else:
        form = RecipeForm()
        formset = RecipeIngredientForm()

    context = {'form': form,
               'formset': formset}
    return HttpResponse(render(request, 'recipe/add_private_recipe.html', context))
