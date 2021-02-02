import tkinter as tk
#import tkFileDialog as tkfd

class AppButton:
    #simple button construction
    #create a button with chosen arguments
    def create_button(self, words, rownum, frame):
        btn = tk.Button(frame, text = words)
        btn.grid(row = rownum, column = 2)

    def create_entry(self, rownum, frame):
        txt = tk.Entry(frame)
        txt.grid(row = rownum, column = 1)

    def create_label(self, words, rownum, frame):
        lbl = tk.Label(frame, text = words)
        lbl.grid(row = rownum, column = 0)

    #input is composed of a Label, an Entry, and a Button. calls the three funcs above
    def create_input(self, words, rownum, frame):
        self.create_label(words, rownum, frame)
        self.create_entry(rownum, frame)
        self.create_button("OK", rownum, frame)

class Application(tk.Frame):
    """A GUI application that creates multiple buttons"""

    #create a class variable from the root(master) called by the constructor
    def __init__(self, master):
        self.master = master
        master.title("The best GUI")
        tk.Frame.__init__(self, master, width=200, height=200)
        self.grid(row = 0, column = 0)

    def new_frame(self, master, color, row, column):
        frame = tk.Frame(master, width=200, height=200, bg=color)
        frame.grid(row = row, column = column)
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Button Test Launch")
    app = Application(root)
    appbutton = AppButton()
    frame1 = app.new_frame(root, "red", 3, 1)
    frame2 = app.new_frame(root, "blue", 2, 2)
    appbutton.create_input("test1", 0, root)
    appbutton.create_input("TableSimple", 1, root)
    appbutton.create_input("test3", 2, root)
    appbutton.create_input("TableWindow", 3, root)
    root.mainloop()