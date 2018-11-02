#!/usr/bin/env python
# ===============================================================================
# TableTester
#
# Description:
#    Script to write scripts to test Tk GUI applications
#
#
# Version:
#    MM.mm    DD/MM/YY
#    00.00    31/10/18    Initial file
#
# Example/Usage:
#
# ===============================================================================

import logging
import os
import random
import threading
import time
import tkinter as tk
import tkinter.scrolledtext as ScrolledText
from tkinter.filedialog import askopenfilename

class createTkGUI(tk.Tk):

    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.tkArea = tk.Frame(root, borderwidth=1, background='#000000')
        self.tkArea.pack(side='left', fill='both', expand=True)

        self.canvasArea = tk.Canvas(self.tkArea, background='#087654')
        self.frameArea = tk.Frame(self.canvasArea, background='#ffaaff')
        self.vertScBar = tk.Scrollbar(self.canvasArea, orient='vertical', command=self.canvasArea.yview)
        self.horzScBar = tk.Scrollbar(self.canvasArea, orient='horizontal', command=self.canvasArea.xview)
        self.canvasArea.configure(yscrollcommand=self.vertScBar.set)
        self.canvasArea.configure(xscrollcommand=self.horzScBar.set)

        self.vertScBar.pack(side='right', fill='y')
        self.horzScBar.pack(side='bottom', fill='x')
        self.canvasArea.pack(side='left', fill='both', expand=True)
        self.canvasArea.create_window((4, 4), window=self.frameArea, anchor='nw')
        self.frameArea.bind('<Configure>', self.onFrameConfigure)

        self.logArea = tk.Canvas(self.tkArea, background='#512345')
        self.logMArea = tk.Frame(self.logArea, background='#AB00EF')
        self.lvScBar = tk.Scrollbar(self.logArea, orient='vertical', command=self.logArea.yview)
        self.lhScBar = tk.Scrollbar(self.logArea, orient='horizontal', command=self.logArea.xview)
        self.logArea.configure(yscrollcommand=self.lvScBar.set)
        self.logArea.configure(xscrollcommand=self.lhScBar.set)

        self.lvScBar.pack(side='right', fill='y')
        self.lhScBar.pack(side='bottom', fill='x')
        self.logArea.pack(side='right', fill='both', expand=True)
        self.logArea.create_window((4,4), window=self.logMArea, anchor='ne')
        self.logMArea.bind('<Configure>', self.onMFrameConfigure)

        logRows = 1
        self.buildMenus()
        root.config(menu=self.menuBar)
        self.displayTestTable()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvasArea.configure(scrollregion=self.canvasArea.bbox("all"))

    def onMFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.logArea.configure(scrollregion=self.logArea.bbox("all"))

    # create callback functions
    def closeTkGUI(self):
        self.destroy()

    def openFile(self, filext='*.txt', prompt='Select File'):
        lenFileXt = len(filext) - 1
        rootfilechooser = tk.Tk()
        fileOpen = askopenfilename(title = prompt,
                                   filetypes = (('text files', filext),
                                                ('all files', '*.*')))
        dirOpen = os.path.split(fileOpen)[0]
        fileName = os.path.split(fileOpen)[1][:-lenFileXt]
        rootfilechooser.destroy()

        self.writeLogArea('Opened File')

    def displayTestTable(self):
        myList = createTestList()
        rows = len(myList)
        cols = len(myList[0])
        index = 0

        for row_idx in range(rows):
            current_row = []
            for col_idx in range(cols):
                self.label = tk.Label(self.frameArea, text=myList[row_idx][col_idx], borderwidth='1')
                self.label.grid(row=row_idx+1, column=col_idx, padx=1, pady=1, sticky='nsew')
                current_row.append(self.label)
        for col_idx in range(cols):
            self.frameArea.grid_columnconfigure(col_idx, weight=1)

        self.writeLogArea('Built Table')

    def writeLogArea(self, logText='Template'):
        logLabel = tk.Label(self.logMArea, text=logText)
        logLabel.grid(row=1)

    def clearLogArea(self):
        self.logMArea.destroy()
        self.logMArea = tk.Frame(self.logArea, background='#90c4e2')
        self.logArea.create_window((4, 4), window=self.logMArea, anchor='nw')
        self.logMArea.bind('<Configure>', self.onMFrameConfigure)
        logRows = 0

    def clearTestTable(self):
        self.frameArea.destroy()
        self.frameArea = tk.Frame(self.canvasArea, background='#45aaff')
        self.canvasArea.create_window((4, 4), window=self.frameArea, anchor='nw')
        self.frameArea.bind('<Configure>', self.onFrameConfigure)
        self.writeLogArea('Cleared Table')

    def buildMenus(self):
        self.menuBar = tk.Menu(self)
        self.mainMenu = tk.Menu(self.menuBar, tearoff=0)
        self.mainMenu.add_command(label='Open File', command=self.openFile)
        self.mainMenu.add_command(label='Exit', command=self.closeTkGUI)
        self.menuBar.add_cascade(label='File', menu=self.mainMenu)

        self.tableMenu = tk.Menu(self.menuBar, tearoff=0)
        self.tableMenu.add_command(label='Display Table', command=self.displayTestTable)
        self.tableMenu.add_command(label='Clear Table', command=self.clearTestTable)
        self.menuBar.add_cascade(label='Table', menu=self.tableMenu)

        self.logMenu = tk.Menu(self.menuBar, tearoff=0)
        self.logMenu.add_command(label='Write Log', command=self.writeLogArea)
        self.logMenu.add_command(label='Clear Log', command=self.clearLogArea)
        self.menuBar.add_cascade(label='Logging', menu=self.logMenu)


def createTestList():
    # unit test function

    # create a 2-D (list of a list) for input into test functions
    myList = []
    singleLine = []
    speedOfLight = 299792458
    FreqInit = 195.900 # 1530.33
    Lambdas = 40
    Rates = ['1G', '2.5G', '10G', '40G', '100G', '200G']
    Types = ['CB', 'MET', 'MIX', 'NOK', 'SONET', 'TEST', 'VID', 'OTN']

    # single elements
    for idx in range(0,Lambdas):
        Circuit = 'Circuit' + str(idx)
        Side ='SideA'
        ToSide = 'SideB'
        LambdaX = round(speedOfLight / FreqInit / 1000, 2)
        DataRate = random.choice(Rates)
        CozBiz = random.choice(Types)

        singleLine.extend((Circuit, Side, ToSide, LambdaX, DataRate, CozBiz))
        myList.append(singleLine)
        singleLine = []
        FreqInit = FreqInit - 0.100

    return myList


def main():
    myList = createTestList()
    #displayTable(myList)

    root = tk.Tk()
    root.geometry('%dx%d+%d+%d' % (500, 700, 100, 125))  # (x,y, posX, posY)
    root.title('WaveTrails Tk GUI')
    myGUI = createTkGUI(root)
    myGUI.mainloop()


if __name__ == '__main__':
    main()