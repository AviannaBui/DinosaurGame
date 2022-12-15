# ========================================================================
# Authors: Avianna Bui and Trung Dam
# COMP 123 Final Project: Dino Game
# ========================================================================

import math
import sys
import random

import pygame as pg
from pygame import mixer

# ========================================================================
# initialization
pg.init()
mixer.init()

# ========================================================================
# screen creation
pg.display.set_caption('Dinosaur Game')
screenWidth = 1200
screenHeight = 500

screen = pg.display.set_mode((screenWidth, screenHeight))

# ========================================================================
# import background and elements
BackGround = pg.image.load('DinoPic/Track.png')
PinkDino = pg.image.load('DinoPic/PinkDino.png')
PinkDinoDuck = pg.image.load('DinoPic/PinkDinoDuck.png')
smCactus1 = pg.image.load('DinoPic/SmallCactus1.png')
smCactus2 = pg.image.load('DinoPic/SmallCactus2.png')
BlueBird = pg.image.load('DinoPic/BlueBird.png')

cactusLst = [smCactus1, smCactus2]

# ========================================================================
class BG:
    """Represent an infinite scrolling background"""
    def __init__(self, x):
        """This function takes in the initial x-coordinate of the track. It then creates
        and sets up a running track in the background"""
        self.width = screenWidth
        self.height = screenHeight
        self.x = x
        self.scaleDown()
        self.show()

    def update(self, newX):
        """This function takes new distance between initial coordinate and wanted coordinate
        to make the screen move by that input distance"""
        self.x -= newX
        if self.x <= -screenWidth:
            self.x = screenWidth

    def show(self):
        screen.blit(BackGround, (self.x, 400))

    def scaleDown(self):
        """Scale down the size of the track image to fit in the screen"""
        self.bg = pg.transform.scale(BackGround, (self.width, self.height))


class Dino:
    """Represent a dinosaur. Set up the dinosaur's actions and positions"""
    def __init__(self):
        self.x = 40
        self.y = 330
        self.y_duck = 380
        self.yPos = self.y
        self.textureNum = 0

        self.standing = True
        self.jumping = False
        self.falling = False
        self.ducking = False

        self.dino = PinkDino
        self.dinoDuck = PinkDinoDuck

        self.image = self.dino
        self.show()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        """Set up conditions for the dinosaur's jumping and falling"""
        if self.jumping:
            self.yPos -= 2.0  # set jump step
            if self.yPos <= 70:
                self.fall()
        elif self.falling:
            self.yPos += 2.4  # set gravity
            if self.yPos >= 330:
                self.touchGround()

    def jump(self):
        self.image = self.dino
        self.jumping = True
        self.falling = False
        self.standing = False
        self.ducking = False

    def fall(self):
        self.image = self.dino
        self.falling = True
        self.standing = False
        self.jumping = False
        self.ducking = False

    def touchGround(self):
        self.image = self.dino
        self.falling = False
        self.standing = True
        self.ducking = False
        self.yPos = self.y

    def duck(self):
        self.ducking = True
        self.falling = False
        self.standing = False
        self.jumping = False
        self.image = self.dinoDuck
        self.yPos = self.y_duck

    def show(self):
        screen.blit(self.image, (self.x, self.yPos))


class Cactus:
    """Represent randomly generated cacti"""
    def __init__(self, x):
        """This function takes initial x-coordinate of the cacti. It then sets up
        and displays the cacti randomly on the screen"""
        self.x = x
        self.y = 340
        self.randomCactus()
        self.show()

    def update(self, newX):
        self.x -= newX

    def randomCactus(self):
        self.randomNum = random.randint(0, len(cactusLst) - 1)

    def show(self):
        screen.blit(cactusLst[self.randomNum], (self.x, self.y))

class Bird:
    """Represent a bird"""
    def __init__(self, x):
        self.x = x
        self.y = 285
        self.show()

    def update(self, newX):
        self.x -= newX

    def show(self):
        screen.blit(BlueBird, (self.x, self.y))


