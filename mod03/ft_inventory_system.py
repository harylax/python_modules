import sys


def parse_input() -> dict[str, int]:
    inventory = {}
    for arg in sys.argv[1:]:
        parts = arg.split(':', 1)
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue
        if parts[0] in inventory:
            print(f"Redundant item '{parts[0]}' - discarding")
            continue
        try:
            inventory[parts[0]] = int(parts[1])
        except ValueError as err:
            print(f"Quantity error for '{parts[0]}': {err}")
    return inventory


def inventory_system_analysis() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_input()
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(
        f"Total quantity of the {len(inventory)} items: "
        f"{sum(inventory.values())}"
        )
    for item in inventory:
        percent = (inventory[item] / sum(inventory.values())) * 100
        print(f"Item {item} represents {round(percent, 1)}%")
    for item in inventory:
        if inventory[item] == max(inventory.values()):
            print(
                f"Item most abundant: {item} "
                f"with quantity {inventory[item]}"
                )
            break
    for item in inventory:
        if inventory[item] == min(inventory.values()):
            print(
                f"Item least abundant: {item} "
                f"with quantity {inventory[item]}"
                )
            break
    inventory.update({'magic_item': 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    try:
        inventory_system_analysis()
    except Exception as err:
        print(f"Error: {err}")
