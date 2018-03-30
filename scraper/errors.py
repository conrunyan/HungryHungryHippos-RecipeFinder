"""Defines errors for the scraper."""

class UnknownWebsiteError(NotImplementedError):
    """Error for if a website has not been implemented yet."""

    pass

class RecipeParsingError(RuntimeError):
    """Error for if the website passed in has an error parsing or doesn't contain the necessary information."""

    pass

class IngredientParsingError(RecipeParsingError):
    """Error for if an ingredient cannot be parsed."""
