from ex0.creature_factory import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    base.describe()
    print(base.attack())
    evolved.describe()
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    print("Testing battle")
    base1 = factory1.create_base()
    base2 = factory2.create_base()
    base1.describe()
    print(" vs.")
    base2.describe()
    print(" fight!")
    print(base1.attack())
    print(base2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    try:
        test_factory(flame_factory)
        print()
        test_factory(aqua_factory)
        print()
        test_battle(flame_factory, aqua_factory)
    except Exception as err:
        print(f"Unexpected error: {err}")
