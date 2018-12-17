from tkinter import  VERTICAL, HORIZONTAL, N, S, E, W, Scrollbar, Canvas
from tkinter import Toplevel, Button, StringVar, Label
from Sentiant.Model import Ant
from .Grid import Grid

class MainView(Toplevel):
    def __init__(self, map, turnmanager = None, size= 500):
        # Init Window
        Toplevel.__init__(self)

        # property
        self.Map = map
        self.TurnManager = turnmanager

        # scrollbars
        vsb = Scrollbar(self, orient=VERTICAL)
        vsb.grid(row=0, column=2, rowspan = 10, sticky=N+S)

        hsb = Scrollbar(self, orient=HORIZONTAL)
        hsb.grid(row=11, column=1, sticky=E+W)

        canvas = Canvas(self, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        canvas.config(width=size + 100)
        canvas.grid(row=0, column=1, rowspan = 10, sticky="news")

        vsb.config(command=canvas.yview)
        hsb.config(command=canvas.xview)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid = Grid(self.Map, canvas, size=(size, size), master=self)
        self.grid.pack()

        if turnmanager is not None:
            self.bNextTurn = Button(self, text = "Next Turn", command=self.TurnManager.NextTurn)
            self.bNextTurn.grid(column = 3, row = 0)

        self.lbl1 = StringVar()
        Label(self, textvariable=self.lbl1).grid(column = 0, row =0)

        canvas.create_window(0, 0, window=self.grid)
        self.grid.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        self.bind_all("<MouseWheel>", lambda e: self.Scroll(canvas, e))

    def Update(self):
        pos = self.grid.currentSelect
        ant = self.Map.layerSolid[pos[0], pos[1]]
        self.UpdateLabel(ant)

    def UpdateLabel(self, ant):
        if isinstance(ant, Ant):
            self.lbl1.set(str(ant))
        else:
            self.lbl1.set("")

        self.update_idletasks()


    def Scroll(self, canvas, event):
        if event.state & 4:
            global tileSize
            tileSize+= event.delta // 120

            for row in self.grid:
                for it in row:
                    it.configure(width=tileSize, height=tileSize)

            canvas.update_idletasks()
            self.update_idletasks()

        elif event.state & 1:
            canvas.xview_scroll(-event.delta // 120, "units")
        else:
            canvas.yview_scroll(-event.delta // 120, "units")

    def Run(self):
        self.mainloop()
