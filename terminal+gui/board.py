import random

class Board: 
    def __init__(self):
        # Initialize a 4x4 grid filled with zeros
        self.rows=[[0]*4 for _ in range(4)]
        # Add two starting random tiles (2 or 4)
        self.add_random_tile()
        self.add_random_tile()
    

    def get_empty_cell(self):
        # Return list of (row, col) positions where the cell value is 0
        return [(i, j) for i in range(4) for j in range(4) if self.rows[i][j] == 0]
    
    def add_random_tile(self):
        # Select a random empty cell and place a 2 (mostly) or 4
        empty_cells = self.get_empty_cell()
        if empty_cells:
            # Choose one empty position randomly
            i, j = random.choice(empty_cells)
            # Insert new tile (higher chance for 2)
            self.rows[i][j] = random.choice([2,2,2,2,4])

    def display(self):
        # Print the board in grid format
        print()
        print("+----" * 4 + "+")
        for row in self.rows:
            for cell in row:
                # Print blank for 0, otherwise print the number
                if cell == 0:
                    print(f"|{' ':^4}", end="")
                else:
                    print(f"|{cell:^4}", end="")
            print("|")
            print("+----" * 4 + "+")

if __name__ == "__main__":
    a = Board()
    a.display()
