#!/usr/bin/env python3

from collections.abc import Callable


def spell_combiner(
        spell1: Callable[[str, int], str],
        spell2: Callable[[str, int], str]
        ) -> Callable[[str, int], tuple[str, str]]:
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined_spell


def power_amplifier(
        base_spell: Callable[[str, int], str],
        multiplier: int) -> Callable[[str, int], str]:
    def mega_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return mega_spell


def conditional_caster(
        condition: Callable[[int], bool],
        spell: Callable[[str, int], str]) -> Callable[[str, int], str]:
    def new_spell(target: str, power: int) -> str:
        if condition(power):
            return spell(target, power)
        return "Spell fizzled"
    return new_spell


def spell_sequence(
        spells: list[Callable[[str, int], str]]
        ) -> Callable[[str, int], list[str]]:
    def cast_all(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return cast_all


if __name__ == "__main__":
    def heal(target: str, power: int) -> str:
        return f"Heal restores {target} for {power} HP"

    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target} for {power} HP"

    def shield(target: str, power: int) -> str:
        return f"Shield protects {target} for {power} HP"

    def blizzard(target: str, power: int) -> str:
        return f"Blizzard hits {target} for {power} HP"

    print("\nTesting spell combiner...")
    combined = spell_combiner(heal, fireball)
    print(combined('Goblin', 36))

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Knight', 10)},")
    print(f"Amplified: {mega_fireball('Knight', 10)}")

    print("\nTesting conditional caster...")

    def condition(power: int) -> bool:
        return power >= 3
    dependant_spell = conditional_caster(condition, blizzard)
    print(f"Condition satisfied: {dependant_spell('Goblin', 52)}")
    print(f"Condition not satisfied: {dependant_spell('Dragon', 2)}")

    print("\nTesting spell_sequence...")
    sequence = spell_sequence([heal, fireball, shield, blizzard])
    print(sequence('Wizard', 20))
