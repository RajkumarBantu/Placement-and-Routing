import sys
import os
import random
import time

class extremeEdge:
    def __init__(self):
        self.start = -1
        self.end = -1

def printSpan(span):
    print("The vector elements are:")
    for i in range(1, len(Span)):
        print(i, "start is", Span[i].start, "end is", span[i].end)

def printvcg(VCG):
    for i in range(1, len(VCG)):
        print(i, end=' ')
        for j in range(len(VCG[i])):
            print(VCG[i][j], end=' ')
        print()

elements = 6
channel_no = 1

Top = [-1, 1, 6, 1, 2, 3, 5]
Bottom = [6, 3, 5, 4, -1, 2, 4]

Span = [extremeEdge() for i in range(elements + 1)]
VCG = [[] for i in range(elements + 1)]

order = [0]
finalorder = [0]
Spancheckorder = [0]

print(len(Top))
for i in range(len(Top)):
    print(Top[i], end=' ')
print()

elements = 6
channel_no = 1

doglegs = []

for i in range(len(Top)):
    top_element = Top[i]
    bottom_element = Bottom[i]

    if top_element > 0 and bottom_element > 0 and top_element != bottom_element:
        VCG[top_element].append(bottom_element)
        for z in VCG[bottom_element]:
            if z == top_element:
                print(f"Found dog leg for {bottom_element} {top_element}")
                doglegs.append((bottom_element, top_element))
    
    if bottom_element > 0:
        if Span[bottom_element].start == -1:
            Span[bottom_element].start = i
            order.append(bottom_element)

    if top_element > 0:
        if Span[top_element].start == -1:
            Span[top_element].start = i
            order.append(top_element)

    if top_element > 0:
        Span[top_element].end = i
    if bottom_element > 0:
        Span[bottom_element].end = i

printSpan(Span)
print("order is: ")
print(order)

Span_visit = [False] * (elements+1)
Temp_Track = [[]]
track_counter = 0

for k in range(1, len(order)):
    temp_span = 0

    currSpan = []
    tempObj = extremeEdge()
    tempObj.start = Span[order[k]].start
    tempObj.end = Span[order[k]].end
    currSpan.append(tempObj)

    for m in range(1, len(Spancheckorder)):
        if order[k] == Spancheckorder[m]:
            temp_span = 1

    if temp_span == 0:
        Temp_Track.append([])
        track_counter += 1
        Temp_Track[track_counter].append(order[k])
        Spancheckorder.append(order[k])
        Span_visit[order[k]] = 1

        for l in range(k+1, len(order)):
            if Span_visit[order[l]] == 0:
                temp_check = 0
                for r in range(len(Temp_Track[track_counter])):
                    if (Span[Temp_Track[track_counter][r]].start <= Span[order[l]].start <= Span[Temp_Track[track_counter][r]].end) or (Span[Temp_Track[track_counter][r]].start <= Span[order[l]].end <= Span[Temp_Track[track_counter][r]].end):
                        temp_check = 1
                        print(f"{order[k]}, {order[l]} failed the check")

                if temp_check == 0:
                    Spancheckorder.append(order[l])
                    Temp_Track[track_counter].append(order[l])
                    Span_visit[order[l]] = 1

# Print Spancheckorder
print("Span Check order:", len(Spancheckorder))
for i in range(1, len(Spancheckorder)):
    print(Spancheckorder[i], end=" ")
print()

# Initialize visited vector to false
visited = [False] * (elements + 1)
for j in range(1, len(Spancheckorder)):
    visited[Spancheckorder[j]] = True
temp_size = 0

# Begin constructing the final order
while True:
    for i in range(1, len(Spancheckorder)):
        if visited[Spancheckorder[i]] == 0:
            if len(VCG[Spancheckorder[i]]) == 0:
                visited[Spancheckorder[i]] = 1
                print("Cell visited is             ", Spancheckorder[i])
                finalorder.append(Spancheckorder[i])
                continue
            else:
                tempvar = 1
                for k in range(len(VCG[Spancheckorder[i]])):
                    if visited[VCG[Spancheckorder[i]][k]] == 0:
                        tempvar = 0
                        
                if tempvar == 0:
                    continue
                else:
                    finalorder.append(Spancheckorder[i])
                    print("Cell visited is             ", Spancheckorder[i])
                    visited[Spancheckorder[i]] = 1
    
    tempnew = 1
    for i in range(1, elements+1):
        if visited[i] == 0:
            tempnew = 0
            
    if tempnew == 1:
        break

# Constructing the final order
print("VCG:")
printvcg(VCG)

print("Final order is:")
for i in range(1, len(finalorder)):
    print(finalorder[i], end=" ")
print()

# Track placement
Track = [[] for _ in range(elements+1)]
Recordtrack = [[]]
Track_Temp = []
Track[0].append(0)
track_no = 0

for p in range(1, len(finalorder)):
    for q in range(len(Recordtrack[track_no])):
        if ((Span[finalorder[p]].start <= Span[Recordtrack[track_no][q]].start and Span[Recordtrack[track_no][q]].start <= Span[finalorder[p]].end and Span[finalorder[p]].end <= Span[Recordtrack[track_no][q]].end) or
            (Span[Recordtrack[track_no][q]].start <= Span[finalorder[p]].start and Span[finalorder[p]].start <= Span[Recordtrack[track_no][q]].end and Span[Recordtrack[track_no][q]].end <= Span[finalorder[p]].end) or
            (Span[Recordtrack[track_no][q]].start <= Span[finalorder[p]].start and Span[finalorder[p]].start <= Span[Recordtrack[track_no][q]].end) or 
            (Span[Recordtrack[track_no][q]].start <= Span[finalorder[p]].end and Span[finalorder[p]].end <= Span[Recordtrack[track_no][q]].end)  or 
            (Span[finalorder[p]].start <= Span[Recordtrack[track_no][q]].start and Span[Recordtrack[track_no][q]].start <= Span[Recordtrack[track_no][q]].end and Span[Recordtrack[track_no][q]].end <= Span[finalorder[p]].end ) or
            (Span[Recordtrack[track_no][q]].start <= Span[finalorder[p]].start and Span[finalorder[p]].start <= Span[finalorder[p]].end and Span[finalorder[p]].end <= Span[Recordtrack[track_no][q]].end)):

            track_no += 1
            Recordtrack.append(Track_Temp)

    Recordtrack[track_no].append(finalorder[p])
    Track[finalorder[p]].append(track_no)
    print(f"Size of track {track_no} {len(Recordtrack[track_no])}")
    print(f"Printing track: {finalorder[p]} {track_no}")

# For each channel end do...
print()
