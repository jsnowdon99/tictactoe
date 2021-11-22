from board import Board

class Ai:
    """"Bot class, requires team assignment. Features Minimax algorithm to choose best move."""
    def __init__(self, team, opponent):
        self.team = team
        self.opponent = opponent

    def get_team(self):
        return self.team
    
    def get_opponent(self):
        return self.opponent
    
    def set_team(self, team):
        self.team = team
    
    def make_move(self, board):
        """Will call Minimax for each empty square on given board. Since only 9 positions, does not utilize depth."""
        
        #Min score is unatainable; register initial move as board[0][0]
        bestScore = -9999
        bestMove = 0, 0
        
        for row in range(3):
            for col in range(3):
                #if empty space, set to current minimizing team.
                if board[row][col] == " ":
                    board[row][col] = self.get_team()
                    #begin recursive search up choice tree
                    currScore = self.miniMax(board, False)
                    #reset board after calculation; update score and moves if necessary
                    board[row][col] = " "
                    if currScore > bestScore:
                        bestScore = currScore
                        # will store best possible result given all choices (typically first)
                        bestMove = row, col
        return bestMove
        
    def miniMax(self, board, maximizing):
        """MiniMax algorithm. Checks if given move is winning state, checks possible moves in choice tree. Returns optimal move for min and max players"""

        #maximize own score, choose winning move
        if check_if_winning_move(board, self.get_team()):
            return 1

        #minimize opponent score
        elif check_if_winning_move(board, self.get_opponent()):
            return -1

        #draw is more maximal than loss. But, not ideal.
        elif is_draw(board):
            return 0
        
        #if player is maximizing their score. 
        if maximizing:
            #Choose move that beats negative score with maximum point value
            bestScore = -9999
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        #Set to current team
                        board[row][col] = self.get_team()
                        #Check for minimizer's best choice
                        currScore = self.miniMax(board, False)
                        #reset
                        board[row][col] = " "
                        if currScore > bestScore:
                            bestScore = currScore
            return bestScore
        
        else:
            #as above, but we want to find minimum score
            bestScore = 9999
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        board[row][col] = self.get_opponent()
                        #Check for maximizer's best choice
                        currScore = self.miniMax(board, True)
                        board[row][col] = " "
                        if currScore < bestScore:
                            bestScore = currScore
            return bestScore
        


def check_if_winning_move(board, team):
    """Check if move wins the game given current board and team."""
    if (board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] == team):
        return True
    elif (board[1][0] == board[1][1] and board[1][2] == board[1][0] and board[1][0] == team):
        return True
    elif (board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] == team):
        return True
    elif (board[0][0] == board[1][0] and board[2][0] == board[0][0] and board[0][0] == team):
        return True
    elif (board[0][1] == board[1][1] and board[2][1] == board[0][1] and board[0][1] == team):
        return True
    elif (board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] == team):
        return True
    elif (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] == team):
        return True
    elif (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] == team):
        return True
    else:
        return False

def is_draw(board):
    """Quick draw check condition given current board"""
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


