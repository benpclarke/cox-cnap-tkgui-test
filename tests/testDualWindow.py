import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.withdraw()

list_of_windows = []

def close_window(tw):
    i = list_of_windows.index(tw)
    list_of_windows[i].destroy()
    del list_of_windows[i]
    if len(list_of_windows) == 0:
        root.destroy()
        print("root destroyed!")

X = 50
Y = 50
for i in range(0,3):
    x = tk.Toplevel(root)
    x.title("Error Box!")
    W = 250
    H = 100
    X += 250
    x.geometry('%dx%d+%d+%d' % (W, H, X, Y))
    # x.resizable(False, False)
    ttk.Label(x, text="oops").pack()
    # ttk.Button(x, text=" OK ", command=lambda tw=x: close_window(tw)).pack(side=tk.BOTTOM)
    # x.protocol("WM_DELETE_WINDOW", lambda tw=x: close_window(tw))
    # list_of_windows.append(x)

root.mainloop()