class Obstacles:
    """Represent a list of obstacles that include cacti and birds"""
    def __init__(self):
        self.obstacleList = []

    def showObstacles(self):
        if len(self.obstacleList) == 0:
            xPos = random.randint(screenWidth + 100, 2000)
        else:
            beforeObstacle = self.obstacleList[-1]
            xPos = random.randint(beforeObstacle.x + 900, screenWidth + beforeObstacle.x + 900)

        if random.randint(0,2) == 0 or random.randint(0,2) == 1:
            cactus = Cactus(xPos)
            self.obstacleList.append(cactus)
        else:
            bird = Bird(xPos)
            self.obstacleList.append(bird)

    def clearObstacle(self):
        self.obstacleList = []


class Score:
    """Generate and update the player's score"""
    def __init__(self):
        self.actualScore = 0
        self.font = pg.font.SysFont('Monaco', 30)
        self.color = (0, 0, 0)
        self.show()

    def update(self, loops):
        self.actualScore = loops // 10

    def show(self):
        self.label = self.font.render(f'SCORE {self.actualScore}', 1, self.color)
        labelWidth = self.label.get_rect().width
        screen.blit(self.label, (screenWidth - labelWidth - 10, 10))


class Crash:
    """Calculate the distance between two objects to determine whether a crash happens"""
    def distance(self, object1, object2):
        dist = math.sqrt((object1.x - object2.x) ** 2 + (object1.yPos - object2.y) ** 2)
        return dist < 60


class Settings:
    """Set up the game's UX/UI components"""
    def __init__(self):
        self.movingBG = [BG(0), BG(screenWidth)]
        self.score = Score()
        self.crash = Crash()
        self.set_labels()
        self.playing = False

    def set_labels(self):
        font1 = pg.font.SysFont('M+', 24, "bold")
        font2 = pg.font.SysFont('M+', 20)
        self.overLabel = font1.render(f'GAME OVER', 1, "#006400")
        self.restartLabel = font2.render(f'Press Space to restart', 1, "#4F7942")

    def over(self):
        """Set up the screen's display, sound, condition when the game is over"""
        mixer.music.stop()
        screen.blit(self.overLabel, (600 - self.overLabel.get_width() // 2, 250))
        screen.blit(self.restartLabel, (600 - self.restartLabel.get_width() // 2, 250
                                        + self.overLabel.get_height()))
        self.playing = False

    def start(self):
        self.playing = True
        self.soundPlay()

    def soundPlay(self):
        mixer.music.load('DinoPic/BabyShark.wav')
        mixer.music.play(-1)

    def restart(self):
        self.__init__()


# ========================================================================
def main():
    running = True
    speed = 1
    default = Settings()
    obstacles = Obstacles()
    loops = 0
    over = False
    dino = Dino()
    clock = pg.time.Clock()

    while running:
        if default.playing:
            screen.fill((255, 240, 245))
            loops += 1

            for bg in default.movingBG:
                bg.update(speed)
                bg.show()

            dino.update()
            dino.show()

            if loops % 500 == 0:
                obstacles.showObstacles()

            obsLst2 = []

            for obs in obstacles.obstacleList:
                obs.update(speed)
                obs.show()
                if obs.x < 0:
                    obsLst2.append(obs)
                if default.crash.distance(dino, obs):
                    over = True

            for el in obsLst2:
                obstacles.obstacleList.remove(el)

            if over:
                default.over()
                obstacles.clearObstacle()

            default.score.update(loops)
            default.score.show()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    if not over and dino.standing and not dino.ducking:
                        dino.jump()
                    if not default.playing:
                        default.start()
                if event.key == pg.K_DOWN:
                    if not over and dino.standing:
                        dino.duck()
                else:
                    if dino.ducking:
                        dino.touchGround()
                if over:
                    if event.key == pg.K_SPACE:
                        screen.fill((0, 0, 0))
                        mixer.music.stop()
                        default.restart()
                        dino = Dino()
                        loops = 0
                        over = False
        clock.tick(400)
        pg.display.update()


# ========================================================================
# running the game
main()


