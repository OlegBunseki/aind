
from utils import *
import time

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_1 = [[rows[i] + cols[i]  for i in range(9)]]
diag_2 = [[rows[i] + cols[8-i]  for i in range(9)]]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diag_1 + diag_2


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    
    for unit in unitlist:
        my_subset = [values[box] for box in unit if len(values[box])>=2]
        if len(my_subset)>=2:
            double_digit = [dd for dd in my_subset if len(dd)==2]
            if len(double_digit)>=2:
                
                my_twins = [twin for twin in double_digit if sum([twin==v for v in double_digit]) == 2]
                
                twins_values = []
                for v in my_twins:
                    if v not in twins_values:
                        twins_values.append(v)
                
                
                if len(twins_values) > 0:
                    
                    #print(twins_values)
                    #display(values)                   
                    #time.sleep(10)
                    
                    for box in unit:
                        for v in twins_values:
                            if values[box] != v:
                                for i in v:
                                    #values[box] = values[box].replace(i,'')
                                    values = assign_value(values, box, values[box].replace(i, ''))
                    #display(values)
            
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
	
    # raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
	
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
	
    # raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
	
    stalled = False
    while not stalled:
        
		# Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        #print('elimination...')
        #display(values)
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        #display(values) 
        #print('elimination done')
        #time.sleep(10)
 
 
        #print('only_choice...')
        #display(values)
		# Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        #display(values)       
        #print('only_choice done')
        #time.sleep(10)

		
        values = naked_twins(values)
		
		
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
		# If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
		# Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
			
    return values
	
    # raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
	
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    
	# raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
