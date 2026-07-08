#!/usr/bin/env python3

from collections.abc import Callable
from functools import wraps
from typing import Any
import time


def spell_timer(func: Callable[..., str]) -> Callable[..., str]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        print(f"Casting {func.__name__}...")
        start: float = time.perf_counter()
        result = func(*args, **kwargs)
        end: float = time.perf_counter()
        print(f"Spell completed in {(end - start):.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable[..., Callable[..., str]]:
    def validate_power_decorator(
            func: Callable[..., str]
            ) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            if 'power' in kwargs:
                power = int(kwargs['power'])
            else:
                if isinstance(args[0], MageGuild):
                    power = int(args[2])
                else:
                    power = int(args[0])

            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return validate_power_decorator


def retry_spell(max_attempts: int) -> Callable[..., Callable[..., str]]:
    def decorator(func: Callable[[int], str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            for i in range(1, max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        "Spell failed, retrying... "
                        f"(attempt {i}/{max_attempts})"
                        )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return (
            len(name) >= 3
            and all(c.isalpha() or c.isspace() for c in name)
        )

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    print("Testing spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.101)
        return "Fireball cast"

    print(f"Result: {fireball()}")

    print("\nTesting power validator...")

    @power_validator(55)
    def blizzard(power: int, target: str) -> str:
        return f"Blizzard cast on {target}, power: {power}"

    print(blizzard(50, 'Dragon'))
    print(blizzard(target='Dragon', power=70))

    print("\nTesting retrying spell...")

    @retry_spell(3)
    def spell(power: int) -> str:
        if power == 10:
            return "Waaaaaaagh spelled !"
        raise Exception()

    print(spell(11))
    print(spell(10))

    print("\nTesting MageGuild...")

    print(MageGuild.validate_mage_name('Joe'))
    print(MageGuild.validate_mage_name('Jo'))

    mage = MageGuild()
    print(mage.cast_spell('Lightning', 15))
    print(mage.cast_spell('Freeze', 5))
