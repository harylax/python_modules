from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self) -> None:
        self.name: str = "Unknown"
        self.type: str = "Standard"

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> None:
        print(f"{self.name} is a {self.type} type Creature")


class Flameling(Creature):
    def __init__(self) -> None:
        self.name = "Flameling"
        self.type = "Fire"

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        self.name = "Pyrodon"
        self.type = "Fire/Flying"

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self) -> None:
        self.name = "Aquabub"
        self.type = "Water"

    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    def __init__(self) -> None:
        self.name = "Torragon"
        self.type = "Water"

    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"
