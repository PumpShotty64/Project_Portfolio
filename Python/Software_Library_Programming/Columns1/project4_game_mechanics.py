
# game board class
class GameState:
    # initialized field variables
    def __init__(self) -> None:
        self._field = []

    # creates field depending on EMPTY or CONTENTS
    def initialize_field(self, rows: int, cols: int, game_start: str) -> list:

        # start game empty
        if game_start == 'EMPTY':
            for i in range(rows + 1):
                self._field.append([])
                for j in range(cols):
                    if i == rows:
                        self._field[i].append('---')
                    else:
                        self._field[i].append('   ')

        # start game with jewels
        elif game_start == 'CONTENTS':
            # for r lines, there must be c characters inputed
            for r in range(rows + 1):
                userInput = ''
                if r < rows:
                    userInput = input()
                self._field.append([])
                for c in range(cols):
                    if r == rows:
                        self._field[r].append('---')
                    else:
                        self._field[r].append(f" {userInput[c]} ")

        return self._field


    # displays field
    def show_field(self) -> list:
        return self._field


# faller object class
class Faller:
    def __init__(self, topF: str, midF: str, botF: str, col:int) -> None:
        self._topF = topF
        self._midF = midF
        self._botF = botF
        self._row = 0
        self._col = col
        self._faller_state = 0 # 0 for floating, 1 for landed, 2 for frozen

    def show_faller_info(self) -> tuple:
        return self._topF, self._midF, self._botF, self._col, self._faller_state

    # show column
    def show_column_info(self) -> tuple:
        return self._topF, self._midF, self._botF

    # show current row and col
    def show_current_row_col(self) -> tuple:
        return  self._row, self._col

    # show border state of column
    def show_column_state(self) -> int:
        return self._faller_state

    # rotates column
    def faller_rotating(self, topF: str, midF: str, botF: str) -> tuple:
        self._topF = botF
        self._midF = topF
        self._botF = midF

        return self._topF, self._midF, self._botF

    # move right
    def faller_right(self) -> int:
        self._col += 1
        return self._col

    # move left
    def faller_left(self) -> int:
        self._col -= 1
        return self._col

    # next border state
    def faller_next_state(self) -> int:
        self._faller_state += 1
        return self._faller_state

    # landed, but unlanded
    def faller_previous_state(self) -> int:
        self._faller_state -= 1
        return self._faller_state

    # next row
    def next_row(self) -> int:
        self._row += 1
        return self._row


class InvalidMoveError(Exception):
    '''
    Raised whenever an invalid move is made
    '''
    pass

# creates a new game
def new_game(game_state: GameState, inputs: tuple) -> list:
    # opens tuples of inputs
    rowLen, colLen, initField = inputs

    # initializes field for new game
    game_state.initialize_field(int(rowLen), int(colLen), initField)

    return game_state.show_field()


# creates a faller object
def create_faller(topF: str, midF: str, botF: str, col: int, gameState: GameState) -> Faller:
    #
    _is_valid_column_number(gameState, col)
    # stores information in new object
    fallerObj = Faller(topF, midF, botF, col)

    return fallerObj


# content setup
def content_intialization(gameState: GameState) -> bool:
    # gather parameters
    theField = gameState.show_field()
    # gather info
    maxRow = len(theField)
    maxCol= len(theField[0])

    # same idea as transposing; just pop and append empty squares at the beginning
    for col in range(maxCol):
        tempList = []

        for row in range(maxRow):
            tempList.append(theField[row][col])

        for l in range(len(tempList)):
            if tempList[l] == '   ':
                tempList.pop(l)
                tempList.insert(0, '   ')

        for n in range(maxRow):
            theField[n][col] = tempList[n]

    # check for any matches
    isMatching = _winning_conditions(gameState)

    return isMatching


# faller falls down one
def faller_falling(fallerObj: Faller, gameState: GameState) -> tuple:
    # obtains info of faller object
    topF, midF, botF = fallerObj.show_column_info() # jewel order top to bottom
    row, col = fallerObj.show_current_row_col()     # row and column
    fallState = fallerObj.show_column_state()       # [] || or **

    # allow use for index
    col = col - 1

    # gathers the current field data
    theField = gameState.show_field()

    # initialize variable
    isMatching = False
    hasFroze = False
    gameOver = False
    emptyCount = 0

    # check for empty squares
    for i in range(len(theField)):
        if theField[i][col] == '   ':
            emptyCount += 1

    # lose immediately if column already full
    if emptyCount == 0 and fallState != 1:
        gameOver = True
        return isMatching, hasFroze, gameOver

    # falling code
    if fallState == 0:

        # changes state if landed
        if theField[row + 1][col] != '   ':
            fallerObj.faller_next_state()

            tF, mF, bF = _faller_status(fallerObj)
        else:
            tF, mF, bF = _faller_status(fallerObj)

        # sets squares as the specific jewels
        if row >= 0:
            theField[row][col] = bF
        if row - 1 >= 0:
            theField[row - 1][col] = mF
        if row - 2 >= 0:
            theField[row - 2][col] = tF
        theField[len(theField) - 1][col] = '---'

        # clear squares above column
        i = 3
        while row - i >= 0:
            theField[row - i][col] = '   '
            i += 1

    # landed and froze code
    else:
        tF = f" {topF} "
        mF = f" {midF} "
        bF = f" {botF} "
        if row - 1 >= 0:
            theField[row - 1][col] = bF
        if row - 2 >= 0:
            theField[row - 2][col] = mF
        if row - 3 >= 0:
            theField[row - 3][col] = tF

        hasFroze = True

        # immediately check for any matches
        isMatching = _winning_conditions(gameState)
        # game over condition
        if not isMatching and row - 3 < 0:
            gameOver = True

    fallerObj.next_row()

    return isMatching, hasFroze, gameOver


