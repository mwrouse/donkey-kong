"""
Class to control mario
"""
from spriteManager import SpriteManager
from framework import GameObject, Clock, SpriteSheet, Keys, Sound
from inputManager import InputManager
from enum import Enum
from collisionDetector import CollisionTypes, CollisionDirection

class PlayerState(Enum):
    IDLE = 0
    LADDER_DOWN = 1
    MOVELEFT = 2
    MOVERIGHT = 3
    JUMP = 4
    DEAD = 5
    ERROR = 6
    LADDER_IDLE = 7
    LADDER_UP = 8


movement = 100.0


class Mario(GameObject):
    def __init__(self):
        super().__init__()

        self._sheet = SpriteSheet('mario')

        self._sprites = {
            'stand_left': self._sheet.sprite(0, 20, 24, 32),
            'stand_right': self._sheet.sprite(0, 20, 24, 32).flip(),
            'run_left1': self._sheet.sprite(45, 20, 31, 32),
            'run_left2': self._sheet.sprite(94, 21, 30, 32),
            'run_right1': self._sheet.sprite(45, 20, 31, 32).flip(),
            'run_right2': self._sheet.sprite(94, 21, 30, 32).flip(),
            'ladder_up1': self._sheet.sprite(142, 20, 28, 32),
            'ladder_up2': self._sheet.sprite(142, 20, 28, 32).flip()
        }

        self.spriteManager = SpriteManager(self._sprites)
        #self.spriteManager.addSprites(self._sprites)

        self.spriteManager.useSprites([
            'stand_right'
        ], 10)

        self.x = 300
        self.y = 300
        self.state = PlayerState.IDLE
        self._isAtLadder = False

        InputManager.subscribe(
            [Keys.LEFT, Keys.RIGHT, Keys.DOWN, Keys.UP, Keys.SPACE],
            self._marioKeyPress
        )

        self._walkingSound = Sound('walking')

    def update(self):
        """ Method used for updating state of a sprite/object """
        if self._isAtLadder != True:
            self.y = self.y + (movement * 2) * Clock.timeDelta # Gravity

        self._isAtLadder = False

        if self.state == PlayerState.MOVELEFT:
            self.x -= movement * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_left1',
                'stand_left',
                'run_left2'
            ], 8)
            self._walkingSound.play()
        elif self.state == PlayerState.MOVERIGHT:
            self.x += movement * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_right1',
                'stand_right',
                'run_right2'
            ], 8)
            self._walkingSound.play()
        elif self.state == PlayerState.LADDER_DOWN:
            self.y += movement * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
            self.spriteManager.useSprites([
                'ladder_up1',
                'ladder_up2'
            ], 10)
        elif self.state == PlayerState.LADDER_UP:
            self.y -= movement * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
            self.spriteManager.useSprites([
                'ladder_up1',
                'ladder_up2'
            ], 10)
        elif self.state == PlayerState.LADDER_IDLE:
            self.spriteManager.useSprites([
                'ladder_up1'
            ], 10)

        else:
            self.state = PlayerState.IDLE
            if 'stand_left' in self.spriteManager.currentAnimation:
                self.spriteManager.useSprites(['stand_left'], 10)
            else:
                self.spriteManager.useSprites(['stand_right'], 10)

            self._walkingSound.stop()

        self.spriteManager.animate()


    def collision(self, collisionType, direction, obj):
        """ Mario collided with something """
        if collisionType == CollisionTypes.Enemy:
            print("You killed Mario!!!!!")
            self.die()

        elif collisionType == CollisionTypes.Ladder:
            self._isAtLadder = True

        elif collisionType == CollisionTypes.Platform:
            if self._isAtLadder == False:
                self.bottom = obj.top + 1

        elif collisionType == CollisionTypes.Immovable:
            self.state = PlayerState.IDLE
            if not obj.isTopOfLadder:
                self.bottom = obj.top


    def _marioKeyPress(self, key):
        def __str__(self):
            return "MarioKeyPress"

        if (key == Keys.LEFT or key == Keys.A) and self.state not in (PlayerState.LADDER_IDLE, PlayerState.LADDER_DOWN, PlayerState.LADDER_UP):
            self.state = PlayerState.MOVELEFT
        elif (key == Keys.RIGHT or key == Keys.D) and self.state != PlayerState.LADDER_IDLE:
            self.state = PlayerState.MOVERIGHT
        elif key == Keys.DOWN or key == Keys.S:
            if self._isAtLadder:
                self.state = PlayerState.LADDER_DOWN
        elif key == Keys.UP:
            if self._isAtLadder:
                self.state = PlayerState.LADDER_UP
        elif key is Keys.SPACE:
            print("Mario Jumped")
        else:
            print(key)

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
