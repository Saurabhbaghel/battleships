from enum import Enum

ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

VESSELS = ["battleship",
           "cruiser",
           "destroyer",
           "submarine"]

DEFAULT_INITIAL_MISSILES_NUM = 15

# sizes of the vessels
class VesselSize(Enum):
    battleship = 4
    cruiser = 3
    destroyer = 2
    submarine = 1
