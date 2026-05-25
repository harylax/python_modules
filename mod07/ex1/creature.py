from ex0.creature import Creature
from .capabilities import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        self.name = "Sproutling"
        self.type = "Grass"

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    def __init__(self) -> None:
        self.name = "Bloomelle"
        self.type = "Grass/Fairy"

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        return f"{self.name} heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        TransformCapability.__init__(self)
        self.name = "Shiftling"
        self.type = "Normal"

    def attack(self) -> str:
        if self.status:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self.status = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self.status = False
        return f"{self.name} returns to normal."


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        TransformCapability.__init__(self)
        self.name = "Morphagon"
        self.type = "Normal/Dragon"

    def attack(self) -> str:
        if self.status:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self.status = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.status = False
        return f"{self.name} stabilizes its form."
