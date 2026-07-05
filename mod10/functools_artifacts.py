from collections.abc import Callable
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    op_dict: dict[str, Callable[[int, int], int]] = {
        'add': add,
        'multiply': mul,
        'max': max,
        'min': min
    }
    try:
        op = op_dict[operation]
    except KeyError:
        print(f"Unknwon operation: {operation}")
        exit(1)
    return reduce(op, spells)

def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    pass

def memoized_fibonacci(n: int) -> int:
    pass

def spell_dispatcher() -> Callable[[Any], str]:
    pass


if __name__ == "__main__":
    print("\nTesting spell reducer...")
    print(f"Sum: {spell_reducer([17, 16, 44, 33, 29, 29], 'add')}")
    print(f"Product: {spell_reducer([17, 16, 44, 33, 29, 29], 'multiply')}")
    print(f"Max: {spell_reducer([17, 16, 44, 33, 29, 29], 'max')}")
    print(f"Min: {spell_reducer([17, 16, 44, 33, 29, 29], 'min')}")
    print(f"Min: {spell_reducer([17, 16, 44, 33, 29, 29], 'modulo')}")
