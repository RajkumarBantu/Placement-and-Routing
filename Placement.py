import random
import sys
import math
import time
from typing import List, Tuple

def sortbysecdesc(item):
    return item[1]

class edgeConnect:
    def __init__(self):
        self.edge = 0
        self.terminal = (0, 0)

class occLoc:
    def __init__(self):
        self.CellNum = 0
        self.occupied = False
        self.locked = False

class CellPos:
    def __init__(self):
        self.x_data = -1
        self.y_data = -1

def write_cells_to_mag(Cellsptr, BoundingBox, ConnList, OutputMag):
    mag_scale = 20
    OutMag = open(OutputMag, 'w')
    OutMag.write("magic\n")
    OutMag.write("tech scmos\n")
    OutMag.write("timestamp\n")
  
    OutMag.write("<< pdiffusion >>\n")
    for i in range(1, len(ConnList)):
        rel_x = Cellsptr[i].x_data * mag_scale
        rel_y = Cellsptr[i].y_data * mag_scale

        OutMag.write("rect {} {} {} {}\n".format(rel_x, rel_y, rel_x+1, rel_y+1))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+2, rel_y, rel_x+3, rel_y+1))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+3, rel_y, rel_x+4, rel_y+1))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+5, rel_y, rel_x+6, rel_y+1))

        OutMag.write("rect {} {} {} {}\n".format(rel_x, rel_y+1, rel_x+6, rel_y+5))

        OutMag.write("rect {} {} {} {}\n".format(rel_x, rel_y+5, rel_x+1, rel_y+6))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+2, rel_y+5, rel_x+3, rel_y+6))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+3, rel_y+5, rel_x+4, rel_y+6))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+5, rel_y+5, rel_x+6, rel_y+6))

    OutMag.write("<< polysilicon >>\n")
    for i in range(1, len(ConnList)):
        rel_x = Cellsptr[i].x_data * mag_scale
        rel_y = Cellsptr[i].y_data * mag_scale

        OutMag.write("rect {} {} {} {}\n".format(rel_x+1, rel_y-1, rel_x+2, rel_y+1))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+4, rel_y-1, rel_x+5, rel_y+1))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+1, rel_y+5, rel_x+2, rel_y+7))
        OutMag.write("rect {} {} {} {}\n".format(rel_x+4, rel_y+5, rel_x+5, rel_y+7))

    OutMag.write("<< labels >>\n")
    for i in range(1, len(ConnList)):
        rel_x = Cellsptr[i].x_data * mag_scale
        rel_y = Cellsptr[i].y_data * mag_scale

        OutMag.write("rlabel pdiffusion {} {} {} {} 0 Cellno = {}\n".format(rel_x+3, rel_y+3, rel_x+4, rel_y+4, i))

    OutMag.write("<< end >>\n")
    OutMag.close()

def SPWL(ConnList, Cellsptr):
    est_length = 0.00
    for i in range(1, len(ConnList)):
        for z in ConnList[i]:
            est_length += abs(Cellsptr[i].x_data - Cellsptr[z.edge].x_data) + abs(Cellsptr[i].y_data - Cellsptr[z.edge].y_data)
    return est_length/2

def findNearestvacant(BoundingBox, x_loc, y_loc):
    VacancyList = []
    nearestVac = CellPos()

    for i in range(len(BoundingBox)):
        for j in range(len(BoundingBox)):
            if BoundingBox[i][j].CellNum == 0:
                VacancyList.append((i,j))   # go through all cells and get vacant coords list

    nearestVac.x_data = VacancyList[0][0]
    nearestVac.y_data = VacancyList[0][1]
    curr_dist_from_cell = abs(nearestVac.x_data - x_loc) + abs(nearestVac.y_data - y_loc)

    for k in range(1, len(VacancyList)):
        new_dist_from_cell = abs(VacancyList[k][0] - x_loc) + abs(VacancyList[k][1] - y_loc)
        if new_dist_from_cell < curr_dist_from_cell:
            curr_dist_from_cell = new_dist_from_cell
            nearestVac.x_data = VacancyList[k][0]
            nearestVac.y_data = VacancyList[k][1]  # getting nearest vacant location from a given x,y

    return nearestVac

