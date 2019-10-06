"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.

Trisha Guttal, tkg32
18th November 2018
"""
from game2d import *
from consts import *
from models import *
import random
import introcs

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    INSTANCE ATTRIBUTES:
        _ship:              the player ship to control [Ship]
        _aliens:            the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:             the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:             the defensive line being protected [GPath]
        _lives:             the number of lives left  [int >= 0]
        _time:              the amount of time since the last Alien "step" [number >= 0]

        _horizontalmove:    determines whether the alien is able to move left or right [True or False]
        _boltrate:          a random number of steps at which the alien begins to fire [number >= 0]
        _laser:             a music file that plays when the spacebar is pressed, firing a bolt from the ship [string]
        _alienrun:          determines the alien speed, which is increased as aliens are killed [int > 0]
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the ship of the Ship class.

        This getter method is to protect access to the ship.
        """
        return self._ship

    def getLives(self):
        """
        Returns the lives attribute value of the Ship class.

        This getter method is to protect access to the ship's lives.
        """
        return self._lives

    def setLives(self, num):
        assert type(num) == int
        self._lives = num

    def getRightAlien(self):
        """
        Returns the x attribute of the rightmost alien in the alien wave.

        This getter method is to protect access to the alien wave.
        It returns the alien closest to the right edge of the screen.
        """
        max = 0
        acc = self._aliens[0][0]
        for nums in range(len(self._aliens[0])):
            for aliens in range(len(self._aliens)):
                if not self._aliens[aliens][nums] is None:
                    if max < self._aliens[aliens][nums].x:
                        if not self._aliens[aliens][nums].x is None:
                            max = self._aliens[aliens][nums].x
                        if not self._aliens[aliens][nums] is None:
                            acc = self._aliens[aliens][nums]
        return acc.x

    def getLeftAlien(self):
        """
        Returns the x attribute of the leftmost alien in the alien wave.

        This getter method is to protect access to the alien wave.
        It returns the alien closest to the left edge of the screen.
        """
        min = GAME_WIDTH
        acc = self._aliens[ALIEN_ROWS-1][ALIENS_IN_ROW-1]
        for aliens in range(len(self._aliens)):
            for nums in range(len(self._aliens[0])):
                if not self._aliens[aliens][nums] is None:
                    if min > self._aliens[aliens][nums].x:
                        if not self._aliens[aliens][nums].x is None:
                            min = self._aliens[aliens][nums].x
                        if not self._aliens[aliens][nums] is None:
                            acc = self._aliens[aliens][nums]
        return acc.x

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a new wave.

        The wave is a set of rows and columns of aliens that move around the
        screen for the ship to fire at. A ship and a defense line is created in this method,
        while also initializing instance attributes.
        In the end of the initializer, the alienrows() method is called to create this
        table of aliens.
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], \
        linecolor=introcs.RGB(51, 204, 255), linewidth=1.5)
        self._ship = Ship()
        self._time = 0
        self._bolts = []
        self._aliens = []
        self._alienrun = ALIEN_SPEED
        self._lives = 3
        self._horizontalmove = False
        self._laser = Sound('laser.wav')
        self._boltrate = 0
        self.alienrows()

    def canmoveRight(self):
        """
        Returns True if the rightmost alien can still move right.

        This method calls the getRightAlien() method and checks that it has not
        covered the entire distance from its position plus half of its width to
        the game's width minus half of the alien's walk.
        """
        if self.getRightAlien() is not None:
            if (self.getRightAlien() + ALIEN_WIDTH/2 < GAME_WIDTH - ALIEN_H_WALK):
                return True
            else:
                return False

    def canmoveLeft(self):
        """
        Returns True if the leftmost alien can still move left.

        This method calls the getLeftAlien() method and checks that it has not
        covered the entire distance from its position minus half of its width to
        the the alien's walk.
        """
        if (self.getLeftAlien() - ALIEN_WIDTH/2 > ALIEN_H_WALK):
            return True
        else:
            return False

    def alienrows(self):
        """
        Creates a wave of aliens.

        This method lines up the aliens neatly into columns by looping through
        all the aliens in the two dmensional list and printing different alien
        shapes for different row numbers.
        """
        x = ALIEN_H_SEP + ALIEN_WIDTH/2
        y = GAME_HEIGHT - ALIEN_CEILING
        source = 'alien-strip1.png'
        for row in range(ALIEN_ROWS):
            new = []
            if (ALIEN_ROWS-1-row) % 6 == 0 or (ALIEN_ROWS-1-row) % 6 == 1:
                source = 'alien-strip1.png'
            elif (ALIEN_ROWS-1-row) % 6 == 2 or (ALIEN_ROWS-1-row) % 6 == 3:
                source = 'alien-strip2.png'
            elif (ALIEN_ROWS-1-row) % 6 == 4 or (ALIEN_ROWS-1-row) % 6 == 5:
                source = 'alien-strip3.png'
            y = y - ALIEN_HEIGHT - ALIEN_V_SEP
            x = ALIEN_H_SEP + ALIEN_WIDTH/2
            for col in range(ALIENS_IN_ROW):
                alienobject = Alien(x, y, source)
                x = x + ALIEN_WIDTH + ALIEN_H_SEP
                new.append(alienobject)
            self._aliens.append(new)

    def aliensright(self, time):
        """
        This method moves the wave of aliens to the right.

        Parameter time: counts the number of seconds that have passed since the
        last animation frame.
        It is added to the _time attribute in each animation frame.
        """
        if self._time > self._alienrun:
            for num in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    if not self._aliens[num][alien] is None:
                        self._aliens[num][alien].x = self._aliens[num][alien].x + ALIEN_H_WALK
                        self._aliens[num][alien].frame = (self._aliens[num][alien].frame+1) % 2
            self._time = 0
        self._time = time + self._time

    def aliensdown(self, time):
        """
        This method moves the wave of aliens down.

        Parameter time: counts the number of seconds that have passed since the last animation frame.
        It is added to the _time attribute in each animation frame.
        """
        for num in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                if not self._aliens[num][alien] is None:
                    self._aliens[num][alien].y = self._aliens[num][alien].y - ALIEN_V_SEP
                    self._aliens[num][alien].frame = (self._aliens[num][alien].frame+1) % 2
        self._horizontalmove = not self._horizontalmove

    def aliensleft(self, time):
        """
        This method moves the wave of aliens to the left.

        Parameter time: counts the number of seconds that have passed since the last animation frame.
        It is added to the _time attribute in each animation frame.
        """
        if self._time > self._alienrun:
            for num in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    if not self._aliens[num][alien] is None:
                        self._aliens[num][alien].x = self._aliens[num][alien].x - ALIEN_H_WALK
                        self._aliens[num][alien].frame = (self._aliens[num][alien].frame+1) % 2
            self._time = 0
        self._time = time + self._time

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, time, input):
        """
        This method calls methods aliensright(), aliensleft() and aliensdown() according
        to certain conditions, allowing the aliens to move in the correct areas of the screen
        and not leave the screen.
        """
        if self._horizontalmove == False and self.canmoveRight():
            self.aliensright(time)
        if self._horizontalmove == False and self.canmoveRight() == False:
            self.aliensdown(time)
            self._horizontalmove = True
        if self._horizontalmove == True and self.canmoveLeft() == True:
            self.aliensleft(time)
        if  self._horizontalmove == True and self.canmoveLeft() == False:
            self.aliensdown(time)
            self._horizontalmove = False
        state = True
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                state = False
        if input.is_key_down('spacebar') and state == True:
            self._laser = Sound('laser.wav')
            self._laser.play()
            self._bolts.append(Bolt(self._ship.x, self._ship.y + SHIP_HEIGHT/2))
        if (not self._bolts == []):
            self.boltpass()
        self.alienbolt()
        self.collisionaction()

    def movebolt(self):
        """
        This method moves the bolt up or down.

        It determines the direction of the bolt's movement by calling isPlayerBolt()
        to check if the bolt is from the ship or from the aliens.
        """
        for bolt in self._bolts:
            if not bolt.isout():
                if bolt.isPlayerBolt():
                    bolt.y += bolt._velocity
                else:
                    bolt.y += bolt._velocity

    def boltpass(self):
        """
        This method deletes the bolts when they move offscreen.

        It first calls the movebolt() method and then calls the isout() method.
        If isout() returns True, the bolt at that specific list index is deleted.
        """
        for bolt in self._bolts:
            self.movebolt()
            if bolt.isout():
                boltindex = self._bolts.index(bolt)
                del self._bolts[boltindex]

    def alienbolt(self):
        """
        This method allows random aliens to shoot bolts.

        The method first selects a nonempty column of aliens at random.
        Then, it finds the alien at the bottom of the column and creates a Bolt object.
        """
        num = random.randint(0, ALIEN_ROWS-1)
        randalien = random.choice(self._aliens[num])
        if not randalien is None:
            if self._time/self._alienrun >= self._boltrate:
                self._bolts.append(Bolt(randalien.x, randalien.y - ALIEN_HEIGHT/2))
        self._boltrate = random.randint(1, BOLT_RATE)

    def collisionaction(self):
        """
        This method handles the effects of collisions on aliens and the ship.

        It checks if the bolt collides with either the alien or the ship based
        on its placement, and sets the alien at that index or the ship to None.
        It also deletes the bolt that collides.
        """
        for bolt in self._bolts:
            if self._ship is not None:
                if self._ship.collides(bolt) == True:
                    self._ship = None
                    self._lives -= 1
                    boltindex = self._bolts.index(bolt)
                    del self._bolts[boltindex]
            for alien in range(len(self._aliens)):
                for num in range(len(self._aliens[0])):
                    if not self._aliens[alien][num] is None:
                        if self._aliens[alien][num].collides(bolt) == True:
                            self._aliens[alien][num] = None
                            self._alienrun = 0.97 * self._alienrun
                            boltindex = self._bolts.index(bolt)
                            del self._bolts[boltindex]

    def noaliens(self):
        """
        Returns True if the list of aliens is None.
        """
        for alien in range(ALIEN_ROWS):
            for num in range(ALIENS_IN_ROW):
                if self._aliens[alien][num] is not None:
                    return False
        else:
            return True

    def aliensbelow(self):
        """
        Returns True if the alien dips below the defense line.
        """
        for alien in range(len(self._aliens)):
            for num in range(len(self._aliens[0])):
                if self._aliens[alien][num] is not None:
                    if self._aliens[alien][num].y <= DEFENSE_LINE:
                        return True

    def lives(self):
        """
        Returns False if:
            i) the player still has lives left after losing a ship, or
            ii) there are no aliens left, or
            iii) any aliens dip below the defense line
        """
        if self._lives == 0 or self.noaliens() or self.aliensbelow():
            return False
        else:
            return True

    def newShip(self):
        self._ship = Ship()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw (self, view):
        """
        Draws the game objects (aliens, ship, defense line and bolts) to the view.

        Every single thing you want to draw in this game is a GObject.
        Therefore, the method g.draw(self.view) is used.
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if not self._aliens[row][col] is None:
                    self._aliens[row][col].draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolts in self._bolts:
            bolts.draw(view)
