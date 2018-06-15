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
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Enemy property variables
zombieWidth, zombieHeight = 40, 60
skeletonWidth, skeletonHeight = 40, 60
batsWidth, batsHeight = 20, 20

RUNNING = True

#Loading images
playerSprite = image.load("coffee.jpg") #player sprite (MUST BE CHANGED)
playerSprite = transform.scale(playerSprite, (20, 20))
backgroundImages = ["hubWorldBack.jpg", "levelUp.jpg"] #List of level backgrounds
levelSizes = [(1820, 800), (4000, 800)] #List of the sizes of each level to use to transform each image, and set limits to how far our character can go
backgrounds = []
for images in backgroundImages:
    backgrounds.append(image.load(images)) #placing background images in a list
for b in range(len(backgrounds)):
    backgrounds[b] = transform.scale(backgrounds[b], levelSizes[b]) #Making each background image match the size of it's respective level



#Defining player and enemy constants

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
PROJECTILES = 3
VULNERABLE = 5
PLAYERHEIGHT = 20

#Tha main player list
player = [500, SIZE[1] - PLAYERHEIGHT, Rect(500, SIZE[1] - PLAYERHEIGHT, 20, 20), 0, 0, True, 500, 100, playerSprite]

#Defining other miscellaneous variables:
attack = False
whipping = 0
myClock = time.Clock()
moving = 0
cooldown = 0

up = False #Variables used to determine which level to use
left = False
right = False

skeletonActivation = False #variables used to activate enemies on all levels upon clearing their espective levels
zombieActivation = False
batActivation = False

#Defining basic functions
def drawScene(guy, backgroundImage, plats, platColours, blocks, blockColours, enemies): #Function taken and modified from the scroll in class program
    """ draws the current state of the game """
    
    global offset
    offset = player[SCREENX] - player[XPOS]#Creating an offset for scrolling
    screen.blit(backgroundImage, (offset - 110,0))  #Blitting background

    #Drawing platforms and blocks
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,platColours,p)
    for bl in blocks:
        b = bl.move(offset,0)        
        draw.rect(screen,blockColours,b)
    #Doing enemy things
    spawnEnemies(enemies[0], enemies[1], enemies[2], enemies[3], enemies[4], enemies[5])
    enemiesAction(enemies[0], enemies[1], enemies[2], enemies[3], enemies[4], enemies[5], blocks)
    
    screen.blit(player[SPRITE], (player[SCREENX], guy[YPOS])) #drawing the player
    #drawing health bar
    if guy[HEALTH] >= 60:
        draw.rect(screen, GREEN, Rect(100, 50, guy[HEALTH], 20))
    elif guy[HEALTH] >= 30:
        draw.rect(screen, YELLOW, Rect(100, 50, guy[HEALTH], 20))
    elif guy[HEALTH] >= 0:
        draw.rect(screen, RED, Rect(100, 50, guy[HEALTH], 20))
    draw.rect(screen, BLACK, Rect(100, 50, 100, 20), 1)
        
    display.flip()

