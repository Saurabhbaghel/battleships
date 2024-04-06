from pydantic import BaseModel, field_validator
from enum import Enum
from copy import deepcopy

# from components.armada import Vessel
from utils.configs import (
VesselSize, ALPHABETS
)


class Position:
    def __init__(self, pos_string: str):
        self.pos_string = pos_string
        self.x = self.pos_string[0]
        self.y = int(pos_string[1])
        self.check_x()
        self.check_y()
        self.x_int = ALPHABETS.index(self.x)

    def check_x(self):
        if self.x not in ALPHABETS:
            raise ValueError("First character of x should be in alphabet.")

    def check_y(self):
        if self.y not in list(range(10)):
            raise ValueError("Second character of position should be 0-9.")


class Grid:
    def __init__(self, size):
        self.size = size
        self.rows, self.cols = (size, size)
        self.num_ships_placed = 0
        self.ships_positions = []
        self.grid = [["." for c in range(self.cols)] for r in range(self.rows)]

        # make a copy of the grid to handle placement of ships
        self.grid_hidden = deepcopy(self.grid)

    def show(self):
        """
        Show the grid.
        If no grid is mentioned,
        by default current grid will be considered.
        :param _grid: list[list[str]]
        :return: None
        """
        # print the columns name
        print(end="  ")
        for i in range(self.size):
            print(ALPHABETS[i], end=" ")
        print("\n")

        for row_num, row in enumerate(self.grid):
            # print row name
            print(str(row_num), end=" ")
            # print rest of the row
            for char in row:
                print(char, end=" ")
            # go to next line for next row
            print("\n")

    def show_hidden(self):
        """
        show the hidden grid
        :return:
        """
        # print the columns name
        print(end="  ")
        for i in range(self.size):
            print(ALPHABETS[i], end=" ")
        print("\n")

        for row_num, row in enumerate(self.grid_hidden):
            # print row name
            print(str(row_num), end=" ")
            # print rest of the row
            for char in row:
                print(char, end=" ")
            # go to next line for next row
            print("\n")

    def place_vessel(self, vessel):
        """
        Place the vessel in the hidden grid
        :param vessel: Vessel
        :return: None
        """

        def check_pos_available(_grid: list, _vessel):
            """
            to check whether placing the ship is feasible.
            :param _grid:
            :param _vessel:
            :return:
            """
            assert vessel.pos.x in ALPHABETS[:self.size-1], (
                "x-coord can be only between A and {}, but it is {}".format(ALPHABETS[self.size-1], vessel.pos.x))
            assert vessel.pos.y in list(range(self.size)), (
                "y-coord can be only between 0 and {} but it is {}".format(self.size-1, vessel.pos.y))

            # vessel.pos.x_int_num = self._alphabet_vessel.pos.x_int_map[vessel.pos.x]

            try:
                for _row in _grid[vessel.pos.y: vessel.pos.y+vessel.size]:
                    _char = _row[vessel.pos.x_int]
                    if _char in ("^", "|", "V"):
                        return False
            except IndexError:
                return False

            return True

        # the coordinates given in the vessels_pos dict are in manner (x-coord, y-coord)
        # this coordinate is for one central cell
        # currently the vessels will be oriented vertically only. Facing North           # TODO to allow orientations
        #   A B C D E F G H I
        # 1 . . . . ^ . . . .
        # 2 ^ . . . | . . . .
        # 3 V . . . | . . . .
        # 4 . . . . V . . . .
        # 5 . . . . . . . . .
        # above the pos of Battleship is E1 and the destroyer is A2

        # vessel_pos will be in the form <alphabetNumber> like E2
        # vessel, pos = vessel_pos.items()

        # vessel.pos.x_int, vessel.pos.y = pos[0], pos[1]

        # checking whether the positions given are even in the grid or not
        # vessel.pos.check_validity_in_grid(self)
        
        # first check the pos is available in the grid
        assert check_pos_available(self.grid_hidden, vessel), f"Cannot place {vessel} there"
        # these are to be placed in the grid_hidden


        # now place the vessel
        # placing the head of the vessel
        self.grid_hidden[vessel.pos.y][vessel.pos.x_int] = "^"

        # placing the body of the vessel except the tail of the vessel
        for row in self.grid_hidden[vessel.pos.y+1: vessel.pos.y+vessel.size-1]:
            row[vessel.pos.x_int] = "|"

        # placing the tail of the vessel
        self.grid_hidden[vessel.pos.y+vessel.size-1][vessel.pos.x_int] = "V"

    def update(self, attack_pos: Position):
        for i, row in enumerate(self.grid_hidden):
            for j, char in enumerate(row):
                if char in ("^", "|", "V"):
                    # ship is attacked
                    # show attacked ship part by "x"
                    # update the grid
                    self.grid[i][j] = "x"
                else:
                    # missile in water
                    # show attacked part by "o"
                    # update the grid
                    self.grid[i][j] = "o"



