
from game import GameManager
from framework import GameObject, SpriteSheet, Clock, GameSprite, GameCollectible, Music
from spriteManager import SpriteManager
from utils import Singleton
from random import randint

@Singleton
class EffectSpawner:
    def __init__(self):
        self.__game = GameManager()

    def spawnExplosion(self, barrel):
        rand = randint(5, 10)
        self.__game.addEnemy(Explosion(barrel, rand))
        Music.playEffect("17_SFX_Stomp")

    def spawnGoo(self, platform):
        rand = randint(500, 1000)

        if platform.nextPlatform is not None:
            self.__game.addCollectible(Goo(platform.nextPlatform, rand))

        self.__game.addCollectible(Goo(platform, rand))

        if platform.previousPlatform is not None:
            self.__game.addCollectible(Goo(platform.previousPlatform, rand))
        Music.playEffect("02_Coin")


class Explosion(GameObject):
    def __init__(self, barrel, rand):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('explosion')
        self.tick = 0
        self.x = barrel.x
        self._barrel = barrel
        self.y = barrel.y
        self._sprites = {
            'explosion_0': self._sheet.sprite(0, 57, 28, 24),
            'explosion_1': self._sheet.sprite(48, 57, 28, 24),
            'explosion_2': self._sheet.sprite(96, 57, 28, 24),
            'explosion_3': self._sheet.sprite(142, 55, 32, 28),
            'explosion_4': self._sheet.sprite(189, 52, 46, 38),
            'explosion_5': self._sheet.sprite(176, 93, 69, 48)
        }
        """'explosion_0': self._sheet.sprite(0,0,3,3),
        'explosion_1': self._sheet.sprite(4,0,10,10),
        'explosion_2': self._sheet.sprite(15,0,15,15),
        'explosion_3': self._sheet.sprite(31,0,20,20),
        'explosion_4': self._sheet.sprite(52,0,25,25),
        'explosion_5': self._sheet.sprite(78,0,35,35),
        'explosion_6': self._sheet.sprite(114,0,45,45),
        'explosion_7': self._sheet.sprite(160,0,75,50),
        'explosion_8': self._sheet.sprite(0,0,0,0)"""

        self.len = (len(self._sprites))

        self.spriteManager = SpriteManager(self._sprites)
        sprites = []
        for i in range(0,self.len):
            sprites.append('explosion_'+str(i))
        self.spriteManager.useSprites(sprites, rand)

    def update(self):
        self.centerX = self._barrel.centerX
        self.bottom = self._barrel.bottom
        self.y -= 3
        if self.getSprite() == self._sprites['explosion_'+ str(self.len - 1)]:
            self.kill()

    def getSprite(self):
        return self.spriteManager.animate()


class Goo(GameCollectible):
    @GameCollectible.IsClearable()
    def __init__(self, platform, rand):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('goo')
        self.tick = 0
        self.x = platform.x
        self.y = platform.y
        self.rand = rand

        self._sprites = {
            'Goo_1': self._sheet.sprite(0, 1, 32, 16),
            'Goo_2': self._sheet.sprite(33, 1, 32, 16),
            'Goo_3': self._sheet.sprite(66, 1, 32, 16),
            'Goo_4': self._sheet.sprite(99, 1, 32, 16)
        }

        self.spriteManager = SpriteManager(self._sprites)
        self.spriteManager.useSprites(['Goo_1', 'Goo_2', 'Goo_3', 'Goo_4', 'Goo_3', 'Goo_2'], 8)

    def update(self):
        self.tick += 1
        if self.tick >= self.rand:
            self.kill()

    def getSprite(self):
        return self.spriteManager.animate()

    def onCollect(self, hit, collectionType):
        pass