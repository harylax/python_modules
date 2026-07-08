#!/usr/bin/env python3

from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count: int = 0

    def call_count() -> int:
        nonlocal count
        count += 1
        return count
    return call_count


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power: int = initial_power

    def accumulate(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power
    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchanted_item(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchanted_item


def memory_vault() -> dict[str, Callable[..., Any]]:
    memory: dict[Any, Any] = {}

    def store(key: Any | None = None, value: Any | None = None) -> None:
        if not key or not value:
            return
        memory[key] = value

    def recall(key: Any | None) -> Any:
        if key in memory:
            return memory[key]
        return "Memory not found"

    return {
        'store': store,
        'recall': recall
    }


if __name__ == "__main__":
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    for i in range(1, 3):
        print(f"counter_a call {i}: {counter_a()}")
    for i in range(1, 2):
        print(f"counter_b call {i}: {counter_b()}")

    print("\nTesting spell accumulator...")
    initial_power: int = 100
    accumulator = spell_accumulator(initial_power)
    print(f"Base: {initial_power}, add 20: {accumulator(20)}")
    print(f"Base: {initial_power}, add 30: {accumulator(30)}")

    print("\nTesting enchantment factory...")
    flaming_sword = enchantment_factory("Flaming")
    print(flaming_sword("Sword"))
    frozen_shield = enchantment_factory("Frozen")
    print(flaming_sword("Shield"))

    print("\nTesting memory vault...")
    print("Store 'secret' = 42")
    vault = memory_vault()
    vault['store']('secret', 42)
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
