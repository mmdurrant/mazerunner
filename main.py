import socket
import sys

DIR_LEFT = "<"
DIR_FORWARD = "^"
DIR_RIGHT = ">"
DIR_BACK = "v"
HEADER_CURRENT = "e"

class MazeClient():
    
    
    def __init__(self, tcp_socket):
        self._socket = tcp_socket

    def _send(self, data):
        self._socket.sendall(data)

    def _receive(self, length=1):
        buf = b""
        try:
            buf = self._socket.recv(length).decode("utf-8")
        except:
            pass
        return buf

    def cmd_help(self):
        msg = b"?"
        self._send(msg)
        help_msg = self._receive(100)
        return help_msg

    def cmd_get_current(self):
        msg = b"\n"
        self._send(msg)
        current_msg = self._receive(100)
        parsed = self._parse_current(current_msg)
        return parsed

    def _parse_current(self, msg):
        b_str = str(msg)
        print(msg)
        header_char = b_str[0]
        if header_char != HEADER_CURRENT:
            raise Exception("{0} found where {1} expected".format(header_char, HEADER_CURRENT))
        c_u = b_str.index("(") + 1
        c_l = b_str.index(")")
        coord_str = b_str[c_u:c_l]
        coords = coord_str.split(",")
        return coords

    def _parse_coordinates(self, data):
        pass


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
        data = my_client.cmd_help()
        data = my_client.cmd_get_current()

        print(data)
    finally:
        sock.close()
    
if __name__ == "__main__":
    main()