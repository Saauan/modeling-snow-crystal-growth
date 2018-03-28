"""
:mod: `snowflake_growth` module
:author: Tristan Coignion Logan Becquembois Tayebi Ajwad
:date: March 2018

Simulates the growth of a snowflake and displays it in real-time
"""
from copy import copy, deepcopy

NUMBER = 500

# Coefficients of the attachment phase
ALPHA = 0.7
BETA  = 0.6
THETA = 0.7
# Coefficients of the melting phase
GAMMA = 0.5 # Proportion of ice that transforms into steam
MU = 0.5 # Proportion of water that transforms into steam

KAPPA = 0.6 # Proportion of steam which transforms into ice for a border cell
RHO = 1.1 # Density of steam in each cell at the begining of the simulation

DIMENSION = (50, 50) # The dimension of the plate (number of rows and columns) (Odd numbers are prefered, because then, there is only one middle cell)
DEFAULT_CELL = {"is_in_crystal":False, "b":0, "c":0, "d":RHO}
# b == proportion of quasi-liquid water
# c == proportion of ice
# d == quantity of steam

# NOTE : The dimension is in the form (rows, columns) And so are the coordinates

def create_plate(dim=DIMENSION, initial_position=-1):
    """
    Returns a newly created plate which is a matrix of dictionnaries (a matrix of cells) and places the first crystal cell in it at the inital_pos
    The keys in a dictionnary represent the properties of the cell
    
    :Keys of the dictionnary:
        - "is_in_crystal" : (bool) True if the cell belongs to the crystal, False otherwise
        - "b": (float) the proportion of quasi-liquid water
        - "c" : (float) the proportion of ice
        - "d" : (float) the proportion of steam
    
    :param dim: (tuple) [DEFAULT: DIMENSION] couple of positives integers (row, column), the dimension of the plate
    :param initial_position: (tuple) [DEFAULT: The middle of the plate] the coordinates of the first crystal
    :return: (list of list of dictionnaries) the plate
    
    Exemples:
    
    >>> DEFAULT_CELL["d"] = 1 # Used in order to not have any problems with doctest
    >>> plate = create_plate(dim=(3,3))
    >>> for line in plate:
    ...     print("[", end="")
    ...     for d in line:
    ...         print("{", end="")
    ...         for k in sorted(d.keys()):
    ...             print(k, ":", d[k], ", ", end="")
    ...         print("}, ", end="")
    ...     print("]")
    [{b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, {b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, {b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, ]
    [{b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, {b : 0 , c : 1 , d : 0 , is_in_crystal : True , }, {b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, ]
    [{b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, {b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, {b : 0 , c : 0 , d : 1 , is_in_crystal : False , }, ]
    >>> DEFAULT_CELL["d"] = RHO # Reverts to original state
    
    """
    plate = [[copy(DEFAULT_CELL) for j in range(dim[1])] for i in range(dim[0])]
    if initial_position == -1:
        initial_position = (dim[0]//2, dim[1]//2)
    plate[initial_position[0]][initial_position[1]] = {"is_in_crystal":True, "b":0, "c":1, "d":0}
    return plate

def generate_neighbours(coordinates):
    """
    Returns the coordinates of potential neighbours of a given cell
    
    :param coordinates: (tuple) the coordinates of the cell
    :return: (list(tuples(int, int))) the list of the coordinates of the potential neighbours of a cell
    
    Examples:
    
    >>> generate_neighbours((0, 0))
    [(0, -1), (-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1)]
    >>> generate_neighbours((4, 2))
    [(4, 1), (3, 1), (3, 2), (4, 3), (5, 2), (5, 1)]
    """
    x = coordinates[1]
    y = coordinates[0]
    
    if y % 2 == 0: # If the number of the line is even
        return [(y, x-1), (y-1, x-1), (y-1, x), (y, x+1), (y+1, x), (y+1, x-1)]

    else:
        return [(y, x-1), (y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x)]

def get_neighbours(coordinates, dim=DIMENSION):
    """
    Returns a list of the coordinates of the neighbours of the cell which `coordinates` are passed as parameter
    
    :param coordinates: (tuple)
    :param dim: (tuple) [DEFAULT: DIMENSION] couple of positives integers (row, column), the dimension of the plate
    :return: (list of tuples) list of the neighbours coordinates
    
    Exemples:
    >>> get_neighbours((0,0), (5,5))
    [(0, 1), (1, 0)]
    >>> get_neighbours((4,0), (5,5))
    [(3, 0), (4, 1)]
    >>> get_neighbours((2,4), (5,5))
    [(2, 3), (1, 3), (1, 4), (3, 4), (3, 3)]
    >>> get_neighbours((2,2), (5,5))
    [(2, 1), (1, 1), (1, 2), (2, 3), (3, 2), (3, 1)]
    """
    list_neighbours = generate_neighbours(coordinates)
    
    # Test if the coordinates are correct, if they are not correct, it removes them from the list
    for neighbour in list(list_neighbours): 
        for i in range(2):
            if neighbour[i] < 0 or neighbour[i] > dim[i]-1:
                list_neighbours.pop(list_neighbours.index(neighbour))
                break
    return list_neighbours

def diffusion(plate_in):
    """
    Returns the plate passed as a parameter updated by the diffusion phase
    
    :param plate: (list(list(dict))) the support of the crystal
    :return: (list(list(dict))) the updated crystal
    """
    changes_to_make = {}
    for (y,x) in NEIGHBOURS:
        cell = plate_in[y][x]
        if cell["is_in_crystal"] == False:
            assert cell["is_in_crystal"] == False, "a cell was in a crystal" # One must check beforehand the cell is not in the crystal
            neighbours = NEIGHBOURS[(y, x)]
            steam = cell["d"]
            for (y2,x2) in neighbours:
                dic = plate_in[y2][x2]
                # If the neighbour is in the crystal, there's no need to add its steam to the mean, therefore, we add the cell's steam
                if dic["is_in_crystal"] == True:
                    steam += cell["d"]
                else:
                    steam += dic["d"] # We add the steam of the neighbour to the list of the steams
            changes_to_make[(y, x)] = steam / (1+len(neighbours))
    for coord, value in changes_to_make.items(): 
        plate_in[coord[0]][coord[1]]["d"] = value
    return plate_in

def freezing(di, k=KAPPA):
    """
    Returns the cell passed as a parameter updated by the freezing phase.
    Under the influence of frost from the cristal, each point of the boundary of
    the cristal will get a fraction k of steam converterd into ice, and a
    fraction 1 - k converted into liquid.
    
    :param di: (dict) The cell on which we apply the freezing phase.
    :param k: (float) [DEFAULT: KAPPA] The fraction used fo the evolution of the snowflake.
    :return: (dict) The updated cell.
    
    UC: A valid plate, 0 <= k <= 1
    """ 
    di["b"] = di["b"] + (1 - k) * di["d"]
    di["c"] = di["c"] + k * di["d"]
    di["d"] = 0
    return di


def attachment(di, cell_at_border, neighbours, new_cells_at_border, alpha=ALPHA, beta=BETA, theta=THETA):
    """
    Returns the cell passed as a parameter updated (or not) by the freezing phase
    
    :param di: (dict) the cell on which the attachment phase is applied
    :param cell_at_border: (tuple(int, int) the coordinates of the cell on which the attachment phase is applied
    :neighbours: (dict) the neighbours of the cell. key: the coordinates of the neighbour, value: the information of the neighbouring cell
    :param new_cells_at_border: (set) the set of all new cells which are on the border
    :param alpha: (float) [DEFAULT: ALPHA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 3 cristal cells in the neighbourhood. Works with theta.
    :param beta: (float) [DEFAULT: BETA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 1 or 2 cristal cells in the neighbourhood.
    :param theta: (float) [DEFAULT: THETA] Coefficient that determine the maximum amount of vapor surrounding
        the cell for it to still turn into a part of the cristal. With alpha, if both condition are True then
        the cell will be part of the cristal if it is surrrounded by 3 cristal cells.
    :return: (di        for coord, di in changes_to_make.items(): 
            plate[coord[0]][coord[1]] = dict, set) the dictionnary is either the updated cell, either None if the cell was not updated. The set is the updated set of cells_at_border
    """
    x = cell_at_border[1]
    y = cell_at_border[0]

    neighbours
    cristal_neighbours = 0
    test_with_theta = 0
    for neigh_coord, neigh_di in neighbours.items():
        if neigh_di["is_in_crystal"] == True:
            cristal_neighbours += 1     
            test_with_theta += neigh_di["d"]
            
    if (((cristal_neighbours in (1, 2)) and (di["b"] > beta))
        or ((cristal_neighbours == 3) and ((di["b"] >= 1) or ((test_with_theta < theta) and (di["b"] >= alpha))))
        or cristal_neighbours > 3): # We attach the cell to the crystal
        di_out = deepcopy(di)
        di_out["c"] = di["c"] + di["b"]
        di_out["b"] = 0
        di_out["d"] = 0
        di_out["is_in_crystal"] = True
        
        # We iterate through the neighbours of the attached cell,
        # and we add them to the set `new_cells_at_border` if they are not in the crystal.
        for neigh_coord, neigh_di in neighbours.items(): 
            if neigh_di["is_in_crystal"] == False:
                new_cells_at_border.add(neigh_coord)
        return di_out, new_cells_at_border
    else:
        # We add the coordinates of the cell that did not attach to the set of border cells
        new_cells_at_border.add((y, x))
        return None, new_cells_at_border
            
    

def melting(di, mu=MU, gamma=GAMMA):
    """
    Does the melting phase for one cell and returns it.
    
    :param di: (dict) the cell on which the melting is applied
    :param mu: (float) [DEFAULT: MU] proportion of water that transforms into steam 
    :param gamma: (float) [DEFAULT: GAMMA] proportion of ice that transforms into steam
    :return: (dict) the updated cell
    """
    di["d"] = di["d"] + mu * di["b"] + gamma * di["c"]
    di["b"] = (1-mu) * di["b"]
    di["c"] = (1-gamma) * di["c"]
    return di

                
def model_snowflake(number=NUMBER, dim=DIMENSION, init_pos=-1, alpha=ALPHA, beta=BETA, theta=THETA, mu=MU, gamma=GAMMA, kappa=KAPPA):
    """
    Displays a snowflake.
    This is the main function of the program, it will actualise the snowflake as well as displaying it and will eventually save its state
    
    :param number: (int) [DEFAULT: NUMBER] the number of times the simulation will update
    :param dim: ((int, int)) [DEFAULT: DIMENSION]
    :param init_pos: ((int, int)) [DEFAULT: -1]
    :param alpha: (float) [DEFAULT: ALPHA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 3 cristal cells in the neighbourhood. Works with theta.
    :param beta: (float) [DEFAULT: BETA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 1 or 2 cristal cells in the neighbourhood.
    :param theta: (float) [DEFAULT: THETA] Coefficient that determine the maximum amount of vapor surrounding
        the cell for it to still turn into a part of the cristal. With alpha, if both condition are True then
        the cell will be part of the cristal if it is surrrounded by 3 cristal cells.
    :param mu: (float) [DEFAULT: MU] proportion of water that transforms into steam 
    :param gamma: (float) [DEFAULT: GAMMA] proportion of ice that transforms into steam
    :param k: (float) [DEFAULT: KAPPA] The fraction used fo the evolution of the snowflake.
    :return: None
    """
    plate = create_plate()
    
    if init_pos == -1: # Initialises the `cells_at_border` set
        init_pos = (dim[0]//2, dim[1]//2)
    cells_at_border = set(NEIGHBOURS[(init_pos[0], init_pos[1])]) # set of tuples of coordinates
    
    # Runs the simulation `number` times
    for i in range(number):
        #DIFFUSION
        plate = diffusion(plate)
        
        new_cells_at_border = set()
        changes_to_make = {}
        for cell in cells_at_border: # `cell` is a tuple of coordinates
            cell_di = plate[cell[0]][cell[1]] # `cell_di` is a dictionnary
            # FREEZING
            cell_di = freezing(cell_di)
            
            # ATTACHMENT
            neighbours = {} # A dictionnary of all neighbours key: coordinates value: dictionnary
            for y, x in NEIGHBOURS[(cell[0], cell[1])]:
                neighbours[(y,x)] = plate[y][x]
            new_cell, new_cells_at_border = attachment(cell_di, cell, neighbours, new_cells_at_border)
            if new_cell:
                changes_to_make[(cell[0], cell[1])] = new_cell
            
            # MELTING
            cell_di = melting(cell_di)
        
        # We now apply the changes made by the attachment phase
        for coord, di in changes_to_make.items(): 
            plate[coord[0]][coord[1]] = di
        # We updated the cells at the border
        cells_at_border = new_cells_at_border
        
        # Display in shell DEBUG
        if i % 5 == 0:
            for line in plate:
                for d in line:
                    if d["is_in_crystal"] == False:
                        print(".", end=" ")
                    else:
                        print("X", end=" ")
                print()
            print()
        # Displaying the plate with the PILLOW library
        
        # Maybe saving its state for further research

# Create a dictionnary which maps a list of neighbours coordinates to the coordinates of a cell
# To access the neughbours of a cell which coordinates are (a, b) you do NEIGHBOURS[(a, b)]
NEIGHBOURS = {}
for i in range(DIMENSION[0]):
    for j in range(DIMENSION[1]):
        NEIGHBOURS[(i,j)] = get_neighbours((i,j))
        
model_snowflake()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
