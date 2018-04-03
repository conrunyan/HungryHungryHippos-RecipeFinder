"""Holds the views for the index page."""

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from accounts.models import PersistentIngredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet
from .ingredient_functions import save_ingredients_to_user, get_ingredient_objs_of_user, get_ingredient_names
from .models import Group, Recipe, RecipeIngredient, IngredientUtils, Ingredient


def index(request):
    """Return the base index page for the site."""
    groups = Group.objects.order_by("name")
    group_dict = {}
    for group in groups:
        ing_list = list(group.ingredient_set.all().order_by("name"))
        group_dict[group.name] = ing_list

    ingredientsAreSelected = False
    ingredients = Ingredient.objects.order_by("name")

    persistent_ingredients = []
    if request.user and not request.user.is_anonymous():
        persistent_ingredients = get_ingredient_objs_of_user(request.user)
        persistent_ingredients = get_ingredient_names(persistent_ingredients)

    context = {"groups": groups, "group_dict": group_dict, "ingredientsAreSelected": ingredientsAreSelected,
               "persistent_ingredients": persistent_ingredients, "ingredients_list": ingredients}
    return HttpResponse(render(request, 'recipe/index.html', context))


@csrf_exempt
def get_recipes(request):
    """Get a JSON object of recipes from the search algorithm."""
    if not request.body:
        return JsonResponse({})

    # parse json string to list of ingredient names
    ing = request.body.decode("utf-8")
    ingredients_to_search_by = ing[1:-1].replace('"', "").split(',')
    # save ingredients for the future
    if request.user and not request.user.is_anonymous():
        save_ingredients_to_user(request.user, ingredients_to_search_by)
    # send ingredients to search algorithm
    found_recipes = IngredientUtils().find_recipes(ingredients_to_search_by)
    # convert queryset to JSON!!!
    values = found_recipes.values()
    return JsonResponse({'results': list(values)})


def recipe_full_view(request, id):
    """Return the full view of a recipe."""
    current_recipe = get_object_or_404(Recipe, id=id)
    if current_recipe.is_private and current_recipe.user != request.user:
        raise PermissionDenied
    ingredients = RecipeIngredient.objects.filter(recipe=current_recipe)
    context = {'current_recipe': current_recipe, 'ingredients': ingredients}
    return HttpResponse(render(request, 'recipe/recipe_full_view.html', context))


@login_required
def add_private_recipe(request):
    """Create a view with a form for adding a recipe."""
    if(request.method == 'POST'):
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
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
