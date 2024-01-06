import pygame
import math
import random

pygame.init()

screen_width = 1200
screen_height = 800

background = pygame.image.load('pics/bg.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))
rocket = pygame.image.load('pics/ship_thrusted.png')
alienship = pygame.image.load('pics/alien ship.png')
star = pygame.image.load('pics/star.png')
asteroid_s = pygame.image.load('pics/asteroid_s.png')
asteroid_m = pygame.image.load('pics/asteroid_M.png')
asteroid_l = pygame.image.load('pics/asteroid_L.png')

shoot = pygame.mixer.Sound('sounds/shoot.wav')
bangLargeSound = pygame.mixer.Sound('sounds/bangLarge.wav')
bangSmallSound = pygame.mixer.Sound('sounds/bangSmall.wav')
shoot.set_volume(.25)
bangLargeSound.set_volume(.25)
bangSmallSound.set_volume(.25)

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game_over = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0

class Gamer(object):
    def __init__(self):
        self.image = rocket
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width // 2, self.y - self.sine * self.height // 2)

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y, self.width, self.height])
        win.blit(self.rotatedSurf, self.rotatedRect)

    def left(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width // 2, self.y - self.sine * self.height // 2)

    def right(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width // 2, self.y - self.sine * self.height // 2)

    def forward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width // 2, self.y - self.sine * self.height // 2)

    def location(self):
        if self.x > screen_width + 50:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = screen_width
        elif self.y < -50:
            self.y = screen_height
        elif self.y > screen_height + 50:
            self.y = 0


class Fire(object):
    def __init__(self):
        self.pt = gamer.head
        self.x, self.y = self.pt
        self.width = 4
        self.height = 4
        self.c = gamer.cosine
        self.s = gamer.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.width, self.height])

    def offscreen(self):
        if self.x < -50 or self.x > screen_width or self.y > screen_height or self.y < -50:
            return True


class Asteroid(object):
    def __init__(self, size):
        self.size = size
        if self.size == 1:
            self.image = asteroid_s
        elif self.size == 2:
            self.image = asteroid_m
        else:
            self.image = asteroid_l
        self.width = 50 * size
        self.height = 50 * size
        self.ranPoint = random.choice(
            [(random.randrange(0, screen_width - self.width), random.choice([-1 * self.height - 5, screen_height + 5])),
             (
             random.choice([-1 * self.width - 5, screen_width + 5]), random.randrange(0, screen_height - self.height))])
        self.x, self.y = self.ranPoint
        if self.x < screen_width // 2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Star(object):
    def __init__(self):
        self.image = star
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, screen_width - self.width), random.choice([-1 * self.height - 5, screen_height + 5])),
                                       (random.choice([-1 * self.width - 5, screen_width + 5]), random.randrange(0, screen_height - self.height))])
        self.x, self.y = self.ranPoint
        if self.x < screen_width//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Alien(object):
    def __init__(self):
        self.image = alienship
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, screen_width - self.width), random.choice([-1 * self.height - 5, screen_height + 5])),
                                       (random.choice([-1 * self.width - 5, screen_width + 5]), random.randrange(0, screen_height - self.height))])
        self.x, self.y = self.ranPoint
        if self.x < screen_width//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class AlienBullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.dx, self.dy = gamer.x - self.x, gamer.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.width, self.height])