start_time = time.time()

tot_cells = 0
tot_nets = 0

inputfile = "b_2000_2000"

with open(inputfile, 'r') as infile:
    lines = infile.readlines()

    for i in range(2):
        line = lines[i].strip()
        if i == 0:
            tot_cells = int(line)
            print("total cells =", tot_cells)
        elif i == 1:
            tot_nets = int(line)
            print("total nets =", tot_nets)

    ConnList = [[] for _ in range(tot_cells+1)]
    ConnFreq = [(0, 0) for _ in range(tot_cells+1)]

    netnum = 0
    node1 = 0
    node2 = 0
    netcount = 0
    foundFlag = 0
    term1 = 0
    term2 = 0

    for i in range(2, len(lines)):
        line = lines[i].strip()
        words = line.split()
        for j in range(0, len(words), 5):
            netnum = int(words[j])
            node1 = int(words[j+1])
            term1 = int(words[j+2])
            node2 = int(words[j+3])
            term2 = int(words[j+4])

            tempObj = edgeConnect()
            tempObj.edge = node2
            tempObj.terminal = (term1, term2)
            ConnList[node1].append(tempObj)

            tempObj = edgeConnect()
            tempObj.edge = node1
            tempObj.terminal = (term2, term1)
            ConnList[node2].append(tempObj)


unconnected_cells = 0

for i in range(tot_cells + 1):
    ConnFreq.append([i, len(ConnList[i])])
    if len(ConnList[i]) == 0:
        unconnected_cells += 1

ConnFreq.sort(key=lambda x: x[1], reverse=True)

