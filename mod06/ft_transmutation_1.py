import alchemy.transmutation
# non expose, besoin de import lead_to_gold from .recipes dans __init__


if __name__ == "__main__":
    print("=== Transmutation 1 ===")
    print("Import transmutation module directly")
    print(f"Testing lead to gold: {alchemy.transmutation.lead_to_gold()}")
