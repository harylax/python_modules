from .red_validator import validate_ingredients


def red_spell_record(spell_name: str, ingredients: str) -> str:
    return (f"Spell recorded: {spell_name} "
            f"({validate_ingredients(ingredients)})")
