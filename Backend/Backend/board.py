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
    def selectpiece(self,x:int,y:int):
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
                if y - self.y == 1 and self.x == x:return True
                return False
            if self.name == "p":
                if self.y - y == 1 and self.x == x:return True
                return False
            if self.name == "B" or self.name == "b":
                if abs(self.x - x) == abs(self.y - y):return True
                return False
            if self.name == "N" or self.name == "n":
                if abs(self.x - x) == 2 and abs(self.y - y) == 1:return True
                if abs(self.x - x) == 1 and abs(self.y - y) == 2:return True
                return False
            if self.name == "R" or self.name == "r":
                if self.x == x and self.y != y:return True
                if self.x != x and self.y == y:return True
                return False
            if self.name == "Q" or self.name == "q":
                if self.x == x and self.y != y:return True
                if self.x != x and self.y == y:return True
                if abs(self.x - x) == abs(self.y - y):return True
                return False
            if self.name == "K" or self.name == "k":
                if abs(self.x - x) == 1 and abs(self.y - y) == 1:return True
                return False
            if self.name == "E" or self.name == "E":return True
            return True
        def trymove(self,x:int,y:int) -> bool:
            if check_line_sight(board.piece_list,self.x,x,self.y,y,self.name) and self.piecemove(x,y):
                check_capture(board.piece_list,x,y,self.name)
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
        if x != 0: fen = fen + str(x)
    fen = fen + " " + next_move + " " + castling + " " + enpasse + " " + cmove + " " + nmove
    return fen
def gnrte_board_ascii(piece_list) -> None:
    x = ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"]
    for i in piece_list:
        x[i.y] = x[i.y][:i.x] + i.name + x[i.y][i.x+1:]
    x = x[0] + "\n" + x[1] + "\n" +  x[2] + "\n" +  x[3] + "\n" + x[4] + "\n" + x[5] + "\n" +  x[6] + "\n" +  x[7]
    print(x)

def update_fen_string(piece_list:list):
    x = ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"]
    for i in piece_list:
        x[i.y] = x[i.y][:i.x] + i.name + x[i.y][i.x+1:]
    x = x[0] + "/" + x[1] + "/" +  x[2] + "/" +  x[3] + "/" + x[4] + "/" + x[5] + "/" +  x[6] + "/" +  x[7]
    x = gnrte_fen_string(x)
    return x

def check_place(piece_list:list,x:int|list,y:int|list) -> bool:
        if type(x) == int:
            for i in piece_list:
                if i.x == x and i.y == y:
                    return False
            return True
        if type(x) == list:
            for i in range(len(x)):
                if not check_place(piece_list,x[i],y[i]):
                    return False
            return True
        else:
            raise TypeError
def check_line_sight(piece_list:list,current_x:int,x:int,current_y:int,y:int,name:chr) -> bool:
            name = name.capitalize()
            if name == "P":
                if check_place(piece_list,x,y):
                    return True
                return False
            if name == "B":
                if abs(current_x - x) == 1:
                    if check_place(piece_list,x,y):
                        return True
                    return False
                else:
                    x_list = []
                    y_list = []
                    x_dir = normalise(current_x-x)
                    y_dir = normalise(current_y-y)
                    for i in range(1,abs(current_x-x)):
                        x_list.append(current_x+x_dir*i)
                        y_list.append(current_y+y_dir*i)
                    if check_place(piece_list,x_list,y_list):
                        return True
                    return False
            if name == "N":
                return True
            if name == "R":
                x_dir = normalise(current_x-x)
                y_dir = normalise(current_y-y)
                if abs(current_x-x) == 1 or abs(current_y-y) == 1:
                    return True
                else:
                    x_list = []
                    y_list = []
                    if x_dir != 0:
                        for i in range(1,abs(current_x-x)):
                            x_list.append(current_x + x_dir)
                            y_list.append(y)
                    else:
                        for i in range(1,abs(current_y-y)):
                            x_list.append(x)
                            y_list.append(current_y + y_dir)
                    if check_place(piece_list,x_list,y_list):
                        return True
                    return False
            if name == "Q":
                if abs(current_x - x) == 1:
                    if check_place(piece_list,x,y):
                        return True
                    return False
                else:
                    x_list = []
                    y_list = []
                    x_dir = normalise(current_x-x)
                    y_dir = normalise(current_y-y)
                    for i in range(1,abs(current_x-x)):
                        x_list.append(current_x+x_dir*i)
                        y_list.append(current_y+y_dir*i)
                    if check_place(piece_list,x_list,y_list):
                        return True
                    x_dir = normalise(current_x-x)
                    y_dir = normalise(current_y-y)
                    if x_dir == 1 or y_dir == 1:
                        return True
                    else:
                        x_list = []
                        y_list = []
                        if x_dir != 0:
                            for i in range(1,abs(current_x-x)):
                                x_list.append(current_x + x_dir)
                                y_list.append(y)
                        else:
                            for i in range(1,abs(current_y-y)):
                                x_list.append(x)
                                y_list.append(current_y + y_dir)
                        if check_place(piece_list,x_list,y_list):
                            return True
                        return False
            if name == "K":
                return True
            if name == "E":
                return True
            return True
def check_capture(piece_list:list,x:int,y:int,name:chr) -> None:
    for i in piece_list:
        if i.x == x and i.y == y and name.islower() != i.name.islower():
            piece_list.remove(i)
def normalise(n:int) -> int:
    if n==0: return 0
    if n < 0: return 1
    else: return -1


fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board_string = "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR"
fen_board,next_move,castling,enpasse,cmove,nmove = fen_string.split(" ",7)

if __name__ == "__main__":
    board_main = board(fen_string)
    print(*board_main.piece_list)
    print(gnrte_fen_string(board_string))
    gnrte_board_ascii(board_main.piece_list)