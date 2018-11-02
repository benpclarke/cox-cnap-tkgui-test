#!/usr/bin/env python
#===============================================================================
# TableSimple
#
# Description:
#     Script to test display table data in a tkiner window, resizable
#
# Version:
#    MM.mm    DD/MM/YY
#    00.01    31/10/18    First version with header code
#
# Example/Usage:
#
#===============================================================================

import tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self, mylist):
        tk.Tk.__init__(self)

        rows = len(mylist)
        cols = len(mylist[0])
        
        t = SimpleTable(self, rows, cols, mylist)
        t.pack(side="top", fill="x")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2, nestlist=[]):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text=nestlist[row][column], #"%s/%s" % (row, column), 
                                 borderwidth=0) #, width=10)
                label.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

#if __name__ == "__main__":
#    app = ExampleApp()
#    app.mainloop()