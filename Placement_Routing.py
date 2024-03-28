# Creating a Force Directed Partitioning  
# vector implementation 
# Components are value, Colomns, row, index

import queue
import time
import random
from typing import List, Tuple

class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

def findPath(node, path):
    if node is not None:
        findPath(node.parent, path)
        path.append((node.x, node.y))

def isValid(x, y, N, n):
    return 0 <= x < N and 0 <= y < N and n == 0

row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]

def findPath(matrix, x, y, a, b):
    path = []
    N = len(matrix)
    if N == 0:
        return path
    
    q = queue.Queue()
    src = Node(x, y, None)
    q.put(src)
    
    visited = set()
    visited.add(src)
    
    while not q.empty():
        curr = q.get()
        i = curr.x
        j = curr.y
        
        if i == a and j == b:
            findPath(curr, path)
            return path
        
        n = matrix[i][j]
        
        for k in range(4):
            x = i + row[k]
            y = j + col[k]
            
            if isValid(x, y, N, n):
                next_node = Node(x, y, curr)
                
                if next_node not in visited:
                    q.put(next_node)
                    visited.add(next_node)
    
    return path

def swap(xPtr: List[int], yPtr: List[int]) -> None:
    temp = xPtr[0]
    xPtr[0] = yPtr[0]
    yPtr[0] = temp
    
def manhattan(ao: int, bo: int, a1: int, b1: int) -> int:
    distance = abs(ao - a1) + abs(bo - b1)
    return distance

def bubbleSort(array: List[int]) -> List[int]:
    n = len(array)
    array1 = [i for i in range(n)]

    for i in range(n - 1):
        # Last i elements are already in place
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                swap([array1[j]], [array1[j + 1]])
                swap([array[j]], [array[j + 1]])
    return array1


