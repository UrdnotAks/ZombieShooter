import pygame
import random
import sys
import math
import os
from pygame.math import Vector2

screenWidth = 800
screenHeight = 600
screenRect = pygame.Rect(0, 0, screenWidth, screenHeight)
screen_sprite = pygame.sprite.Group()
fontColor = (153, 13, 13)
GameRunning = False
game = None
FPS = 30


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def terminate():
    pygame.quit()
    sys.exit()


def restartGame(obj):
    global game
    obj.__del__()
    game = Game()


def startScreen(surf, bg, font):
    global GameRunning
    titleTxt = 'MISSION: SURVIVE!'
    title = font.render(titleTxt, True, fontColor)
    titleRect = title.get_rect()
    titleRect.center = (400, 250)

    start = pygame.image.load(resource_path('start.png'))
    startRect = start.get_rect()
    startRect.center = (400, 382)

    GameRunning = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if startRect.collidepoint(mousePos):
                    return

        surf.blit(bg, (0, 0))
        surf.blit(title, titleRect)
        surf.blit(start, startRect)
        pygame.display.update()


def gameOverScreen(surf, bg, obj, font):
    helpfont = pygame.font.Font(resource_path("ExquisiteCorpse.ttf"), 15)

    titleTxt = 'YOU DIED!'
    title_orig = font.render(titleTxt, True, fontColor)
    titleRect = title_orig.get_rect()
    titleRect.center = (400, 250)

    restart_orig = pygame.image.load(resource_path('restart.png'))
    restartRect = restart_orig.get_rect()
    restartRect.center = (400, 382)

    helpTxt = 'Press ESC to Quit'

    helpSurf = helpfont.render(helpTxt, True, (182, 182, 182))
    helpRect = helpSurf.get_rect(bottomleft=screenRect.bottomleft)

    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    title = title_orig.copy()
    restart = restart_orig.copy()

    alpha = 0
    restart_alpha_surf = pygame.Surface(restart.get_size(), pygame.SRCALPHA)
    title_alpha_surf = pygame.Surface(title.get_size(), pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if restartRect.collidepoint(mousePos):
                    restartGame(obj)

        if alpha < 255:
            alpha = min(alpha + 1, 255)
            title = title_orig.copy()
            title_alpha_surf.fill((255, 255, 255, alpha))
            title.blit(title_alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            restart = restart_orig.copy()
            restart_alpha_surf.fill((255, 255, 255, alpha))
            restart.blit(restart_alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        surf.blit(bg, (0, 0))
        surf.blit(title, titleRect)
        surf.blit(restart, restartRect)
        if alpha >= 150:
            surf.blit(helpSurf, helpRect)
        pygame.display.update()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    playerOrig = pygame.image.load(resource_path('player.png'))

    def __init__(self):
        super().__init__()
        self.image = self.playerOrig.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.position = (screenWidth // 2, screenHeight // 2)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        pos = Vector2(self.position)
        direction = pygame.mouse.get_pos() - pos
        radius, angle = direction.as_polar()
        self.image = pygame.transform.rotate(self.playerOrig, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Bullets(pygame.sprite.Sprite):
    bulletImg = pygame.image.load(resource_path('bullet.png'))

    def __init__(self, mousePos, playerPos):
        super().__init__()
        self.image = self.bulletImg.convert_alpha()
        self.rect = self.image.get_rect()

        # Rotating the sprite
        pos = Vector2(playerPos)
        direction = mousePos - pos
        radius, angle = direction.as_polar()
        self.image = pygame.transform.rotate(self.bulletImg, -angle - 90)

        # finding bullet velocity
        bulletPos = [0, 0]
        bulletPos[0] = mousePos[0] - playerPos[0]
        bulletPos[1] = mousePos[1] - playerPos[1]
        bulletDistance = math.sqrt(abs(bulletPos[0] ^ 2) + abs(bulletPos[1] ^ 2))
        self.xVel = bulletPos[0] / bulletDistance
        self.yVel = bulletPos[1] / bulletDistance

        # setting bullet position
        self.rect = self.image.get_rect(center=playerPos)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        x, y = self.rect.center
        x += self.xVel
        y += self.yVel
        self.rect.center = (x, y)

        if not screenRect.contains(self.rect):
            self.kill()


class Zombie(pygame.sprite.Sprite):
    zombieWalkingOrig = [pygame.image.load(resource_path('zombie/skeleton-move_0.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_2.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_4.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_5.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_6.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_7.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_8.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_9.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_10.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_11.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_12.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_13.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_14.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_15.png')),
                         pygame.image.load(resource_path('zombie/skeleton-move_16.png'))]

    def __init__(self, xVel, yVel):
        super().__init__()
        self.zombieWalking = []
        self.image = self.zombieWalkingOrig[0]
        self.xVel, self.yVel = xVel, yVel
        self.zombieWalkCount = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, playerPosition, pt):
        pos = Vector2(pt)
        direction = playerPosition - pos
        radius, angle = direction.as_polar()
        for img in self.zombieWalkingOrig:
            imgRotated = pygame.transform.rotate(img, -angle)
            self.zombieWalking.append(imgRotated.convert_alpha())
        self.rect = imgRotated.get_rect(center=pt)

    def update(self):
        if self.zombieWalkCount + 1 >= 30:
            self.zombieWalkCount = 0

        self.zombieWalkCount += 1
        x, y = self.rect.center
        x += self.xVel
        y += self.yVel
        self.rect.center = (x, y)
        self.image = self.zombieWalking[self.zombieWalkCount // 2]
        self.mask = pygame.mask.from_surface(self.image)

        if not screenRect.contains(self.rect):
            self.kill()

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Game(pygame.sprite.Sprite):

    def __init__(self):
        self.win = pygame.display.set_mode((screenWidth, screenHeight))#, pygame.FULLSCREEN)
        pygame.display.set_caption('ZOMBIESSSSSS!!!')
        self.bg = pygame.image.load(resource_path('bg.jpg'))
        super().__init__()
        self.player_sprite = pygame.sprite.Group()
        self.zombie_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.gunFireSound = pygame.mixer.Sound(resource_path("gun.wav"))
        self.gameOverSound = pygame.mixer.Sound(resource_path("gameover.wav"))
        pygame.mixer.music.load(resource_path('bgm.wav'))

        self.score = 0
        self.font = pygame.font.Font(resource_path("ExquisiteCorpse.ttf"), 40)

        self.clock = pygame.time.Clock()

        self.player = Player()
        self.player_sprite.add(self.player)
        self.all_sprites_list.add(self.player)

        self.zombieSpeed = 100
        self.spawnPoints = [(150, 50), (550, 60), (730, 280), (50, 420), (350, 520), (680, 500)]
        self.numSpawnPts = 6
        self.zombieAddCounter = 0
        self.zombieAddRate = 50

        if not GameRunning:
            startScreen(self.win, self.bg, self.font)

        self.main()

    def __del__(self):
        return

    def collisionDetect(self):
        zombieHitList = pygame.sprite.groupcollide(self.bullet_sprites, self.zombie_sprites, True, True,
                                                   pygame.sprite.collide_mask)

        for zombie in zombieHitList:
            self.score += 1

        playerGotAttacked = pygame.sprite.spritecollide(self.player, self.zombie_sprites, False,
                                                        pygame.sprite.collide_mask)

        if playerGotAttacked:
            pygame.mixer.music.stop()
            self.gameOverSound.play()
            gameOverScreen(self.win, self.bg, self, self.font)

    def update_score(self):
        scoretext = self.font.render("Score: " + str(self.score), True, fontColor)
        self.win.blit(scoretext, (5, 5))

    def main(self):
        pygame.mouse.set_visible(False)
        pygame.mixer.music.play(-1)

        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminate()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    bullet = Bullets(mousePos, self.player.position)
                    self.bullet_sprites.add(bullet)
                    self.all_sprites_list.add(bullet)
                    self.gunFireSound.play()

            self.player.rotate()

            self.collisionDetect()

            self.win.blit(self.bg, (0, 0))
            self.update_score()

            # draw sprites
            self.bullet_sprites.draw(self.win)
            self.player_sprite.draw(self.win)
            self.zombie_sprites.draw(self.win)

            # move sprites
            self.all_sprites_list.update()

            # spawn zombies
            self.zombieAddCounter += 1
            if self.zombieAddCounter == self.zombieAddRate:
                self.zombieAddCounter = 0
                ind = random.randint(0, 5)
                pt = self.spawnPoints[ind]
                dx = self.player.position[0] - pt[0]
                dy = self.player.position[1] - pt[1]
                xVel = dx / self.zombieSpeed
                yVel = dy / self.zombieSpeed
                zombie = Zombie(xVel, yVel)
                zombie.rotate(self.player.position, pt)
                self.zombie_sprites.add(zombie)
                self.all_sprites_list.add(zombie)

            pygame.display.update()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    game = Game()
