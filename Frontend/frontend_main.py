import tkinter as tk
import subprocess as sp
root = tk.Tk()
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()
root.geometry(f"{str(ScreenWidth)}x{str(ScreenHeight)}")
root.title("Iwantstockfish")
root.configure(background='black')

tk.Label(fg="#7657FF",bg="#191d3f", text="Hello World!",font=("TkDefaultFont",70)).grid(column=0, row=0)
tk.Button(fg="#627cf3",bg="#23263d", text="Quit",font=("TkDefaultFont",20), command=root.destroy).grid(column=1, row=0)

root.mainloop()