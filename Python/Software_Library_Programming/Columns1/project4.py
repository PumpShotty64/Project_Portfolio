# Jordan Nguyen
#25409215

import project4_game_mechanics as GM

# gathers user input
def _field_input() -> tuple:
    rowLength = input()
    colLength = input()
    initializeField = input()

    return rowLength, colLength, initializeField


# creates faller object or quits
def _create_faller(gameState: 'GameState', command: str) -> 'Faller':

    if command.startswith('F'):
        faller, column, topF, midF, botF = command.split()
        if int(column) >= 1:
            fallerObj = GM.create_faller(topF, midF, botF, int(column), gameState)
            return fallerObj

    elif command == 'Q':
        quit()


# game commands for faller
def _game_commands(game_state: 'GameState', fallerObj: 'Faller', track_row: int, command: str, isMatching: bool) -> tuple:

    # intialize variables
    hasFrozen = False
    gameOver = False

    # pretty self explanatory
    if not isMatching:
        if command == 'R':
            GM.faller_rotate(fallerObj, game_state)

        elif command == '<':
            GM.faller_move_left(fallerObj, game_state)

        elif command == '>':
            GM.faller_move_right(fallerObj, game_state)

        elif command == "":
            isMatching, hasFrozen, gameOver = GM.faller_falling(fallerObj, game_state)
            track_row += 1

    elif isMatching:
        if command == "":
            isMatching, hasFrozen, gameOver = GM.clear_matches(fallerObj, game_state, track_row)
            track_row += 1

    if command == 'Q':
        quit()

    return track_row, isMatching, hasFrozen, gameOver


# prints user interface
def _user_interface(gameField: list) -> None:

    # actual interface
    for i in range(len(gameField)):
        colStr = ''
        for j in range(len(gameField[i])):
            colStr += gameField[i][j]

        if i == len(gameField) - 1:
            print(' ' + colStr + ' ')
        else:
            print('|' + colStr + '|')


# runs main functions
def run() -> None:
    # gathers user input
    fieldInput = _field_input()

    # create field object. gameState will hold all class information
    gameState = GM.GameState()

    # initialized game
    theField = GM.new_game(gameState, fieldInput)

    # expand inputs
    rowLength, colLength, commandInput = fieldInput

    # specific to contents only
    if commandInput == 'CONTENTS':
        isMatching = GM.content_intialization(gameState)

        # display user interface
        _user_interface(theField)

        # IF MATCH
        while isMatching:
            userInput = input()
            # game commands
            currentRow, isMatching, hasFroze, gameOver = _game_commands(gameState, None, 0, userInput, isMatching)

            # prints user interface again
            _user_interface(theField)

    # print field for when empty
    elif commandInput == 'EMPTY':
        # display user interface
        _user_interface(theField)

    # a series of commands during endless game
    while True:
        # user input to either create object or quit
        while True:
                userInput = input()
                theFaller = _create_faller(gameState, userInput)
                if theFaller is not None:
                    break
                _user_interface(theField)

        # initialize variables
        currentRow, col = theFaller.show_current_row_col()
        isMatch = False
        hasFroze = False

        # quick status update of field after faller created
        isMatching, hasFrozen, gameOver = GM.faller_falling(theFaller, gameState)

        # prints board
        _user_interface(theField)

        if gameOver:
            print('GAME OVER')
            quit()

        # STAGE 1
        while not hasFroze:
            userInput = input()

            # runs game command
            currentRow, isMatch, hasFroze, gameOver = _game_commands(gameState, theFaller, int(currentRow), userInput, isMatch)

            # prints user interface again
            _user_interface(theField)

            # IF MATCH
            while isMatch:
                userInput = input()
                currentRow, isMatch, hasFroze, gameOver = _game_commands(gameState, theFaller, int(currentRow), userInput, isMatch)

                # prints user interface again
                _user_interface(theField)

            if gameOver:
                print('GAME OVER')
                quit()


if __name__ == '__main__':
    run()
