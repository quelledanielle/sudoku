class Sudoku(object):
    """3x3 Sudoku puzzle with the following format:
     |--------|-------|-------|-------|-------|
     | Square |       |   0   |   1   |   2   |
     |--------|-------|-------|-------|-------|
     |        | Entry | 0 1 2 | 3 4 5 | 6 7 8 |
     |--------|-------|-------|-------|-------|
     |        |   0   | _ _ _ | _ _ _ | _ _ _ |
     |   0    |   1   | _ _ _ | _ _ _ | _ _ _ |
     |        |   2   | _ _ _ | _ _ _ | _ _ _ |
     |--------|-------|-------|-------|-------|
     |        |   3   | _ _ _ | _ _ _ | _ _ _ |
     |   1    |   4   | _ _ _ | _ _ _ | _ _ _ |
     |        |   5   | _ _ _ | _ _ _ | _ _ _ |
     |--------|-------|-------|-------|-------|
     |        |   6   | _ _ _ | _ _ _ | _ _ _ |
     |   2    |   7   | _ _ _ | _ _ _ | _ _ _ |
     |        |   8   | _ _ _ | _ _ _ | _ _ _ |
     |--------|-------|-------|-------|-------|
       
       Blank entries have a value of 0.
       Valid entries have a value between 1-9.
    """
    
    def __init__(self, filename='1.txt'):
        self.__puzzle = None
        self.__square_coords = [(i, j) for i in range(3) for j in range(3)]
        self.__read(filename)
        self.__given_coords = [(i, j) for i in range(9) for j in range(9)
                               if self.__puzzle[i][j] != 0]
    
    def __str__(self):
        string = ''
        for i in range(9):
            for j in range(9):
                string += '%s ' % self.__puzzle[i][j]
                if j % 3 == 2 and j != 8:
                    string += '| '
                if j == 8:
                    string += '\n'
            
            if i % 3 == 2 and i != 8:
                string += '------|-------|------\n'
        
        return string
    
    def __read(self, filename):
        """Reads puzzle from a file into a 2D int list"""
        with open(filename, 'r+') as f:
            self.__puzzle = [[int(x) for x in line.split()] for line in f]
    
    def get_entry(self, i, j):
        """Returns the (i, j)th entry"""
        return self.__puzzle[i][j]
    
    def set_entry(self, i, j, value):
        """Sets the (i, j)th entry to a given value"""
        if (i, j) in self.__given_coords:
            raise ValueError("Trying to change original puzzle value")
        
        self.__puzzle[i][j] = value

    def blank_entry(self, i, j):
        """Returns true if an entry is blank"""
        return self.get_entry(i, j) == 0
    
    def get_blank_coords(self):
        """Returns the coordinates of the first blank entry"""
        for i in range(9):
            for j in range(9):
                if self.blank_entry(i, j):
                    return (i, j)
    
    def get_row(self, i):
        """Returns the ith row"""
        return self.__puzzle[i]
    
    def get_column(self, j):
        """Returns the jth column"""
        return [row[j] for row in self.__puzzle]
    
    def get_square(self, i, j):
        """Returns the (i, j)th square"""
        return map(lambda (x, y): self.get_entry(x + 3 * i, y + 3 * j),
                   self.__square_coords)

    def get_puzzle(self):
        """Returns a copy of the puzzle"""
        return list(self.__puzzle)
    
    def get_possible_values(self, i, j):
        """Returns the possible values for the (i, j)th entry"""
        if self.blank_entry(i, j):
            values = set(range(1, 10))
            values -= set(self.get_row(i))
            values -= set(self.get_column(j))
            values -= set(self.get_square(i / 3, j / 3))
            return values
        else:
            return [self.get_entry(i, j)]


def solve(s):
    """Return solved puzzle (or False if puzzle is impossible)"""
    coords = s.get_blank_coords()
    if coords == None:
        # No blank entries remaining
        return s
   
    values = s.get_possible_values(*coords)
    for value in values:
        # Set the first blank entry to a possible value
        s.set_entry(coords[0], coords[1], value)
        
        # Recursively solve puzzle from current configuration
        result = solve(s)
        if result:
            return result
        else:
            # Undo last move
            s.set_entry(coords[0], coords[1], 0)
    
    # Puzzle is impossible from current configuration
    return False


if __name__ == '__main__':
    s = Sudoku()
    print s
    print solve(s)
