import logging

from constants import CellType, CellStatus, MoveDirection

logger = logging.getLogger(__name__)

EXPLORABLE = [CellStatus.Explored, CellStatus.Unexplored]

class MazeMap():
    def __init__(self, bound):
        self._bound = bound
        self._mapdata = [[CellStatus.Unexplored for y in range(self._bound)] for x in range(self._bound)]

    def __str__(self):
        rows = []
        for x in range(self._bound):
            mapline = []
            for y in range(self._bound):                
                mapline.append(str(self.get_cell(x, y)))
            z = " ".join(mapline)
            rows.append(z)
        return "\n".join(rows)

    def get_cell(self, x, y):
        logger.debug("Getting {} {}".format(x, y))
        return self._mapdata[x][y]
    
    def set_cell(self, x, y, value):
        self._mapdata[x][y] = value

    def print_map(self):
        for x in range(self._bound):
            mapline = []
            for y in range(self._bound):                
                mapline.append(str(self.get_cell(x, y)))
            print(" ".join(mapline))

    def can_explore(self, x, y):
        return self.get_cell(x, y) in EXPLORABLE

    def is_explored(self, x, y):
        return self.get_cell(x, y) in [CellStatus.Explored]