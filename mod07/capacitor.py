from ex1 import HealingCreatureFactory, TransformCreatureFactory


def test_healing_factory() -> None:
    print("Testing Creature with healing capability")
    hf = HealingCreatureFactory()
    print(" base:")
    base = hf.create_base()
    base.describe()
    print(base.attack())
    print(base.heal())
    print(" evolved:")
    evolved = hf.create_evolved()
    evolved.describe()
    print(evolved.attack())
    print(evolved.heal())


def test_transforming_factory() -> None:
    print("Testing Creature with transform capability")
    tf = TransformCreatureFactory()
    print(" base:")
    base = tf.create_base()
    base.describe()
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print(" evolved:")
    evolved = tf.create_evolved()
    evolved.describe()
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    try:
        test_healing_factory()
        print()
        test_transforming_factory()
    except Exception as err:
        print(f"Unexpected error: {err}")
