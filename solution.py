assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
             ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]

unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for c in values.keys():
        if len(values[c]) == 2:
            for e in units[c][0]:
                if e != c:
                    if values[c] == values[e]:
                        for d in units[c][0]:
                            if d != e:
                                if d != c:
                                    for f in values[c]:
                                        values = assign_value(values, d, values[d].replace(f, ''))
            for e in units[c][1]:
                if e != c:
                    if values[c] == values[e]:
                        for d in units[c][1]:
                            if d != e:
                                if d != c:
                                    for f in values[c]:
                                        values = assign_value(values, d, values[d].replace(f, ''))
            for e in units[c][2]:
                if e != c:
                    if values[c] == values[e]:
                        for d in units[c][2]:
                            if d != e:
                                if d != c:
                                    for f in values[c]:
                                        values = assign_value(values, d, values[d].replace(f, ''))
    return (values)
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    if len(grid) == 81:
        myListGrid = []
        myListBoxes = []
        dico = {}
        for i in grid:
            myListGrid.append(i)
        for j in boxes:
            myListBoxes.append(j)
        n = len(myListBoxes)
        for k in range(0, n):
            if myListGrid[k] == '.':
                dico[myListBoxes[k]] = '123456789'
            else:
                dico[myListBoxes[k]] = myListGrid[k]
        return (dico)
    else:
        print("Error on the grid")


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    for c, d in values.items():
        if len(values[c]) != 1:
            for k in peers[c]:
                if len(values[k]) == 1:
                    values = assign_value(values, c, values[c].replace(values[k], ""))

    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here



    for c, d in values.items():

        if len(values[c]) != 1:

            for i in values[c]:
                seenTF = 0
                for j in units[c]:

                    for k in j:
                        if k != c:
                            if values[k].find(i) != -1:
                                seenTF = 1

                if seenTF == 0:
                    values = assign_value(values, c, i)

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)

    if values is False:
        return False

    if len([box for box in values.keys() if len(values[box]) == 1]) == 81:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    fewestposs = 9
    fewestindex = ""
    for c, d in values.items():
        if len(d) != 1:
            if len(d) < fewestposs:
                fewestposs = len(d)
                fewestindex = c
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    for i in values[fewestindex]:
        newGrid = values.copy()
        newGrid[fewestindex] = i
        tree = search(newGrid)
        if tree:
            return tree


            # If you're stuck, see the solution.py tab!


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')