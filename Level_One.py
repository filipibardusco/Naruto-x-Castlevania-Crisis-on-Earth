# scroll3
# simple example of a scrolling background. This one uses just one picture that
# is drawn to a negative position.
from pygame import *
from random import randint
from datetime import datetime
from math import *

import pygame
pygame.init()
pygame.mixer.init()
init()
size = width, height = 900, 500
screen = display.set_mode(size)
backPic = image.load("backg.jpg")
shurikenPic=image.load("shuriken.png")

music='EoT OST.wav'
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

chakra=pygame.mixer.Sound('Rasengan SFX.wav')
hit=pygame.mixer.Sound('Punch SFX.wav')
shuriken=pygame.mixer.Sound('Shuriken SFX.wav')



def drawScenery(screen,guy):
    """ draws the current state of the game """
    offset = guy[SCREENX] - guy[X]
    screen.blit(backPic, (offset,0))
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,(151,151,151),p)
      
    guyPic = pics[move][int(frame)]
    screen.blit(guyPic, (guy[SCREENX],guy[Y]))

    for b in bullets:
        draw.circle(screen,(0,0,0),(int(b[0]),int(b[1])), 0)
        screen.blit(shurikenPic,bulletRect)
        
    display.flip()

'''
    The guy's x position is where he is in the "world" we then draw the map
    at a negative position to compensate.
'''
def moveNaruto(guy):
    keys = key.get_pressed()
    global move, frame

    if keys[K_SPACE] and guy[ONGROUND]:
        guy[VY] = -10
        guy[ONGROUND]=False
    
    newMove=-1
    if keys[K_LEFT] and guy[X] > 250:
        guy[X] -= 10
        newMove=LEFT
        if guy[SCREENX] > 250:
            guy[SCREENX] -= 10

    elif keys[K_RIGHT] and guy[X] < 5650:
        guy[X] += 10
        newMove=RIGHT
        if guy[SCREENX] <450:
            guy[SCREENX] += 10

    elif keys[K_LSHIFT]:
    	newMove=ATTACK
    	chakra.play()

    elif keys[K_a]:
    	newMove=PUNCH
    	hit.play()

    elif keys[K_s]:
    	newMove=THROW
    	shuriken.play()

    else:
    	frame=0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.15 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
        print("hello")

    guy[Y]+=guy[VY]     # add current speed to Y
    if guy[Y] >= 440:
        guy[Y] = 440
        guy[VY] = 0
        guy[ONGROUND]=True
    guy[VY]+=.7     # add current speed to Y


def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%01d.png" % (name,name,i)))
        
    return move

    
def checkTouch(guy,plats):
    rec = Rect(guy[X],guy[Y],56,57)
    for p in plats:
        if rec.colliderect(p):
            if guy[VY]>0 and rec.move(0,-guy[VY]).colliderect(p)==False:
                guy[ONGROUND]=True
                guy[VY] = 0
                guy[Y] = p.y - 57

RIGHT = 0 # These are just the indices of the moves
LEFT = 1  
PUNCH = 2
ATTACK=3
THROW=4

pics = [] #2d list
pics.append(makeMove("NarutoReg",1,7))      #RIGHT
pics.append(makeMove("NarutoReg",8,14))		#LEFT
pics.append(makeMove("NarutoReg",15,19))	#PUNCH
pics.append(makeMove("NarutoReg",20,63))    #ATTACK
pics.append(makeMove("NarutoReg",64,68))    #THROW

print(len(pics))
frame=0     # current frame within the move
move=0      # current move being performed (right, down, up, left)
              
running = True         
myClock = time.Clock()

X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4
guy = [150,450,0,True,150]

rapid = 20
px,py=guy[X]+300,guy[Y]+30 #player's position
ex,ey=600,250
bullets = []


plats=[Rect(260,430,100,10),Rect(500,370,100,10),Rect(260,320,100,10),Rect(460,260,100,10),Rect(260,190,100,10),Rect(1080,430,2000,10),Rect(1550,355,100,10)]


##plats = []
##for i in range(20):
##    plats.append(Rect(randint(100,2000),randint(250,480),60,10))

while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False

    keys = key.get_pressed()

    moveNaruto(guy)        
    checkTouch(guy,plats)
    drawScenery(screen, guy)

    if rapid<20:
        rapid+=1
    if keys[K_s] and rapid==20: #K_s is the S key
        rapid = 0
        vx = 7
        vy = 0
        bullets.append([px,py,vx,vy])
        #print(bullets)

    for b in bullets[:]:#this is the copy of the bullet list
        #b[2]*=1.1
        #b[3]*=1.1
        b[0]+=b[2]
        b[1]+=b[3]

        bulletRect=Rect(b[0]-5,b[1]-5,10,10)

        #if bulletRect.colliderect(enemyRect):
         #   print("boom")
          #  bullets.remove(b)
           # ex,ey=5000,5000

 
        if max(b) > 1000 or min(b) < -100:
            bullets.remove(b)#removing the bullets that are not on the stage


    myClock.tick(60)
    #print(guy)
    #print (guy[ONGROUND])

quit()
