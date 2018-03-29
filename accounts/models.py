"""Tables to extend the user functionality."""

from django.db import models
from django.contrib.auth.models import User
from recipe.models import Ingredient

class PersistentIngredient(models.Model):
    """Holds the current ingredients a user has selected.

    Allows the user's ingredients to persist across searches and sessions.
    """

    # Holds the user to which this ingredient points
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Holds the ingredient this user has selected
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        """Construct a string representation of this ingredient link."""
        return '{0} : {1}'.format(self.user, self.ingredient)
