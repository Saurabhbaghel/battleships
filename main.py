import os
import argparse

from components.grid import Grid, Position
from components.armada import (
    Vessel, Armada, Battleship, Cruiser, Destroyer, Submarine
   )
from gameplay.gameplay import (
    Game
)
from utils.configs import (DEFAULT_INITIAL_MISSILES_NUM)


def clearscreen():
    # clear the screen
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_rules():
    print(
"""
+++++++++
+ RULES +
+++++++++

1. One move allowed per step.
2. Give the coordinate in this format - <column-alphabet><row-number>. Eg - E3
3. When the missile hits a vessel , you will see "x" on the board else "o".
4. Total {} missiles are available.
5. You Won when you are able to find and destroy all the vessels.
6. You Lose when all the missiles get exhausted before winning.
""".format(DEFAULT_INITIAL_MISSILES_NUM)
    )


def main(args):

    # clear the screen
    clearscreen()

    # initialize grid with given size
    grid = Grid(size=args.grid_size)

    # show grid and other instructions
    grid.show()

    # _____________________
    # | initialize armada |
    # |___________________|

    # vessels
    vessels = ("Battleship", "Cruiser", "Destroyer", "Submarine")

    # input how many vessels user wants
    input_prompt = "{sno} Count of {vessel}: "

    # vessels_count = {
    #     vessel: int(input(input_prompt.format(sno+1, vessel)))
    #     for sno, vessel in enumerate(vessels)
    # }
    #

    battleships_count = int(input("A. Count of Battleships: "))
    cruisers_count = int(input("B. Count of Cruisers: "))
    destroyers_count = int(input("C. Count of Destroyers: "))
    submarines_count = int(input("D. Count of Submarines: "))

    # make vessels
    fleet_of_battleships = [Battleship(name=f"battleship_{i+1}") for i in range(battleships_count)]
    fleet_of_cruisers = [Cruiser(name=f"cruiser_{i+1}") for i in range(cruisers_count)]
    fleet_of_destroyers = [Destroyer(name=f"destroyer_{i+1}") for i in range(destroyers_count)]
    fleet_of_submarines = [Submarine(name=f"submarine_{i+1}") for i in range(submarines_count)]

    all_vessels = fleet_of_battleships \
                    + fleet_of_cruisers \
                    + fleet_of_destroyers \
                    + fleet_of_submarines

    # make armada
    armada = Armada(all_vessels)

    # Get Positions


    # _____________________________
    # | begin placing the vessels |
    # |___________________________|

    # take the initial position for all the vessels
    vessels_pos = {}
    # vessels_pos = { "Battleship": E1 , ... }
    #   A B C D E F G H I
    # 1 . . . . ^ . . . .
    # 2 ^ . . . | . . . .
    # 3 V . . . | . . . .
    # 4 . . . . V . . . .
    # 5 . . . . . . . . .
    # above the pos of Battleship is E1 and the destroyer is A2

    for vessel in armada:
        # check if the vessel
        # if armada.num(vessel) != 0:
        # for position
        while True:
            _pos = str(input(f"Enter the position for the {vessel.name}: "))

            # add this position to the vessel
            vessel.pos = Position(pos_string=_pos)
            # pos_dict_for_vessel = {vessel: pos}
            try:
                grid.place_vessel(vessel)
            except AssertionError as e:
                print("Cannot place {} at {}, position overlapping with another vessel".format(vessel.name, _pos))
                continue
            except IndexError:
                print("Cannot accomodate {} at {}.".format(vessel.name, _pos))
            except ValueError:
                print("{} position not available.".format(_pos))
            else:
                break

        # add the vessel-position dict to main positions dict
        # vessels_pos.update(pos_dict_for_vessel)

    # ask user whether he wants to see the placement of vessels
    show_hidden_grid = input("Do you want to see the placed vessels in the grid (y/n)? ")
    if show_hidden_grid.lower() == "y":
        # placed vessels will be shown in the hidden grid
        grid.show_hidden()


    # __________________
    # | begin the game |
    # |________________|

    input("Press any key to start the game ...")

    # initialize game
    game = Game(grid,
                armada,
                args.num_missiles
                )

    while True:
        clearscreen()

        # print the new game screen
        # it will have :
        # 1. Rules
        # 2. Current grid
        # 3. Input
        print_rules()

        # show grid
        grid.show()

        # show the score, etc.
        # show number of vessels left, number of missiles left.
        game.show_stats()

        # check winning condition
        if game.is_won():
            break

        # check losing condition
        if game.is_lost():
            break

        # Take a step
        # in step, the player will be asked to give the coordinate
        # where he wants to drop the missile
        game.step()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid-size", type=int, default=9, help="Specify the size of the grid of the game.")
    parser.add_argument("--num-missiles", type=int, default=15, help="Number of missiles.")
    args = parser.parse_args()
    main(args)
