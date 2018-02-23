"""Holds the routing information for the recipe app."""

from django.conf.urls import url

from . import views

app_name = "recipe"
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
