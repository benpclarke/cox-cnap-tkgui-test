#!/usr/bin/env python
# ===============================================================================
# GUITester
#
# Description:
#    Script to write scripts to test Tk GUI applications
#
#
# Version:
#    MM.mm    DD/MM/YY
#    00.00    02/11/18    Initial file
#
# Example/Usage:
#
# ===============================================================================

from datetime import datetime
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

        # initialize global Frame area under root
        self.tkArea = tk.Frame(root, borderwidth=2, background='#0ff00f')
        self.tkArea.grid(row=0, column=0, sticky='nsew')
        #self.tkArea.pack(side='left', fill='both', expand=True)

        # create two container frames within the globalframe
        self.FrameLeft = tk.Frame(self.tkArea, bg='#001155')
        self.FrameRight = tk.Frame(self.tkArea, bg='#66aaff')
        self.FrameLeft.grid(row=0, column=0)
        self.FrameRight.grid(row=0, column=1)

        # initialize Table Area under tkArea
        self.TableContainer = tk.Canvas(self.FrameLeft, background='#087654')
        self.TableContainerVScroll = tk.Scrollbar(self.FrameLeft, orient='vertical',
                                                  command=self.TableContainer.yview)
        self.TableContainerHScroll = tk.Scrollbar(self.FrameLeft, orient='horizontal',
                                                  command=self.TableContainer.xview)
        self.TableFrame = tk.Frame(self.TableContainer,  background='#ffaa60')
        self.TableContainer.configure(yscrollcommand=self.TableContainerVScroll.set)
        self.TableContainer.configure(xscrollcommand=self.TableContainerHScroll.set)

        # align & grid Table Area elements
        self.TableContainer.grid(row=0, column=0, sticky='nsew')
        self.TableFrame.grid(row=0, column=0, ipadx=200, ipady=300, sticky='nsew')
        self.TableContainerHScroll.grid(row=1, column=0, sticky='sew')
        self.TableContainerVScroll.grid(row=0, column=1, sticky='nse', rowspan=2)
        self.TableContainer.create_window((0, 0), window=self.TableFrame, anchor='nw')
        self.TableFrame.bind('<Configure>', self.onFrameConfigure)

        # initialize Log Area under tkArea
        self.LogContainer = tk.Canvas(self.FrameRight, background='#013579')
        self.LogContainerVScroll = tk.Scrollbar(self.FrameRight, orient='vertical',
                                                  command=self.LogContainer.yview)
        self.LogContainerHScroll = tk.Scrollbar(self.FrameRight, orient='horizontal',
                                                  command=self.LogContainer.xview)
        self.LogFrame = tk.Frame(self.LogContainer, background='#deaaff')
        self.logLabel = tk.Label(self.LogFrame, text='Log Area goes here', justify='left')
        self.LogContainer.configure(yscrollcommand=self.LogContainerVScroll.set)
        self.LogContainer.configure(xscrollcommand=self.LogContainerHScroll.set)

        # align & grid Log Area elements
        self.LogContainer.grid(row=0, column=1, sticky='nsew')
        self.LogFrame.grid(row=0, column=0, ipadx=50, ipady=300, sticky='nsew')
        self.LogContainerHScroll.grid(row=1, column=0, sticky='sew', columnspan=2)
        self.LogContainerVScroll.grid(row=0, column=1, sticky='nse', rowspan=2)
        self.logLabel.grid(row=0, column=0, sticky='ew')
        self.LogContainer.create_window((0,0), window=self.LogFrame, anchor='nw')
        self.LogFrame.bind('<Configure>', self.onMFrameConfigure)

        self.buildMenus()
        root.config(menu=self.menuBar)
        self.writeLogArea('Initialized and put a lot of text in the log area')
        #self.displayTestTable()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.TableContainer.configure(scrollregion=self.TableContainer.bbox("all"))

    def onMFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.LogContainer.configure(scrollregion=self.LogContainer.bbox("all"))

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

        for row_idx in range(rows):
            current_row = []
            for col_idx in range(cols):
                self.label = tk.Label(self.TableFrame, text=myList[row_idx][col_idx], borderwidth='1')
                self.label.grid(row=row_idx+1, column=col_idx, padx=1, pady=1, sticky='nsew')
                current_row.append(self.label)
        for col_idx in range(cols):
            self.TableFrame.grid_columnconfigure(col_idx, weight=1)

        self.writeLogArea('Built Table')

    def writeLogArea(self, logText='Default log statement'):
        currentText = self.logLabel.cget('text')
        print(currentText)
        logStatement = 'log %s>> %s' % (str(datetime.now()), logText)
        logUpdate = currentText + '\n' + logStatement
        self.logLabel.config(text=logUpdate)

    def clearLogArea(self):
        self.LogFrame.destroy()
        self.LogFrame = tk.Frame(self.LogContainer, background='#90c4e2')
        self.LogFrame.grid(row=0, column=0, ipadx=50, ipady=300, sticky='nsew')
        self.LogContainer.create_window((0, 0), window=self.LogFrame, anchor='nw')
        self.LogFrame.bind('<Configure>', self.onMFrameConfigure)
        self.logLabel = tk.Label(self.LogFrame, text='', justify='left')
        self.logLabel.grid(row=0, column=0, sticky='ew')
        self.writeLogArea('Cleared Logging Area')

    def clearTestTable(self):
        self.TableFrame.destroy()
        self.TableFrame = tk.Frame(self.TableContainer, background='#45aaff')
        self.TableFrame.grid(row=0, column=0, ipadx=200, ipady=300, sticky='nsew')
        self.TableContainer.create_window((0, 0), window=self.TableFrame, anchor='nw')
        self.TableFrame.bind('<Configure>', self.onFrameConfigure)
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
        Circuit = 'This is a really long and has lots of text in the name of the Circuit' + str(idx)
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
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d' % (900, 700, 100, 125))  # (x,y, posX, posY)
    root.title('WaveTrails Tk GUI')
    myGUI = createTkGUI(root)
    myGUI.mainloop()


if __name__ == '__main__':
    main()