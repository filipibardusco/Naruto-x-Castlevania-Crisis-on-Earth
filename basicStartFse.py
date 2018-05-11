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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

#Loading images
playerSprite = image.load("coffee.jpg")
playerSprite = transform.scale(playerSprite, (20, 20))
backgroundImages = ["hubWorldBack.jpg"]
levelSizes = [(2000, 800)] #List of the sizes of each level to use to transform each image, and set limits to how far our character can go
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
player = [Rect(20, 780, 20, 20), 0, 0, True, 20, 100, playerSprite, 20, 780]


#Defining basic functions
def drawScene(guy, backgroundImage, plats, platColours): #Function taken and modified from the scroll in class program
    """ draws the current state of the game """
    
    offset = player[SCREENX] - guy[XPOS]
    screen.blit(backgroundImage, (offset,0))  #Blitting background
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,platColours,p)
    screen.blit(player[SPRITE], (player[SCREENX], guy[YPOS]))
        
    display.flip()

def moveGuy(guy, limit): #Function taken and modified from the scroll in class program
    keys = key.get_pressed()
    if keys[K_LEFT] and guy[XPOS] > 20:
        guy[XPOS] -= 10
        if guy[SCREENX] > 0:
            guy[SCREENX] -= 10
    if keys[K_RIGHT] and guy[XPOS] < 1800:
        guy[XPOS] += 10
        if guy[SCREENX] < (900):
            guy[SCREENX] += 10
    if keys[K_SPACE] and guy[ONGROUND] and guy[YSPEED] <= 0.7:
        guy[YSPEED] = -30
        guy[ONGROUND] = False

    guy[YPOS] += guy[YSPEED]     # add current speed to Y
    if guy[YPOS] >= 780:
        guy[YPOS] = 780
        guy[YSPEED] = 0
        guy[ONGROUND] = True
    guy[YSPEED]+=.7     # add current speed to Y
    guy[HURTBOX] = Rect(guy[XPOS], guy[YPOS], 20, 20)
    

def checkCollide(guy,plats): #Function taken and modified from the scroll in class program
    
    guy[HURTBOX] = Rect(guy[XPOS], guy[YPOS], 20, 20)
    rec = guy[HURTBOX]
    for p in plats:
        if rec.colliderect(p):
            print("yes")
            if guy[YSPEED] > 0 and rec.move(0, -guy[YSPEED]).colliderect(p) == False:
                guy[ONGROUND] = True
                guy[YSPEED] = 0
                guy[YPOS] = p.y - 19
        
        

#defining level functions
def hub():
    drawScene(player, backgrounds[0], hubPlats, GREEN)
    moveGuy(player, levelSizes[0])
    checkCollide(player, hubPlats)
    

#defining level variables
hubPlats = [Rect(220,750,60,10),Rect(310,450,60,10)]





#starting main game loop
while RUNNING:
    for evt in event.get():
        if evt.type == QUIT: 
            RUNNING = False
    hub()
    
    print(player[0], player[ONGROUND])

    display.flip()







quit()
