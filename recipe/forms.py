from django import forms
from django.contrib.auth.models import User
from django.core import exceptions

from .models import Recipe, RecipeIngredient, Ingredient, Comment

import re


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Recipe
        fields = ('title', 'summary', 'difficulty',
                  'time', 'image_url', 'instructions')
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Name'}),
            'summary':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'difficulty':   forms.Select(attrs={'class': 'form-control', 'placeholder': 'Difficulty'}),
            'time':         forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Time (Minutes)'}),
            'image_url':    forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Image URL'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instructions'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(widget=forms.Select(attrs={
                                        'placeholder': 'Ingredient'}),
                                        empty_label='--Ingredient--',
                                        queryset=Ingredient.objects)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount', 'unit')
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Amount (ex: 2 1/2)'}),
            'unit':   forms.TextInput(attrs={'placeholder': 'Unit (ex: Cups)'}),
        }

    def is_valid(self):
        valid = super(RecipeIngredientForm, self).is_valid()

        return valid


RecipeIngredientFormSet = forms.inlineformset_factory(Recipe, RecipeIngredient,
                        form=RecipeIngredientForm, extra=10, min_num=1, validate_min=True, can_delete=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment'})
        }
