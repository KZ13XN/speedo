#!/usr/bin/env python
import time
import math
import pygame
from pygame.locals import *
import os
import RPi.GPIO as GPIO

os.environ["SDL_FBDEV"] = "/dev/fb1"

tra = 0
mph = 0
kph = 0
rpm = 0
cyc = 0
bur = 0
rev = 0
hall = 40
st = time.time()

def i_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(hall, GPIO.IN, GPIO.PUD_UP)
    
def i_i():
    GPIO.add_event_detect(hall, GPIO.FALLING, callback=cc, bouncetime=2)
    
def cc(channel):
    global bur, st, cyc
    bur += 1
    cyc = time.time() - st
    st = time.time()
    
def css(r):
    global bur, cyc, rpm, jm, tra, mps, mph, kps, kph, jk, c, rev
    if cyc != 0:
        rpm = 1/cyc * 60
        c = (2*math.pi)*r
        jm = c/160934
        jk = c/100000
        mps = jm / cyc
        kps = jk / cyc
        kph = kps * 3600
        mph = mps * 3600
        tra = ((jm*bur)*1000)/1600
        rev = 2300+(rpm * 3.214)
        return mph, kph, rev
    
def p_d():
    global size, f1, f2, f3, f4, WHITE
    size = width, height = 480,320
    f1 = pygame.font.Font("/home/pi/d.ttf", 114)
    f2 = pygame.font.Font("/home/pi/d.ttf", 18)
    f3 = pygame.font.Font("/home/pi/d.ttf", 30)
    f4 = pygame.font.Font("/home/pi/d.ttf", 28)
    WHITE = (255,255,255)
    
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
def stat():
    global B
    screen.fill(WHITE)
    B = Background("/home/pi/b.jpg", [0,0])

def statr():
    global B
    screen.fill(WHITE)
    B = Background("/home/pi/br.jpg", [0,0])

def draw():
    rpms = f3.render("{0:04.0f}".format(rpm), 1, (10,10,10))
    mphs = f1.render("{0:05.1f}".format(mph), 1, (10,10,10))
    ms = f4.render("M/h", 1, (10,10,10))
    ks = f2.render("KM/h", 1, (10,10,10))
    dis = f3.render("{0:06.2f}".format(tra), 1, (10,10,10))
    revs = f3.render("{0:05.0f}".format(rev), 1, (10,10,10))
    kphs = f3.render("{0:05.1f}".format(kph), 1, (10,10,10))
    screen.blit(B.image, B.rect)
    screen.blit(rpms, (390, 275))
    screen.blit(mphs, (80, 80))
    screen.blit(ms, (390, 165))
    screen.blit(ks, (170, 212))
    screen.blit(dis, (75, 275))
    screen.blit(revs, (390, 200))
    screen.blit(kphs, (87, 200))
    time.sleep(0.2)
    pygame.display.flip()
    
if __name__ == '__main__':
    try:
        i_GPIO()
        i_i()
        pygame.init()
        size = width, height = 480,320
        screen = pygame.display.set_mode((size))
        pygame.mouse.set_visible(False)
        f1 = pygame.font.Font("/home/pi/d.ttf", 114)
        f2 = pygame.font.Font("/home/pi/d.ttf", 18)
        f3 = pygame.font.Font("/home/pi/d.ttf", 30)
        f4 = pygame.font.Font("/home/pi/d.ttf", 28)
        WHITE = (255,255,255)
        while True:
            pygame.display.flip()
            css(24)
            if rev > 9999:
                statr()
                draw()
            if (time.time() - st) > 2:
                rpm = 0
                mph = 0
                kph = 0
                rev = 2300
                stat()
                draw()
            stat()
            draw()
    except KeyboardInterrupt:
        print('Stopped')
        GPIO.cleanup()
