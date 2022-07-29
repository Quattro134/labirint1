from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def fire(self):
        bullet = Bullet('Bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
    def update(self):
        if hero.rect.x <=win_width-80 and hero.x_speed > 0 or hero.rect.x >= 0 and hero.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.right)
        if hero.rect.y <= win_height-80 and hero.y_speed > 0 or hero.rect.y >= 0 and hero.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top. p.rect.bottom)
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = 'left'
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.rect
        if self.rect.x > win_width + 10:
            self.kill()
win_width = 700
win_height = 500
display.set_caption('Лабиринт')
window = display.set_mode((win_width,win_height))
back = (119, 210, 223)

mixer.init()
mixer.music.load('Music.mp3')
mixer.music.play()
sound_fire = mixer.Sound('vyistrel-pistoleta-magnum-357-36128.ogg')

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
w1 = GameSprite('Wall.png', win_width / 2 - win_width / 3, win_height / 2 , 300, 50)
w2 = GameSprite('Wall.png', 300, 70, 30, 350)
barriers.add(w1)
barriers.add(w2)
hero = Player("Hero.png", 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('Enemy.png', win_width - 80, 180, 80, 0, 5)
monster2 = Enemy('Enemy.png', win_width - 80, 230, 80, 4, 5)
monsters.add(monster1)
monsters.add(monster2)
final_sprite = GameSprite('Finish.png', win_width - 85, win_height - 100, 80, 80)
finish = False
run = True
while run:
    time.delay(50)
    window.fill(back)
 
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.type == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
            elif e.key == K_DOWN:
                hero.y_speed = 5
        elif e.type == KEYUP:
            if e.type == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0
    if not finish:
        window.fill(back)
        barriers.draw(window)
        bullets.draw(window)
        final_sprite.reset()
        hero.reset()
        bullets.update()
        hero.update()
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90,0))
        if sprite.collide_rect(hero, final_sprite):
            finish = True
            img = image.load('Win.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()
