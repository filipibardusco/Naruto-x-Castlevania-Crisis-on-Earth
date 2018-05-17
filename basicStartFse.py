#Importing necessary libraries
from pygame import *
from random import *
from math import *
from tkinter import *

#Defining screen variables
SIZE = (1100, 800)
screen = display.set_mode(SIZE)

#Defining colours and other constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

#Loading images
playerSprite = image.load("coffee.jpg")
playerSprite = transform.scale(playerSprite, (20, 20))
backgroundImages = ["hubWorldBack.jpg"]
levelSizes = [(2100, 800)] #List of the sizes of each level to use to transform each image, and set limits to how far our character can go
backgrounds = []
for images in backgroundImages:
    backgrounds.append(image.load(images))
for b in range(len(backgrounds)):
    backgrounds[b] = transform.scale(backgrounds[b], levelSizes[b])



#Defining player variables
XPOS = 7
YPOS = 8
HURTBOX = 0
XSPEED = 1
YSPEED = 2
ONGROUND = 3
SCREENX = 4 
HEALTH = 5
SPRITE = 6
player = [Rect(20, 780, 20, 20), 0, 0, True, 20, 100, playerSprite, 100, 780]


#Defining basic functions
def drawScene(guy, backgroundImage, plats, platColours, blocks, blockColours): #Function taken and modified from the scroll in class program
    """ draws the current state of the game """
    
    offset = player[SCREENX] - guy[XPOS]
    screen.blit(backgroundImage, (offset,0))  #Blitting background
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,platColours,p)
    for bl in blocks:
        b = bl.move(offset,0)        
        draw.rect(screen,blockColours,b)
    
    screen.blit(player[SPRITE], (player[SCREENX], guy[YPOS]))
        
    display.flip()

def moveGuy(guy, limit, blocks): #Function taken and modified from the scroll in class program
    keys = key.get_pressed()
    if keys[K_LEFT] and guy[XPOS] > 20:
        freeLeft = True
        for b in blocks:
            if guy[HURTBOX].colliderect(Rect(b.right, b.top, 1, (b.bottom - b.top))):
                freeLeft = False
        if freeLeft:
            guy[XPOS] -= 10
            if guy[SCREENX] > 0:
                guy[SCREENX] -= 10
        
    if keys[K_RIGHT] and guy[XPOS] < 2000:
        freeRight = True
        for b in blocks:
            if guy[HURTBOX].colliderect(Rect(b.left - 1, b.top, 1, (b.bottom - b.top))):
                freeRight = False
        if freeRight:
            guy[XPOS] += 10
            if guy[SCREENX] < 990:
                guy[SCREENX] += 10
    for b in blocks:
        if guy[HURTBOX].move(0, -guy[YSPEED]).colliderect(Rect(b.left, b.top - 1, b.right - b.left, 1)): #Creating floor for blocks
            guy[ONGROUND] = True
            guy[YSPEED] = 0
            guy[YPOS] = b.y - 20
    if keys[K_SPACE] and guy[ONGROUND] and guy[YSPEED] <= 0.7:
        print("jump")
        guy[YSPEED] = -15
        guy[ONGROUND] = False
    
    blockedUp = False
    for b in blocks:
        
        if guy[HURTBOX].colliderect(Rect(b.left, b.bottom + 1, b.right - b.left, 1)):
            blockedUp = True #Creating ceiling for blocks

        
    if blockedUp:
        guy[YSPEED] = 1.4

    

        

    guy[YPOS] += guy[YSPEED]     # add current speed to Y
    if guy[YPOS] >= 780:
        guy[YPOS] = 780
        guy[YSPEED] = 0
        guy[ONGROUND] = True

    guy[YSPEED] += .7     # add current speed to Y
    
    
    

def checkCollide(guy,plats, blocks): #Function taken and modified from the scroll in class program
    
    guy[HURTBOX] = Rect(guy[XPOS], guy[YPOS], 20, 20)
    rec = guy[HURTBOX]
    for p in plats:
        if rec.colliderect(p):
            if guy[YSPEED] > 0 and rec.move(0, -guy[YSPEED]).colliderect(p) == False:
                guy[ONGROUND] = True
                guy[YSPEED] = 0
                guy[YPOS] = p.y - 19
        
        

#defining level functions
def hub():
    drawScene(player, backgrounds[0], hubPlats, GREEN, hubBlocks, RED)
    moveGuy(player, levelSizes[0], hubBlocks)
    checkCollide(player, hubPlats, hubBlocks)
    

#defining level variables
hubPlats = [Rect(130, 700, 100, 10), Rect(130, 400, 100, 10), Rect(130, 550, 100, 10)]
hubBlocks = [Rect(500, 350, 100, 350), Rect(0, 0, 100, 350), Rect(0, 450, 100, 350), Rect(1900, 700, 200, 100), Rect(1900, 0, 200, 100)]





#starting main game loop
while RUNNING:
    for evt in event.get():
        if evt.type == QUIT: 
            RUNNING = False
    hub()
    
    print(player[0], player[ONGROUND], player[YSPEED])

    display.flip()







quit()
