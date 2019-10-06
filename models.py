"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game.

Trisha Guttal, tkg32
18th November 2018
"""
from consts import *
from game2d import *
import introcs

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.

class Ship(GImage):
    """
    A class to represent the game ship.
    """

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializes the Ship class.

        The ship is an image that shoots bolts. It is controlled by the player.
        """
        super().__init__(x=GAME_WIDTH/2, y=SHIP_BOTTOM, width=SHIP_WIDTH, height=SHIP_HEIGHT, source='ship.png')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def shipright(self):
        """
        This method moves the ship right by SHIP_MOVEMENT steps.

        It checks if the ship is not at the right boundary, and stops it from
        going beyond this boundary and off the screen.
        """
        if self.x+SHIP_WIDTH/2 < GAME_WIDTH:
            self.x = self.x + SHIP_MOVEMENT
        else:
            self.x = GAME_WIDTH - SHIP_WIDTH/2

    def shipleft(self):
        """
        This method moves the ship leftt by SHIP_MOVEMENT steps.

        It checks if the ship is not at the left boundary, and stops it from
        going beyond this boundary and off the screen.
        """
        if self.x-SHIP_WIDTH/2 > 0:
            self.x = self.x - SHIP_MOVEMENT
        else:
            self.x = SHIP_WIDTH/2

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with this ship

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt() == False:
            if self.contains((bolt.x - BOLT_WIDTH/2,bolt.y + BOLT_HEIGHT/2)) \
            or self.contains((bolt.x - BOLT_WIDTH/2,bolt.y - BOLT_HEIGHT/2)) \
            or self.contains((bolt.x + BOLT_WIDTH/2,bolt.y + BOLT_HEIGHT/2)) \
            or self.contains((bolt.x + BOLT_WIDTH/2,bolt.y - BOLT_HEIGHT/2)):
                return True
        return False


class Alien(GSprite):
    """
    A class to represent a single alien.
    """

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        Initializes the Alien class.

        Parameter x: the x value of the alien on the screen.
        Precondition: x is an integer value

        Parameter y: the y value of the alien on the screen.
        Precondition: y is an integer value

        Paramter source: the image source.
        Precondition: source is a string value.
        """
        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=source, format=(3,2))

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt() == True:
            if self.contains((bolt.x - BOLT_WIDTH/2,bolt.y + BOLT_HEIGHT/2)) \
            or self.contains((bolt.x - BOLT_WIDTH/2,bolt.y - BOLT_HEIGHT/2)) \
            or self.contains((bolt.x + BOLT_WIDTH/2,bolt.y + BOLT_HEIGHT/2)) \
            or self.contains((bolt.x + BOLT_WIDTH/2,bolt.y - BOLT_HEIGHT/2)):
                return True
        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def __init__(self,x,y):
        """
        Initializes the Bolt class.

        Parameter x: the x value of the bolt on the screen.
        Precondition: x is an integer value

        Parameter y: the y value of the bolt on the screen.
        Precondition: y is an integer value
        """
        super().__init__(x=x, y=y , width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor= introcs.RGB(255, 255, 255))
        self._velocity = 0
        if self.y + BOLT_HEIGHT/2 < DEFENSE_LINE:
            self._velocity = BOLT_SPEED
        else:
            self._velocity = -BOLT_SPEED

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isout(self):
        """
        Returns True if the current bolt is beyond the game's screen.
        """
        if self.y + BOLT_HEIGHT/2 > GAME_HEIGHT or self.y + BOLT_HEIGHT/2 < 0:
            return True

    def isPlayerBolt(self):
        """
        Returns True if the current bolt has been released by the ship.

        Checks if the bolt has a positive speed value, therefore implying that
        the bolt has been released upwards by the ship.
        """
        if self._velocity == BOLT_SPEED:
            return True
        else:
            return False
