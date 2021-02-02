import tkinter as tk
from OpenFileWaveTrails import openRawFile
from SetMetroName import MetroLookup
from WLEN import drawOffset


class createTkGUI(tk.Tk):

    def __init__(self, root, metroDB):

        self.COLORTBLHD = '#a6a6a6'
        self.COLORRDC = '#c55a11'
        self.COLORMTC = '#bf9000'
        self.COLORSTC = '#2e75b5'
        self.COLORCOLO = '#538135'
        self.COLORGT = '#7f7f7f'
        self.COLOR30 = '#c4d79b'
        self.COLOR50 = '#9bc2e6'
        self.COLOR70 = '#ffc000'
        self.COLOR100 = '#ff0000'
        self.FIELDMARKET = 'Market'
        self.FIELDWAVES = 'Waves'

        tk.Frame.__init__(self, root)
        self.displayDiagram(metroDB)

    def displayDiagram(self, metroDB):
        w = 800
        h = 700
        x = 100
        y = 100
        self.diagram = tk.Tk()
        self.diagram.geometry('%dx%d+%d+%d' % (w,h,x,y))
        self.diagram.title(metroDB[self.FIELDMARKET])

        # tkinter variable with initial setting
        self.FrameDiagram = tk.Frame(self.diagram)
        self.FrameDiagram.grid(sticky='ew')

        self.DiagramHeader = tk.Label(self.FrameDiagram, text=metroDB[self.FIELDMARKET],
                                      bg=self.COLORTBLHD)
        self.DiagramDisplay = tk.Frame(self.FrameDiagram, bd=1, relief='groove')
        self.DiagramHeader.grid(sticky='ew')
        self.DiagramDisplay.grid(sticky='ew')

        self.DiagramCanvas = tk.Canvas(self.DiagramDisplay, width=w-20, height=h-60)
        self.DiagramKey = tk.Frame(self.DiagramDisplay)
        self.DiagramCanvas.grid(row=0, column=0)
        self.DiagramKey.grid(row=0, column=1)

        self.createDiagram(self.DiagramCanvas, metroDB)
        self.diagram.focus_force()
        self.diagram.mainloop()

    def colorSite(self, data):
        if data == 'RDC': color = self.COLORRDC
        elif data == 'MTC': color = self.COLORMTC
        elif data == 'STC': color = self.COLORSTC
        elif data == 'Colo': color = self.COLORCOLO
        elif data == 'GT': color = self.COLORGT
        else: color = 'black'
        return color

    def colorLink(self, data):
        if data < 0.3: color = self.COLOR30
        elif data < 0.5: color = self.COLOR50
        elif data < 0.7: color = self.COLOR70
        else: color = self.COLOR100 # data > 0.7:
        return color

    def createSite(self, parent, x, y, rad, label, fill):
        x0 = x-rad
        y0 = y-rad
        x1 = x + rad
        y1 = y + rad
        self.arc = parent.create_oval(x0, y0, x1, y1, fill=fill)
        self.site = parent.create_text(x,y,text=label)

    def createLink(self, parent, x0, y0, x1, y1, fill):
        self.link = parent.create_line(x0, y0, x1, y1, fill=fill, width=5)

    def createDiagram(self, parent, metroDB):
        rad = 20
        Waves = metroDB[self.FIELDWAVES]
        dictSites = [v for k,v in metroDB.items() if k == 'dictSites'][0]
        dictLinks = [v for k,v in metroDB.items() if k == 'dictLinks'][0]
        dictSites = drawOffset(dictSites) # updates proportional spacing

        for c,f in dictLinks.items():
            offset = f['Offset']
            color = self.colorLink(f['Chans']/Waves)

            for k,v in dictSites.items():
                if f['SideA'][:-2] == v['TID']:
                    x0 = v['xLoc']
                    y0 = v['yLoc']
                if f['SideZ'][:-2] == v['TID']:
                    x1 = v['xLoc']
                    y1 = v['yLoc']
            if x0 > x1:
                x0 = x0 - rad/2
                x1 = x1 + rad/2
            elif x0 < x1:
                x0 = x0 + rad / 2
                x1 = x1 - rad / 2
            if y0 > y1:
                y0 = y0 - rad/2
                y1 = y1 + rad/2
            elif y0 < y1:
                y0 = y0 + rad / 2
                y1 = y1 - rad / 2
            if offset != 0: # e.g. duplicate link or return side
                if offset == 1:
                    x0 -= 10
                    x1 -= 10
                elif offset == 2:
                    y0 -= 10
                    y1 -= 10
            self.createLink(parent, x0, y0, x1, y1, color)

        for k,v in dictSites.items():
            color = self.colorSite(v['Type'])
            label = v['Name']
            self.createSite(parent, v['xLoc'], v['yLoc'], rad, label, color)


def main():
    fileName = openRawFile()[0]
    metroDB = MetroLookup(fileName)

    root = tk.Tk()
    root.geometry('%dx%d+%d+%d' % (800, 700, 100, 100))  # (x,y, posX, posY)
    root.title(metroDB['Market'])

    myGUI = createTkGUI(root, metroDB)
    myGUI.mainloop()


if __name__ == '__main__':
    main()