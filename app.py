"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Trisha Guttal, tkg32
18th November 2018
"""
from consts import *
from game2d import *
from wave import *
import introcs

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.
    """

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        """
        self._pressed = False
        self._state = STATE_INACTIVE
        self._backgroundmusic = Sound('bgmusic.mp3')
        self._backgroundmusic.volume = 1
        self._backgroundmusic.play()
        self._background = GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,height=GAME_HEIGHT,source='stars.jpg')
        if self._state == STATE_INACTIVE:
            self._text = GLabel(text='PRESS \'P\' TO PLAY', linecolor = introcs.RGB(255, 255, 255), \
            font_size= 70, font_name='Arcade.ttf', x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
            self._subtext = GLabel(text='PRESS \'M\' TO MUTE SOUND', linecolor = introcs.RGB(255, 255, 255), \
            font_size= 50, font_name='Arcade.ttf', x=GAME_WIDTH/2, y=GAME_HEIGHT/4)
            self._wave = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self.inputkeys()
        if self._state == STATE_NEWWAVE:
            self.newwavestate()
        if self._state == STATE_ACTIVE:
            self.activestate(dt)
        if self._state == STATE_PAUSED:
            self.pausedstate()
        if self._state == STATE_CONTINUE:
            self.continuestate()
        if self._wave is not None:
            if self._wave.noaliens() and self._wave.getLives() > 0:
                self._text = GLabel(text='YOU WON!', linecolor = introcs.RGB(255, 255, 255),\
                font_size= 75, font_name='Arcade.ttf', x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
                self._subtext = None
                self._state = STATE_COMPLETE

    def newwavestate(self):
        """
        This method determines the actions taken when the game is in the state newwave.

        In general, the new wave state has no text or subtext, and creates a
        new wave to begin the game.
        """
        self._text = None
        self._subtext = None
        self._wave = Wave()
        self._state = STATE_ACTIVE

    def activestate(self, dt):
        """
        This method determines the actions taken when the game is in the active state.

        In general, the active state has no text or subtext initially.
        The ship is able to move in this state, and the wave update class is also
        called here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._text = None
        self._subtext = None
        self.moveship()
        if self._wave is not None:
            self._wave.update(dt,self.input)
        if self._wave.lives() == True:
            if self._wave.getLives() > 0:
                self._templife = self._wave.getLives()
                self._wave.setLives(self._templife)
                self._state = STATE_ACTIVE
            if self._wave.getShip() is None and self._wave.getLives() > 0:
                self._state = STATE_PAUSED
        if self._wave.lives() == False or self._wave.aliensbelow():
            self._text = GLabel(text='YOU LOST', linecolor = introcs.RGB(255, 255, 255), \
            font_size= 75, font_name='Arcade.ttf', x=GAME_WIDTH/2, y=200)
            self._subtext = None
            self._state = STATE_COMPLETE

    def pausedstate(self):
        """
        This method determines the actions taken when the game is in the paused state.

        The game changes to this state when the ship's lives has decreased but is not 0.
        Text is displayed, allowing the user to press p to continue playing with
        the ship's remaining lives that are reset with the _templife attribute.
        The function inputkeys() is called to allow the user to press the 'p' key.
        If this key is pressed, the state is changed to continue.
        """
        self._text = GLabel(text='PRESS \'P\' TO CONTINUE', linecolor = introcs.RGB(227, 224, 224), \
        font_size= 55, font_name='Arcade.ttf', x=GAME_WIDTH/2, y=200)
        self._subtext = None
        if self.inputkeys():
            self._state = STATE_CONTINUE

    def continuestate(self):
        """
        This method determines the actions taken when the game is in the continue state.

        The game changes to this state when the user is waiting for a new ship if
        they have lives > 0. Once a new ship is created, the state is changed to active and
        the text attributes are set to None (no text is visible on the screen).
        """
        self._wave.newShip()
        self._state = STATE_ACTIVE
        self._text = None
        self._subtext = None

    def moveship(self):
        """
        This method moves the ships according to the user's key presses.

        To move right, the function is_key_down() checks if the right key is
        being pressed. If it is, the shipright method is called, allowing the
        ship to move right.

        To move left, the function is_key_down() checks if the left key is
        being pressed. If it is, the shipleft method is called, allowing the
        ship to move left.
        """
        if self._input.is_key_down('right'):
            if self._wave.getShip() is not None:
                self._wave.getShip().shipright()
        if self._input.is_key_down('left'):
            if self._wave.getShip() is not None:
                self._wave.getShip().shipleft()

    def draw(self):
        """
        Draws the game objects (background image, text, alien wave and subtext) to the view.
        """
        self._background.draw(self.view)
        if not self._text is None:
            self._text.draw(self.view)
        if not self._wave is None:
            self._wave.draw(self.view)
        if not self._subtext is None:
            self._subtext.draw(self.view)

    def inputkeys(self):
        """
        Checks if the key being pressed has also been pressed beforehand.

        When state is inactive, the state is changed to newwave, no text is displayed, and as a key has been
        pressed previously, _pressed is set to True.

        When state is paused, the state is changed to active, no text is displayed, and as a key has been
        pressed previously, _pressed is set to True.

        When state is inactive in the beginning of the game, the background music's volume can be changed
        to 0 if the key 'm' is pressed on the welcome screen.
        """
        if self._pressed == False and self._input.is_key_down('p') and self._state == STATE_INACTIVE:
                self._state = STATE_NEWWAVE
                self._text = None
                self._pressed = True
                self._subtext = None
                return True
        elif self._pressed == False and self._input.is_key_down('p') and self._state == STATE_PAUSED:
            self._state = STATE_ACTIVE
            self._pressed = True
            self._text = None
            self._subtext = None
            return True
        elif self._pressed == False and self._input.is_key_down('m') and self._state == STATE_INACTIVE:
            self._backgroundmusic.volume = 0
        else:
            self._pressed = False