def moveGuy(guy, limit, blocks): #Function taken and modified from the scroll in class program
    'Function made for moving the player, but not through blocks or past the limits of the level'
    keys = key.get_pressed()
    global attack
    global moving
    global cooldown
    for b in blocks: #Preventing movement of player through blocks
        if guy[HURTBOX].move(0, -guy[YSPEED]).colliderect(Rect(b.left, b.top - 1, b.right - b.left, 1)): #Creating floor for blocks
            guy[ONGROUND] = True
            guy[YSPEED] = 0
            guy[YPOS] = b.y - PLAYERHEIGHT
    #making the player jump upon pressing space
    if keys[K_SPACE] and guy[ONGROUND] and guy[YSPEED] <= 0.7:
        print("entered")
        guy[YSPEED] = -15
        guy[ONGROUND] = False
    
    blockedUp = False #setting the player to have no roof above him as a default
    for b in blocks:
        if guy[HURTBOX].colliderect(Rect(b.left, b.bottom + 1, b.right - b.left, 1)):
            blockedUp = True #Creating ceiling for blocks
    if blockedUp: #making the player move downwards if there is a ceiling above them
        guy[YSPEED] = 1.4
    guy[YPOS] += guy[YSPEED]     # add current speed to Y
    if guy[YPOS] >= limit[1] - PLAYERHEIGHT: #preventing the player from moving past the bottom of the screen
        guy[YPOS] = limit[1] - PLAYERHEIGHT
        guy[YSPEED] = 0
        guy[ONGROUND] = True
    guy[YSPEED] += .7     # add current speed to Y
    
    if attack and -1.5 <= player[YSPEED] <= 1.5: #preventing the player from moving if they are groundedand attacking
        return "attacking"
    
    if keys[K_LEFT] and guy[XPOS] > 20:
        moving = -1 #Variable used to store direction moved last for attack direction
        freeLeft = True
        for b in blocks:#checking for blocks to make sure the player doesn't phase through them
            if guy[HURTBOX].colliderect(Rect(b.right, b.top, 1, (b.bottom - b.top))):
                freeLeft = False
        if freeLeft: #Moving the player leftwards
            guy[XPOS] -= 10
            if guy[SCREENX] > 110:
                guy[SCREENX] -= 10
    if keys[K_RIGHT] and guy[XPOS] < limit[0] - 220:
        moving = 1 #Variable used to store direction moved last for attack direction
        freeRight = True
        for b in blocks: #checking for blocks to make sure the player doesn't phase through them
            if guy[HURTBOX].colliderect(Rect(b.left - 1, b.top, 1, (b.bottom - b.top))):
                freeRight = False
        if freeRight: #Moving the player rightward
            guy[XPOS] += 10
            if guy[SCREENX] < 990:
                guy[SCREENX] += 10
    
    if keys[K_z] and cooldown <= 0: #Activating player's attack
        attack = True
    cooldown -= 1
    
    

def checkCollide(guy,plats, blocks, enemies): #Function taken and modified from the scroll in class program
    'Checking collisions mainy for blocks, platforms, and enemies'
    global attack
    guy[HURTBOX] = Rect(guy[XPOS], guy[YPOS], 20, PLAYERHEIGHT)
    rec = guy[HURTBOX]
    for p in plats:
        if rec.colliderect(p):
            if guy[YSPEED] > 0 and rec.move(0, -guy[YSPEED]).colliderect(p) == False:
                guy[ONGROUND] = True
                guy[YSPEED] = 0
                guy[YPOS] = p.y - PLAYERHEIGHT
    #Removing health from the player upon touching enemies
    for enemy in enemies[0]:
        if enemies[3]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], skeletonWidth, skeletonHeight)):
                player[HEALTH] -= 1
    for enemy in enemies[1]:
        if enemies[4]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], zombieWidth, zombieHeight)):
                player[HEALTH] -= 3
    for enemy in enemies[2]:
        if enemies[5]:
            if rec.colliderect(Rect(enemy[XPOS], enemy[YPOS], batsWidth, batsHeight)):
                player[HEALTH] -= 1
    #checking for attacking enemies
    if attack:
        whipAttack(enemies)

def spawnEnemies(positionsS, positionsZ, positionsB, skeletons, zombies, bats):
    "Spawns in enemies for a given level at the specified positions"
    global offset
    #Only drawing enemies if they are activated in a level
    if skeletons:
        for p in positionsS:
            draw.rect(screen, WHITE, Rect(int(p[XPOS]) + offset, int(p[YPOS]), skeletonWidth, skeletonHeight)) #CHANGE TO SKELETON IMAGE
    if zombies:
        for p in positionsZ:
            draw.rect(screen, GREEN, Rect(int(p[XPOS]) + offset, int(p[YPOS]), zombieWidth, zombieHeight)) #CHANGE TO ZOMBIE IMAGE
    if bats:
        for p in positionsB:
            draw.rect(screen, BLACK, Rect(int(p[XPOS]) + offset, int(p[YPOS]), batsWidth, batsHeight))  #CHANGE TO BAT IMAGE
