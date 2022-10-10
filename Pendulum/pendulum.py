import math
import pygame as pg
from numpy import random

from settings import *


pg.init()
background = pg.display.set_mode((width, height))

class Pendulum(pg.sprite.Sprite):
    def __init__(self, gui, initial_position, dt=0, color='red'):
        super().__init__()
        self.length = initial_position[1]
        self.color = random_color()
        self.t0 = initial_position[0]
        self.theta = initial_position[0]
        self.w = math.sqrt(gravity/self.length)
        self.dt = dt

    def draw(self):
        rx, ry = angle_to_xy(self.theta, self.length)

        pg.draw.line(background, 'grey', hang, (rx, ry), 2)
        pg.draw.circle(background, self.color, (rx, ry), radius)

    def update(self):
        self.theta = self.t0*math.cos(self.w*self.dt)
        self.dt += 0.1


class Button():
    def __init__(self, gui, pos, image, tag, scale=False):
        self.image = image
        if scale:
            self.image = pg.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.tag = tag

    def draw(self):
        background.blit(self.image, (self.rect.x, self.rect.y))

    def button_function(self):
        try:
            pen = pendulums.sprites()[-1]
            if self.tag == 'plus':
                pen.length += 10
            if self.tag == 'minus':
                pen.length -= 10
            if self.tag == 'clear':
                pendulums.empty()
        except:
            pass


class Box():
    def __init__(self, gui, pos, images):
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False

    def draw(self):
        background.blit(self.image, (self.rect.x, self.rect.y))

    def button_function(self):
        if gui.length:
            gui.length = 0
            self.image = self.images[0]
            self.clicked = False
        else:
            try:
                pen = pendulums.sprites()[-1]
                gui.length = pen.length
                gui.dt = pen.dt
                self.image = self.images[1]
                self.clicked = True
            except:
                pass
    def update(self):
        if self.clicked:
            gui.dt += 0.1

class GUI():
    def __init__(self):
        self.length = 0
        self.general_dt = 0


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))

def angle_to_xy(theta, length):
    x = length * math.sin(theta) + hang[0]
    y = length * math.cos(theta)
    return [x, y]

def coord_length(pos):
    len = gui.length
    true_len = math.sqrt(math.pow(abs(hang[0]-pos[0]),2) + math.pow(pos[1],2))
    angle = math.acos(pos[1]/true_len)
    if hang[0]-pos[0] >= 0:
        angle = -angle
    if len:
        return angle, len
    return angle, true_len

def add_pendulum(coords):
    if gui.length:
        dt = gui.dt
    else:
        dt = 0
    pendulums.add(Pendulum(gui, coord_length(coords), dt, color=list(random.choice(range(256), size=3))))

def create_gui():
    plus_image = pg.image.load('images/plus.png').convert_alpha()
    plus = Button(gui, pos=(10,10), image=plus_image, tag='plus', scale=(32,32))
    buttons.append(plus)

    minus_image = pg.image.load('images/minus.png').convert_alpha()
    minus = Button(gui, pos=(50,10), image=minus_image, tag='minus' ,scale=(32,32))
    buttons.append(minus)

    fix_length_text = pg.image.load('images/fix_len.png').convert_alpha()
    fix_text = Button(gui, pos=(50,50), image=fix_length_text, tag=False)
    buttons.append(fix_text)

    box_images = [pg.image.load('images/box.png').convert_alpha(), pg.image.load('images/box_ticked.png').convert_alpha()]
    box = Box(gui, (10,50), box_images)
    buttons.append(box)

    clear_images = pg.image.load('images/x.png').convert_alpha()
    clear = Button(gui, pos=(width-50,10), image=clear_images, tag='clear')
    buttons.append(clear)

def mouse_click_function(mpos):
        for button in buttons:
            if button.rect.collidepoint(mpos):
                button.button_function()
                return
        add_pendulum(mpos)


pendulums = pg.sprite.Group()
buttons = []
gui = GUI()
run = True
create_gui()

while run:
    pg.time.Clock().tick(120)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            mouse_click_function(event.pos)

    pendulums.update()
    for button in buttons:
        if hasattr(button, 'update'):
            button.update()
    background.fill("black")
    pg.draw.line(background, 'blue', hang, (hang[0], height), 1)
    for pendulum in pendulums:
        pendulum.draw()
    for button in buttons:
        button.draw()

    pg.display.flip()

pg.quit()
