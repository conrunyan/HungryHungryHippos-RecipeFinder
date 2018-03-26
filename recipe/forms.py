from django import forms
from django.contrib.auth.models import User
from django.core import exceptions

from .models import Recipe, RecipeIngredient, Ingredient


class RecipeForm(forms.ModelForm):
    # time = forms.CharField(widget=forms.TextInput(attrs={
    #                        'class': 'form-control', 'placeholder': 'Time HH:MM'}))

    class Meta:
        model = Recipe
        fields = ('title', 'summary', 'difficulty',
                  'time', 'image_url', 'instructions')
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Name'}),
            'summary':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'difficulty':   forms.Select(attrs={'class': 'form-control', 'placeholder': 'Difficulty'}),
            'image_url':    forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Image URL'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instructions'}),
        }

    def is_valid(self):
        valid = super(CreateRecipeForm, self).is_valid()

        return valid


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(widget=forms.Select(attrs={
                                        'class': 'form-control', 'placeholder': 'Ingredient'}),
                                        empty_label='--Ingredient--',
                                        queryset=Ingredient.objects)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'unit', 'amount')
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount (ex: 2 1/2)'}),
            'unit':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (ex: Cups)'})
        }

    def is_valid(self):
        valid = super(AddRecipeIngredientForm, self).is_valid()

        return valid


RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=3)
