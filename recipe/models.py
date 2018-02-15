from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Appliance(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=280, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    DIFFICULTY_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('D', 'Difficult')
    )
    difficulty = models.CharField(max_length=1, null=True, choices=DIFFICULTY_CHOICES)
    time = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    instructions = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    appliances = models.ManyToManyField(Appliance)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    unit = models.CharField(max_length=10, null=True, blank=True)

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=500)

    def __str__(self):
        return "%s : %s".format(self.user, self.recipe[:30])
