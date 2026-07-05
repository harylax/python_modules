from collections.abc import Callable


def shield(target: str, power: int) -> str:
    return f"Shield protects {target} for {power} HP"


def flash(target: str, power: int) -> str:
    return f"Flash hits {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified_spell


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def new_spell(target: str, power: int) -> str:
        return (
            'Spell fizzled'
            if 'Dragon' in condition(target, power)
            else spell(target, power)
        )
    return new_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    def cast_spells(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return cast_spells


if __name__ == "__main__":
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    print(f"Combined spell result: {' - '.join(combined("Dragon", 19))}")

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(
        f"Original: {fireball("Goblin", 10)}, "
        f"Amplified: {mega_fireball("Goblin", 10)}"
        )

    print("\nTesting conditionalcaster...")
    conditional = conditional_caster(shield, flash)
    print(f"Condition is True: {conditional("Knight", 9)}")
    print(f"Condition fails: {conditional("Dragon", 100)}")

    print("\nTesting spell sequence...")
    sequence = spell_sequence([heal, shield, fireball, flash])
    print(f"List of all spell results: {' - '.join(sequence("Wizard", 12))}")