def enemiesAction(positionsS, positionsZ, positionsB, skeletons, zombies, bats, blocks):
    'Moving all enemies and making them do their appropriate attacks'
    global offset
    if zombies: #only doing the zombies actions if zombies are activated
        for x in positionsZ:
            x[ACTIVE] = True #making the zombie active by default
            #Moving the zombie slowly towards the player only if there are no blocks in the way
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
                    
    if bats: #only doing the bats actions if bats are activated
        for x in positionsB:
            x[ACTIVE] = False #making the bats inactive by default
            if player[XPOS] - 350 < x[XPOS] < player[XPOS] + 350 and player[YPOS] - 300 < x[YPOS] < player[YPOS] + 300:
                x[ACTIVE] = True #Making the bat active only if they're close enough to the player
            if x[ACTIVE]:
                #Making the bats move towards the player. Random variables used to emulate more sporadic motion, like flapping bats, but favouing advancement towards the player
                if player[XPOS] > x[XPOS]:
                    x[XPOS] += (randint(1, 15) / 4)
                elif player[XPOS] < x[XPOS]:
                    x[XPOS] -= (randint(1, 15) / 4)
                if player[YPOS] > x[YPOS]:
                    x[YPOS] += (randint(-3, 8) / 2)
                elif player[YPOS] < x[YPOS]:
                    x[YPOS] -= (randint(-3, 8) / 2)
                #firing a projectile occasionally
                if randint(0, 60) == 1:
                    #Making the projectile travel the appropriate direction
                    if player[XPOS] > x[XPOS]:
                        fireDirection = 1
                    else:
                        fireDirection = -1
                    
                    x[PROJECTILES].append([x[XPOS], x[YPOS], 10, 10, fireDirection])

            for fball in x[PROJECTILES]: #moving fireball projectiles
                fireball = Rect(fball[0] + offset, fball[1], fball[2], fball[3])
                draw.rect(screen, RED, fireball) #CHANGE TO FIREBALL IMAGE
                fball[0] += fball[4] * 5 #Moving the x position of the fireball in the appropriate diection
                #Checking collisions of fireballs with player
                if player[HURTBOX].colliderect(Rect(fball[0], fball[1], fball[2], fball[3])):
                    player[HEALTH] -= 15 #Lowering player health in accordance to them being hit
                    x[PROJECTILES].pop(x[PROJECTILES].index(fball)) #destroying the projectile
    if skeletons: #only doing the skeletons actions if skeletons are activated
        for x in positionsS:
            x[ACTIVE] = False #making the skeletons inactive by default
            #Making the skeletons throw bones if they are close enough to the player
            if x[YPOS] + 200 > player[YPOS] > x[YPOS] - 200 and x[XPOS] + 1100 > player[XPOS] > x[XPOS] - 1100:
                x[ACTIVE] = True
                if randint(0, 60) == 1:
                    if player[XPOS] > x[XPOS]: #throwing bone in appropriate direction
                        boneDirection = 1
                    else:
                        boneDirection = -1
                    x[PROJECTILES].append([x[XPOS], x[YPOS], 20, 20, boneDirection])
        
            for bones in x[PROJECTILES]:
                bone = Rect(bones[0] + offset, bones[1], bones[2], bones[3])
                draw.rect(screen, WHITE, bone) #CHANGE TO PICTURE OF BONE
                bones[0] += bones[4] * 5 #Changing the x position of the bone in accordance to the direction thrown
                #Checking collisions of fireballs with player
                if player[HURTBOX].colliderect(Rect(bones[0], bones[1], bones[2], bones[3])):
                    player[HEALTH] -= 10 #Lowering player health in accordance to them being hit
                    x[PROJECTILES].pop(x[PROJECTILES].index(bones)) #Removing bone on hit
