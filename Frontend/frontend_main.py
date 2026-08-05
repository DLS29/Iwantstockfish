import tkinter as tk
import subprocess as sp
root = tk.Tk()
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()
root.geometry(f"{str(ScreenWidth)}x{str(ScreenHeight)}")
root.title("Iwantstockfish")

#creation of bacground
SIZE = int((ScreenHeight*0.8)/8)
canvas = tk.Canvas(root, width=SIZE*8,height=SIZE*8,highlightthickness=0,bg="#aaaaaa")
canvas.pack(padx=50)
color = ["#c7e4cd","#09af03"]

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

root.mainloop()