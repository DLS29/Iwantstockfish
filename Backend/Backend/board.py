class board:
    piece_list = []
    def __init__(self,start_position:str):
        self.start_position = start_position
        x = 0
        y = 7
        for i in board_string:
            if i == "/":
                y = y-1
                x = 0
            elif i == "0":
                x = x+1
            else:
                i = board.piece(x,y,i)
                x = x+1
    def selectpiece(self,x:int,y:int) -> None|piece:
        for piece in self.piece_list:
            if piece.x == x and piece.y == y:
                return piece
        return None
    class piece:
        def __init__(self,x:int,y:int,name:chr):
            self.x = x
            self.y = y
            self.name = name

            board.piece_list.append(self)
        def move(self,x:int,y:int) ->  None:
            self.x = x
            self.y = y
        def piecemove(self,x:int,y:int) -> bool:
            if self.name == "P":
                if y - self.y == 1 and self.x == x:
                    return True
                return False
            if self.name == "p":
                if self.y - y == 1 and self.x == x:
                    return True
                return False
            if self.name == "B" or self.name == "b":
                if abs(self.x - x) == abs(self.y - y):
                    return True
                return False
            if self.name == "N" or self.name == "n":
                if abs(self.x - x) == 2 and abs(self.y - y) == 1:
                    return True
                if abs(self.x - x) == 1 and abs(self.y - y) == 2:
                        return True
            if self.name == "R" or self.name == "r":
                if self.x == x and self.y != y:
                    return True
                if self.x != x and self.y == y:
                    return True
                return False
            if self.name == "Q" or self.name == "q":
                if self.x == x and self.y != y:
                    return True
                if self.x != x and self.y == y:
                    return True
                if abs(self.x - x) == abs(self.y - y):
                    return True
                return False
            if self.name == "K" or self.name == "k":
                if abs(self.x - x) == 1 or abs(self.y - y) == 1:
                    return True
                return False
            if self.name == "E" or self.name == "E":
                return True
            return True
        def trymove(self,x:int,y:int) -> bool:
            if check_place(board.piece_list,x,y) and self.piecemove(x,y):
                self.x = x
                self.y = y
                return True
            return False


def gnrte_fen_string(board_string:str) -> str:
    fen = ""
    x = 0
    for i in board_string:
        if i == "0":
            x = x + 1
        elif i == "/":
            if x != 0:
                fen = fen + str(x)
            x = 0
            fen = fen + i
        else:
            if x != 0:
                fen = fen + str(x)
                x = 0
            fen = fen + i
    fen = fen + " " + next_move + " " + castling + " " + enpasse + " " + cmove + " " + nmove
    return fen
def gnrte_board_string(fen_board:str) -> str:
    board_string = ""
    for i in fen_board:
        if i.isdigit():
            for n in range(int(i)):
                board_string = board_string + "0"
        else:
            board_string = board_string + i
    return board_string

def update_board_string(piece_list):
    x = ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"]
    for i in piece_list:
        x[i.y] = x[i.y][:i.x] + i.name + x[i.y][i.x+1:]
    x = x[0] + "/" + x[1] + "/" +  x[2] + "/" +  x[3] + "/" + x[4] + "/" + x[5] + "/" +  x[6] + "/" +  x[7]
    return x

def check_place(piece_list,x:int,y:int) -> bool:
        for i in piece_list:
            if i.x == x and i.y == y:
                return False
        return True
def check_sight(piece_list,x_list,y_list) -> bool:
    for i in range(len(x_list)):
        if not check_place(piece_list,x_list[i],y_list[i]):
            return False
    return True
def check_line_sight(piece_list,current_x:int,x:int,current_y:int,y:int,name:chr) -> bool:
            if name == "P" or name == "p":
                if check_place(piece_list,x,y):
                    return True
                return False
            if name == "B" or name == "b":
                if abs(current_x - x) == 1:
                    if check_place(piece_list,x,y):
                        return True
                    return False
                else:
                    x_list = []
                    y_list = []
                    if current_x-x > 0: x_dir = 1
                    else: x_dir = -1
                    if current_y-y > 0: y_dir = 1
                    else: y_dir = -1
                    for i in range(abs(current_x-x)-1):
                        x_list.append(current_x+x_dir)
                        y_list.append(current_y+y_dir)
                    if check_sight(piece_list,x_list,y_list):
                        return True
                    return False
            if name == "N" or name == "n":
                return True
            if name == "R" or name == "r":
                x_dir = current_x - x
                y_dir = current_y - y
                if x_dir == 1 or y_dir == 1:
                    return True
                else:
                    x_list = []
                    y_list = []
                    if x_dir != 0:
                        for i in range(current_x-x):
                            x_list.append(current_x + x_dir)
                            y_list.append(y)
                    else:
                        for i in range(current_y-y):
                            x_list.append(x)
                            y_list.append(current_y + y_dir)
                    if check_sight(piece_list,x_list,y_list):
                        return True
                    return False
            if name == "Q" or name == "q":
                if abs(current_x - x) == 1:
                    if check_place(piece_list,x,y):
                        return True
                    return False
                else:
                    x_list = []
                    y_list = []
                    if current_x-x > 0: x_dir = 1
                    else: x_dir = -1
                    if current_y-y > 0: y_dir = 1
                    else: y_dir = -1
                    for i in range(abs(current_x-x)-1):
                        x_list.append(current_x+x_dir)
                        y_list.append(current_y+y_dir)
                    if check_sight(piece_list,x_list,y_list):
                        return True
                    x_dir = current_x - x
                    y_dir = current_y - y
                    if x_dir == 1 or y_dir == 1:
                        return True
                    else:
                        x_list = []
                        y_list = []
                        if x_dir != 0:
                            for i in range(current_x-x):
                                x_list.append(current_x + x_dir)
                                y_list.append(y)
                        else:
                            for i in range(current_y-y):
                                x_list.append(x)
                                y_list.append(current_y + y_dir)
                        if check_sight(piece_list,x_list,y_list):
                            return True
                        return False
            if name == "K" or name == "k":
                return True
            if name == "E" or name == "E":
                return True
            return True

fen_string = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR w KQkq - 0 1"
board_string = "rnbkqbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBKQBNR"
fen_board,next_move,castling,enpasse,cmove,nmove = fen_string.split(" ",7)

board_main = board(fen_string)
print(*board_main.piece_list)
print(gnrte_fen_string(board_string))
print(gnrte_board_string(fen_board))
pawn = board_main.selectpiece(0,1)
r = pawn.trymove(0,5)
print(r)
print(pawn.x,pawn.y,pawn.name)
print(gnrte_fen_string(board_string))
print(update_board_string(board_main.piece_list))