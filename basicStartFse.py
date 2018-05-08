#Importing necessary libraries
from pygame import *
from random import *
from math import *
from tkinter import *

#Defining screen variables
SIZE = (1000, 800)
screen = display.set_mode(SIZE)

#Defining colours and other constants
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

#Loading images
playerSprite = image.load("coffee.jpg")
playerSprite = transform.scale(playerSprite, (20, 20))
backgroundImages = ["testBackground.jpg"]
levelSizes = [(2000, 800)] #List of the sizes of each level to use to transform each image, and set limits to how far our character can go
backgrounds = []
for images in backgroundImages:
    backgrounds.append(image.load(images))
for b in range(len(backgrounds)):
    backgrounds[b] = transform.scale(backgrounds[b], levelSizes[b])



#Defining player variables
xPos = 20
yPos = 780
HURTBOX = 0
XSPEED = 1
YSPEED = 2
ONGROUND = 3
SCREENX = 4
HEALTH = 5
SPRITE = 6
player = [Rect(xPos, yPos, 20, 20), 0, 0, True, 20, 100, playerSprite]


#Defining basic functions
def drawScene(guy, backgroundImage): #Function taken and modified from the scroll in class program
    """ draws the current state of the game """
    
    offset = player[SCREENX] - xPos
    screen.blit(backgroundImage, (offset,0))  #Blitting background
    #for pl in plats:
    #    p = pl.move(offset,0)        
    #    draw.rect(screen,(111,111,111),p)
    screen.blit(player[SPRITE], (player[SCREENX], yPos))
        
    display.flip()

def moveGuy(guy, limit = 0): #Function taken and modified from the scroll in class program
    keys = key.get_pressed()
    global yPos
    global xPos
    if keys[K_LEFT] and xPos > 20:
        xPos -= 10
        if guy[SCREENX] > 50:
            guy[SCREENX] -= 10
    if keys[K_RIGHT] and xPos < 1800:
        xPos += 10
        if guy[SCREENX] < (900):
            guy[SCREENX] += 10
    if keys[K_SPACE] and guy[ONGROUND]:
        guy[YSPEED] = -10
        guy[ONGROUND] = False

    yPos += guy[YSPEED]     # add current speed to Y
    if yPos >= 450:
        yPos = 450
        guy[YSPEED] = 0
        guy[ONGROUND] = True
    guy[YSPEED]+=.7     # add current speed to Y

#defining level functions
def hub():
    drawScene(player, backgrounds[0])
    moveGuy(player, levelSizes[0])




#starting main game loop
while RUNNING:
    for evt in event.get():
        if evt.type == QUIT: 
            RUNNING = False
    hub()
    
    print(player)

    display.flip()







quit()
