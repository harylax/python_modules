from ex0 import CreatureFactory as Ex0Factory, FlameFactory, AquaFactory
from ex1 import (
    CreatureFactory as Ex1Factory,
    HealingCreatureFactory, TransformCreatureFactory
    )
from ex2 import (
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy
)

CreatureFactory = Ex0Factory | Ex1Factory


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            opponent1, strategy1 = opponents[i]
            creature1 = opponent1.create_base()
            opponent2, strategy2 = opponents[j]
            creature2 = opponent2.create_base()
            print()
            print("* Battle *")
            creature1.describe()
            print(" vs.")
            creature2.describe()
            print(" now fight!")
            try:
                strategy1.act(creature1)
                strategy2.act(creature2)
            except InvalidStrategyError as err:
                print(f"Battle error, aborting tournament: {err}")
                return


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame_factory, normal), (healing_factory, defensive)])

    print()
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame_factory, aggressive), (healing_factory, defensive)])

    print()
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([
        (aqua_factory, normal),
        (healing_factory, defensive),
        (transform_factory, aggressive)
        ])
