import pygame, sys, os
import random
from board import Board
from Ai import Ai


#------------------------------------------------Pyame Global variables-----------------------------------------------------------------#

#load module
pygame.init()
clock = pygame.time.Clock()

#colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (225, 93, 68)
SQUARES = (30, 170, 150)
GRID = (30, 30, 50)

#settings for display
s_width = 600
s_height = 400
screen = pygame.display.set_mode([s_width, s_height], pygame.RESIZABLE)
pygame.display.set_caption("TicTacToe")
screen.fill( BG )
user_input = []
x = 100
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#game font
pygame.font.init()
font_words = pygame.font.SysFont("georgia", 15)
font_plays = pygame.font.SysFont("georgia", s_height//3)


#grid size
g_width = 390//3
g_height = 390//3
g_margin = 2
g_center = (400//3 + 10)


#------------------------------------------------General game UI methods-----------------------------------------------------------------#

def draw_grid( board=False, gameplay = False):
    """Implements grid, complete with border and space for UI"""
    screen.fill( BG )
    for row in range(3):
        for column in range(3):
            #draw grids for UI
            pygame.draw.rect(screen, SQUARES, [(g_margin + g_width) * column + g_margin, (g_margin+g_height)
            * row + g_margin, g_width, g_height])
            #vertical interior grid
            pygame.draw.line( screen, GRID, (130 * column + (2 * column), 0), ((130 * column) + (2 * column), 397), width=5)
            if board:
                if board[row][column] == "X":
                    board_play = font_plays.render(("X"), 1, BLACK)
                    screen.blit(board_play, ( 25 + (130 * column), (130 * row)))
                if board[row][column] == "O":
                    board_play = font_plays.render(("O"), 1, BLACK)
                    screen.blit(board_play, (25 + (130 * column),(130 * row)))
        #horizontal interior grid
        pygame.draw.line( screen, GRID, (0, (row * 130) + (2 * row)), (397, (row * 130) + (2 * row)), width=5)

    #bottom and top grid
    pygame.draw.line( screen, GRID, (0, 2), (397, 2), width=5)
    pygame.draw.line( screen, GRID, (0, 397), (397, 397), width=5)

    #leftmost and rightmost vertical grid
    pygame.draw.line( screen, GRID, (2, 0), (2, 400), width=5)
    pygame.draw.line( screen, GRID, (397, 0), (397, 400), width=5)

 
def draw_instructions(instr = False):
    """Method to show instructions, initialized to False."""
    #If passed instr in method, user has selected an incorrect team
    if instr:
        text = font_words.render("Please choose 'X' or 'O'", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (500, 25)
        screen.blit(text, textRect)
    else:
        text = font_words.render("To play as 'X', please press 'X'", True, BLACK)
        text2 = font_words.render("Otherwise, please press 'O'", True, BLACK)
        textRect1, textRect2 = text.get_rect(), text2.get_rect()
        textRect1.center = (500, 25)
        textRect2.center = (496, 50)
        screen.blit(text, textRect1), screen.blit(text2, textRect2)


#------------------------------------------------General game logic-----------------------------------------------------------------#

def check_draw(board):
    """Method to make a quick check if there are empty spaces to play"""
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True

def player_win(board, team):
    """"Method to check if given team has a win condition on given board"""
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

def replay_screen(result):
    """#method to ask user if they want to replay. Takes game result as argument"""
    pos = pygame.mouse.get_pos()

    #Prompt text
    text = font_words.render(f"You {result}! Play again?", True, BLACK)
    screen.blit(text , (405 ,s_height//2 - 14))
    text = font_words.render("Yes ('Y')", True, BLACK)
    screen.blit(text , (410,s_height//2 + 14))
    text = font_words.render("No, I can't win! ('N')", True, BLACK)
    screen.blit(text , (410,s_height//2 + 39))
    pygame.display.update()
    
    #wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    game_loop()
                if event.key == pygame.K_n:
                    waiting = False
                    quit()

def bot_move(board, bot):
    """Method to register computer player moves. Utilizes method in Ai class"""
    row, col = bot.make_move(board)
    return row, col
        

#------------------------------------------------General gameplay methods-----------------------------------------------------------------#

def new_game(player, opponent):
    """"Method to initialize new game. Takes chosen player team and alternative computer team as arguments."""
    
    #retrieve new Board class object
    board = Board()
    board.get_current_board()

    #initialize a player and bot class, with team set to opponenet
    player_team = player
    bot = Ai(opponent, player_team)
    draw_grid(board.get_current_board(), gameplay=True)
    
    #randomly select who goes first
    inProgress = True
    bot_first = [False, True]
    bot_turn = random.choice(bot_first)
    first_turn = True

    while inProgress:
        pos = pygame.mouse.get_pos()
        
        #Determine bot move
        while bot_turn:
            board.get_current_board()
            draw_grid(board.get_current_board(), gameplay=True)
            #Notify player to await turn
            text = font_words.render("Computer is making a move...", True, BLACK)
            textRect = text.get_rect()
            textRect.center = (995, 100)
            screen.blit(text, textRect)
            pygame.display.update()
            if not first_turn:
                #Call bot move method, register move, update board
                bot_moves = bot_move(board.get_current_board(), bot)
                board.update_board(bot_moves[0], bot_moves[1], opponent)
                bot_turn = False
                board.get_current_board()
                draw_grid(board.get_current_board(), gameplay=True)
            if first_turn:
                first_turn = False
                #First turn must consider ~255,000 different moves, most efficient if random
                bot_moves = (random.randint(0,2), random.randint(0,2))
                board.update_board(bot_moves[0], bot_moves[1], opponent)
                bot_turn = False
                board.get_current_board()
                draw_grid(board.get_current_board(), gameplay=True)
        # User turn
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and pos[0] < 389 and pos[1] < 389:
                #Register player click  location, translate to board index
                first_turn = False
                column = pos[0]//130
                row = pos[1]//130
                if board.update_board(row, column, player):
                    draw_grid(board.get_current_board(), gameplay=True)
                    pygame.display.update()
                    bot_turn = True #switch turns

            #prompt user to play turn
            board.get_current_board()
            draw_grid(board.get_current_board(), gameplay=True)
            text = font_words.render("Make your move...", True, BLACK)
            textRect = text.get_rect()
            textRect.center = (497, 50)
            screen.blit(text, textRect)
            pygame.display.update()

            #check game conditions
            
            if player_win(board.board, player_team):
                inProgress = False
                result = "won"
            elif player_win(board.board, opponent):
                inProgress = False
                result = "lost"
            elif check_draw(board.board):
                inProgress = False
                result = "drew"
       
    
    draw_grid(board.get_current_board(), gameplay=True)
    replay_screen(result)

initial = True
def game_loop():
    """Method called to initialize game loop. First initializes intro screen, generates new game state."""    
    
    gameExit = False
    initial = True
    while not gameExit:
        #initial screen prompts user to choose team, show empty grid
        if initial:
            draw_grid()
            draw_instructions()
        #player input for team choice
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #player chooses team, assign opposite to bot
                if event.key == pygame.K_x and initial == True:
                    initial = False
                    draw_grid()
                    new_game("X", "O")
                if event.key == pygame.K_o and initial == True:
                    initial = False
                    draw_grid()
                    new_game("O", "X")
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    game_loop()
    pygame.quit()
    quit()