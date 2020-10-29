
class CellType():
    Wall  = "x"
    Self  = "e"
    Moved = "."


class CellStatus():
    Unexplored = 0
    Explored = 1
    
    
class MoveDirection():
    Left = "<"
    Up = "^"
    Right = ">"
    Down = "v"