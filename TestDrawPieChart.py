import tkinter as tk



class createTkPie(tk.Tk):

    def __init__(self, root):


        tk.Frame.__init__(self, root)

        self.FrameMaster = tk.Frame(root, borderwidth=2)
        self.FrameMaster.grid()

        self.createPercentages()


    def createPie(self, parent, x, y, rad, start, extent, fill, tag):
        self.arc = parent.create_arc(x-rad, y-rad, x+rad, y+rad,
                                            fill=fill, tag=tag,
                                            start=start, extent=extent)

    def createPercentages(self):
        arc10G = 10
        arc40G = 5
        arc100G = 40
        arc200G = 45

        percentages = [arc10G, arc40G, arc100G, arc200G]
        colors = ['orange', 'green', 'blue', 'pink']
        tags = ['10G', '40G', '100G', '200G']
        x = 100
        y = 100
        rad = 50
        st = 0

        self.pieHeader = tk.Label(self.FrameMaster, text='Pie Chart', borderwidth=2, bg='pink')
        self.pieDisplay = tk.Frame(self.FrameMaster)
        self.pieCanvas = tk.Canvas(self.pieDisplay, width=200, height=200, borderwidth=0,
                                highlightthickness=0, bg='grey')
        self.pieKey = tk.Frame(self.pieDisplay)
        self.pieHeader.grid(row=0, sticky='ew')
        self.pieDisplay.grid(row=1)

        self.pieCanvas.grid(row=0, column=0)
        self.pieKey.grid(row=0, column=1)

        parent = self.pieCanvas
        for i in range(len(percentages)):
            extent = percentages[i]/100*360
            self.createPie(parent, x, y, rad, st, extent, colors[i], tags[i])
            st = st + extent

        r = 0
        parent = self.pieKey
        for i in range(len(tags)):
            self.label = tk.Label(parent, text=tags[i], bg=colors[i])
            self.label.grid(row=r, sticky='new')
            r +=1



def main():
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d' % (400, 400, 100, 125))  # (x,y, posX, posY)
    root.title("Circles and Arcs")
    myPie = createTkPie(root)
    myPie.mainloop()

if __name__ == '__main__':
    main()