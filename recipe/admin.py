from django.contrib import admin

from . import models

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'time', 'creation_date')

admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Ingredient)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.Appliance)
admin.site.register(models.Comment)
admin.site.register(models.Group)
