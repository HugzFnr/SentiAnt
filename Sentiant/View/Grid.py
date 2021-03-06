from tkinter import Frame, Label, Tk
from Sentiant.Model import QueenTile

from Sentiant.View.ImageManager import ImageManager

class Grid(Frame):

    def __init__(self, map, boss, size, master):
        self.buttons = []

        self.currentSelect = None

        # init Frame
        Frame.__init__(self, boss)
        self.config(width=size[0], height=size[1])

        # property
        self.map = map
        self.boss = master

        self.map.SetView(self)

        w = size[0] // map.layerFloor.GetWidth()
        h = size[1] // map.layerFloor.GetHeight()

        ImageManager.LoadImages((w, h))

        # create buttons
        for i in range(map.layerFloor.GetWidth()):
            self.buttons.append([])

            for j in range(map.layerFloor.GetHeight()):
                b = Label(self, width=w, height=h, image=ImageManager.EMPTY)
                b.grid(row=i, column=j, padx=0, pady=0)
                b.bind("<Button-1>", lambda event, ix = i, jx = j : self.Select(event, pos = (ix, jx)))
                self.buttons[-1].append(b)

        self.UpdateAll()

    def Select(self, event, pos):
        self.buttons[pos[0]][pos[1]].config(relief="groove")

        if self.currentSelect is not None:
            self.buttons[self.currentSelect[0]][self.currentSelect[1]].config(relief="flat")
        self.currentSelect = pos
        self.boss.Update()
        self.update_idletasks()

    def Update(self, x, y):
        tileSolid = self.map.layerSolid[x, y]
        tilePheromone = self.map.layerPheromone[x, y]
        tileFloor = self.map.layerFloor[x, y]

        img, bgc = None, None

        if isinstance(tileSolid, QueenTile):
            queensPos = self.map.layerSolid.GetQueenTiles(tileSolid.team)
            if x == queensPos[0][0] and y == queensPos[0][1]:
                img, bgc = ImageManager.GetContent(tileSolid, tileFloor, tilePheromone, metadata=0)
            elif x == queensPos[1][0] and y == queensPos[1][1]:
                img, bgc = ImageManager.GetContent(tileSolid, tileFloor, tilePheromone, metadata=1)
            elif x == queensPos[2][0] and y == queensPos[2][1]:
                img, bgc = ImageManager.GetContent(tileSolid, tileFloor, tilePheromone, metadata=2)
            else:
                img, bgc = ImageManager.GetContent(tileSolid, tileFloor, tilePheromone, metadata=3)
        else :
            img, bgc = ImageManager.GetContent(tileSolid, tileFloor, tilePheromone)

        self.buttons[x][y].config(image=img, bg=bgc, padx = 0, pady = 0)
        self.update_idletasks()

    def UpdateAll(self):
        for i in range(self.map.layerFloor.GetWidth()):
            for j in range(self.map.layerFloor.GetHeight()):
                self.Update(i, j)


if __name__ == "__main__":
    from Sentiant.Model.Point import Point
    from Sentiant.Model.Ant import Ant
    from Sentiant.Model.QueenTile import QueenTile
    from Sentiant.Model.MapManager import MapManager

    import os

    os.chdir("..\\..\\")
    print(os.getcwd())

    root = Tk()

    mapGen = MapManager(width=16, height=16)
    mapGen.RegisterQueen(QueenTile(1, "team"), Point(4, 4))

    map = mapGen.Generate()

    map.layerSolid.Append(Ant(1, "name", "team"), Point(6, 7))
    map.layerSolid.Append(Ant(1, "name", "team"), Point(5, 3))

    grid = Grid(boss=root, map=map, size=(480, 480))
    grid.pack()

    root.mainloop()
