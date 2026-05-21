from abc import ABC, abstractmethod


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target) -> None:
        pass


class TransformCapability(ABC):
    