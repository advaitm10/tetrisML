'''
Notes:
- Collision errors occur because the temp block is not calling the same hitbox as the current block,
  this occurs because a block may have a rotated hitbox, but the temp block calls a non rotated hitbox from the dict
- REWORKING ROT SYSTEM CHECK THAT ALL FUNCTIONS WORK
- Need to change levelling speeds
- Consider adding different colors to the blocks
'''

blockSize= 20

import random
import pygame
import sys
pygame.init()
win=pygame.display.set_mode((blockSize*10+20, blockSize*20+40))
clock= pygame.time.Clock()

score= 0
level= 0
lines= 0
field= [[0]*10 for _ in range(22)]

run= True
play= True
setState= False
t= 48
frameCounter= 0
font= pygame.font.SysFont('arial', 15)


hitboxes= {
    '(0,0)': [[0, 0, 0, 0], 
              [1, 1, 1, 1], 
              [0, 0, 0, 0], 
              [0, 0, 0, 0]]

    '(0,1)': [[0, 0, 1, 0], 
              [0, 0, 1, 0], 
              [0, 0, 1, 0], 
              [0, 0, 1, 0]]

    '(0,2)': [[0, 0, 0, 0],
              [0, 0, 0, 0], 
              [1, 1, 1, 1],
              [0, 0, 0, 0]]

    '(0,3)': [[0, 1, 0, 0], 
              [0, 1, 0, 0], 
              [0, 1, 0, 0], 
              [0, 1, 0, 0]]

    '(1,0)': [[1, 0, 0],
              [1, 1, 1],
              [0, 0, 0]]

    '(1,1)': [[0, 1, 1],
              [0, 1, 0],
              [0, 1, 0]]

    '(1,2)': [[0, 0, 0],
              [1, 1, 1],
              [0, 0, 1]]

    '(1,3)': [[0, 1, 0],
              [0, 1, 0],
              [1, 1, 0]]

    '(2,0)': [[0, 0, 1],
              [1, 1, 1],
              [0, 0, 0]]

    '(2,1)': [[0, 1, 0],
              [0, 1, 0],
              [0, 1, 1]]

    '(2,2)': [[0, 0, 0],
              [1, 1, 1],
              [1, 0, 0]]

    '(2,3)': [[1, 1, 0],
              [0, 1, 0],
              [0, 1, 0]]

    '(3,0)': [[0, 1, 0],
              [1, 1, 1],
              [0, 0, 0]]

    '(3,1)': [[0, 1, 0],
              [0, 1, 1],
              [0, 1, 0]]

    '(3,2)': [[0, 0, 0],
              [1, 1, 1],
              [0, 1, 0]]

    '(3,3)': [[0, 1, 0],
              [1, 1, 0],
              [0, 1, 0]]

    '(4,0)': [[1, 1],
              [1, 1]]

    '(5,0)': [[0, 1, 1],
              [1, 1, 0],
              [0, 0, 0]]

    '(5,1)': [[0, 1, 0],
              [0, 1, 1],
              [0, 0, 1]]

    '(5,2)': [[0, 0, 0],
              [0, 1, 1],
              [1, 1, 0]]

    '(5,3)': [[1, 0, 0],
              [1, 1, 0],
              [0, 1, 0]]

    '(6,0)': [[1, 1, 0],
              [0, 1, 1],
              [0, 0, 0]]

    '(6,1)': [[0, 0, 1],
              [0, 1, 1],
              [0, 1, 0]]

    '(6,2)': [[0, 0, 0],
              [1, 1, 0],
              [0, 1, 1]]

    '(6,3)': [[0, 1, 0],
              [1, 1, 0],
              [1, 0, 0]]
}

