class board:
    piece_list = []
    def __init__(self,start_position:str):
        self.start_position = start_position
        x = 0
        y = 7
        for i in start_position:
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
            global enpasse
            if self.name == "P":
                canmove = check_empty(board_main.piece_list,self.x,self.y + 1) and check_empty(board_main.piece_list,self.x,y)
                if y - self.y == 2 and self.x == x and self.y == 1 and canmove:
                    enpasse = str((x,y-1))
                    return True
                if y - self.y == 1 and self.x == x and check_empty(board_main.piece_list,self.x,y):return True
                if y - self.y == 1 and abs(self.x - x) == 1 and check_capture(board.piece_list,x,y,self.name):return True
                return False
            if self.name == "p":
                canmove = check_empty(board_main.piece_list,self.x,self.y - 1) and check_empty(board_main.piece_list,self.x,y)
                if self.y - y  == 2 and self.x == x and self.y == 6 and canmove:
                    enpasse = str((x,y+1))
                    return True
                if self.y - y == 1 and self.x == x and check_empty(board_main.piece_list,self.x,y):return True
                if self.y - y == 1 and abs(self.x - x) == 1 and check_capture(board.piece_list,x,y,self.name):return True
                return False
            if self.name == "K":
                if abs(self.x - x) <= 1 and abs(self.y - y) <= 1 and (x,y) not in attacked_squares_b:return True
                return False
            if self.name == "k":
                if abs(self.x - x) <= 1 and abs(self.y - y) <= 1 and (x,y) not in attacked_squares_w:return True
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
            if self.name == "E" or self.name == "E":return True
            return True
        def trymove(self,x:int,y:int) -> bool:
            global next_move,enpasse,cmove,nmove,castling
            gnrte_attack_square(board_main.piece_list)
            line_sight = check_line_sight(board.piece_list,self.x,x,self.y,y,self.name)
            correct_move = self.piecemove(x,y)
            allowed_capture = check_capture(board_main.piece_list,x,y,self.name)or check_empty(board_main.piece_list,x,y)
            print(self.name,line_sight,correct_move,allowed_capture,(self.x,self.y))
            if line_sight and correct_move and allowed_capture:
                if self.name.isupper():
                    next_move = "b"
                    nmove = str(int(nmove) + 1)
                else: next_move = "w"
                if self.name.upper() != "P":
                    cmove = "0"
                    if enpasse != "-":
                        enpasse = "-"
                else:
                    cmove = str(int(cmove) + 1)
                self.x = x
                self.y = y
                capture_piece(board_main.piece_list,x,y,self.name)
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
def gnrte_attack_square(piece_list) -> None:
    attacked_squares_w.clear()
    attacked_squares_b.clear()
    for i in piece_list:
        pieceid = i.name+str(i.x)+str(i.y)
        possible_moves[pieceid] = []
        if i.name == "P":
            attacked_squares_w.add((i.x-1,i.y+1))
            attacked_squares_w.add((i.x+1,i.y+1))
        if i.name == "p":
            attacked_squares_b.add((i.x-1,i.y-1))
            attacked_squares_b.add((i.x+1,i.y-1))
        for y in range(8):
            for x in range(8):
                line_sight = check_line_sight(board.piece_list,i.x,x,i.y,y,i.name)
                correct_move = i.piecemove(x,y)
                allowed_capture = check_capture(board_main.piece_list,x,y,i.name)or check_empty(board_main.piece_list,x,y)
                if line_sight and correct_move:
                    if i.name != "P" and i.name.islower() == False:attacked_squares_w.add((x,y))
                    elif i.name != "p" and i.name.islower() == True:attacked_squares_b.add((x,y))
                    if allowed_capture:
                        possible_moves[pieceid].append((x,y))


def update_fen_string(piece_list:list):
    x = ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"]
    for i in piece_list:
        y = 7-i.y
        x[y] = x[y][:i.x] + i.name + x[y][i.x+1:]
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

def diagonal_moves(piece_list:list,current_x:int,x:int,current_y:int,y:int) -> bool:
    if abs(current_x - x) == 1:return True
    x_list = []
    y_list = []
    x_dir = normalise(current_x-x)
    y_dir = normalise(current_y-y)
    for i in range(1,abs(current_x-x)):
        x_list.append(current_x+x_dir*i)
        y_list.append(current_y+y_dir*i)
    return check_place(piece_list,x_list,y_list)
def sides_moves(piece_list:list,current_x:int,x:int,current_y:int,y:int) -> bool:
    if abs(current_x-x + current_y-y) == 1:return True
    x_dir = normalise(current_x-x)
    y_dir = normalise(current_y-y)
    x_list = []
    y_list = []
    if x_dir != 0:
        for i in range(1,abs(current_x-x)):
            x_list.append(current_x + x_dir*i)
            y_list.append(current_y)
    else:
        for i in range(1,abs(current_y-y)):
            x_list.append(current_x)
            y_list.append(current_y + y_dir*i)
    return check_place(piece_list,x_list,y_list)
def check_line_sight(piece_list:list,current_x:int,x:int,current_y:int,y:int,name:chr) -> bool:
    name = name.capitalize()
    if name == "P":
        if current_x == x:
            return check_place(piece_list,x,y)
        return True
    if name == "B":
        return diagonal_moves(piece_list,current_x,x,current_y,y)
    if name == "N":
        return True
    if name == "R":
        return sides_moves(piece_list,current_x,x,current_y,y)
    if name == "Q":
        if abs(current_x-x) == abs(current_y-y):
            return diagonal_moves(piece_list,current_x,x,current_y,y)
        else:
            return sides_moves(piece_list,current_x,x,current_y,y)
    if name == "K":
        return True
    if name == "E":
        return True
    return True
def check_capture(piece_list:list,x:int,y:int,name:chr) -> bool:
    for i in piece_list:
        if i.x == x and i.y == y and name.islower() != i.name.islower():return True
        if i.x == x and i.y == y and name.islower() == i.name.islower():return False
    return False
def check_empty(piece_list,x:int,y:int) -> bool:
    for i in piece_list:
        if i.x == x and i.y == y:return False
    return True
def capture_piece(piece_list:list,x:int,y:int,name:chr) -> None:
    global cmove
    for i in piece_list:
        if i.x == x and i.y == y and name.islower() != i.name.islower():
            piece_list.remove(i)
            cmove = "0"
            return None
    return None
def normalise(n:int) -> int:
    if n==0: return 0
    if n < 0: return 1
    else: return -1
def find_piece(x:int,y:int):
    for i in board.piece_list:
        if i.x == x and i.y == y:
            return i
    return None

attacked_squares_b = set()
attacked_squares_w = set()
possible_moves = {}
fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board_string = "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR"
fen_board,next_move,castling,enpasse,cmove,nmove = fen_string.split(" ",7)
board_main = board(board_string)

if __name__ == "__main__":
    print(*board_main.piece_list)
    gnrte_board_ascii(board_main.piece_list)
    gnrte_attack_square(board_main.piece_list)