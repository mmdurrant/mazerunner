
class CellType():
    Wall  = "x"
    Floor = "."

class CellStatus():
    Unexplored = False
    Explored = True
    
    
class MoveDirection():
    Left = "<"
    Up = "^"
    Right = ">"
    Down = "v"
    

class MoveResponse():
    Wall = "x"
    Empty = "e"
    Moved = "."
