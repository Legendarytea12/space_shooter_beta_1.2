import pygame
import random


pygame.init()



FPS = 60
wind = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (700, 500))





class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))
        self.speed = speed
    def draw(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, w, h, image, bullets_max, need_reolad):
        self.rect = pygame.Rect(x, y, w, h)
        self.bullets_max = bullets_max
        self.have_bullets = bullets_max
        self.need_reolad = False
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            player.rect.x +=3
        if k[pygame.K_a]:
            player.rect.x -=3
    def collide(self, item):
        if self.rect.colliderect(item.rect):
            return True
        else:
            return False
    def fire(self):
        if not self.need_reolad:
            Bullet(self.rect.x, self.rect.y, 10, 12, bullet_img, 1)
            self.have_bullets -= 1
            if self.have_bullets == 0:
                self.need_reolad = True

per = 0
lifes = 3
score = 0
per_record = score
lost = 0
bot_group = pygame.sprite.Group()


class Bot(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        self.speed = speed
        self.speed = 1
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        bot_group.add(self)
    def bot_start(self):
        self.rect.y = 0
        self.rect.y = random.randint(0, 700 - self.rect.w)
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            bot_group.remove(self)
            lost += 1
            game_over = font.render("Game over", True, (0,0,0))



bullet_group = pygame.sprite.Group()



class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        self.speed = speed
        self.speed = 5
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        bullet_group.add(self)
    def bullet_start(self):
        player.rect.x
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            bullet_group.remove(self)






pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play(-1)



player_img = pygame.image.load("rocket.png")
player = Player(200, 400, 50, 50, player_img, 30, False)

bot_img = pygame.image.load("ufo.png")

bullet_img = pygame.image.load("bullet.png")
#bullet = Bullet(player.rect.x, player.rect.y, 10, 12, bullet_img, 1)


start_btn_img = pygame.image.load("start_btn_img.jpg")
sett_btn_img = pygame.image.load("sett_btn_img.jpg")
qiut_btn_img = pygame.image.load("qiut_btn_img.jpg")
back_btn_img = pygame.image.load("back_btn_img.jpg")

start_btn = GameSprite(250, 50, 200, 100, start_btn_img, 1)
sett_btn = GameSprite(250, 200, 200, 100, sett_btn_img, 1)
exit_btn = GameSprite(250, 400, 200, 100, qiut_btn_img, 1)
back_btn = GameSprite(250, 250, 200, 100, back_btn_img, 1)




bot_wait = 0
font = pygame.font.SysFont("Arial", 32)


screen = 'menu'
game = True
finish = False

while game:
    if screen == 'menu':
        wind.blit(background, (0,0))
        start_btn.draw()
        sett_btn.draw()
        exit_btn.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if sett_btn.rect.collidepoint(x, y):
                    screen = 'settings'
                if exit_btn.rect.collidepoint(x, y):
                    game = False
                if start_btn.rect.collidepoint(x, y):
                    screen = 'game_wind'
    elif screen == 'settings':
        back_btn.draw()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if back_btn.rect.collidepoint(x, y):
                    screen = 'menu'
    
    
    
    
    
    elif screen == 'game_wind':               
        if not finish:
            wind.blit(background, (0 ,0))
            player.draw()
            player.move()

            if bot_wait == 0:
                bot = Bot(random.randint(0, 650), 0, 70, 50, bot_img, 1)
                bot_wait = random.randint(90, 260)
            else:
                bot_wait -= 1
            bot_group.draw(wind)
            bot_group.update()
            bullet_group.draw(wind)
            bullet_group.update()
            rec = font.render("Рекорд " + str(score) , True, (255,255,255))
            bullets_hav = font.render("Пуль осталось " + str(player.have_bullets) , True, (255,255,255))
            lost_text = font.render("Пропущенно " + str(lost) , True, (255,255,255))
            wind.blit(bullets_hav, (400, 0))
            wind.blit(rec, (0, 0))
            wind.blit(lost_text, (0, 50))


            if pygame.sprite.spritecollide(player, bot_group, True):
                lifes -= 1
                if lifes == 0:
                    if score >= per_record:
                        per_record = score
                        with open("record.txt", "w") as file:
                            file.write(str(per_record))
                        rec = font.render("Новый Рекорд! " + str(per_record), True, (255,255,255))
                        wind.blit(rec, (700/2,500/2))
                    else:
                        rec_r = font.render("Рекорд " + str(score) , True, (255,255,255))
                        wind.blit(rec_r, (700/2,150))
                    finish = True
            elif lost >= 5:
                finish = True
                rec_r = font.render("Рекорд " + str(score) , True, (255,255,255))
                wind.blit(rec_r, (700/2,150))
            

            if pygame.sprite.groupcollide(bullet_group, bot_group, True, True):
                score += 1
                if score >= per_record:
                    per_record += 1
                    with open ("record.txt", "w+") as file:
                        file.write(str(per_record))
                    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish:
            bot_group.empty()
            player.rect.x = 200
            player.rect.y = 400
            finish = False
            lost = 0
            screen = 'menu'
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.fire()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and player.need_reolad:
            player.have_bullets = player.bullets_max
            player.need_reolad = False

    clock.tick(FPS)
    pygame.display.update()