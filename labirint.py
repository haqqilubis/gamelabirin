from pygame import *
class GameSprite(sprite.Sprite):
    def __init__ (self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

walls = sprite.Group()

class Player(GameSprite):
    def __init__ (self, picture, w, h, x, y, speedx, speedy):
        super().__init__ (picture, w, h, x, y)
        self.speedx = speedx
        self.speedy = speedy
    def update(self):
        self.rect.x += self.speedx
        platform_touch = sprite.spritecollide(self, walls, False)
        if self.speedx >0:
            for p in platform_touch:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speedx <0:
            for p in platform_touch:
                self.rect.left = max(self.rect.left, p.rect.right)
    
        self.rect.y += self.speedy
        platform_touch = sprite.spritecollide(self, walls, False)
        if self.speedy >0:
            for p in platform_touch:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speedy <0:
            for p in platform_touch:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        peluru = Peluru("arrow.png", 30, 30, self.rect.centerx, self.rect.centery, 10)
        bulat.add(peluru)

class Enemy(GameSprite):
    def __init__ (self, picture, w, h, x, y, speed):
        super().__init__ (picture, w, h, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 470:
            self.direction = "kanan"
        if self.rect.x >= 600:
            self.direction = "kiri"
        if self.direction == "kiri":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

enemies = sprite.Group()

class Peluru(GameSprite):
    def __init__ (self, picture, w, h, x, y, speed):
        super().__init__ (picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 600:
            self.kill()

bulat = sprite.Group()

wall_1 = GameSprite('home.png', 300, 300, 200, 50)
walls.add(wall_1)
player = Player('instagram.png', 80, 100, 100, 250, 0, 0)
final = GameSprite('arcade.png', 80, 100, 600, 250)
menang = transform.scale(image.load('download.jpeg'), (700, 500))
enemy = Enemy('pacman.png',  80, 100, 350, 390, 15)
enemies.add(enemy)
kalah = transform.scale(image.load('hantu.jpeg'), (700, 500))

yellow = (255, 255, 0)
window = display.set_mode((700, 500))
display.set_caption("pigame by haqqi")
finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.speedx = -10
            elif e.key == K_RIGHT:
                player.speedx = 10
            elif e.key == K_UP:
                player.speedy = -10
            elif e.key == K_DOWN:
                player.speedy = 10
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.speedx = 0
            elif e.key == K_RIGHT:
                player.speedx = 0
            elif e.key == K_UP:
                player.speedy = 0
            elif e.key == K_DOWN:
                player.speedy = 0
            elif e.key == K_SPACE:
                player.fire()
    if finish != True:
        window.fill(yellow)
        walls.draw(window)
        player.reset()
        player.update()
        enemies.draw(window)
        enemies.update()
        final.reset()
        bulat.update()
        bulat.draw(window)
        sprite.groupcollide(bulat, walls, True, False)
        sprite.groupcollide(enemies, bulat, True, True)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(menang, (0, 0))
        if sprite.spritecollide(player, enemies, False):
            finish = True
            window.blit(kalah, (0,0))
    display.update()