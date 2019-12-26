# import modules that are needed
import connectfour
import connectfour_interface


'''
Checks whose turn it is.
'''
def _print_turn(GameStatus: "GameStatus"):

    if GameStatus.turn == 1:
        print("RED'S TURN")
    elif GameState.turn == 2:
        print("YELLOW'S TURN")


'''
Checks for a winner if there is a winner.
'''
def _check_winner(GameStatus: "GameStatus") -> int:

    winner: int = connectfour.winner(GameStatus)
    if winner == 1:
        print("RED WINS")
    elif winner == 2:
        print("YELLOW WINS")
    else:
        winner = 0

    return winner


'''
Runs the game.
Creates new game.
Game continues until there is a winner.
'''
if __name__ == '__main__':

    #initialize
    theWinner: int = 0
    GameState = connectfour.new_game()

    while theWinner == 0:

        # user interface
        connectfour_interface.print_board(GameState)
        _print_turn(GameState)

        # player input
        GameState, action, col = connectfour_interface.player_input(GameState)

        # checks for winner
        theWinner = _check_winner(GameState)

