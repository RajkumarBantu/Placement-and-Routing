# 
The placement was achieved using a force-directed algorithm. The algorithm was specifically designed to treat cells as unit cells occupying a single grid. Additional implementation specifics and data structures utilized are outlined in the following section.
Data Structures used:
To store the input netlist, an adapted version of an adjacency list is employed. This is implemented as atuple in Python. Each node has a corresponding entry within the tuple, containing a tuple of all connected edges as well as the corresponding from and to terminals.
Input Netlist with Net details:
The Nets are given constant-time access rather than the cells.
Sorted and Unsorted connectivity list:
In order to rapidly obtain the weight (connectivity) of any given node, an unsorted list is kept, as exemplified below: Node 1 -> (Node 1, Connectivity Weight 3) Subsequently, this list is sorted in
decreasing order according to the connectivity weights and preserved in a similar data structure.
Bounding Box used for Force directed:
A square matrix with dimensions n*n is generated, where n is equal to the square root of the total number of cells. Each location within the matrix represents a class object that includes the following particulars:
1. Whether the cell is occupied or unoccupied.
2. Whether the cell is locked or unlocked.
3. If the cell is either occupied or locked, what is the cell number for that position? Boolean variables are used to represent 1 and 2, while an integer is employed for 3.
4. Implementation of Force directed placement:
Here are the steps involved in the algorithm:
1. Provide an initial random placement for all connected cells.
2. Arrange the cells in descending order based on their connectivity.
3. Select the top cell from the sorted connectivity list and mark its current location as unoccupied.
4. Determine the target coordinates for the cell utilizing the formula for calculating the optimal position.
5. If the target location is unoccupied, occupy and lock it. If the target location is occupied but not locked, swap the other cell in that position and perform a ripple for the moved cell. If the target location is locked, place the cell in the nearest vacant position and increment the abort count by 1, then continue.
6. Continue with the ripple until the ripple flag is set to true. If the abort limit has been reached, halt the iteration and begin a new one, repeating steps 3 through 6.
ROUTING:
The input for a channel routing problem consists of two groups of figures: one indicating the pinnumbers at the top of the channel, and the other indicating the pin numbers at the bottom of the
channel. We utilized the Breadth-First Search (BFS) algorithm to execute the routing process for the placed cells.When a source is provided as input, the BFS algorithm examines the neighboring cells to determine if they are vacant or locked. If they are locked, the algorithm checks the next four neighboring cells. If theyare vacant, the counter value increments after each iteration, and the four neighboring cells are checked for vacancy.
The above process is repeated until the source reaches the destination cell. After this, we use backtracking to find the shortest path by checking for the least integer value at the destination side. The value present in the destination cell is decremented until it reaches 1. We aim to have fewer bends in the wires; therefore, we follow certain conditions while decrementing the value. If the decremental value is in the left or right direction, we stay in the i-row and increment or decrement the j-column based on the
decremental value. If the decremental value is in the up or down direction, we stay in the j-column and increment or decrement the i-row based on the decremental value. This approach results in fewer bends.
After the path is found, we mark it as -1 and make the cells neighboring to the path in j+1 and j-1 cells as -1. Finally, all cells are made vacant except the path and its neighboring areas. This entire process needs to be repeated until all the net connections are completed
Integration of Placement and routing:
As the output of the force directed placement algorithm is simply a matrix of cells, it cannot be utilized directly to execute channel routing. For channel routing, a collection of top and bottom arrays are
required, with some empty spaces in between for the feed-through cells. To satisfy this requirement, a larger matrix (BoundingBox_router) was produced from the unit grid
Bounding Box router used in Force Directed. The object encompasses information about the cell number, network number, terminal number, and a Boolean value indicating if the location contains a
feed-through cell or a regular cell. This new data structure has a CellNetTerminalFeed object at each location, making it suitable for beginning the routing process. As a first step, the channel router takes the BoundingBox_router as input and considers each set of arrays (1,2), (3,4), etc. as a collection of top and bottom arrays and performs the insertion of feedthrough
cells.
Feed through Cell insertion:
In each channel, if a net is encountered only once, it implies that the net cannot be routed in the current channel and must be fed through to the next one. This is accomplished via a straightforward traversal through the selected Top and Bottom arrays. For each net requiring a feed-through, the nearest available feed-through location on the matrix is calculated and assigned the net number. This procedure is repeated for all channels.
Upon completion, we will have a fully connected array of channels with the necessary number of feedthroughs to commence the routing process.
