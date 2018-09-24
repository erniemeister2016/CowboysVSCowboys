#Author: Ernesto Pimentel
#Cowboys VS Cowboys
#Music: Eliot Corley from ChaosIsHarmony


import pygame, sys, time, random
from pygame.locals import *


WIDTH = 1200
HEIGHT = 678

#background set up
screen = pygame.display.set_mode((1200, 678))
bg = pygame.image.load('purpatown.png').convert()
bg_rect = bg.get_rect()

pygame.display.set_caption('Cowboys VS Cowboys')

WHITE = (255, 255, 255)


#Player class
class Cowboy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cowboySprite.png')
        self.image = pygame.transform.scale(self.image, (130, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH //2
        self.rect.bottom= HEIGHT // 2
        self.rect.center = (150, HEIGHT //2)
        self.speedy = 0

    #Player movement with boundaries
    def update(self):
        self.speedy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.speedy = -10
        if key[pygame.K_DOWN]:
            self.speedy = 10
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


    def shoot(self):
        bullet = projectile(self.rect.centerx, self.rect.right)
        all_sprites.add(bullet)
        bullets.add(bullet)


#NPC class
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (180, 290))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 130
        self.rect.y = HEIGHT // 2
        self.speedy = 10

    #NPC movement and boundaries
    def update(self):
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 50
            self.speedy = 10
            self.speedy *= 1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy *= -1
        if random.randint(0, 50) == 1:
            self.shoot()

    #NPC automated shooting
    def shoot(self):
        bullet = projectileEnemy(self.rect.x, self.rect.y)
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y + 100
        all_sprites.add(bullet)
        enemBullets.add(bullet)
      

#Bullet class
class projectile(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()

    #Bullet dies off screen
    def update(self):
        self.rect.x += 30
        if self.rect.right > 1500:
            self.kill()

#Seperate Bullet movement for enemy
class projectileEnemy(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 30
        if self.rect.left < 0:
            self.kill()




pygame.init()

#Game Music
pygame.mixer.music.load('Showdown.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops = -1)

#Function to display text
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

#Main menu/Game over menu
def show_go_screen():
    draw_text(screen, 'Cowboys VS Cowboys', 64, WIDTH//2, HEIGHT//4)
    draw_text(screen,'Arrow keys to move, Space to fire', 22,WIDTH//2, HEIGHT//2)
    draw_text(screen,'Exit out to quit or press any key to continue', 18, WIDTH//2, HEIGHT *3 //4 )
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


clock = pygame.time.Clock()
prev = pygame.time.get_ticks()
running = True
game_over = True

#Main game loop
while running:
    #Checks if user still wants to play
    if game_over:
        show_go_screen()
        game_over = False
        #Scores and sprites are reset if the game continues
        all_sprites = pygame.sprite.Group()
        bullets_list = pygame.sprite.Group()
        enemBullets = pygame.sprite.Group()
        player = Cowboy()
        enemy = Enemy()
        all_sprites.add(player)
        all_sprites.add(enemy)
        enemScore = 0
        score = 0

    current = pygame.time.get_ticks()
    clock.tick(30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            #Space to shoot
            if event.key == pygame.K_SPACE:
                #Limits shooting rate
                if current - prev > 1000:
                    prev = current
                    bull = projectile(player.rect.midright, player.rect.center)
                    bull.rect.x = player.rect.x + 75
                    bull.rect.y = player.rect.y + 50
                    all_sprites.add(bull)
                    bullets_list.add(bull)

    bg = pygame.image.load('purpatown.png').convert()
    bg_rect = bg.get_rect()

    #Tracks collison for bullets that hit enemy
    hits = pygame.sprite.spritecollide(enemy, bullets_list, False)
    for hit in hits:
        bullets_list.remove(bullets_list)
        all_sprites.remove(bullets_list)
        score += 1
        print(score)
        if score == 3:
            enemy.kill()
            game_over = True
    #Tracks collision for bullets that hit player
    enemyHits = pygame.sprite.spritecollide(player, enemBullets, False)
    for enemyHit in enemyHits:
        enemBullets.remove(enemBullets)
        all_sprites.remove(enemBullets)
        enemScore += 1
        print(enemScore)
        if enemScore == 3:
            player.kill()
            game_over = True

    #update
    all_sprites.update()


    #draw

    screen.fill(WHITE)
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen,'Cowboys VS Cowboys',70, 640, 10)
    pygame.display.flip()


pygame.quit()