# rotate faller
def faller_rotate(fallerObj: Faller, gameState: GameState) -> None:
    # obtains info of faller object
    topF, midF, botF = fallerObj.show_column_info()  # jewel order top to bottom
    row, col = fallerObj.show_current_row_col()  # row and column

    # allow use for index
    col = col - 1

    # gathers the current field data
    theField = gameState.show_field()

    # rotate object
    fallerObj.faller_rotating(topF, midF, botF)

    # determine border symbol for object
    tF, mF, bF = _faller_status(fallerObj)

    # we have the row of the bottom most tile, we also have the column of the tiles
    if row - 1 >= 0:
        theField[row - 1][col] = bF
    if row - 2 >= 0:
        theField[row - 2][col] = mF
    if row - 3 >= 0:
        theField[row - 3][col] = tF


# move faller right
def faller_move_right(fallerObj: Faller, gameState: GameState) -> None:
    # obtains info of faller object
    row, col = fallerObj.show_current_row_col()  # row and column
    fallState = fallerObj.show_column_state()  # shows border state

    # gathers the current field data
    theField = gameState.show_field()
    # conditions for moving right
    if col < len(theField[0]) and theField[row - 1][col] == '   ':
        if theField[row][col] == '   ':
            if fallState == 1:
                fallerObj.faller_previous_state()
        else:
            if theField[row][col - 1] == '   ':
                fallerObj.faller_next_state()

        # determine border symbol for object
        tF, mF, bF = _faller_status(fallerObj)

        # move left object
        col = fallerObj.faller_right()

        # allow use for index
        col = col - 1

        # we have the row of the bottom most tile, we also have the column of the tiles
        if row - 1 >= 0:
            theField[row - 1][col] = bF
            theField[row - 1][col - 1] = '   '
        if row - 2 >= 0:
            theField[row - 2][col] = mF
            theField[row - 2][col - 1] = '   '
        if row - 3 >= 0:
            theField[row - 3][col] = tF
            theField[row - 3][col - 1] = '   '


# move faller left
def faller_move_left(fallerObj: Faller, gameState: GameState) -> None:
    # obtains info of faller object
    row, col = fallerObj.show_current_row_col()  # row and column
    fallState = fallerObj.show_column_state()    # shows border state

    # gathers the current field data
    theField = gameState.show_field()

    if col > 1 and theField[row - 1][col - 2] == '   ':

        if theField[row][col - 2] == '   ':
            if fallState == 1:
                fallerObj.faller_previous_state()
        else:
            if theField[row][col - 1] == '   ':
                fallerObj.faller_next_state()

        # determine border symbol for object
        tF, mF, bF = _faller_status(fallerObj)

        # move left object
        col = fallerObj.faller_left()

        # allow use for index
        col = col - 1

        # we have the row of the bottom most tile, we also have the column of the tiles
        if row - 1 >= 0:
            theField[row - 1][col] = bF
            theField[row - 1][col + 1] = '   '
        if row - 2 >= 0:
            theField[row - 2][col] = mF
            theField[row - 2][col + 1] = '   '
        if row - 3 >= 0:
            theField[row - 3][col] = tF
            theField[row - 3][col + 1] = '   '


# clear matches
def clear_matches(fallerObj: Faller, gameState: GameState, currentRow: int) -> tuple:

    # intialize parameters
    gameField = gameState.show_field()
    gameOver = False

    # checks for matches. Matching clears the square
    for row in range(len(gameField)):
        for col in range(len(gameField[0])):
            if gameField[row][col].startswith('*'):
                gameField[row][col] = '   '

    # moves all the blocks down
    for col in range(len(gameField[0])):
        tracker = 0
        while True:
            for row in range(len(gameField) - 1):
                # gathers gem data that is floathing and furthest down
                # conditions could be off
                if gameField[row + 1][col] == '   ' and gameField[row][col] != '   ':
                    tempJewel = gameField[row][col]
                    # checks for collision
                    if gameField[row + 1] != '   ':
                        gameField[row + 1][col] = tempJewel
                        gameField[row][col] = '   '
            # condition to break loop
            tracker += 1
            # basically after the thing checks the entire column, then move to next column
            if tracker >= len(gameField):
                break

    # bring down the leftover jewels not on screen
    if fallerObj is not None:
        tF, mF, bF = fallerObj.show_column_info()
        rowF, colF = fallerObj.show_current_row_col()
        for row in range(len(gameField) - 1):
            if gameField[row][colF - 1] == '   ' and gameField[row + 1][colF - 1] != '   ':
                if currentRow == 1 and rowF - 1 == 1:
                    gameField[row][colF - 1] = f" {tF} "
                    if row - 1 >= 0:
                        gameField[row - 1][colF - 1] = f" {mF} "
                    else:
                        gameOver = True

                elif currentRow == 2 and rowF - 1 == 2:
                    gameField[row][colF - 1] = f" {tF} "

    # checks for any matches
    isMatching = _winning_conditions(gameState)
    hasFroze = True

    return isMatching, hasFroze, gameOver


