import pygame
import random
import pandas as pd

pygame.init()

word=pd.read_csv("assets/files/words.csv")
wordlist=word['Word']

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typing Racer!')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

score = 0

background=pygame.image.load("assets/images/background.jpg")
red_car_image=pygame.image.load("assets/images/redcar.jpg")
yellow_car_image=pygame.image.load("assets/images/yellowcar.png")
green_car_image=pygame.image.load("assets/images/greencar.png")
black_car_image=pygame.image.load("assets/images/blackcar.png")
blue_car_image=pygame.image.load("assets/images/blackcar.png")
carwidth,carheight=red_car_image.get_size()
carwidth=int(carwidth/12)
carheight=int(carheight/12)
# print(carwidth,carheight)
red_car=pygame.transform.scale(red_car_image,(carwidth, carheight)).convert_alpha()
yellow_car=pygame.transform.scale(yellow_car_image,(carwidth,carheight)).convert_alpha()
green_car=pygame.transform.scale(green_car_image,(carwidth,carheight)).convert_alpha()
black_car=pygame.transform.scale(black_car_image,(carwidth,carheight)).convert_alpha()
blue_car=pygame.transform.scale(blue_car_image,(carwidth,carheight)).convert_alpha()
car_list=[red_car,yellow_car,green_car, black_car, blue_car]
header_font = pygame.font.Font('assets/fonts/Jersey25.ttf', 70)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 40)
banner_font = pygame.font.Font('assets/fonts/Jersey25.ttf', 45)
font = pygame.font.Font('assets/fonts/Montserrat.ttf', 30)
# music and sounds
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('assets/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('assets/sounds/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 5
word_objects = []
file = open('assets/files/high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()
pz = True
new_level = True
level_no=0
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class Car:
    def __init__(self, text, speed, y_pos, x_pos, car):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.car= car

    def draw(self):
        screen.blit(self.car,(self.x_pos-carwidth/4,self.y_pos-carheight/4.5))
        color = 'white'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed


class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, 'black', (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (7, 70, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (70, 7, 35), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


def draw_screen():
    # screen outlines for main game window and 'header' section
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, (32, 42, 68), [0, 0, WIDTH, 50], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (0,50), (WIDTH, 50), 2)
    pygame.draw.line(screen, 'white', (190, 0), (190, 50), 2)
    pygame.draw.line(screen, 'white', (500, 0), (500, 50), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    # text for showing current level, player's current string, high score and pause options
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 90))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 90))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    # draw lives, score, and high score on top of screen
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (220, 3))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'white'),(530, 3))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'white'), (30, 3))
    return pause_btn.clicked


def draw_pause():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 70, 600, 270], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 70, 600, 270], 5, 5)
    resume_btn = Button(160, 278, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(495, 278, 'X', False, surface)
    quit_btn.draw()
    surface.blit(header_font.render('MENU', True, 'white'), (325, 95))
    surface.blit(header_font.render('PLAY!', True, 'white'), (200, 240))
    surface.blit(header_font.render('QUIT!', True, 'white'), (535, 240))
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, quit_btn.clicked

def game_level():
    word_objs = []
    lane_positions={102:random.randint(1,3), 250:random.randint(1,3), 435:random.randint(1, 3), 600:random.randint(1,3)}
    separation=random.randint(20 , 25)
    temp=level
    if level>=10:
        temp=10
    for i in range(temp):
        y_pos = random.choice(list(lane_positions.keys()))
        x_pos = WIDTH + (separation + carwidth) * (i+1)
        text= random.choice(wordlist)
        new_word = Car(text.lower(), lane_positions[y_pos]+0.025*level, y_pos, x_pos,random.choice(car_list))
        word_objs.append(new_word)
    return word_objs



def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            scor += int(points)
            word_objects.remove(wrd)
            woosh.play()
    return scor


def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('assets/files/high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

#gameloop
run = True
while run:
    screen.blit(background,(0,0))
    timer.tick(fps)
    # draw static background
    pause_butt = draw_screen()
    if pz:
        resume_butt,quit_butt = draw_pause()
        if resume_butt:
            if(lives<=0):
                lives=5
                level=1
                score=0
            pz = False
        if quit_butt:
            check_high_score()
            run = False
    if new_level and not pz:
        word_objects = game_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1
                level_no+=1
    if len(word_objects) <= 0 and not pz:
        if level_no==0:
            level += 1
        level_no=0
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if pz:
                    pz = False
                else:
                    pz = True

    if pause_butt:
        pz = True

    if lives < 0:
        pz = True
        lives = 0
        word_objects = []
        new_level = True
        check_high_score()
    
    if pz:
        resume_butt,quit_butt = draw_pause()

    pygame.display.flip()
pygame.quit()