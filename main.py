import socket
import sys

BYTE_ENCODING = "utf-8"

MAP_WALL = "x"
MAP_SELF = "e"
MAP_MOVED = "."
MAP_UNEXPLORED = "0"
MAP_FULLY_EXPLORED = "-"
MAP_PARTIAL_EXPLORED = "+"

DIR_LEFT = "<"
DIR_FORWARD = "^"
DIR_RIGHT = ">"
DIR_DOWN = "v"
HEADER_CURRENT = MAP_SELF   # change this

class MazeMap():
    def __init__(self, bound):
        self._bound = bound
        self._mapdata = [[MAP_UNEXPLORED for y in range(self._bound)] for x in self._map_limit]

    def get_cell(self, x, y):
        return self._mapdata[x][y]

    def print_map(self):
        for x in range(self._map_limit):
            mapline = []
            for y in range(self._map_limit):                
                mapline.append(str(self.get_cell(x, y)))
            print(" ".join(mapline))

    def is_explored(self, x, y):
        return self.get_cell(x, y) in [MAP_FULLY_EXPLORED, MAP_PARTIAL_EXPLORED, MAP_UNEXPLORED]
    

class MazeWalker():
    def __init__(self, client):
        self._client = client
        self._map_limit = 10
        self._init_map()
        self.location = (0,0)

    def _can_move(self):
        cur_x, cur_y = self.location
        _can_forward = cur_y-1 >= 0 and self._is_explored((cur_x, cur_y - 1))
        _can_left = cur_x - 1 >= 0 and self._is_explored((cur_x - 1, cur_y))
        _can_right = self._is_explored((cur_x + 1, cur_y))
        _can_down = self._is_explored((cur_x, cur_y + 1))
        return  _can_forward or _can_left or _can_right or _can_down

    def walk(self):
        self._client.cmd_reset()
        data = self._client.cmd_get_current()
        self._mapdata[self.location] = MAP_PARTIAL_EXPLORED
        assert(data == [0,0])
        while self._can_move():
            response,coords = self._client.cmd_move_down()
            current = self._client.cmd_get_current()
            self.location = current 
            self._mapdata[tuple([x for x in coords])] = response
        
        print(self.location)


class MazeClient():
    def __init__(self, tcp_socket):
        self._socket = tcp_socket

    def _send(self, data):
        self._socket.sendall(data)

    def _receive(self, length=1):
        buf = b""
        buf = self._socket.recv(length).decode(BYTE_ENCODING)
        return buf

    def cmd_reset(self):
        msg = b'r'
        self._send(msg)
        reset_msg = self._receive(100).strip()
        assert(str(reset_msg) == str("r (0, 0)"))

    def cmd_help(self):
        msg = b"?"
        self._send(msg)
        help_msg = self._receive(100)
        return help_msg

    def cmd_move_down(self):
        return self._cmd_move(DIR_DOWN)

    def _cmd_move(self, direction):
        msg = bytearray(direction, BYTE_ENCODING)
        self._send(msg)
        move_response = self._receive(100)
        parsed = self._parse_move(move_response)
        return parsed

    def cmd_get_current(self):
        msg = b"\n"
        self._send(msg)
        current_msg = self._receive(100)
        parsed = self._parse_current(current_msg)
        return parsed

    def _parse_current(self, data):
        header_char = data[0]
        if header_char != HEADER_CURRENT:
            raise Exception("{0} found where {1} expected".format(header_char, HEADER_CURRENT))
        coords = self._parse_coordinates(data)
        return coords

    def _parse_coordinates(self, data):
        header_char = data[0]
        # It's a wall.
        if header_char == MAP_WALL:
            pass
        elif header_char == MAP_MOVED:
            pass
        elif header_char == MAP_SELF:
            pass
        else:
            raise Exception("{} is unknown.".format(header_char))
        
        c_u = data.index("(") + 1
        assert(c_u == 3)
        c_l = data.index(")")
        coord_str = data[c_u:c_l]
        coords = [int(x.strip()) for x in coord_str.split(",")]
        return coords

    def _parse_move(self, data):
        header_char = data[0]
        if header_char not in [MAP_WALL, MAP_MOVED]:
            raise Exception("{} move failed".format(header_char))
        coords = self._parse_coordinates(data)
        return (header_char,coords)


def main():
    open_client()

def open_client():
    server_address = "dougpuzzle"
    server_port = 49999

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))
        # sock.sendall(b"\n")
        my_client = MazeClient(sock)
        my_walker = MazeWalker(my_client)
        my_walker.walk()
        my_walker.print_map()
        
    finally:
        sock.close()
    
if __name__ == "__main__":
    main()