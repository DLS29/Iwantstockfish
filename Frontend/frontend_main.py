import tkinter as tk
import subprocess as sp
from PIL import Image,ImageTk
import math
import constance

#board rendering will be done with FEN string for now
root = tk.Tk()
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()
root.geometry(f"{str(ScreenWidth)}x{str(ScreenHeight)}")
root.title("Iwantstockfish")
root.configure(bg="#2c2c2c")


class piece:
    def __init__(self,x,y,name,move_straight,move_diagonaly,custom_flag):
        pass
    def trymove(self,board):
        pass

def image_procesing(dir):
    image = Image.open(dir)
    image = image.resize((100,100))
    image = ImageTk.PhotoImage(image)
    return image

pawn_white_image = image_procesing(constance.piece_image_dir[7])
pawn_w1 = piece(0,0,"pawn",1,0,0)



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

label = tk.Label(fg="#7657FF",bg="#191d3f", text="Hello World!",font=("TkDefaultFont",70))
button = tk.Button(fg="#627cf3",bg="#23263d", text="Quit",font=("TkDefaultFont",20), command=root.destroy)

canvas.create_window(200,100,window=label, anchor="nw")
canvas.create_window(100,100,window=button, anchor="nw")
canvas.create_image(0,SIZE*7,image=pawn_white_image,anchor="nw")

root.mainloop()