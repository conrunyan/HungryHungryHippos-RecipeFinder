from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^myrecipes/', views.myrecipes_view, name='myRecipes'),
    url(r'^favorites/', views.favorite_recipes, name='favorites'),
    url(r'^profile/', views.profile, name='profile'),
]
