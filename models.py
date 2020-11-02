from itertools import chain
import logging

from constants import CellType, CellStatus, MoveDirection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

EXPLORABLE = [CellStatus.Explored, CellStatus.Unexplored]

class MazeCell():
    def __init__(self, x, y, celltype=None):
        self._x = x
        self._y = y
        self.explored = False
        self.celltype = celltype

    def get_coord(self):
        # You  know the coodinate when you get it. ... we probably don't need this.
        return (self._x, self._y)


class MazeMap():
    def __init__(self, bound):
        self._bound = bound
        self._mapdata = [[MazeCell(x,y) for y in range(self._bound)] for x in range(self._bound)]
        self._coorditer = lambda: [(x,y) for y in range(self._bound) for x in range(self._bound)]
        self._celliter = lambda: [self._mapdata[x][y] for y in range(self._bound) for x in range(self._bound)]
        
    def set_floor_data(self, floor_coordinates):
        for x,y in self._celliter():
            ct = CellType.Floor if (x,y) in floor_coordinates else CellType.Wall
            self._mapdata[x][y].celltype = ct

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
        cell = self.get_cell(x,y)
        return cell.explored == CellStatus.Unexplored or cell.explored and cell.celltype in [CellType.Wall, ]


    def is_explored(self, x, y):
        return self.get_cell(x, y).explored == CellStatus.Explored