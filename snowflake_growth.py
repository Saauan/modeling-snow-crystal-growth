"""
:mod: `snowflake_growth` module
:author: Tristan Coignion Logan Becquembois Tayebi Ajwad
:date: March 2018
:last revision: []

Simulates the growth of a snowflake and displays it in real-time
"""
from copy import copy

P = 2 # Density of steam in each cell at the begining of the simulation
DIMENSION = (5, 5) # The dimension of the plate (number of rows and columns) (Odd numbers are prefered, because then, there is only one middle cell)
DEFAULT_CELL = {"is_in_crystal":False, "b":0, "c":0, "d":P}
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
    >>> DEFAULT_CELL["d"] = P # Reverts to original state
    
    """
    plate = [[copy(DEFAULT_CELL) for i in range(dim[1])] for j in range(dim[0])]
    if initial_position == -1:
        initial_position = (dim[1]//2, dim[0]//2)
    plate[initial_position[1]][initial_position[0]] = {"is_in_crystal":True, "b":0, "c":1, "d":0}
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


def diffusion(coordinates, plate):
    """
    Computes diffusion for a cell in a `plate` put as parameter. It has a side effect, that is, it changes the value of key "d" of the cell.
    Diffusion computes the steam for the cell by doing the average of its steam and the steam of its neighbours.
    
    :param coordinates: (tuple(int, int)) the coordinates of the cell
    :param plate: (list(list(dict))) the support of the crystal
    :return: None
    """
    cell = plate[coordinates[0]][coordinates[1]]
    assert cell["is_in_crystal"] == False, "a cell was in a crystal" # One must check beforehand the cell is not in the crystal
    neighbours = get_neighbours(coordinates)
    list_steam = [cell["d"]]
    for coord in neighbours:
        dic = plate[coord[0]][coord[1]]
        # If the neighbour is in the crystal, there's no need to add its steam to the mean, therefore, we add the cell's steam
        if dic["is_in_crystal"] == True:
            list_steam.append(cell["d"]) 
        else:
            list_steam.append(dic["d"]) # We add the steam of the neighbour to the list of the steams
    cell["d"] = sum(list_steam) / (1+len(neighbours)) # We make the average of the steams, and the value of "d" inside the cell is changed
    return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
