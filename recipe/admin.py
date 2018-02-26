"""Configures the display of recipe app components in the admin app."""

from django.contrib import admin
from django import forms

from . import models


class RecipeIngredientInline(admin.TabularInline):
    """Allows adding ingredients directly to recipe."""

    model = models.RecipeIngredient
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    """Defines the display of recipe attributes in the admin app."""

    list_display = ('title', 'user', 'difficulty', 'time', 'creation_date')
    filter_horizontal = ('appliances',)
    inlines = (RecipeIngredientInline,)


class RecipeIngredientAdmin(admin.ModelAdmin):
    """Defines the display of recipe-ingredient attributes in the admin app."""

    list_display = ('recipe', 'ingredient', 'amount', 'unit')


class CommentModelForm(forms.ModelForm):
    """Defines the display of Comments in the admin app.

    This changes the default html element for the content to be a textarea.
    """

    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        """This class is required for Django."""

        model = models.Comment
        fields = '__all__'


class CommentAdmin(admin.ModelAdmin):
    """Defines the display of comments in the admin app."""

    list_display = ('recipe', 'user', 'creation_date')
    form = CommentModelForm


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Ingredient)
admin.site.register(models.RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(models.Appliance)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Group)
