from .red_spellbook import red_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    lst = ingredients.split()
    lst = [ingredient.strip(', ').lower() for ingredient in lst]
    for ingredient in lst:
        if ingredient in red_spell_allowed_ingredients():
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
