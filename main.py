import logging
import socket
import sys

from client import MazeClient
from constants import CellStatus,  CellType, MoveDirection
from models import MazeMap

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
DEBUG = True

BYTE_ENCODING = "utf-8"

GRID_LIMIT = 10
MOVE_LIMIT = 10

HEADER_CURRENT = CellType.Self

class MazeWalker():
    def __init__(self, client, mazemap):
        self._client = client
        self._map_limit = GRID_LIMIT
        self._map = mazemap or MazeMap(self._map_limit)
        self._x = 0
        self._y = 0

    def print_map(self):
        print(self._map)

    def _can_up(self):
        # We're not an edge 
        return self._y-1 >= 0 and self._map.can_explore(self._x, self._y - 1)

    def _can_down(self):
        return self._map.can_explore(self._x, self._y + 1)

    def _can_left(self):
        return self._x - 1 >= 0 and self._map.can_explore(self._x - 1, self._y)
    
    def _can_right(self):
        return self._map.can_explore(self._x + 1, self._y)

    def _can_move(self):
        return self._can_right() or self._can_down() or  self._can_left() or self._can_right()

    def walk(self):
        self._client.cmd_reset()
        data = self._client.cmd_get_current()
        self._x, self._y = data
        self._map.set_cell(self._x, self._y, CellStatus.Explored)
        
        assert(data == [0,0])
        should_loop = True 
        move_count = 0
        while should_loop:
            if self._can_right():
                response,coords = self._client.cmd_move_right()
            elif self._can_down():
                response,coords = self._client.cmd_move_down()
            elif self._can_left():
                response,coords = self._client.cmd_move_left()
            elif self._can_up():
                response,coords = self._client.cmd_move_up()
            else:
                raise Exception("Can't move")

            move_count += 1
            self._x, self._y = coords
            self._map.set_cell(self._x, self._y, response)
            should_loop = self._can_move() and move_count < MOVE_LIMIT
        
        print((self._x, self._y))



def main():
    open_client()

def open_client():
    server_address = "dougpuzzle"
    server_port = 49999

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))
        # sock.sendall(b"\n")
        my_client = MazeClient(sock, BYTE_ENCODING)
        my_walker = MazeWalker(my_client, MazeMap(GRID_LIMIT))
        my_walker.walk()
        my_walker.print_map()
        
    finally:
        sock.close()
    
if __name__ == "__main__":
    main()