from components.grid import Grid, Position
from components.armada import Armada


def print_rules():
    print(
        """
        +++++++++
        + RULES +
        +++++++++
        
        1.
        """
    )


class Game:
    def __init__(self,
                 grid: Grid,
                 armada: Armada,
                 num_missiles: int
                 ):
        self.is_over: bool = False
        self.num_missiles = num_missiles
        self.current_move: str | None = None
        self.score: int = 0
        self.grid = grid
        self.armada = armada

    def step(self):
        """
        ask coordinate to attack
        :return:
        """
        attack_pos = Position(pos_string=str(input(
            "Give Coordinate to attack: "
        ))
        )

        for vessel in self.armada:
            # check if it is attacked
            if vessel.is_attacked(attack_pos):
                # inflict damage on this vessel
                vessel.damage()

                # update the grid to show attack
                self.grid.update(attack_pos)
                # self.grid.show()

        # reduce missiles
        self.num_missiles -= 1

    def is_won(self):
        if not self.is_over:
            if self.armada.size() == 0:
                print("Hurray, You destroyed all the vessels.")
                self.is_over = True
                return True
            else:
                return False

    def is_lost(self):
        if self.num_missiles == 0:
            print("All the missiles are finished. You Lost.")
            self.is_over = True
            return True
        return False

