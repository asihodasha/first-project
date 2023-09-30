#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer
win_height = 500        
win_width = 700  

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
window = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
class GameSprite(sprite.Sprite):

    def __init__(self,player_image,player_x,player_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x =  player_x
        self.rect.y =  player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

font.init()
font1= font.SysFont("Arial",80)
font2 = font.SysFont('"Arial',35)
win = font1.render(' YOU WIN', True, (255,255,255))
lose = font2.render(' YOU LOSE ', True, (100,0,0))





score = 0
goal = 10
lost = 0
count = 3
class  Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if  self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
  
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT]  and self.rect.x < win_width - 80:
            self.rect.x += self.speed  
    def fire(self):
         bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top, -15)
         bullets.add(bullet)

player = Player('rocket.png', 5, win_height - 80, 4)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40,  randint(1,5))
    monsters.add(monster)


clock = time.Clock()
FPS = 60

game = True
finish = False

rel_time = False

num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire + 1
                        fire_sound.play()
                        player.fire()    
                    if num_fire >= 5 and rel_time == False :
                        last_time = timer()
                        rel_time = True
    
    if finish != True: 
        window.blit(background,(0,0))
        text = font2.render(" Счет:" + str(score),1,(255,255,255))
        window.blit (text, (10, 20 ))

        text_lose = font2.render(" Пропущено:" + str(lost),1,(255,255,255))
        window.blit (text_lose, (10, 50 ))
        player.update()
        monsters.update()
        monsters.draw(window)
        player.reset()

        bullets.update()
        bullets.draw(window) 


        if rel_time == True :
            now_time = timer()

            if now_time - last_time < 3 :
                reload = font2.render('Wait, reload ...', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40,  randint(1,5))
            monsters.add(monster)


        if sprite.spritecollide(player,monsters, False) or lost >= count:
            finish = True
            window.blit(lose,(200,200))


        if score >= goal:
            finish = True
            window.blit(win,(200,200))
           
       
        display.update()
    clock.tick(FPS) 