def gamewindow():
    win.blit(background, (0, 0))
    font = pygame.font.SysFont('Comic Sans MS', 60 )
    livesText = font.render('Lives:' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Restart the game', 1, (255,255,255))
    scoreText = font.render('Score: ' + str(score), 1, (255,255,255))
    highScoreText = font.render('High Score: ' + str(highScore), 1, (255, 255, 255))

    gamer.draw(win)
    for a in asteroids:
        a.draw(win)
    for g in gamerFires:
        g.draw(win)
    for s in stars:
        s.draw(win)
    for a in aliens:
        a.draw(win)
    for b in alienBullets:
        b.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [screen_width // 2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [screen_width // 2 - 50, 20, 100 - 100 * (count - rfStart) / 500, 20])

    if game_over:
        win.blit(playAgainText, (screen_width//2-playAgainText.get_width()//2, screen_height//2 - playAgainText.get_height()//2))
    win.blit(scoreText,(screen_width - scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    #win.blit(highScoreText, (screen_width - highScoreText.get_width() - 25, 35 + scoreText.get_height()))
    pygame.display.update()


gamer = Gamer()
gamerFires = []
asteroids = []
count = 0
stars = []
aliens = []
alienBullets = []
run = True
while run:
    clock.tick(60)
    count += 1
    if not game_over:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroids.append(Asteroid(ran))
        if count % 1000 == 0:
            stars.append(Star())
        if count % 750 == 0:
            aliens.append(Alien())
        for i, a in enumerate(aliens):
            a.x += a.xv
            a.y += a.yv
            if a.x > screen_width + 150 or a.x + a.width < -100 or a.y > screen_height + 150 or a.y + a.height < -100:
                aliens.pop(i)
            if count % 60 == 0:
                alienBullets.append(AlienBullet(a.x + a.width // 2, a.y + a.height // 2))

            for b in gamerFires:
                if (b.x >= a.x and b.x <= a.x + a.width) or b.x + b.width >= a.x and b.x + b.width <= a.x + a.width:
                    if (b.y >= a.y and b.y <= a.y + a.height) or b.y + b.height >= a.y and b.y + b.height <= a.y + a.height:
                        aliens.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        break

        for i, b in enumerate(alienBullets):
            b.x += b.xv
            b.y += b.yv
            if (
                    b.x >= gamer.x - gamer.width // 2 and b.x <= gamer.x + gamer.width // 2) or b.x + b.width >= gamer.x - gamer.width // 2 and b.x + b.width <= gamer.x + gamer.width // 2:
                if (
                        b.y >= gamer.y - gamer.height // 2 and b.y <= gamer.y + gamer.height // 2) or b.y + b.height >= gamer.y - gamer.height // 2 and b.y + b.height <= gamer.y + gamer.height // 2:
                    lives -= 1
                    alienBullets.pop(i)
                    break

        gamer.location()
        for g in gamerFires:
            g.move()
            if g.offscreen():
                gamerFires.pop(gamerFires.index(g))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= gamer.x - gamer.width // 2 and a.x <= gamer.x + gamer.width // 2) or (a.x + a.width <= gamer.x + gamer.width // 2 and a.x + a.width >= gamer.x + gamer.width // 2):
                if (a.y >= gamer.y - gamer.height // 2 and a.y <= gamer.y + gamer.height // 2) or a.y + a.height >= gamer.y - gamer.height // 2 and a.y + a.height <= gamer.y + gamer.height // 2:
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        bangLargeSound.play()
                    break



            # bullets hit
            for g in gamerFires:
                if (g.x >= a.x and g.x <= a.x + a.width) or g.x + g.width >= a.x and g.x + g.width <= a.x + a.width:
                    if (g.y >= a.y and g.y <= a.y + a.height) or g.y + g.height >= a.y and g.y + g.height <= a.y + a.height:
                        if a.size == 3:
                            if isSoundOn:
                                bangLargeSound.play()
                            score += 15
                            new_asteroid1 = Asteroid(2)
                            new_asteroid2 = Asteroid(2)
                            new_asteroid1.x = a.x
                            new_asteroid2.x = a.x
                            new_asteroid1.y = a.y
                            new_asteroid2.y = a.y
                            asteroids.append(new_asteroid1)
                            asteroids.append(new_asteroid2)
                        elif a.size == 2:
                            if isSoundOn:
                                bangSmallSound.play()
                            score += 20
                            new_asteroid1 = Asteroid(1)
                            new_asteroid2 = Asteroid(1)
                            new_asteroid1.x = a.x
                            new_asteroid2.x = a.x
                            new_asteroid1.y = a.y
                            new_asteroid2.y = a.y
                            asteroids.append(new_asteroid1)
                            asteroids.append(new_asteroid2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmallSound.play()
                        asteroids.pop(asteroids.index(a))
                        gamerFires.pop(gamerFires.index(g))
                        break
        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.width or s.x > screen_width + 100 or s.y > screen_height + 100 or s.y < -100 - s.height:
                stars.pop(stars.index(s))
                break
            for g in gamerFires:
                if (g.x >= s.x and g.x <= s.x + s.width) or g.x + g.width >= s.x and g.x + g.width <= s.x + s.width:
                    if (g.y >= s.y and g.y <= s.y + s.height) or g.y + g.height >= s.y and g.y + g.height <= s.y + s.height:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        gamerFires.pop(gamerFires.index(g))
                        break
        if lives <= 0:
            game_over = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            gamer.left()
        if keys[pygame.K_RIGHT]:
            gamer.right()
        if keys[pygame.K_UP]:
            gamer.forward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                gamerFires.append(Fire())
                if isSoundOn:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    if not rapidFire:
                        gamerFires.append(Fire())
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if game_over:
                    game_over = False
                    lives = 3
                    score = 0
                    asteroids.clear()
                    alienBullets.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0

    gamewindow()
pygame.quit()
