import logging
import socket
import sys
import time

from client import MazeClient
from constants import CellStatus,  CellType, MoveDirection
from models import MazeMap

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEBUG = True

BYTE_ENCODING = "utf-8"

GRID_LIMIT = 10
MOVE_LIMIT = 200

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
        rv = self._y-1 >= 0 and self._map.can_explore(self._x, self._y - 1)
        logger.debug("Can up {}".format(rv))
        return  rv

    def _can_down(self):
        rv = self._map.can_explore(self._x, self._y + 1)
        logger.debug("Can down {}".format(rv))
        return rv 

    def _can_left(self):
        rv = self._x - 1 >= 0 and self._map.can_explore(self._x - 1, self._y)
        logger.debug("Can left {}".format(rv))
        return rv

    def _can_right(self):
        rv = self._map.can_explore(self._x + 1, self._y)
        logger.debug("Can right {}".format(rv))
        return rv

    def _can_move(self):
        rv = self._can_right() or self._can_down() or  self._can_left() or self._can_right()
        return rv

    def walk(self):
        self._client.cmd_reset()
        start_pos = self._client.cmd_get_current()
        assert(start_pos == [0,0])
        self._x, self._y = start_pos
        logger.debug("Start position: {}".format(start_pos))
        self._map.set_cell(self._x, self._y, CellStatus.Explored)
        
        should_loop = True 
        move_count = 0
        while should_loop:
            print("Loop {}".format(move_count))
            if self._can_right():
                move_func = self._client.cmd_move_right
            elif self._can_down():
                move_func = self._client.cmd_move_down
            elif self._can_left():
                move_func = self._client.cmd_move_left
            elif self._can_up():
                move_func = self._client.cmd_move_up
            else:
                raise Exception("Can't move")

            logger.debug("Executing {}".format(str(move_func)))
            response, coords = move_func()
            move_count += 1
            self._x, self._y = coords
            self._map.set_cell(self._x, self._y, response)
            should_loop = self._can_move() and move_count < MOVE_LIMIT
            time.sleep(0.2)
        
        logger.debug("Ended at {} {}".format(self._x, self._y))


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