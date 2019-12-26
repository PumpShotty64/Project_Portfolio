# Jordan Nguyen
# 25409215

import pygame
import random
import project5_game_mechanics as GM

class ColumnGame:
    # variables needed to keep track
    def __init__(self):
        self._isRunning = True
        self._gameState = GM.GameState().initialize_field()
        self._currentFaller = None
        self._isMatching = False
        self._hasFroze = True
        self._gameOver = False
        self._gameSpeed = 600 # game speed
        self._speed = self._gameSpeed
        self._gameTimer = 0
        self._gameScore = 0

    # main run function
    def run(self) -> None:

        # initializes pygame for use
        pygame.init()
        try:
            self._resize_surface((300, 700))
            # game timer
            clock = pygame.time.Clock()
            # sounds
            self._froze_sound = pygame.mixer.Sound('faller_froze.wav') # froze
            self._match_sound = pygame.mixer.Sound('faller_match.wav') # match
            self._faller_sound = pygame.mixer.Sound('faller_falling.wav') # falling
            # keeps running until game ends
            while self._isRunning:
                # all functions needed to run game
                self._gameTimer += clock.tick(30)
                self._handle_events()
                self._create_faller()
                if not self._hasFroze:
                    self._faller_falling()
                if self._gameOver:
                    self._end_game()
                self._update_board()
        finally:
            # quits the game
            pygame.quit()

    # handles all game events
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            # key presses DOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._faller_move_left()
                elif event.key == pygame.K_RIGHT:
                    self._faller_move_right()
                elif event.key == pygame.K_SPACE:
                    self._faller_rotate()
                elif event.key == pygame.K_DOWN:
                    self._speed = 50
            # key up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self._speed = self._gameSpeed

    # draws the board and updates the board
    def _update_board(self) -> None:
        # intialize constants and variables
        surface = pygame.display.get_surface()
        # background color
        surface.fill(pygame.Color(25, 25, 25))
        # constants
        SURFACE_WIDTH, SURFACE_HEIGHT = surface.get_size()
        FALLER_WITDH_RATIO, FALLER_HEIGHT_RATIO = 0.166, 0.07
        jewel_color_dict = {'S': (0, 0, 255), 'T': (255, 0, 0),
                            'V': (0, 255, 0), 'W': (255, 255, 0),
                            'X': (0, 255, 255), 'Y': (255, 120, 0),
                            'Z': (255, 0, 255)}
        # variables
        rect_width = FALLER_WITDH_RATIO * SURFACE_WIDTH
        rect_height = FALLER_HEIGHT_RATIO * SURFACE_HEIGHT
        delta_y = 0

        for row in range(len(self._gameState)):
            delta_x = 0
            for col in range(len(self._gameState[row])):
                # draws black square grid
                if self._gameState[row][col] == '   ':
                    pygame.draw.rect(surface, (0, 0, 0), (delta_x, delta_y, rect_width, rect_height))
                    delta_x += rect_width + 1
                elif self._gameState[row][col] == '---':
                    pygame.draw.rect(surface, (100, 100, 100), (delta_x, delta_y, rect_width, rect_height))
                    delta_x += rect_width + 1
                # jewel with this border is normal color. Indicates falling and frozen
                elif self._gameState[row][col].startswith('[') or self._gameState[row][col].startswith(' '):
                    for theJewel, theColor in jewel_color_dict.items():
                        if self._gameState[row][col][1] == theJewel:
                            pygame.draw.rect(surface, theColor, (delta_x, delta_y, rect_width, rect_height))
                            delta_x += rect_width + 1
                # this border, faller color becomes darker to indicate landed
                elif self._gameState[row][col].startswith('|'):
                    for theJewel, theColor in jewel_color_dict.items():
                        if self._gameState[row][col][1] == theJewel:
                            # changes the color to a little darker
                            tintList = list(theColor)
                            for i in range(len(theColor)):
                                if tintList[i] >= 80:
                                    tintList[i] -= 80
                            theColor = tuple(tintList)
                            pygame.draw.rect(surface, theColor, (delta_x, delta_y, rect_width, rect_height))
                            delta_x += rect_width + 1
                # faller color becomes brighter to indicate matching
                elif self._gameState[row][col].startswith('*'):
                    for theJewel, theColor in jewel_color_dict.items():
                        if self._gameState[row][col][1] == theJewel:
                            tintList = list(theColor)
                            # changes the color to brighter color
                            for i in range(len(theColor)):
                                if tintList[i] <= 185:
                                    tintList[i] += 70
                            theColor = tuple(tintList)
                            pygame.draw.rect(surface, theColor, (delta_x, delta_y, rect_width, rect_height))
                            delta_x += rect_width + 1
            delta_y += rect_height + 1

        pygame.display.flip() # updates window

    # creating the faller
    def _create_faller(self) -> None:

        jewel_key_tuple = ('S','T','V','W','X','Y','Z')

        if self._hasFroze:
            tempFaller = []
            for i in range(3):
                rand_val = random.randint(0, 6)
                tempFaller.append(jewel_key_tuple[rand_val])
            self._currentFaller = GM.Faller(tempFaller[0], tempFaller[1], tempFaller[2])
            self._hasFroze = False

    # continous fall of faller
    def _faller_falling(self) -> None:
        # while falling -----------------
        if self._gameTimer > self._speed:
            self._isMatching, self._hasFroze, self._gameOver = GM.faller_falling(self._currentFaller, self._gameState)
            if self._hasFroze:
                self._froze_sound.play()
            else:
                self._faller_sound.play()
            # if matching ------------------
            clock = pygame.time.Clock()
            tempTimer = 0
            while self._isMatching:
                tempTimer += clock.tick(30)
                if tempTimer > self._speed:
                    self._clear_matches()
                    self._gameScore += 300 # increase score when match
                    self._match_sound.play()
                    # speeds up if score is greater than a certain score
                    # this increases difficulty
                    if self._gameScore % 1000 == 0:
                        self._gameSpeed -= 25
                    tempTimer = 0
                    print('YOUR SCORE: ', self._gameScore)
                self._update_board()
            self._gameTimer = 0
    # ACTIONS
    # move left
    def _faller_move_left(self) -> None:
        GM.faller_move_left(self._currentFaller, self._gameState)
    # move right
    def _faller_move_right(self) -> None:
        GM.faller_move_right(self._currentFaller, self._gameState)
    # rotate
    def _faller_rotate(self) -> None:
        GM.faller_rotate(self._currentFaller, self._gameState)
    # clear matches
    def _clear_matches(self) -> None:
        self._isMatching, self._hasFroze, self._gameOver = GM.clear_matches(self._currentFaller, self._gameState)
    # game end bool set to false
    def _end_game(self) -> None:
        self._isRunning = False
    # resizes the window
    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)


if __name__ == '__main__':
    ColumnGame().run()
