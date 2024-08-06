import pygame
import os
import time 
pygame.init()
import random
pygame.mixer.init()
pygame.init()
pygame.font.init()

width=1200
height=700

window= pygame.display.set_mode((width,height))
pygame.display.set_caption('FlyBird 2.0')
m=os.path.join(os.path.abspath(__file__ + "/.."),"retrophonk.mp3")
b=os.path.join(os.path.abspath(__file__ + "/.."),"background.jpg")
pygame.mixer.music.load(m)
pygame.mixer.music.play()
background = pygame.transform.scale(pygame.image.load(b), (width, height))
game = True
clock = pygame.time.Clock()
back=(0,0,0)

class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color
    def color(self, new_color):
        self.fill_color = back
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)                      

class Label(Area):	
    def set_text(self, text, fsize =12, text_color=(0,0,0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text,True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        window.blit(self.image, (self.rect.x + shift_x,self.rect.y + shift_y))

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, angle=0):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.transform.scale(pygame.image.load(filename),(width,height))
        self.image = pygame.transform.rotate(self.image, angle)
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
q = random.randint(100, 200)
ptichka = Picture('ptichka.png', 270, 270, 100, 100)
cookie = Picture("cookie.png", 270, q, 100, 70 )
YELLOW = (255,255,0)
DARK_BLUE = (0,0,100)
BLUE = (80,80,255)
RED = (255, 0, 0)
GREEN = (0, 255, 51)

time_text = Label(0,0,50,50,back)
time_text.set_text('Час:',40, RED)
time_text.draw(20, 20)

timer = Label(0,55,50,50,back)
timer.set_text('0', 40, RED)
timer.draw(0,0)

score_text = Label(800,0,50,50,back)
score_text.set_text('Рахунок:',40, GREEN)
score_text.draw(20, 20)

score = Label(800,100,50,50,back)
score.set_text('0', 40, GREEN)
score.draw(0,0)

columnMove = 400
move_up = False
column_list = []
cookie_list = []
columnX = [0, 200, 400, 600, 800, 1000, 1200, 1400]
for i in range(4):
    a = random.randint(100, 200)
    columnDownY = height - a
    columnUpY = height - a - 650
    column = Picture('column.png', i*200+600, columnDownY, 100, 300)
    column1 = Picture('column.png', i*200+600, columnUpY, 100, 300, 180)
    column_list.append(column)
    column_list.append(column1)
finish = False
start_time = time.time()
cur_time = start_time
while game:
    window.blit(background,(0,0))
    time_text.draw()
    timer.draw()
    score_text.draw()
    score.draw()
    if finish != True:
        ptichka.rect.y += 4
        new_time=time.time()
        if int(new_time) - int(cur_time) == 1: 
            timer.set_text(str(int(new_time - start_time)),40, RED)
            k = int(new_time - start_time)
            timer.draw(0,0)
            cur_time = new_time 
        for i in range(len(column_list)):
            column_list[i].rect.x -= 4
            column_list[i].draw()
            if column_list[i].rect.x <= - 100:
                del column_list[1]
                del column_list[0]
                a = random.randint(100, 300)
                columnDownY = height - a
                columnUpY = height - a - 650
                column = Picture('column.png', 700, columnDownY, 100, 300)
                column1 = Picture('column.png', 700, columnUpY, 100, 300, 180)
                column_list.append(column)
                column_list.append(column1)
        ptichka.draw()
        cookie.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                move_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                move_up = False
    if move_up:
        ptichka.rect.y -= 10 
    for cookie in cookie_list:
        if ptichka.rect.colliderect(cookie):
            score = score + 1
            if score >= 20:
                finish = True
                window.blit(background(0,0))
                win = Label(0, 0, 500, 500, GREEN)
                win.set_text("Ти виграв!!!", 60, DARK_BLUE)
    for column in column_list:
        if ptichka.rect.colliderect(column):
            k -=1
            if k < -10:
                finish = True
                window.blit(background,(0,0))
                win = Label(0, 0, 500, 500, GREEN)
                win.set_text("Ты програв!!!", 60, RED)
                win.draw(140, 180)
    if new_time - start_time  >= 60:
       win = Label(0, 0, 500, 500, GREEN)
       win.set_text("Ти виграв!!!", 60, DARK_BLUE) 
       win.draw(110, 180) 
    clock.tick(60)
    pygame.display.update()