def setSpeed(): 
    global t
    if(level>=29):
        t= 1
    elif(level>=19):
        t= 2
    elif(level>=16):
        t= 3
    elif(level>=13):
        t= 4
    elif(level>=10):
        t= 5
    elif(level==9):
        t= 6
    elif(level==8):
        t= 8
    elif(level==7):
        t= 13
    elif(level==6):
        t= 18
    elif(level==5):
        t= 23
    elif(level==4):
        t= 28
    elif(level==3):
        t= 33
    elif(level==2):
        t= 38
    elif(level==1):
        t= 43

def blockTypeInit(last): 
    if(last==None):
        return random.randint(0,6)
    else:
        temp= random.randint(0, 7)
        if(temp==7 or temp==last):
            return random.randint(0, 6)
        return temp

def clear(): 
    global field
    global score
    global lines
    global level
    global t
    lineCount= 0
    lineNums= []
    for i in range(len(field)):
        if(field[i].count(1)==10):
            lineCount+=1
            lineNums.append(i)
        if(lineCount==4):
            break

    for i in range(len(lineNums)):
        field.pop(lineNums[0])

    for i in range(lineCount):
        field.insert(0, [0]*10)

    lines+=lineCount
    level= lines//10
    setSpeed()

    if(lineCount==1):
        score+= 40* (level+1)
    elif(lineCount==2):
        score+= 100* (level+1)
    elif(lineCount==3):
        score+= 300* (level+1)
    elif(lineCount==4):
        score+= 1200* (level+1)

def drawWin():
    win.fill((0, 0, 0))
    tempY= 40
    for y in range(2, len(field)):
        tempX= 10
        if(field[y].count(1)==0):
            tempY+=blockSize
            continue
        for x in field[y]:
            if(x==1):
                win.fill((255, 255, 255), (tempX, tempY, blockSize, blockSize))
                pygame.draw.rect(win, (0, 0, 255), (tempX, tempY, blockSize, blockSize), 5)
            tempX+=blockSize
        tempY+=blockSize

    pygame.draw.rect(win, (255, 255, 255), (10, 40, blockSize*10, blockSize*20), 2)
    
    blockY= 40+(block.y-2)*blockSize
    if(block.y>1):
        for y in range(len(block.hbox)):
            blockX= 10+(block.x)*blockSize
            if(block.hbox[y].count(1)==0):
                blockY+=blockSize
                continue
            for x in block.hbox[y]:
                if(x==1):
                    win.fill((255, 255, 255), (blockX, blockY, blockSize, blockSize))
                    if(block.checkCollide()):
                        pygame.draw.rect(win, (255, 0, 0), (blockX, blockY, blockSize, blockSize), 5)
                    else:
                        pygame.draw.rect(win, (0, 0, 255), (blockX, blockY, blockSize, blockSize), 5)
                blockX+=blockSize
            blockY+=blockSize

    text= font.render('Score: '+ str(score), 1, (255, 255, 255))
    win.blit(text, (10, 0))
    text= font.render('Level: '+ str(level), 1, (255, 255, 255))
    win.blit(text, (10, 15))

def drawEndScreen():
    win.fill((0, 0, 0))
    text= font.render('Score: '+ str(score), 1, (255, 255, 255))
    win.blit(text, (10, 0))
    text= font.render('Level: '+ str(level), 1, (255, 255, 255))
    win.blit(text, (10, 15))

def checkKeys(keys):
    temp= Block(None)
    temp.x= block.x
    temp.y= block.y
    temp.hbox= hitboxes[str(block.blockType)]

    if(keys[pygame.K_LEFT]):
        if(not block.checkSide(True)):
            temp.x-=1
            if(not temp.checkCollide()):
                block.x-=1
    elif(keys[pygame.K_RIGHT]):
        if(not block.checkSide(False)):
            temp.x+=1
            if(not temp.checkCollide()):
                block.x+=1

    #Testing
    elif(keys[pygame.K_UP]):
        temp.y-=1
        if(not temp.checkCollide()):
            block.y-=1
    elif(keys[pygame.K_DOWN]):
        temp.y+=1
        if(not temp.checkCollide()):
            block.y+=1

