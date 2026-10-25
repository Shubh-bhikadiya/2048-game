score = 0 # Global score variable

def move_left(matrix):
    global check
    check = True # Used to check if any movement or merge happened

    def compress(matrix):
        # Shift all non-zero elements to the left side
        new_matrix=[]
        for row in matrix:
            new_row=[]
            for x in row:
                if x!=0 :
                    new_row.append(x) # Keep non-zero values
            while len(new_row)<4:
                new_row.append(0) # Fill remaining spaces with zeros
            new_matrix.append(new_row)
        return new_matrix

    def merge(matrix):
        # Combine equal adjacent tiles (left to right)
        global score
        for i in range(0,4):
            for j in range(0,3):
                if matrix[i][j]==matrix[i][j+1]:
                    matrix[i][j]+=matrix[i][j+1] # Merge tiles
                    score+=matrix[i][j] # Update score
                    matrix[i][j+1]=0 # Set merged tile to zero
        return matrix
    
    # Copy original matrix to detect change later
    original = [row[:] for row in matrix]

    matrix=compress(matrix) # First shift
    matrix=merge(matrix)    # Merge equal tiles
    matrix=compress(matrix) # Shift again after merge


    if matrix == original:
        check = False # No change occurred


    return matrix


def move_right(matrix):

    def mirror_image(matrix):
        # Reverse each row to mirror horizontally
        new_matrix=[]
        for row in matrix:
            new_row=[]
            for i in range(3,-1,-1):
                new_row.append(row[i])
            new_matrix.append(new_row)
        return new_matrix
    
    matrix=mirror_image(matrix) # Mirror left-right
    matrix=move_left(matrix)    # Reuse move_left logic
    matrix=mirror_image(matrix) # Mirror back to original orientation   
    return matrix



def move_up(matrix):

    def transpose(matrix):
        # Convert rows to columns and vice versa
        return [[row[i] for row in matrix] for i in range(4)]
    
    matrix=transpose(matrix) # Transpose → treat up as left move
    matrix=move_left(matrix)
    matrix=transpose(matrix) # Transpose back

    return matrix

def move_down(matrix):

    def transpose(matrix):
        # Convert rows to columns and vice versa
        return [[row[i] for row in matrix] for i in range(4)]
    
    matrix=transpose(matrix) # same as upper one
    matrix=move_right(matrix)
    matrix=transpose(matrix)

    return matrix

def Game_win(matrix):
    result=False
    # Check if any cell contains 2048 or more
    for row in matrix:
        for x in row:
            if x>=2048:
                result=True

    return result
                
def Game_over(matrix):

    def transpose(matrix):
        # Convert rows to columns
        return [[row[i] for row in matrix] for i in range(4)]
    
    # If any cell is empty, the game is not over
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                return False
            
    transpose_matrix=transpose(matrix)

    # Check for possible merges in rows and columns
    for i in range(4):
        for j in range(3):
            # If any adjacent equal tiles exist, game is not over
            if (matrix[i][j]==matrix[i][j+1] or transpose_matrix[i][j]==transpose_matrix[i][j+1]):
                return False
            
    return True  # No moves left
