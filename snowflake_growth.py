"""
:mod: `snowflake_growth` module
:author: Tristan Coignion Logan Becquembois Tayebi Ajwad
:date: March 2018
:last revision: []

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

DIMENSION = (80, 115) # The dimension of the plate (number of rows and columns) (Odd numbers are prefered, because then, there is only one middle cell)
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
    Computes diffusion for a cell in a `plate` put as parameter. It has a side effect, that is, it changes the value of key "d" of the cell.
    Diffusion computes the steam for the cell by doing the average of its steam and the steam of its neighbours.
    
    :param coordinates: (tuple(int, int)) the coordinates of the cell
    :param plate: (list(list(dict))) the support of the crystal
    :return: None
    """
    plate_out = deepcopy(plate_in)
    for (y,x) in NEIGHBOURS:
        cell = plate_in[y][x]
        if cell["is_in_crystal"] == False:
            assert cell["is_in_crystal"] == False, "a cell was in a crystal" # One must check beforehand the cell is not in the crystal
            neighbours = NEIGHBOURS[(y, x)]
            list_steam = [cell["d"]]
            for (y2,x2) in neighbours:
                dic = plate_in[y2][x2]
                # If the neighbour is in the crystal, there's no need to add its steam to the mean, therefore, we add the cell's steam
                if dic["is_in_crystal"] == True:
                    list_steam.append(cell["d"]) 
                else:
                    list_steam.append(dic["d"]) # We add the steam of the neighbour to the list of the steams
            plate_out[y][x]["d"] = sum(list_steam) / (1+len(neighbours)) # We make the average of the steams, and the value of "d" inside the cell is changed
        
    return plate_out

def freezing(plate, cells_at_border, k=KAPPA):
    """
    Under the influence of frost from the cristal, each point of the boundary of
    the cristal will get a fraction k of steam converterd into ice, and a
    fraction 1 - k converted into liquid.
    :param plate: (list of list of dict) The plate which contain the cristal.
    :param k: (float) The fraction used fo the evolution of the snowflake.
    :return: (list of list of dict) The modified plate.
    
    UC: A valid plate, 0 <= k <= 1
    """ 
    for (y, x) in cells_at_border:
        di = plate[y][x] 
        di["b"] = di["b"] + (1 - k) * di["d"]
        di["c"] = di["c"] + k * di["d"]
        di["d"] = 0
    return plate


def attachment(plate_in, cells_at_border, alpha=ALPHA, beta=BETA, theta=THETA):
    """
    Determine if a cell will attach itself to the cristal.
    :param plate: (list of list of dict) The plate which contain the cristal.
    :param alpha: (float) [DEFAULT: ALPHA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 3 cristal cells in the neighbourhood. Works with theta.
    :param beta: (float) [DEFAULT: BETA] Coefficient that determine the minimum amount of ice in a cell for it
        to attach itself to the cristal if it only has 1 or 2 cristal cells in the neighbourhood.
    :param theta: (float) [DEFAULT: THETA] Coefficient that determine the maximum amount of vapor surrounding
        the cell for it to still turn into a part of the cristal. With alpha, if both condition are True then
        the cell will be part of the cristal if it is surrrounded by 3 cristal cells.
    :return: (Nun) A holy praying person.
    
    UC: A valid plate.
    """
    plate_out = deepcopy(plate_in)
    new_cells_at_border = []
    for i, (y,x) in enumerate(cells_at_border):
        di = plate_in[y][x]
        di_out = plate_out[y][x]
        neighbours = NEIGHBOURS[(y, x)]
        cristal_neighbours = 0
        test_with_theta = 0
        for (y2, x2) in neighbours:
            neighbour = plate_in[y2][x2]
            if neighbour["is_in_crystal"] == True:
                cristal_neighbours += 1     
                test_with_theta += neighbour["d"]  
#         if (y,x) == (3,2):
#             print("oui")
        if (((cristal_neighbours in (1, 2)) and (di["b"] > beta))
            or ((cristal_neighbours == 3) and ((di["b"] >= 1) or ((test_with_theta < theta) and (di["b"] >= alpha))))
            or cristal_neighbours > 3):
            di_out["c"] = di["c"] + di["b"]
            di_out["b"] = 0
            di_out["d"] = 0
            di_out["is_in_crystal"] = True
            for y3, x3 in NEIGHBOURS[(y,x)]:
                if plate_in[y3][x3]["is_in_crystal"] == False:
                    new_cells_at_border.append((y3, x3))
        else:
            new_cells_at_border.append((y, x))
            
    return plate_out

def melting(plate, cells_at_border, mu=MU, gamma=GAMMA):
    """
    """
    for (y, x) in cells_at_border:
        di = plate[y][x]
        di["d"] = di["d"] + mu * di["b"] + gamma * di["c"]
        di["b"] = (1-mu) * di["b"]
        di["c"] = (1-gamma) * di["c"]
    return None

def update_border(plate, dim=DIMENSION):
    """
    """
    res = []
    for y in range(dim[0]):
        for x in range(dim[1]):
            for (y1, x1) in NEIGHBOURS[(y,x)]:
                if plate[y1][x1]["is_in_crystal"] == True:
                    res.append((y,x))
    return res
        
                
def model_snowflake(dim=DIMENSION, init_pos=-1, alpha=ALPHA, beta=BETA, theta=THETA, gamma=GAMMA, mu=MU, kappa=KAPPA):
    """
    Displays a snowflake.
    This is the main function of the program, it will actualise the snowflake as well as displaying it and will eventually save its state
    """
    plate = create_plate()
    if init_pos == -1:
        init_pos = (dim[0]//2, dim[1]//2)
    cells_at_border = list(NEIGHBOURS[(init_pos[0], init_pos[1])]) # List of tuples of coordinates
    plate[0][0]["d"] = 0.2
    for i in range(NUMBER):
        plate = diffusion(plate)
        plate = freezing(plate, cells_at_border)
        plate = attachment(plate, cells_at_border) # Runs the attachement phase and updates cells_at_border
        cells_at_border = update_border(plate)
        melting(plate, cells_at_border)        
        
        if i % 3 == 0:
            for line in plate:
                for d in line:
                    (b0, c0, d0, crystal) = sorted(d.keys())
                    if d[crystal] == False:
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
    