# check faller border
def _faller_status(fallerObj: Faller) -> tuple:
    # obtains info of faller object
    topF, midF, botF = fallerObj.show_column_info()  # jewel order top to bottom
    fallState = fallerObj.show_column_state()        # [] || or **

    if fallState == 0:
        bF = f"[{botF}]"
        mF = f"[{midF}]"
        tF = f"[{topF}]"

    elif fallState == 1:
        bF = f"|{botF}|"
        mF = f"|{midF}|"
        tF = f"|{topF}|"

    else:
        bF = f" {botF} "
        mF = f" {midF} "
        tF = f" {topF} "

    return tF, mF, bF


# winning conditions for gems
def _winning_conditions(gameState: GameState) -> bool:
    # gather parameters
    gameField = gameState.show_field()
    maxRow = len(gameField) - 1
    maxCol = len(gameField[0])

    # initiate variables
    isMatching = False

    # matching in column
    for col in range(maxCol):
        matchCounter = 1
        for row in range(1, maxRow):
            # thing is initiating at second row and moving down
            if gameField[row][col][1] == gameField[row - 1][col][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and gameField[row][col][1] != gameField[row + 1][col][1]:
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row - i][col] = f"*{theJewel}*"
            # reset
            else:
                matchCounter = 1
    # check row match
    for row in range(maxRow):
        matchCounter = 1
        for col in range(1, maxCol):
            if gameField[row][col][1] == gameField[row][col - 1][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and (col >= maxCol - 1 or gameField[row][col][1] != gameField[row][col + 1][1]):
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row][col - i] = f"*{theJewel}*"
            # reset
            else:
                matchCounter = 1
    # matching diagonals - from bottom left to top right
    for row in range(maxRow):
        # this only covers half the diagonal
        # if row is greater than max, then loop over the columns from 1 to maxCol
        matchCounter = 1
        col = 0
        while True:
            if col >= 1 and gameField[row][col][1] == gameField[row + 1][col - 1][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and (col > maxCol - 2 or gameField[row][col][1] != gameField[row - 1][col + 1][1]):
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row + i][col - i] = f"*{theJewel}*"
            # reset
            else:
                matchCounter = 1
            if row <= 0 or col >= maxCol - 1:
                break
            row -= 1
            col += 1
    # other half of diagonal
    for col in range(maxCol):
        matchCounter = 1
        row = maxRow - 1
        while True:
            if col >= 2 and gameField[row][col][1] == gameField[row + 1][col - 1][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and (col > maxCol - 2 or gameField[row][col][1] != gameField[row - 1][col + 1][1]):
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row + i][col - i] = f"*{theJewel}*"
            else:
                matchCounter = 1
            if row <= 0 or col >= maxCol - 1:
                break
            row -= 1
            col += 1
    # other diagonal - top left to bottom right
    for row in range(maxRow):
        matchCounter = 1
        col = 0
        while True:
            if col >= 1 and gameField[row][col][1] == gameField[row - 1][col - 1][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and (col > maxCol - 2 or gameField[row][col][1] != gameField[row + 1][col + 1][1]):
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row - i][col - i] = f"*{theJewel}*"
            else:
                matchCounter = 1
            if row >= maxRow - 1 or col >= maxCol - 1:
                break
            row += 1
            col += 1
    # other half of diagonal
    for col in range(maxCol):
        matchCounter = 1
        row = 0
        while True:
            if col >= 2 and gameField[row][col][1] == gameField[row - 1][col - 1][1] and gameField[row][col] != '   ':
                matchCounter += 1
                if matchCounter >= 3 and (col > maxCol - 2 or gameField[row][col][1] != gameField[row + 1][col + 1][1]):
                    isMatching = True
                    theJewel = gameField[row][col].strip().strip('*')
                    for i in range(matchCounter):
                        gameField[row - i][col - i] = f"*{theJewel}*"
            else:
                matchCounter = 1
            if row >= maxRow - 1 or col >= maxCol - 1:
                break
            row += 1
            col += 1

    return isMatching

# raises exception if invalid column number
def _is_valid_column_number(gameState: GameState, col_num: int):
    theField = gameState.show_field()
    if col_num > len(theField) - 1:
        raise InvalidMoveError()