def checkEvent():
    global run
    temp= Block(None)
    temp.x= block.x
    temp.y= block.y
    temp.hbox= hitboxes[str(block.blockType)]

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run= False
        elif(event.type== pygame.KEYDOWN):
            # if(event.key== pygame.K_DOWN):
            #     while(not block.checkFloor()):
            #         block.y+=1
            #     block.set= True
            #     return True
            if(event.key== pygame.K_a):
                temp.rotate(True)
                if(not temp.checkCollide()):
                    block.rotate(True)
                return False
            elif(event.key== pygame.K_s):
                temp.rotate(False)
                if(not temp.checkCollide()):
                    block.rotate(False)
                return False

def setBlock():
    global field
    blockY= block.y
    for y in block.hbox:
        blockX= block.x
        for x in y:
            if(x==1):
                field[blockY][blockX]= 1
            blockX+=1
        blockY+=1
    clear()

class Block:
    def __init__(self, last):
        self.blockType= blockTypeInit(last)
        self.rotPos= 0
        self.hbox= hitboxes[str((self.blockType, self.rotPos))]
        self.set= False
        self.x= 3
        self.y= 0
        self.rotCoords= (None, None)
        global field

    def checkFloor(self): #TODO
        floorY= self.y+len(self.hbox)-1
        if(floorY== 21):
            return True
        blockX= 0
        for x in range(self.x, self.x+len(self.hbox[0])):
            if(self.hbox[-1][blockX]==1 and field[floorY+1][x]): #ERROR
                return True
            blockX+=1
        return False

    def rotate(self, ccw): #TODO rot coord system
        if(self.blockType!=4 and (self.y!= 0)):
            if(ccw):
                self.rotPos-=1
                if(self.rotPos<0):
                    self.rotPos= 3
            else: #ie clockwise
                self.rotPos+=1
                if(self.rotPos>3):
                    self.rotPos= 0
            self.hbox= hitboxes[str((self.blockType, self.rotPos))]

    def checkCollide(self):
        blockY= self.y 
        for y in self.hbox:
            blockX= self.x
            for x in y:
                if(field[blockY][blockX]==1 and x==1): #ERROR
                    return True
                blockX+=1
            blockY+=1
        return False
    
    def checkSide(self, left): #TODO
        if(left):
        else:

block= Block(None)
last= block.blockType
nextBlock= Block(last)

# while run:

#     if(play):
#         drawWin()
            
#         if(block.set):
#             block= nextBlock
#             last= block.blockType
#             nextBlock= Block(last)
        
#         keys= pygame.key.get_pressed()

#         if(setState):
#             frameCount= 1500//t
#             if(block.checkFloor()):
#                 if(frameCounter<frameCount):
#                     frameCounter+=1
#                     checkKeys(keys)
#                     tempBool= checkEvent()
#                     if(tempBool):
#                         setBlock()
#                         if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
#                             play= False
#                         setState= False
#                         continue
#                 else:
#                     frameCounter= 0
#                     block.set= True
#                     setBlock()
#                     if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
#                         play= False
#                     setState= False
#                     continue
#             else:
#                 setState= False
#                 frameCounter= 0
#                 continue
#         else:
#             if(block.checkFloor()):
#                 setState= True
#                 continue
#             else:
#                 checkKeys(keys)
#                 tempBool= checkEvent()
#                 if(tempBool):
#                     setBlock()
#                 if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
#                     play= False
#                 block.y+=1
#     else:
#         drawEndScreen()

#     pygame.display.update()
#     clock.tick(10)

#Testing
field[9][5]= 1
field[10][5]= 1
field[9][4]= 1
field[10][4]= 1

block.blockType= 0
block.hbox= hitboxes[str(0)]

while run:
    drawWin()
    keys= pygame.key.get_pressed()
    checkKeys(keys)
    checkEvent()
    pygame.display.update()
    clock.tick(20)

pygame.quit()
sys.exit()