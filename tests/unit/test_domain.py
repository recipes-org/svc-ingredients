from recipes.domain import RecipeInDB


def test_recipe_in_db_eq_not_implemented() -> None:
    """Comparing `RecipeInDB` to anything except another `RecipeInDB` is not
    implemented.

    Python docs recommend returning `NotImplemented` for special methods, such
    as, `__eq__` that might be used in a list comprehension.
    `NotImplemented` is `False`.
    """
    assert not RecipeInDB(name="", id="", requirements=[]) == 2
