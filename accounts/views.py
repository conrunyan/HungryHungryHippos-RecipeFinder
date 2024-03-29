from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from emailauth import models as EA_models

from .forms import CreateUserForm, LoginForm
from emailauth.views import sendAuthEmail
from recipe.models import Recipe, RecipeIngredient, Favorite


def login_view(request):
    """View for when the user goes to the login page."""
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipe:index')
            else:
                form.add_error(None, 'Invalid Username/Password')

    else:
        form = LoginForm()

    context = {'form': form}
    return HttpResponse(render(request, 'accounts/login.html', context))


def register_view(request):
    """View for when the user goes to the creating account page."""
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            cur_usr = User.objects.create_user(user_name, email, password)
            # adding creation of email_authentication/user relationship step
            # TODO: add EmailAuth creation step, called from models.py
            EA_models.makeEmailAuth(cur_usr, False)

            success_context = {'user_name': user_name, 'email': email}
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
            else:
                form.add_error(None, 'Failed to create account')
                context = {'form': form}
                return HttpResponse(render(request, 'accounts/register.html', context))
            # adding authentication email step call
            sendAuthEmail(email)
            return render(request, 'accounts/register_successful.html', success_context)

    else:
        form = CreateUserForm()

    context = {'form': form}
    return HttpResponse(render(request, 'accounts/register.html', context))


def logout_view(request):
    """View for when the user logs out."""
    logout(request)
    response = redirect('recipe:index')
    response.user = request.user
    return response

@login_required
def myrecipes_view(request):
    """View for when the user goes to the My Recipes page."""
    my_recipes = Recipe.objects.filter(user=request.user)
    context = {"my_recipes" : my_recipes}
    return HttpResponse(render(request, 'recipe/myRecipes.html', context))

@login_required
def favorite_recipes(request):
    """View for the Favorites page."""
    favorites = Favorite.objects.filter(user=request.user)
    
    context = {"favorites" : favorites}
    return HttpResponse(render(request, 'recipe/favorites.html', context))

@login_required
def profile(request):
    """View for when the user goes to the Profile page."""
    user = User.objects.get(username=request.user)
    users_recipes = Recipe.objects.filter(user=request.user)[:3]
    users_favorites = Favorite.objects.filter(user=request.user)[:3]
    context = { 'user' : user, 'users_recipes' : users_recipes, 'users_favorites' : users_favorites}
    return HttpResponse(render(request, 'accounts/profile.html', context))
