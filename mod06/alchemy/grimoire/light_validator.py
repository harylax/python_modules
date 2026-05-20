from .light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    lst = ingredients.split()
    lst = [ingredient.strip(', ').lower() for ingredient in lst]
    lst.remove('and')
    for ingredient in lst:
        if ingredient in light_spell_allowed_ingredients():
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
