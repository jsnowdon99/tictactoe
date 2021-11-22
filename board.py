class Board:
    """Simple board class to store and modify board plays"""
    def __init__(self):
        self.board = [
            [" ", " "," "],
            [" "," "," "],
            [" "," "," "]
            ]

    #getters
    def get_current_board(self):
        return self.board
    
    #method to update current board class, takes a row, column and player team as arguments.
    def update_board(self, row, col, player):
        # move must be within bounds and in empty cell
        if self.board[row][col] == "X" or self.board[row][col] == "Y" or row > 2 or col > 2:
            self.board[row][col] = player
            return False
        else:
            self.board[row][col] = player
            return True
