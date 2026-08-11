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
def draw_board(fen_board:str):
    x = 0
    y = 7
    piece_dir = {
        "P":constance.piece_image_dir[7],
        "p":constance.piece_image_dir[6],
        "B":constance.piece_image_dir[1],
        "b":constance.piece_image_dir[0],
        "N":constance.piece_image_dir[5],
        "n":constance.piece_image_dir[4],
        "K":constance.piece_image_dir[5],
        "k":constance.piece_image_dir[4],
        "Q":constance.piece_image_dir[9],
        "q":constance.piece_image_dir[8],
        "R":constance.piece_image_dir[11],
        "r":constance.piece_image_dir[10],
    }
    for i in fen_board:
        if i == "/":
            y = y - 1
            x = 0
        elif i.isdigit():
            x = x +int(i)
        else:
            image = image_procesing(piece_dir[i])
            image_references.append(image)
            canvas.create_image((x*SIZE) + (SIZE//2),(y*SIZE) + (SIZE//2),image=image,anchor="center")
            x = x + 1
draw_board(board.fen_board)
root.mainloop()