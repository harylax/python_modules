from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    count: int = 0

    def call_count() -> int:
        nonlocal count
        count += 1
        return count
    return call_count


def spell_accumulator(initial_power: int) -> Callable:
    total_power: int = initial_power

    def accumulate(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power
    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def the_item(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return the_item


def memory_vault() -> dict[str, Callable]:
    memory: dict[Any, Any] = {}

    def store(key: Any, value: Any) -> None:
        nonlocal memory
        memory[key] = value

    def recall(key: Any) -> str:
        value = memory.get(key, None)
        return value if value else 'Memory not found'
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
    total_power = spell_accumulator(100)
    print(f"Base {100}, add 20: {total_power(20)}")
    print(f"Base {100}, add 30: {total_power(30)}")

    print("\nTesting enchantment factory...")
    enchanted_item_1 = enchantment_factory("Flaming")
    print(enchanted_item_1("Sword"))
    enchanted_item_2 = enchantment_factory("Frozen")
    print(enchanted_item_2("Shield"))

    print("\nTesting memory vault...")
    memory = memory_vault()
    print("Store 'secret' = 42")
    memory['store']('secret', 42)
    print(f"Recall 'secret': {memory['recall']('secret')}")
    print(f"Recall 'unknown': {memory['recall']('unknown')}")