def whipAttack(enemies):
    'Making an attack that will hit enemies'
    #declaring necessary global variables
    global offset
    global whipping
    global attack
    global moving
    global cooldown
    
    if moving == -1: #checking if player last moved o the left or right and placing the whip hitbox appropriately
        whip = (player[XPOS] - 60, player[YPOS] + 10, 60, 30)
    else:
        whip = (player[XPOS] + 40, player[YPOS] + 10, 60, 30)
    draw.rect(screen, BLACK, Rect(whip[0] + offset, whip[1], whip[2], whip[3])) #Drawing the whip (to be changed with a picture)
    whipping += 1 #adding a counter to stop the whip from attacking after 20 frames
    hitbox = Rect(whip[0], whip[1], whip[2], whip[3]) #turning the whip into a rect object
    for enemyType in enemies[0:3]: #checking collisions with all enemies
        for enemy in enemyType:
            if enemyType in enemies[2]:
                if hitbox.colliderect(Rect(enemy[XPOS], enemy[YPOS], 20, 20)):
                    enemyType.pop(enemyType.index(enemy))
            else:
                if hitbox.colliderect(Rect(enemy[XPOS], enemy[YPOS], 40, 60)) and enemy[VULNERABLE]:
                    enemy[4] -= 1
                    enemy[VULNERABLE] = False #making sure enemies don't get hit on every frame the attack is active
                if enemy[4] <= 0:
                    enemyType.pop(enemyType.index(enemy))
            for projectiles in enemy[PROJECTILES]: #checking collisions with projectiles
                if hitbox.colliderect(Rect(projectiles[0], projectiles[1], projectiles[2], projectiles[3])):
                    enemy[PROJECTILES].pop(enemy[PROJECTILES].index(projectiles))
    if whipping >= 10: #stopping the whip attack after 10 frames
        for enemyType in enemies[0:3]:
            for enemy in enemyType:
                enemy[VULNERABLE] = True #making all enemies vunerable to the next attack
        whipping = 0
        cooldown = 10 #preventing the player from always having the whip active
        attack = False #stop the player from entering this loop until the next press of the attack button
#defining level functions
def hub():
    'Creating a hub world for the player to enter other levels from'
    #declaring necesarry global variables
    global up
    global left
    global right

    #Checking to see if a character has entered a portal
    if player[YPOS] <= 10:
        up = True
    elif player[XPOS] <= 20:
        left = True
    elif player[XPOS] >= 1600:
        right = True

    #doing basic level functions
    drawScene(player, backgrounds[0], hubPlats, (86,176,0), hubBlocks, (83, 49, 24), hubEnemies)
    moveGuy(player, levelSizes[0], hubBlocks)
    checkCollide(player, hubPlats, hubBlocks, hubEnemies)
def levelUp():
    'creating the level that is accesed through the top portal in the hub world'
    #declaring necessary global variables
    global batActivation
    global skeletonActivation
    global zombieActivation
    global up
    global offset
    global hubEnemies
    
    #clearing basic level functions
    drawScene(player, backgrounds[1], upPlats, (86,176,0), upBlocks, (83, 49, 24), upEnemies)
    moveGuy(player, levelSizes[1], upBlocks)
    checkCollide(player, upPlats, upBlocks, upEnemies)
    
    if player[XPOS] >= 3700: #checking if player has cleared the level
        #resetting player health and position, as well as sending them back to hub 
        player[SCREENX] = 500
        player[XPOS] = 500
        player[HEALTH] = 100
        up = False
        batActivation = True #Activating bats on all levels post clearance of bat level
        skeletonActivation = True #REMOVE IN FINAL VERSION, PLACE IN APPROAPRITE LEVEL
        zombieActivation = True #REMOVE IN FINAL VERSION, PLACE IN APPROAPRITE LEVEL

        #refreshing all level's enemies
        upEnemies = [[[100, 740, True, [], 2, True], [300, 740, True, [], 2, True], [400, 740, True, [], 2, True], [600, 740, True, [], 2, True]], [[1200, 740, True, [], 3, True], [1350, 740, True, [], 3, True], [1400, 740, True, [], 3, True], [1600, 740, True, [], 3, True], [1500, 740, True, [], 3, True]], [[500, 200, True, [], 1, True], [1000, 200, True, [], 1, True], [1200, 200, True, [], 1, True], [1700, 710, True, [], 1, True], [1750, 710, True, [], 1, True], [1800, 710, True, [], 1, True], [1850, 710, True, [], 1, True], [1900, 710, True, [], 1, True], [1950, 710, True, [], 1, True], [2500, 500, True, [], 1, True], [2530, 500, True, [], 1, True], [2560, 500, True, [], 1, True], [2590, 500, True, [], 1, True], [2620, 500, True, [], 1, True], [2650, 500, True, [], 1, True], [2680, 500, True, [], 1, True], [2710, 500, True, [], 1, True], [2740, 500, True, [], 1, True], [1770, 500, True, [], 1, True]], skeletonActivation, zombieActivation, True]
        hubEnemies = ([[300, 740, True, [], 2, True]], [[1200, 740, True, [], 3, True]], [[775, 200, True, [], 1, True]], True, True, True)