tot_cells_matrix = int(math.sqrt(tot_cells)) + 1
unconnected_rows = (unconnected_cells // tot_cells_matrix) + 1
print("unconnected rows = ", unconnected_rows)


BoundingBox = [[occLoc() for j in range(tot_cells_matrix+1+unconnected_rows)] for i in range(tot_cells_matrix+1+unconnected_rows)]
print("size is", len(BoundingBox), len(BoundingBox[1]))

Cells = [CellPos() for i in range(tot_cells+1)]

# InitialRandomPlacement
for i in range(1, tot_cells + 1):
    if not ConnList[i]:
        continue
    x_cord, y_cord = random.randint(0, len(BoundingBox) - 1), random.randint(0, len(BoundingBox) - 1)
    while BoundingBox[x_cord][y_cord].occupied != 0:
        x_cord, y_cord = random.randint(0, len(BoundingBox) - 1), random.randint(0, len(BoundingBox) - 1)
    Cells[i].x_data = x_cord
    Cells[i].y_data = y_cord
    BoundingBox[x_cord][y_cord].CellNum = i
    BoundingBox[x_cord][y_cord].occupied = 1

initial_SPWL = SPWL(ConnList, Cells)
print("initial length = ", initial_SPWL)
iter = 1
iter_limit = 6
sorted_item = 0
abort_count = 0
abort_limit = 6
end_ripple = False
CompletedList = [False] * (tot_cells + 1)
cells_moved_counter = 1
continue_loop = 1

# begin Force Directed Placement
iter = 1
while iter <= iter_limit:
    print("iteration number", iter)
    if sorted_item >= tot_cells - unconnected_cells:
        sorted_item = 0
    print("sorted item number is:", sorted_item)
    for i in range(1, len(CompletedList)):
        CompletedList[i] = 0  # None of the cells are completed
    continue_loop = 1
    cells_moved_counter = 1
    
    abort_count = 0
    
    vacancy_counter = 0
    ripple_counter = 0
    locked_counter = 0
    
    for i in range(len(BoundingBox)):
        for j in range(len(BoundingBox)):
            BoundingBox[i][j].locked = 0  # free all cells
    
    while cells_moved_counter < tot_cells + 1 and continue_loop == 1:
        end_ripple = 0
        print(ConnFreq[sorted_item])
        while CompletedList[ConnFreq[sorted_item][0]] == 1:
            sorted_item += 1
        
        Selected_Cell = ConnFreq[sorted_item][0]
        if len(ConnList[Selected_Cell]) == 0:
            cells_moved_counter += 1
            continue
        
        BoundingBox[Cells[Selected_Cell].x_data][Cells[Selected_Cell].y_data].occupied = 0  # make the chosen location vacant
        BoundingBox[Cells[Selected_Cell].x_data][Cells[Selected_Cell].y_data].CellNum = 0
        
        while end_ripple == 0:
            x_opt = 0.00
            y_opt = 0.00
            Selected_Cell_weight = len(ConnList[Selected_Cell])
            
            for z in ConnList[Selected_Cell]:
                x_opt += Cells[z.edge].x_data
                y_opt += Cells[z.edge].y_data
            x_opt = round(x_opt / Selected_Cell_weight)
            y_opt = round(y_opt / Selected_Cell_weight)  # calculate best possible location 
            
            #if iter > 1:
            #    print("planned to move to", x_opt, y_opt)
            
            # begin 4 cases
            if BoundingBox[x_opt][y_opt].occupied == 0:  # cell is vacant
                CompletedList[Selected_Cell] = 1
                Cells[Selected_Cell].x_data = x_opt
                Cells[Selected_Cell].y_data = y_opt
                BoundingBox[x_opt][y_opt].occupied = 1
                BoundingBox[x_opt][y_opt].locked = 1
                BoundingBox[x_opt][y_opt].CellNum = Selected_Cell
                abort_count = 0
                end_ripple = 1  # 8 lines done for all combos
                cells_moved_counter += 1
                vacancy_counter += 1
            else:
                if BoundingBox[x_opt][y_opt].locked == 0:  # cell is occupied, but not locked (ripple)
                    newCellID = BoundingBox[x_opt][y_opt].CellNum
                    CompletedList[Selected_Cell] = 1
                    Cells[Selected_Cell].x_data = x_opt
                    Cells[Selected_Cell].y_data = y_opt
                    BoundingBox[x_opt][y_opt].occupied = 1
                    BoundingBox[x_opt][y_opt].locked = 1
                    BoundingBox[x_opt][y_opt].CellNum = Selected_Cell
                    abort_count = 0
                    end_ripple = 0
                    
                    Selected_Cell = newCellID  # New cell selected
                    
                    cells_moved_counter += 1
                    ripple_counter += 1
                else:  # cell is occupied and locked
                    tempLoc = findNearestvacant(BoundingBox, x_opt, y_opt)
                    CompletedList[Selected_Cell] = 1
                    Cells[Selected_Cell].x_data = tempLoc.x_data
                    Cells[Selected_Cell].y_data = tempLoc.y_data
                    BoundingBox[tempLoc.x_data][tempLoc.y_data].occupied = 1
                    BoundingBox[tempLoc.x_data][tempLoc.y_data].locked = 1
                    BoundingBox[tempLoc.x_data][tempLoc.y_data].CellNum = Selected_Cell
                    abort_count += 1
                    end_ripple = 1
                    cells_moved_counter += 1
                    locked_counter += 1
                    if abort_count > abort_limit:
                        iter += 1
                        continue_loop = 0
                        for i in range(1, len(CompletedList)):
                            CompletedList[i] = 0  # res
    if continue_loop != 0:
        iter += 1
    temp_SPWL = SPWL(ConnList, Cells)
    print(f"in this iteration, vacant moves, ripple moves, locked moves = {vacancy_counter}, {ripple_counter}, {locked_counter}")
    print(f"SPWL length = {temp_SPWL}")                        

final_SPWL = SPWL(ConnList, Cells)
print(f"final length = {final_SPWL}")

print("Matrix is: ")
for i in range(len(BoundingBox)):
    print("")
    for j in range(len(BoundingBox)):
        print(BoundingBox[i][j].CellNum, " ", end="")

write_cells_to_mag(Cells, BoundingBox, ConnList, "results_b_2000_2000.mag")
print("")
