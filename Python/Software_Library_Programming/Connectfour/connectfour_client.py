# import modules that are needed
import connectfour
import connectfour_server
import connectfour_interface

'''
Asks the user for the host and port.
Connects them to the server if connection is found.
'''
def _connecting_to_server() -> tuple:

    while True:
        try:
            host, port = server.read_server()

            print(f"Connecting to {host} port {port}...")
            serverConnection = server.connection(host, port)
            print("Connected!")

            return serverConnection

        except:
            print("Server not found!")



'''
Asks for the username of User and returns username.
Makes sure the username is in correct format.
'''
def _user_name() -> str:

    while True:
        name = str(input("Username: "))
        if " " in name:
            print("Cannot have whitespace")
        else:
            break

    return name


'''
Runs the protocol to connect to a game with AI
'''
def _run_protocol():

    message = f"I32CFSP_HELLO {userName}"
    server.send_message(connection, message)
    server.recieve_action(connection)

    message = "AI_GAME"
    server.send_message(connection, message)
    server.recieve_action(connection)


'''
Function that runs the players turn.
Asks for user input and returns the updated game status.
'''
def _player_turn(GameStatus: "GameStatus"):

    # prints board
    interface.print_board(GameStatus)

    # player input
    GameStatus, action, col = interface.player_input(GameStatus)

    # talks to server
    server.send_action(connection, action, col)

    return GameStatus


'''
AI calls out an action and it runs and updates game status.
'''
def _ai_turn(GameStatus: "GameStatus"):

    interface.print_board(GameStatus)
    print("AI'S MOVE:", response)

    action, col = response.split()
    GameStatus = interface.game_command(GameStatus, action, int(col))

    return GameStatus


'''
Allows user to play with AI.
Calls functions that connect to server.
Then creates a new game.
Then communicates with user until game is over.
Game over leads to server connection closing.
'''
if __name__ == '__main__':

    # steps to connecting to server
    server = connectfour_server
    interface = connectfour_interface
    connection = _connecting_to_server()
    userName: str = _user_name()
    print("Welcome", userName)
    _run_protocol()

    # starts new game
    GameState = connectfour.new_game()

    while True:

        response: str = ""

        # player move
        GameState = _player_turn(GameState)

        while response != "READY":
            # server talks to client
            response = server.recieve_action(connection)

            if response[0] == "D" or response[0] == "P":
                # AI moves
                # makes sure server returns something that is valid
                try:
                    GameState = _ai_turn(GameState)
                except:
                    server.close(connection)
                    exit()

            # ends program if winner
            elif response == "WINNER_RED" or response == "WINNER_YELLOW":
                print(response)
                break

        # ends program if winner
        if response == "WINNER_RED" or response == "WINNER_YELLOW":
            break

    server.close(connection)

# ron-cadillac.ics.uci.edu
# 4444