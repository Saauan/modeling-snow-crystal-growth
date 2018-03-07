"""
:mod: `snowflake_growth` module
:author: Tristan Coignion Logan Becquembois Tayebi Ajwad
:date: March 2018
:last revision: []

Simulates the growth of a snowflake and displays it in real-time
"""

P = 2 # Density of steam in each cell at the begining of the simulation
DIMENSION = (5, 5) # The dimension of the plate (number of rows and columns) (Odd numbers are prefered, because then, there is only one middle cell)
DEFAULT_CELL = {"is_in_crystal":False, "b":0, "c":0, "d":P}
# b == proportion of quasi-liquid water
# c == proportion of ice
# d == quantity of steam

# NOTE : The dimension is in the form (rows, columns) but the coordinates will be in the form (number of column, number of rows)
# This might be subject to change in the future

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
    
    >>> DEFAULT_CELL["d"] = 1 # Used in order to don't have problems with doctest
    >>> plate = create_plate(dim=(3,3))
    >>> for line in plate:
    ...     print(line)
    [{'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}]
    [{'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': True, 'b': 0, 'c': 1, 'd': 0}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}]
    [{'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}]
    
    >>> plate = create_plate(dim=(2,3), initial_position=(1,0))
    >>> for line in plate:
    ...     print(line)
    [{'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': True, 'b': 0, 'c': 1, 'd': 0}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}]
    [{'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}, {'is_in_crystal': False, 'b': 0, 'c': 0, 'd': 1}]
    >>> DEFAULT_CELL["d"] = P # Reverts to original state
    
    """
    plate = [[DEFAULT_CELL for i in range(dim[1])] for j in range(dim[0])]
    if initial_position == -1:
        initial_position = (dim[1]//2, dim[0]//2)
    plate[initial_position[1]][initial_position[0]] = {"is_in_crystal":True, "b":0, "c":1, "d":0}
    return plate
    
    
def get_neighbours(coordinates, dim=DIMENSION):
    """
    Returns a list of the coordinates of the neighbours of the cell which `coordinates` are passed as parameter
    WORKS!
    Explanation can be made easily on paper.
    All conditions for finding neighbours were found by empirical measures, and tested accordingly
    
    :param coordinates: (tuple)
    :param dim: (tuple) [DEFAULT: DIMENSION] couple of positives integers (row, column), the dimension of the plate
    :return: (list of tuples) list of the neighbours coordinates
    
    Exemples:
    >>> get_neighbours((0,0), (5,5))
    [(1, 0), (0, 1)]
    >>> get_neighbours((4,0), (5,5))
    [(3, 0), (4, 1), (3, 1)]
    >>> get_neighbours((2,4), (5,5))
    [(1, 4), (3, 4), (1, 3), (2, 3)]
    >>> get_neighbours((2,2), (5,5))
    [(1, 2), (3, 2), (1, 1), (2, 1), (2, 3), (1, 3)]
    """
    neighbours_coordinates = []

    left_border = False
    right_border = False
    top_border = False
    bottom_border = False
    if coordinates[0] == 0:
        left_border = True
    if coordinates[0] == dim[1]-1:
        right_border = True
    if coordinates[1] == 0:
        top_border = True
    if coordinates[1] == dim[0] - 1:
        bottom_border = True
    
    if not left_border:
        neighbours_coordinates.append((coordinates[0]-1, coordinates[1])) # West cell
    if not right_border:
        neighbours_coordinates.append((coordinates[0]+1, coordinates[1])) # East cell 
    if coordinates[1] % 2 == 1:
        neighbours_coordinates.append((coordinates[0], coordinates[1]-1)) # North-West cell
        if not right_border:
            neighbours_coordinates.append((coordinates[0]+1, coordinates[1]-1)) # North-East cell 
        if not bottom_border:
            if not right_border:
                neighbours_coordinates.append((coordinates[0]+1, coordinates[1]+1)) # South-East cell
            neighbours_coordinates.append((coordinates[0], coordinates[1]+1)) # South-West cell
    else:
        if not top_border:
            if not left_border: 
                neighbours_coordinates.append((coordinates[0]-1, coordinates[1]-1)) # North-West cell
            neighbours_coordinates.append((coordinates[0], coordinates[1]-1)) # North-East cell 
        if not bottom_border:
            neighbours_coordinates.append((coordinates[0], coordinates[1]+1)) # South-East cell
            if not left_border:
                neighbours_coordinates.append((coordinates[0]-1, coordinates[1]+1)) # South-West cell        
    return neighbours_coordinates

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
print(get_neighbours((2,2)))