def main():
    start = time.perf_counter()
    net = 0
    node = 0
    fileName = input("Enter the name of input file: ")
    inputFile = open(fileName, "r")
    outputFile = open("output.txt", "w")
    outputFile.write("magic\ntech scmos\ntimestamp\n")

    node = int(inputFile.readline().strip())
    unrouted = 0
    net = int(inputFile.readline().strip())

    # weights of node are calculated for ordering
    value = []
    columns = []
    rows = [0] * (node + 1)

    # matrix to save the individual net connections
    matrix = [[0] * node for i in range(node)]

    # save the Cell and Terminal info of the given benchmarks
    cell1 = []
    cell2 = []
    terminalCell1 = []
    terminalCell2 = []

    net_pairs = [(0, 0)] * net
    cell_pairs = [(0, 0)] * net

    i = 0
    while i < node:
        j = 0
        while j <= i:
            matrix[i].append(0)
            j += 1
        i += 1

    counter = net
    i = 0
    while counter:
        netNum, cellNum1, terminalCellNum1, cellNum2, terminalCellNum2 = map(int, inputFile.readline().strip().split())

        cellNum1 -= 1
        cellNum2 -= 1
        cell1.append(cellNum1)
        cell2.append(cellNum2)
        net_pairs[i] = (terminalCellNum1, terminalCellNum2)
        cell_pairs[i] = (cellNum1, cellNum2)

        if cellNum1 < cellNum2:
            matrix[cellNum2][cellNum1] += 1
        else:
            matrix[cellNum1][cellNum2] += 1

        terminalCell1.append(str(terminalCellNum1))
        terminalCell2.append(str(terminalCellNum2))

        counter -= 1
        i += 1

    for i in range(net):
        # print(net_pairs[i][0], "cell 1 terminal", net_pairs[i][1], "cell 2 terminal") # save net pairs
        pass

    # Initializing DSS matrix vectors
    k = 0
    while k < node:
        counter, j = 0, 0
        while j <= k:
            if matrix[k][j] != 0:
                value.append(matrix[k][j])
                columns.append(j)
                counter += 1
            rows[k + 1] = rows[k] + counter
            j += 1
        k += 1

    list_nodes = [0] * node
    list_cells = [0] * node
    z, m = 0, 0
    while m < node:
        j = rows[m + 1] - rows[m]
        n = 0
        while n < j:
            if m != columns[z]:
                list_nodes[m] += value[z]  # i denotes row node
                list_nodes[columns[z]] += value[z]  # saving the column node
            z += 1
            n += 1
        m += 1
    list_cells = bubbleSort(list_nodes)
    zero = []
    z = 0

    # Move all the zero elements to the end of the list
    for i in range(len(list_cells)):
        if list[list_cells[i]] == 0:
            zero.append(list_cells[i])
            z += 1

    list_cells = list_cells[z:]
    abort_counter = 0
    abort_limit = 10
    iteration_counter = 1
    iteration_limit = 20 * len(list_cells)
    seed = 0
    s = int(node ** 0.5) + 1
    cellStatus = [False] * node
    post = [[0] * s for i in range(s)]
    random.seed(time.time())
    xCells = list(range(node))
    yCells = list(range(node))
    random.shuffle(list_cells)
    z = 0
    i = 0
    while i < s:
        j = 0
        while j < s:
            post[i][j] = list_cells[z] + 1
            z += 1
            if z == len(list_cells):
                break
            j += 1
        if z == len(list_cells):
            break
        i += 1

    i = 0
    while i < s:
        j = 0
        while j < s:
            if post[i][j] != 0:
                xCells[post[i][j] - 1] = j
                yCells[post[i][j] - 1] = j
            j += 1
        i += 1

    length = 0
    i = 0
    while i < node:
        j = 0
        while j < node:
            if i > j:
                if matrix[i][j] != 0:
                    length += manhattan(xCells[i], yCells[i], xCells[j], yCells[j])
            if i < j:
                if matrix[j][i] != 0:
                    length += manhattan(xCells[i], yCells[i], xCells[j], yCells[j])
            j += 1
        i += 1

    rippleEnd = False
    z = len(list_cells) - 1
    print(z)
    iteration_counter = 0
    iteration_limit = 100
    abort_counter = 0
    abort_limit = 10
    s = len(post)

    while iteration_counter < iteration_limit:
        seed = list_cells[z]
        if cellStatus[seed] == 0:
            i = 0
            while i < s:
                k = False
                j = 0
                while j < s:
                    if post[i][j] == seed + 1:
                        post[i][j] = 0
                        k = True
                        break
                    if k == True:
                        break
                    j += 1
                i += 1
            rippleEnd = False

            while not rippleEnd:
                xo, yo = 0, 0
                sum_xd, sum_yd, sum_xn, sum_yn = 1, 1, 1, 1
                i = 0
                while i < s:
                    j = 0
                    while j < s:
                        x = post[i][j] - 1
                        if (x > seed) and (x >= 0):
                            sum_xd += matrix[x][seed]
                            sum_yd += matrix[x][seed]
                            sum_xn += i * matrix[x][seed]
                            sum_yn += j * matrix[x][seed]
                        elif x < seed and (x >= 0):
                            sum_xd += matrix[seed][x]
                            sum_yd += matrix[seed][x]
                            sum_xn += i * matrix[seed][x]
                            sum_yn += j * matrix[seed][x]
                        j += 1
                    i += 1
                xo = int(sum_xn / sum_xd)
                yo = int(sum_yn / sum_yd)

                if post[xo][yo] == 0:
                    post[xo][yo] = seed + 1
                    rippleEnd = True
                    abort_counter = 0
                    cellStatus[post[xo][yo] - 1] = 1
                elif seed == post[xo][yo] - 1:
                    cellStatus[post[xo][yo] - 1] = 1
                    rippleEnd = True
                    abort_counter = 0
                elif (cellStatus[post[xo][yo] - 1] == 1) and (post[xo][yo] > 0):
                    distance = 0
                    temp = 0
                    netNum = xo
                    y1 = yo
                    i = 0
                    while i < s:
                        j = 0
                        while j < s:
                            if post[i][j] == 0:
                                distance = abs(i - xo) + abs(j - yo)
                                if temp == 0:
                                    temp = distance
                                    netNum = i
                                    y1 = j
                                if distance < temp:
                                    netNum = i
                                    y1 = j
                                    temp = distance
                            j += 1
                        i += 1
                    xo = netNum
                    yo = y1
                    post[xo][yo] = seed + 1
                    rippleEnd = True
                    abort_counter += 1
                    if abort_counter > abort_limit:
                        cellStatus = [0] * len(cellStatus)
                elif ((post[xo][yo] != 0) and (cellStatus[post[xo][yo] - 1] == 0)):
                    temp = post[xo][yo] - 1
                    post[xo][yo] = seed + 1
                    cellStatus[post[xo][yo] - 1] = 1
                    seed = temp
                    rippleEnd = 0
                    abort_counter = 0
        z -= 1
        iteration_counter += 1
        if z == 4294967295:
            break

    # node in the zeroes list are added back to the placement 
 

    # Final placement
    length = 0
    i = 0
    while i < node:
        j = 0
        while j < node:
            if i > j:
                if matrix[i][j] != 0:
                    length += manhattan(xCells[i], yCells[i], xCells[j], yCells[j])
            if i < j:
                if matrix[j][i] != 0:
                    length += manhattan(xCells[i], yCells[i], xCells[j], yCells[j])
            j += 1
        i += 1

    xCells.clear()
    yCells.clear()

    cell_x = [0] * node
    cell_y = [0] * node
    cell_o = [False] * node

    channel_size = 0
    bb = 0
    if net >= 400:
        channel_size = net // 10
        bb = 10
    elif net < 400:
        channel_size = (net // 10) + 15
        bb = 6

    i = 0
    while i < s:
        j = 0
        while j < s:
            if post[i][j] != 0:
                cell_x[post[i][j] - 1] = channel_size * (j + 1) + 6 * j
                cell_y[post[i][j] - 1] = channel_size * (i + 1) + 6 * i
            j += 1
        i += 1

    counter = s * (6 + channel_size) + channel_size
    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4

    i = 0
    while i < node:
        outputFile.write("<< pdiffusion >>\n")
        outputFile.write(f"rect {cell_x[i]} {cell_y[i]} {cell_x[i]+6} {cell_y[i]+6}\n")
        outputFile.write("<< labels >>\n")
        outputFile.write(f"rlabel pdiffusion {cell_x[i]} {cell_y[i]} {cell_x[i]+6} {cell_y[i]+6} 0 cell_no = {i+1}\n")
        i += 1

    i = 0
    while i < node:
        outputFile.write("<< polysilicon >>\n")
        outputFile.write(f"rect {cell_x[i]+1} {cell_y[i]-1} {cell_x[i]+2} {cell_y[i]}\n")
        outputFile.write(f"rect {cell_x[i]+4} {cell_y[i]-1} {cell_x[i]+5} {cell_y[i]}\n")
        outputFile.write(f"rect {cell_x[i]+1} {cell_y[i]+6} {cell_x[i]+2} {cell_y[i]+7}\n")
        outputFile.write(f"rect {cell_x[i]+4} {cell_y[i]+6} {cell_x[i]+5} {cell_y[i]+7}\n")
        outputFile.write("<< labels >>\n")
        outputFile.write(f"rlabel polysilicon {cell_x[i]+1} {cell_y[i]-1} {cell_x[i]+2} {cell_y[i]} 0 T3\n")
        outputFile.write(f"rlabel polysilicon {cell_x[i]+4} {cell_y[i]-1} {cell_x[i]+5} {cell_y[i]} 0 T4\n")
        outputFile.write(f"rlabel polysilicon {cell_x[i]+1} {cell_y[i]+6} {cell_x[i]+2} {cell_y[i]+7} 0 T1\n")
        outputFile.write(f"rlabel polysilicon {cell_x[i]+4} {cell_y[i]+6} {cell_x[i]+5} {cell_y[i]+7} 0 T2\n")
        i += 1

    net1 = 0
    alpha = 1
    blockage = [[0] * counter for i in range(counter)]
    counter = s * (6 + channel_size) + channel_size
    i = 0
    while i < node:
        for k in range(cell_x[i]-1, cell_x[i]+7):
            for j in range(cell_y[i]-1, cell_y[i]+7):
                blockage[k][j] = -1
        i += 1

    i = 0
    while i < node:
        blockage[cell_x[i]-1][cell_y[i]+1] = 0
        blockage[cell_x[i]-1][cell_y[i]+4] = 0
        blockage[cell_x[i]+6][cell_y[i]+1] = 0
        blockage[cell_x[i]+6][cell_y[i]+4] = 0
        i += 1

    for i in range(counter):
        for j in range(counter):
            print(blockage[i][j], end=' ')
        print()

    vec = []
    for itr in range(counter):
        vec.append([])
        for jtr in range(counter):
            vec[itr].append(blockage[itr][jtr])

    for i in range(net):
        cell_one, cell_two = cell_pairs[i]
        net_one, net_two = net_pairs[i]
        x, y, a, b = -1, -1, -1, -1
        if net_one == 1:
            x, y = cell_x[cell_one] - 1, cell_y[cell_one] + 1
        elif net_one == 2:
            x, y = cell_x[cell_one] - 1, cell_y[cell_one] + 4
        elif net_one == 3:
            x, y = cell_x[cell_one] + 6, cell_y[cell_one] + 1
        elif net_one == 4:
            x, y = cell_x[cell_one] + 6, cell_y[cell_one] + 4
            
        if net_two == 1:
            a, b = cell_x[cell_two] - 1, cell_y[cell_two] + 1
        elif net_two == 2:
            a, b = cell_x[cell_two] - 1, cell_y[cell_two] + 4
        elif net_two == 3:
            a, b = cell_x[cell_two] + 6, cell_y[cell_two] + 1
        elif net_two == 4:
            a, b = cell_x[cell_two] + 6, cell_y[cell_two] + 4
            
        path = findPath(vec, x, y, a, b)

        for itr in range(len(path)):
            vec[path[itr][0]][path[itr][1]] = 1
            if path[itr][1] - 1 >= 0 and vec[path[itr][0]][path[itr][1] - 1] == 0:
                vec[path[itr][0]][path[itr][1] - 1] = -2
            if path[itr][1] + 1 < counter and vec[path[itr][0]][path[itr][1] + 1] == 0:
                vec[path[itr][0]][path[itr][1] + 1] = -2
            if path[itr][0] - 1 >= 0 and vec[path[itr][0] - 1][path[itr][1]] == 0:
                vec[path[itr][0] - 1][path[itr][1]] = -2
            if path[itr][0] - 1 >= 0 and path[itr][1] - 1 >= 0 and vec[path[itr][0] - 1][path[itr][1] - 1] == 0:
                vec[path[itr][0] - 1][path[itr][1] - 1] = -2
            if path[itr][0] - 1 >= 0 and path[itr][1] + 1 < counter and vec[path[itr][0] - 1][path[itr][1] + 1] == 0:
                vec[path[itr][0] - 1][path[itr][1] + 1] = -2
            if path[itr][0] + 1 < counter and vec[path[itr][0] + 1][path[itr][1]] == 0:
                vec[path[itr][0] + 1][path[itr][1]] = -2
            if path[itr][0] + 1 < counter and path[itr][1] - 1 >= 0 and vec[path[itr][0] + 1][path[itr][1] - 1] == 0:
                vec[path[itr][0] + 1][path[itr][0] - 1] = -2
            if path[itr][0] + 1 < counter and path[itr][1] + 1 < counter and vec[path[itr][0] + 1][path[itr][1] + 1] == 0:
                vec[path[itr][0] + 1][path[itr][1] + 1] = -2

    for itr in range(counter):
        for jtr in range(counter):
            print(vec[itr][jtr], end=' ')
        print()
        
    outputFile.write("<< end >>\n")
    end = time.time()
    elapsed = end - start
    # print("Elapsed time in seconds:", elapsed, "s")
    # print("Elapsed time in minutes:", elapsed / 60,)
    outputFile.close()

if __name__ == '__main__':
    main()