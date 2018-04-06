from django.contrib import admin

from . import models

# Register your models here.
class PersistentIngredientAdmin(admin.ModelAdmin):
    """Defines the display of persistent ingredients in the admin app."""

    list_display = ('user', 'ingredient')

admin.site.register(models.PersistentIngredient, PersistentIngredientAdmin)
