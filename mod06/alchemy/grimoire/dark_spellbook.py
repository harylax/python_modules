def dark_spell_allowed_ingredients() -> list[str]:
    return ['bats', 'frogs', 'arsenic', 'eyeball']


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    from .dark_validator import validate_ingredients
    return (f"Spell recorded: {spell_name} "
            f"({validate_ingredients(ingredients)})")
