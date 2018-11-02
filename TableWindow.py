#!/usr/bin/env python
#===============================================================================
# TableWindow
# 
# Description:
#     Script to test display table data in a tkiner window, resizable
#
# Version:
#    MM.mm    DD/MM/YY
#    00.01    25/06/18    First version with header code
#    00.02    29/06/18    Remove specific project references/scripts. Rename
#    from test4.py to TableWindow.py
#
# Example/Usage:
#
#===============================================================================


import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self, root, mylist):
        tk.Frame.__init__(self, root)
        
        self.canvas = tk.Canvas(root, borderwidth=0, background='#000000')
        self.frame = tk.Frame(self.canvas, background='#ffffff')
        self.vsb = tk.Scrollbar(root, orient='vertical', command=self.canvas.yview)
        self.hsb = tk.Scrollbar(root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)
 
        self.vsb.pack(side='right', fill='y')
        self.hsb.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor='nw', 
                                  tags='self.frame')
        self.frame.bind('<Configure>', self.onFrameConfigure)
        
        rows = len(mylist)
        cols = len(mylist[0])
        self._widgets = []
        self.populate(rows, cols, mylist)

    def populate(self, rows=5, columns=5, nestlist=[]):
        '''Put in some data'''

        for row_idx in range(rows):
            current_row = []
            for col_idx in range(columns):
                #print('data is:', nestlist[row_idx][col_idx])
                mylabel = tk.Label(self.frame, text=nestlist[row_idx][col_idx], borderwidth='1')
                mylabel.grid(row=row_idx+1, column=col_idx, padx=1, pady=1, sticky='nsew')
                current_row.append(mylabel)
            self._widgets.append(current_row)
            
        for col_idx in range(columns):
            self.grid_columnconfigure(col_idx, weight=1)

    def populateheader(self, columns=5, nestlist=[]):
        '''Put in some data'''
        for col_idx in range(columns):
            mylabel = tk.Label(self.frame, text=nestlist[col_idx], width=10, borderwidth=0)
            mylabel.grid(row=0, column=col_idx)
 
        self._widgets.append(mylabel)
        for col_idx in range(columns):
            self.grid_columnconfigure(col_idx, weight=1)
 
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
