
from constants import CellType, MoveDirection, MoveResponse

class MazeClient():
    def __init__(self, tcp_socket, byte_encoding):
        self._socket = tcp_socket
        self._byte_encoding = byte_encoding

    def _send(self, data):
        data_enc = bytearray(data, self._byte_encoding)
        self._socket.sendall(data_enc)

    def _receive(self, length=1):
        buf = b""
        buf = self._socket.recv(length).decode(self._byte_encoding)
        return buf

    def cmd_reset(self):
        msg = "r"
        self._send(msg)
        reset_msg = self._receive(100).strip()
        assert(str(reset_msg) == str("r (0, 0)"))

    def cmd_help(self):
        msg = "?"
        self._send(msg)
        help_msg = self._receive(100)
        return help_msg

    def cmd_move_up(self):
        return self._cmd_move(MoveDirection.Up)

    def cmd_move_down(self):
        return self._cmd_move(MoveDirection.Down)

    def cmd_move_right(self):
        return self._cmd_move(MoveDirection.Right)

    def cmd_move_left(self):
        return self._cmd_move(MoveDirection.Left)

    def _cmd_move(self, direction):
        self._send(direction)
        move_response = self._receive(100)
        parsed = self._parse_move(move_response)
        return parsed

    def cmd_get_current(self):
        msg = "\n"
        self._send(msg)
        current_msg = self._receive(100)
        parsed = self._parse_current(current_msg)
        return parsed

    def _parse_current(self, data):
        header_char = data[0]
        if header_char != CellType.Self:
            raise Exception("{0} found where {1} expected".format(header_char, CellType.Self))
        coords = self._parse_coordinates(data)
        return coords

    def _parse_coordinates(self, data):
        c_u = data.index("(") + 1
        assert(c_u == 3)
        c_l = data.index(")")
        coord_str = data[c_u:c_l]
        coords = [int(x.strip()) for x in coord_str.split(",")]
        # Returns list(x,y)
        if len(coords) != 2:
            raise Exception("{} should only have 2 members x and y, parsed from data  \"{}\"".format(coords, data))
        return coords

    def _parse_move(self, data):
        # Moves return "x" if it's a wall, "." if we move to empty floor, and "e" (?) if we no-op
        header_char = data[0]
        # If not a response we know, bail.
        if header_char not in [MoveResponse.Empty, MoveResponse.Moved, MoveResponse.Wall]:
            raise Exception("{} move failed".format(header_char))
        coords = self._parse_coordinates(data)
        # Returns the tuple(char, tuple(x,y))
        return (header_char,coords)
