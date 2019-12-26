# import modules that are needed
import connectfour

'''
Prints board interface
'''
def print_board(GameStatus: "GameStatus"):
    for i in range(1, connectfour.BOARD_COLUMNS + 1):
        print(i, end="  ")
    print()

    for row in range(connectfour.BOARD_ROWS):
        for column in range(connectfour.BOARD_COLUMNS):
            if GameStatus.board[column][row] == 0:
                print(".", end="  ")
            elif GameStatus.board[column][row] == 1:
                print("R", end="  ")
            elif GameStatus.board[column][row] == 2:
                print("Y", end="  ")
        print()


'''
Asks user for action input.
Checks if input is valid.
If not, returns an error statement.
Replays code until input is valid.
'''
def player_input(GameStatus: "GameStatus") -> tuple:

    while True:

        try:
            action, col = str(input("Input Format [DROP or POP] [#]: ")).strip().split()

            if action == "DROP" or action == "POP":

                if col.isdigit() == True and 1 <= int(col) <= 7:

                    GameStatus = game_command(GameStatus, action, int(col))
                    break

                else:
                    print("ERROR! Input must be an integer 1 through 7")
            else:
                print("ERROR! Input must be DROP or POP")

        except ValueError:
            print("ERROR! Invalid input format")

        except connectfour.InvalidMoveError:
            print("ERROR! INVALID MOVE")

        except:
            print("ERROR! Try again!")

    return GameStatus, action, col


'''
Runs the action of DROP or POP.
Returns game status once action is played.
'''
def game_command(GameStatus: "GameStatus", action: str, col: int):

    if action == "DROP":
        GameStatus = connectfour.drop(GameStatus, col - 1)

    elif action == "POP":
        GameStatus = connectfour.pop(GameStatus, col - 1)

    return GameStatus

