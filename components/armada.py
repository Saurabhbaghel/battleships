from pydantic import BaseModel, field_validator, Field
from enum import Enum
from utils.configs import (
    ALPHABETS, VESSELS, VesselSize
)
from components.grid import Position


class Orientation(Enum):
    East = 0
    North = 1
    West = 2
    South = 3


class Vessel:
    def __init__(self,
                 name: str | None = None,
                 pos: Position | None = None):
        self.vessel_type = "Battleship"
        self.name = name
        self.pos = pos
        # self.size = getattr(VesselSize, self.vessel_type.lower()).value
        # self.health = self.size

    def is_attacked(self, attack_coord: Position):
        """
        tells whether the vessel is attacked
        :return: bool
        """
        if not self.is_sunk():
            if attack_coord.y in range(self.pos.y, self.pos.y+self.size):
                if attack_coord.x == self.pos.x:
                    # self.health -= 1
                    return True
        return False

    def damage(self):
        """
        reduces health
        :return:
        """
        self.health -= 1

    def is_sunk(self):
        return True if self.health == 0 else False


class Battleship(Vessel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.vessel_type = "battleship"
        self.size = 4
        self.health = self.size


class Cruiser(Vessel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.vessel_type = "cruiser"
        self.size = 3
        self.health = self.size


class Destroyer(Vessel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.vessel_type = "destroyer"
        self.size = 2
        self.health = self.size


class Submarine(Vessel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.vessel_type = "submarine"
        self.size = 1
        self.health = self.size


class Armada:
    def __init__(self, list_of_vessels: list[Vessel] | None = None):
        self.list_of_vessels = list_of_vessels
        self.alive_vessels = list_of_vessels

    def size(self):
        return len(self.alive_vessels)

    def add_vessel(self, vessel: Vessel):
        self.alive_vessels.append(vessel)

    def to_list(self):
        return self.list_of_vessels

    def __getitem__(self, index):
        return self.alive_vessels[index]

    def update(self):
        """
        to remove sunken vessel from the armada
        :return:
        """
        for vessel in self:
            if vessel.is_sunk():
                self.alive_vessels.remove(vessel)

    def num(self, vessel: Vessel):
        return self.alive_vessels.count(vessel)

