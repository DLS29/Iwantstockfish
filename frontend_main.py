import tkinter as tk
import subprocess as sp
from PIL import Image,ImageTk
import Frontend.constance as constance
import Backend.Backend.board as board

#board rendering will be done with FEN string for now
root = tk.Tk()
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()
root.geometry(f"{str(ScreenWidth)}x{str(ScreenHeight)}")
root.title("Iwantstockfish")
root.configure(bg="#2c2c2c")


def image_procesing(dir):
    image = Image.open(dir)
    image = image.resize((100,100))
    image = ImageTk.PhotoImage(image)
    return image



#creation of bacground
SIZE = int((ScreenHeight*0.9)/8)
canvas = tk.Canvas(root, width=SIZE*8,height=SIZE*8,highlightthickness=0,bg="#aaaaaa")
canvas.pack(padx=0,pady=10)
color = ["#a5beaa","#0c9007"]

for y in range(int(ScreenWidth/SIZE)+1):
    for x in range(int(ScreenHeight/SIZE)+1):
        x1 = x*SIZE
        y1 = y*SIZE
        x2 = x1 + SIZE
        y2 = y1 + SIZE
        color_id = (x+y)%2
        canvas.create_rectangle((x1,y1,x2,y2),fill=color[color_id],outline="")

label = tk.Label(fg="#7657FF",bg="#191d3f", text="Hello World!",font=("TkDefaultFont",55))
button = tk.Button(fg="#627cf3",bg="#23263d", text="Quit",font=("TkDefaultFont",20), command=root.destroy)

canvas.create_window(950,100,window=label, anchor="nw")
canvas.create_window(950,200,window=button, anchor="nw")

image_references = []
pieceid = []
def draw_board(fen_board:str):
    for piece in pieceid:
        canvas.delete(piece)
    pieceid.clear()
    image_references.clear()
    x = 0
    y = 0
    piece_dir = {
        "P":constance.piece_image_dir[7],
        "p":constance.piece_image_dir[6],
        "B":constance.piece_image_dir[1],
        "b":constance.piece_image_dir[0],
        "N":constance.piece_image_dir[5],
        "n":constance.piece_image_dir[4],
        "K":constance.piece_image_dir[3],
        "k":constance.piece_image_dir[2],
        "Q":constance.piece_image_dir[9],
        "q":constance.piece_image_dir[8],
        "R":constance.piece_image_dir[11],
        "r":constance.piece_image_dir[10],
    }
    for i in fen_board:
        if i == "/":
            y = y + 1
            x = 0
        elif i.isdigit():
            x = x +int(i)
        else:
            image = image_procesing(piece_dir[i])
            image_references.append(image)
            pieceid.append(canvas.create_image((x*SIZE) + (SIZE//2),(y*SIZE) + (SIZE//2),image=image,anchor="center"))
            x = x + 1

def in_area(xy1:tuple,xy2:tuple) -> bool:
    return xy2[0]<=xy1[0]<=xy2[0]+xy2[2] and xy2[1]<=xy1[1]<=xy2[1]+xy2[3]

possible_moves_selected = []
def gnrte_posible_moves(piece):
    for i in possible_moves_selected:
        canvas.delete(i)
    possible_moves_selected.clear()
    board.gnrte_attack_square(board.board_main.piece_list)
    piece_id_pm = piece.name+str(piece.x)+str(piece.y)
    print(board.possible_moves[piece_id_pm])
    moves = board.possible_moves.get(piece_id_pm, [])
    if moves:
        for i in board.possible_moves[piece_id_pm]:
            x = i[0]
            y = 7 -  i[1]
            possible_moves_selected.append(canvas.create_rectangle(x*SIZE,y*SIZE,x*SIZE+SIZE,y*SIZE+SIZE,outline="brown",width=2))

selected_square = None
is_piece_selected = False
selected_piece = None
def select_piece(event) -> None:
    global selected_square,is_piece_selected,selected_piece
    if in_area((event.x,event.y),(0,0,SIZE*8,SIZE*8)):
        if is_piece_selected:
            col = event.x // SIZE
            row = event.y // SIZE
            selected_piece.trymove(col,7-row)
            fen_board = board.update_fen_string(board.board.piece_list)
            fen_board,_ = fen_board.split(" ",1)
            draw_board(fen_board)
            is_piece_selected = False
            return None
        canvas.delete(selected_square)
        if in_area((event.x,event.y),(0,0,SIZE*8,SIZE*8)):
            col = event.x // SIZE
            row = event.y // SIZE
            selected_square = canvas.create_rectangle(col*SIZE,row*SIZE,col*SIZE+SIZE,row*SIZE+SIZE,outline="yellow",width=5)
            selected_piece = board.find_piece(col,7-row)
            if selected_piece is not None:
                is_piece_selected = True
                gnrte_posible_moves(selected_piece)
                return None
canvas.bind("<Button-1>",select_piece)

draw_board(board.fen_board)
root.mainloop()