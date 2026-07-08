#!/usr/bin/env python3

from collections.abc import Callable
from typing import Any
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    operator: Callable[..., int] | None = None
    if operation == 'add':
        operator = add
    elif operation == 'multiply':
        operator = mul
    elif operation == 'max':
        operator = max
    elif operation == 'min':
        operator = min
    else:
        print("Unknown operation")
        raise ValueError()
    return reduce(operator, spells)


def partial_enchanter(
        base_enchantment: Callable[[int, str, str], str]
        ) -> dict[str, Callable[[int, str, str], str]]:
    specialized_enchants: dict[str, Callable[[int, str, str], str]] = {
        'fire_enchant': partial(base_enchantment, 50, 'fire'),
        'ice_enchant': partial(base_enchantment, 50, 'ice'),
        'air_enchant': partial(base_enchantment, 50, 'air'),
    }
    return specialized_enchants


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 2) + memoized_fibonacci(n - 1)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def dispatcher(spell: Any) -> str:
        return "Unknown spell type"

    @dispatcher.register(int)
    def _(damage_spell: int) -> str:
        return f"Damage spell: {damage_spell} damage"

    @dispatcher.register(str)
    def _(enchantment: str) -> str:
        return f"Enchantment: {enchantment}"

    @dispatcher.register(list)
    def _(multi_cast: list[Any]) -> str:
        return f"Multi-cast: {len(multi_cast)} spells"

    return dispatcher


def main() -> None:
    print("\nTesting spell reducer...")
    spell_powers = [36, 49, 22, 34, 50, 26]
    for label, op in [
        ('Sum', 'add'),
        ('Product', 'multiply'),
        ('Max', 'max'),
        ('Min', 'min'),
        ('Modulo', 'modulo'),
    ]:
        try:
            print(f"{label}: {spell_reducer(spell_powers, op)}")
        except ValueError:
            pass

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return (
            f"The {target} has been enchanted "
            f"with {element} element of {power} power"
            )
    specialized_enchant: dict[
        str, Callable[..., str]
        ] = partial_enchanter(base_enchantment)
    print(specialized_enchant['fire_enchant']('Goblin'))
    print(specialized_enchant['ice_enchant']('Knight'))
    print(specialized_enchant['air_enchant']('Orc'))

    print("\nTesting memoized fibonacci...")
    for i in [0, 1, 10, 15, 40]:
        print(f"Fib({i}): {memoized_fibonacci(i)}")

    print("\nTesting spell dispatcher...")
    for param in [
        42,
        'fireball',
        ['blizzard', 'tsunami', 'heal'],
        ('Goblin', 'Dragon')
    ]:
        dispatched = spell_dispatcher()
        print(dispatched(param))


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
    except KeyboardInterrupt:
        print("\nProgram interrupted")
