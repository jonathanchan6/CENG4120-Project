import os
import argparse
import sys

class Cell:
    def __init__(self, locX, locY, width, height):
        assert isinstance(locX, float) or isinstance(locX, int)
        assert isinstance(locY, float) or isinstance(locY, int)
        assert isinstance(width, int) and isinstance(height, int)
        assert height in [8, 12]

        self.locX = locX
        self.locY = locY
        self.width = width
        self.height = height
        self.tempX = 0
        self.tempY = 0
        self.finalX = 0
        self.finalY = 0

class Row:
    def __init__(self, RY, Rheight, RX):
        assert isinstance(RY, int)
        assert Rheight in [8, 12]
        assert isinstance(RX, int)

        self.RY = RY
        self.Rheight = Rheight
        self.RX = RX
        self.pos = []
        self.w =[]
        self.CelloldX = []
        self.CelloldY = []
        self.Cellnum = []

class Solution:
    def __init__(self):
        self.clear()

    def clear(self):
        self.nSites = None
        self.nRows = None
        self.nTracks = None

        self.siteWidth = 0.216
        self.trackHeight = 0.27
        
        self.nCells = 0
        self.vCells = []
        self.name2CellId = {}
        
        self.vLegCells = []
        self.name2LegCellId = {}

        self.displBound = None
        
        self.n8 = 0
        self.n12 = 0
        self.rows = []


    def readInput(self, path):
        print("Reading Input...")
        with open(path, "r") as f:
            data = f.read().splitlines()

        for i, line in enumerate(data):
            tokens = line.strip().split(" ")
            tokens = [ elem.strip() for elem in tokens ]
            if i == 0:
                self.nRows, self.nSites = int(tokens[0]), int(tokens[1])
            elif i == 1:
                self.trackHeight, self.siteWidth = float(tokens[0]), float(tokens[1])
            elif i == 2:
                self.displBound = float(tokens[0])
            elif i == 3:
                self.nCells = int(tokens[0])
            else:
                name = tokens[0]
                locY, locX = float(tokens[1]), float(tokens[2])
                h, w = int(tokens[3]), int(tokens[4])
                if h == 8:
                    self.n8 = self.n8 + 1
                elif h == 12:
                    self.n12 = self.n12 + 1
                cell = Cell(locX, locY, w, h)
                self.name2CellId[name] = len(self.vCells)
                self.vCells.append(cell)
                
        assert len(self.vCells) == self.nCells
        assert len(self.vCells) == len(self.name2CellId)
        self.nTracks = 4 * self.nRows

    def getrow(self, result):
        print("Forming Row...")
        flag = 0
        if self.n8 >= self.n12:
            flag = 8
            if self.n12 == 0:
                ratio = -1
            else:
                ratio = int(self.n8 / self.n12)
        elif self.n12 > self.n8:
            flag = 12
            if self.n8 == 0:
                ratio = -1
            else:
                ratio = int(self.n12 / self.n8)
        nTracks = self.nTracks
        y = 0
        count = 0
        if flag == 8:
            while y < self.nTracks:
                count = count + 1
                if count % (ratio + 1) == 0 and ratio != -1:
                    if self.nTracks - y >= 12:
                        row = Row (y, 12, 0)
                        self.rows.append(row)
                        y = y + 12
                    else:
                        if self.nTracks - y >= 8:
                            row = Row (y, 8, 0)
                            self.rows.append(row)
                            y = y + 8
                        else:
                            y = self.nTracks
                else:
                    if self.nTracks - y >= 8:
                        row = Row (y, 8, 0)
                        self.rows.append(row)
                        y = y + 8
                    else:
                        y = self.nTracks
        elif flag == 12:
            while y < self.nTracks:
                count = count + 1
                if count % (ratio + 1) == 0 and ratio != -1:
                    if self.nTracks - y >= 8:
                        row = Row (y, 8, 0)
                        self.rows.append(row)
                        y = y + 8
                    else:
                        y = self.nTracks
                else: 
                    if self.nTracks - y >= 12:
                        row = Row (y, 12, 0)
                        self.rows.append(row)
                        y = y + 12
                    else:
                        if self.nTracks - y >= 8:
                            row = Row (y, 8, 0)
                            self.rows.append(row)
                            y = y + 8
                        else:
                            y = self.nTracks
        result = result + str(len(self.rows)) + "\n"
        for i in range(len(self.rows)):
            result = result + str(self.rows[i].RY) + " " + str(self.rows[i].Rheight) + "\n"

        return result

    def displacement(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(x1 - x2)
        disp = dx*dx + dy*dy
        return disp

    def implement(self, result):
        print("Implementing...")
        #legalization
        for i in range(len(self.vCells)):
            disp = sys.maxsize
            for j in range(len(self.rows)):
                temp = self.displacement(self.vCells[i].locX, self.vCells[i].locY, self.rows[j].RX, self.rows[j].RY)
                if temp < disp and self.vCells[i].height == self.rows[j].Rheight and self.nSites - self.rows[j].RX >= self.vCells[i].width:
                    disp = temp
                    rowInsert = j
            self.vCells[i].tempX = self.rows[rowInsert].RX
            self.vCells[i].tempY = self.rows[rowInsert].RY
            self.rows[rowInsert].pos.append(self.vCells[i].tempX)
            self.rows[rowInsert].w.append(self.vCells[i].width)
            self.rows[rowInsert].CelloldX.append(self.vCells[i].locX)
            self.rows[rowInsert].CelloldY.append(self.vCells[i].locY)
            self.rows[rowInsert].Cellnum.append(i)
            self.rows[rowInsert].RX = self.rows[rowInsert].RX + self.vCells[i].width
        #Detailed Placement
        for i in range(len(self.rows)):
            last = self.nSites
            for j in reversed(range(len(self.rows[i].pos))):
                disp = sys.maxsize
                for k in range(self.rows[i].pos[j], last - self.rows[i].w[j] + 1):
                    temp = self.displacement(self.rows[i].CelloldX[j], self.rows[i].CelloldX[j], k, self.rows[i].RY)
                    if temp <= disp:
                        disp = temp
                        finalpos = k
                self.vCells[self.rows[i].Cellnum[j]].finalX = finalpos
                self.vCells[self.rows[i].Cellnum[j]].finalY = self.vCells[self.rows[i].Cellnum[j]].tempY
                last = finalpos
                
        for i in range(len(self.vCells)):
            if i == len(self.vCells) - 1:
                result = result + "c" + str(i) + " " + str(self.vCells[i].finalY) + " " + str( self.vCells[i].finalX)
            else:
                result = result + "c" + str(i) + " " + str(self.vCells[i].finalY) + " " + str( self.vCells[i].finalX) + "\n"
        return result

    def result(self, path):
        self.clear()
        result = ""
        self.readInput(path)
        result = self.getrow(result)
        result = self.implement(result)
        return result

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("usage: python alpha.py <in_file> <out_file>")
        exit(1)
    in_file, out_file = sys.argv[1], sys.argv[2]
    sol = Solution()
    result = sol.result(in_file)
    print("Finish!")
    with open(out_file, 'w') as f:
        sys.stdout = f
        print(result)
        sys.stdout = sys.__stdout__