#defining level variables
hubPlats = [Rect(130, 700, 100, 10), Rect(530, 700, 100, 10), Rect(330, 550, 100, 10), Rect(130, 400, 100, 10), Rect(530, 400, 100, 10), Rect(970, 700, 100, 10), Rect(1370, 700, 100, 10), Rect(1170, 550, 100, 10), Rect(970, 400, 100, 10), Rect(1370, 400, 100, 10), Rect(750, 100, 100, 10)]
hubBlocks = [Rect(-110, 0, 210, 350), Rect(-110, 450, 210, 350), Rect(750, 250, 100, 600), Rect(1500, 0, 210, 350), Rect(1500, 450, 210, 350), Rect(0, 0, 750, 50), Rect(850, 0, 970, 50)]
hubEnemies = ([[300, 740, True, [], 2, True]], [[1200, 740, True, [], 3, True]], [[775, 200, True, [], 1, True]], True, True, True)
upPlats = [Rect(630, 400, 100, 10), Rect(630, 550, 100, 10), Rect(10, 700, 700, 10), Rect(1400, 100, 200, 10), Rect(1600, 250, 100, 10), Rect(1500, 400, 350, 10)]
upBlocks = [Rect(750, 250, 100, 600), Rect(2000, 150, 250, 700), Rect(1200, 150, 20, 20), Rect(1700, 600, 300, 75), Rect(1700, -400, 50, 700), Rect(1000, 500, 100, 10), Rect(1000, 600, 100, 10), Rect(1000, 700, 100, 10), Rect(1000, 300, 100, 10), Rect(1000, 400, 100, 10), Rect(1800, 250, 20, 20), Rect(3600, 0, 800, 600), Rect(2500, 0, 300, 500)]
upEnemies = [[[100, 740, True, [], 2, True], [300, 740, True, [], 2, True], [400, 740, True, [], 2, True], [600, 740, True, [], 2, True]], [[1200, 740, True, [], 3, True], [1350, 740, True, [], 3, True], [1400, 740, True, [], 3, True], [1600, 740, True, [], 3, True], [1500, 740, True, [], 3, True]], [[500, 200, True, [], 1, True], [1000, 200, True, [], 1, True], [1200, 200, True, [], 1, True], [1700, 710, True, [], 1, True], [1750, 710, True, [], 1, True], [1800, 710, True, [], 1, True], [1850, 710, True, [], 1, True], [1900, 710, True, [], 1, True], [1950, 710, True, [], 1, True], [2500, 500, True, [], 1, True], [2530, 500, True, [], 1, True], [2560, 500, True, [], 1, True], [2590, 500, True, [], 1, True], [2620, 500, True, [], 1, True], [2650, 500, True, [], 1, True], [2680, 500, True, [], 1, True], [2710, 500, True, [], 1, True], [2740, 500, True, [], 1, True], [1770, 500, True, [], 1, True]], skeletonActivation, zombieActivation, True]



#starting main game loop
while RUNNING:
    for evt in event.get():
        if evt.type == QUIT: 
            RUNNING = False
    #Updating enemies lists to make sure that the appropriate enemies are present when necessary
    upEnemies[3] = skeletonActivation
    upEnemies[4] = zombieActivation

    #Checking to see if the player has entered a portal to a level
    if up:
        levelUp()
    elif left:
        print("left")
    elif right:
        print("right")
    else:
        hub()
    myClock.tick(60)
    display.flip()

quit()
