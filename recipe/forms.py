from django import forms
from django.contrib.auth.models import User
from django.core import exceptions

from .models import Recipe, RecipeIngredient, Ingredient, Comment

import re


class RecipeForm(forms.ModelForm):
    time = forms.CharField(widget=forms.TextInput(attrs={
                           'class': 'form-control', 'placeholder': 'Time (Hours:Minutes)'}))

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

    def clean_time(self):
        time = self.cleaned_data['time']
        time_re = re.compile(r'(\d*):?(\d*)')
        hourmin = time_re.match(time)

        hours = 0
        mins = 0
        if hourmin.group(1) != "":
            hours = int(hourmin.group(1))
        if hourmin.group(2) != "":
            mins = int(hourmin.group(2))
        time = hours * 60 + mins
        if(time == 0):
            vaild = False
            self.add_error(
                'time', 'You must enter a valid non-zero time! (Hours:Minutes)')
#            ValidationError(_('Invalid value'), code='invalid')

        return time

    def is_valid(self):
        valid = super(RecipeForm, self).is_valid()

        return valid


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