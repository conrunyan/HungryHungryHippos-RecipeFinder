"""Defines errors for the scraper."""

class UnknownWebsiteError(NotImplementedError):
    """Error for if a website has not been implemented yet."""

    pass

class RecipeParsingError(RuntimeError):
    """Error for if the website passed in has an error parsing or doesn't contain the necessary information."""

    def __init__(self, description, saved_url=None):
        """Create a recipe parsing error with the description. The saved url holds the already saved recipe if already scraper."""
        self.description = description
        self.saved_url = saved_url

    def __str__(self):
        """Return a string of the error."""
        return str(self.description)

class IngredientParsingError(RecipeParsingError):
    """Error for if an ingredient cannot be parsed."""
