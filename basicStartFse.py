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

zombieWidth, zombieHeight = 40, 60
skeletonWidth, skeletonHeight = 40, 60
batsWidth, batsHeight = 20, 20

RUNNING = True

#Loading images
playerSprite = image.load("coffee.jpg")
playerSprite = transform.scale(playerSprite, (20, 20))
backgroundImages = ["hubWorldBack.jpg"]
levelSizes = [(1820, 800)] #List of the sizes of each level to use to transform each image, and set limits to how far our character can go
backgrounds = []
for images in backgroundImages:
    backgrounds.append(image.load(images))
for b in range(len(backgrounds)):
    backgrounds[b] = transform.scale(backgrounds[b], levelSizes[b])



#Defining player variables

invincible = False
XPOS = 0
YPOS = 1
HURTBOX = 2
XSPEED = 3
YSPEED = 4
ONGROUND = 5
SCREENX = 6
HEALTH = 7
SPRITE = 8
ACTIVE = 2
player = [500, 780, Rect(500, 780, 20, 20), 0, 0, True, 500, 100, playerSprite]


#Defining basic functions
def drawScene(guy, backgroundImage, plats, platColours, blocks, blockColours, enemies): #Function taken and modified from the scroll in class program
    """ draws the current state of the game """
    
    offset = player[SCREENX] - guy[XPOS]
    screen.blit(backgroundImage, (offset - 110,0))  #Blitting background
    

    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,platColours,p)
    for bl in blocks:
        b = bl.move(offset,0)        
        draw.rect(screen,blockColours,b)

    spawnEnemies(enemies[0], enemies[1], enemies[2], enemies[3], enemies[4], enemies[5], offset)
    
    screen.blit(player[SPRITE], (player[SCREENX], guy[YPOS]))
    draw.rect(screen, GREEN, Rect(100, 50, guy[HEALTH], 20))
    draw.rect(screen, BLACK, Rect(100, 50, 100, 20), 1)

        
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

            if guy[SCREENX] > 110:
                guy[SCREENX] -= 10
        
    if keys[K_RIGHT] and guy[XPOS] < limit[0] - 220:

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
    
    
    

def checkCollide(guy,plats, blocks, enemies): #Function taken and modified from the scroll in class program
    
    guy[HURTBOX] = Rect(guy[XPOS], guy[YPOS], 20, 20)
    rec = guy[HURTBOX]
    for p in plats:
        if rec.colliderect(p):
            if guy[YSPEED] > 0 and rec.move(0, -guy[YSPEED]).colliderect(p) == False:
                guy[ONGROUND] = True
                guy[YSPEED] = 0
                guy[YPOS] = p.y - 19

    for enemy in enemies[0]:
        if enemies[3]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], skeletonWidth, skeletonHeight)) and invincible == False:
                player[HEALTH] -= 1
    for enemy in enemies[1]:
        if enemies[4]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], zombieWidth, zombieHeight)) and invincible == False:
                player[HEALTH] -= 3
    for enemy in enemies[2]:
        if enemies[5]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], batsWidth, batsHeight)) and invincible == False:
                player[HEALTH] -= 1

def spawnEnemies(positionsS, positionsZ, positionsB, skeletons, zombies, bats, offset):
    "Spawns in enemies for a given level at the specified positions"
    if skeletons:
        for p in positionsS:
            draw.rect(screen, WHITE, Rect(int(p[XPOS]) + offset, int(p[YPOS]), skeletonWidth, skeletonHeight)) #Change to blit the skeleton image
    if zombies:
        for p in positionsZ:
            draw.rect(screen, GREEN, Rect(int(p[XPOS]) + offset, int(p[YPOS]), zombieWidth, zombieHeight))
    if bats:
        for p in positionsB:
            draw.rect(screen, BLACK, Rect(int(p[XPOS]) + offset, int(p[YPOS]), batsWidth, batsHeight))                  
def enemiesAction(positionsS, positionsZ, positionsB, skeletons, zombies, bats, blocks):
    if zombies:
        for x in positionsZ:
            x[ACTIVE] = True
            if x[XPOS] > player[XPOS]:
                for b in blocks:
                    if x[XPOS] > b.right and player[XPOS] < b.right:
                        x[ACTIVE] = False
                if x[ACTIVE]:
                    x[XPOS] -= 0.7
            elif x[XPOS] < player[XPOS] and x[ACTIVE]:
                for b in blocks:
                    if x[XPOS] < b.left and player[XPOS] > b.left:
                        x[ACTIVE] = False
                if x[ACTIVE]:
                    x[XPOS] += 0.7
    if bats:
        for x in positionsB:
            x[ACTIVE] = False
            if player[XPOS] - 350 < x[XPOS] < player[XPOS] + 350 and player[YPOS] - 250 < x[YPOS] < player[YPOS] + 250:
                x[ACTIVE] = True
            if x[ACTIVE]:
                if player[XPOS] > x[XPOS]:
                    x[XPOS] += (randint(1, 15) / 4)
                elif player[XPOS] < x[XPOS]:
                    x[XPOS] -= (randint(1, 15) / 4)
                if player[YPOS] > x[YPOS]:
                    x[YPOS] += (randint(-3, 8) / 2)
                elif player[YPOS] < x[YPOS]:
                    x[YPOS] -= (randint(-3, 8) / 2)
    if zombies:
        for x in positionsS:
            if x[YPOS] + 300 > player[YPOS] > x[YPOS] - 300:
                print("Active skeleton")
                
    
#defining level functions
def hub():

    drawScene(player, backgrounds[0], hubPlats, (86,176,0), hubBlocks, (83, 49, 24), hubEnemies)
    moveGuy(player, levelSizes[0], hubBlocks)
    checkCollide(player, hubPlats, hubBlocks, hubEnemies)
    enemiesAction(hubEnemies[0], hubEnemies[1], hubEnemies[2], hubEnemies[3], hubEnemies[4], hubEnemies[5], hubBlocks)

    if player[YPOS] <= 10:
        print("Level: up")
    if player[XPOS] <= 20:
        print("Level: Left")
    if player[XPOS] >= 1600:
        print("Level: Right")


#defining level variables
hubPlats = [Rect(130, 700, 100, 10), Rect(530, 700, 100, 10), Rect(330, 550, 100, 10), Rect(130, 400, 100, 10), Rect(530, 400, 100, 10), Rect(970, 700, 100, 10), Rect(1370, 700, 100, 10), Rect(1170, 550, 100, 10), Rect(970, 400, 100, 10), Rect(1370, 400, 100, 10), Rect(750, 100, 100, 10)]
hubBlocks = [Rect(-110, 0, 210, 350), Rect(-110, 450, 210, 350), Rect(750, 250, 100, 600), Rect(1500, 0, 210, 350), Rect(1500, 450, 210, 350), Rect(0, 0, 750, 50), Rect(850, 0, 970, 50)]
hubEnemies = ([[300, 740, True]], [[1200, 740, True], [200, 740, True]], [[775, 200, True]], True, True, True)




#starting main game loop
while RUNNING:
    for evt in event.get():
        if evt.type == QUIT: 
            RUNNING = False
    hub()


    display.flip()







quit()
