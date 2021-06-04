from pygame import *
from random import randint
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
font2 = font.Font(None, 36)
 

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько
goal = 10


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        super().__init__()

        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def shows(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.centery, 15, 20, -15)
        bullets.add(bullet)
 
#класс спрайта-врага  
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            
 
#класс спрайта-пули  
class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
 

 
#создаем спрайты
ship = Player("rocket.png", 5, 420, 40, 60, 10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 

 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
game = True #флаг сбрасывается кнопкой закрытия окна
while game:
    #событие нажатия на кнопку Закрыть
    kp = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        if kp[K_SPACE]:
            ship.fire()
    if finish != True:
        
        #обновляем фон
        window.blit(background,(0,0))

        #пишем текст на экране
    

        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()

        #обновляем их в новом местоположении при каждой итерации цикла
        ship.shows()
        
        monsters.draw(window)
        bullets.draw(window)
       
        display.update()
   #цикл срабатывает каждую 0.05 секунд
    time.delay(50)