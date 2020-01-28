import pygame
from pygame.locals import *



def loadResource(name):
    return pygame.image.load(name)

def loadAnimation(animationImages):
    retval=list()
    for i in animationImages:
        retval.append(loadResource("assets/sprites/"+i+".png"))
    return retval

pygame.init()
window = (500,512)
screen = pygame.display.set_mode(window)


birdAnimation=["yellowbird-downflap","yellowbird-midflap","yellowbird-upflap"]
birdAnimationImages=loadAnimation(birdAnimation)

base=loadResource("/home/stefan/Desktop/neuroreport/flappy/src/assets/sprites/base.png")
base_rect=base.get_rect()

bg = loadResource("/home/stefan/Desktop/neuroreport/flappy/src/assets/sprites/background-day.png")
bg_rect=bg.get_rect()

pipe = loadResource("/home/stefan/Desktop/neuroreport/flappy/src/assets/sprites/pipe-green.png")
pipe_rect=pipe.get_rect()

#bird
animationCounter=0
rect = birdAnimationImages[animationCounter].get_rect().move(30, 150)
speed=0
weight=15
height=0
cnt=0
angle=0
isDead=False


pipesTotalHeight=200


pipesUpperHeight=0.7 #0 to 1
pipesWidth=550

pipesList=[[0.7,450],[0.7,550],[0.7,650]]

def getBiggestPipeYCoordinate():
    v = ([x[1] for x in pipesList])
    v.sort()
    return v[-1]

#[(upperHeight percent of total ,pipes width)]

def drawBird():
    global animationCounter, height, speed, cnt, angle
    surf=pygame.transform.rotate(birdAnimationImages[animationCounter], angle-20)
    screen.blit(surf, rect.move(30,height))

def drawBase():
    screen.blit(base,base_rect.move(0,480))
    screen.blit(base, base_rect.move(200,480))

def drawBg():
    screen.blit(bg,bg_rect.move(0,0))
    screen.blit(bg,bg_rect.move(window[0]/2,0))

def drawPipe(index):
    global pipesList, pipesTotalHeight
    surf = pygame.transform.rotate(pipe, 180)
    screen.blit(surf,surf.get_rect().move(pipesList[index][1],0-(pipesTotalHeight*pipesList[index][0]))) #up
    surf=pipe
    screen.blit(surf,surf.get_rect().move(pipesList[index][1],220+(pipesTotalHeight*(1-pipesList[index][0])))) #down

def animate():
    #bird
    global animationCounter, height, speed, cnt, angle,isDead
    if(speed>0):
        animationCounter = (animationCounter + 1) % 3
    else:
        animationCounter = 1

    angle = (speed * 90 / 75)
    if (cnt % 15 == 0):
        speed = speed - weight
        height = height - speed
        cnt = 0
    cnt += 1
    if (speed < 10): speed = 0
    if (speed > 70): speed = 70
    if (height > window[1] - 210):
        isDead=True
        height = window[1] - 21

    if (height < -150):
        height = -150
    #pipes
    global pipesList, pipesTotalHeight

    for index in range(len(pipesList)):
        if (pipesList[index][1] < -50):
            pipesList[index][1] = 200+getBiggestPipeYCoordinate()+random.randint(100,150)
            pipesList[index][0] = random.randint(0, 10) / 10
            break
        pipesList[index][1] = pipesList[index][1] - 2



import random

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed=speed+55
    drawBg()
    if(not isDead):
        animate()
    drawBird()
    for i in range(len(pipesList)):
        drawPipe(i)

    drawBase()
    pygame.display.flip()
