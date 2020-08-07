'''
Notes:
- implement speed change
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
    (0,0): ([[0, 0, 0, 0], 
            [1, 1, 1, 1], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0]], (4, 1), (0, 1)),

    (0,1): ([[0, 0, 1, 0], 
            [0, 0, 1, 0], 
            [0, 0, 1, 0], 
            [0, 0, 1, 0]], (1, 4), (2, 0)),

    (0,2): ([[0, 0, 0, 0],
            [0, 0, 0, 0], 
            [1, 1, 1, 1],
            [0, 0, 0, 0]], (4, 1), (0, 2)),

    (0,3): ([[0, 1, 0, 0], 
            [0, 1, 0, 0], 
            [0, 1, 0, 0], 
            [0, 1, 0, 0]], (1, 4), (1, 0)),

    (1,0): ([[1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]], (3 ,2), (0, 0)),

    (1,1): ([[0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]], (2, 3), (1, 0)),

    (1,2): ([[0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]], (3, 2), (0, 1)),

    (1,3): ([[0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]], (2, 3), (0, 0)),

    (2,0): ([[0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]], (3, 2), (0, 0)),

    (2,1): ([[0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]], (2, 3), (1, 0)),

    (2,2): ([[0, 0, 0],
            [1, 1, 1],
            [1, 0, 0]], (3, 2), (0, 1)),

    (2,3): ([[1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]], (2, 3), (0, 0)),

    (3,0): ([[0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]], (3, 2), (0, 0)),

    (3,1): ([[0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]], (2, 3),(1, 0)),

    (3,2): ([[0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]], (3, 2), (0, 1)),

    (3,3): ([[0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]], (2, 3), (0, 0)),

    (4,0): ([[1, 1],
            [1, 1]], (2, 2), (0, 0)),

    (5,0): ([[0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]], (3, 2), (0, 0)),

    (5,1): ([[0, 1, 0],
            [0, 1, 1],
            [0, 0, 1]], (2, 3), (1, 0)),

    (5,2): ([[0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]], (3, 2), (0, 1)),

    (5,3): ([[1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]], (2, 3), (0, 0)),

    (6,0): ([[1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]], (3, 2), (0, 0)),

    (6,1): ([[0, 0, 1],
            [0, 1, 1],
            [0, 1, 0]], (2, 3), (1, 0)),

    (6,2): ([[0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]], (3, 2), (0, 1)),

    (6,3): ([[0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]], (2, 3), (0, 0))
}

wallKick= {
    (0, 1):[(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    (1, 0):[(0,0), (1,0), (1,-1), (0,2), (1,2)],
    (1, 2):[(0,0), (1,0), (1,-1), (0,2), (1,2)],
    (2, 1):[(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    (2, 3):[(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    (3, 2):[(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    (3, 0):[(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    (0, 3):[(0,0), (1,0), (1,1), (0,-2), (1,-2)]
}

wallKickLong= {
    (0, 1):[(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    (1, 0):[(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    (1, 2):[(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
    (2, 1):[(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    (2, 3):[(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    (3, 2):[(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    (3, 0):[(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    (0, 3):[(0,0), (-1,0), (2,0), (-1,2), (2,-1)]
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
    if(score>999999):
        score= 999999

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
                    # if(block.checkFloor()):
                    #     pygame.draw.rect(win, (255, 0, 0), (blockX, blockY, blockSize, blockSize), 5)
                    # else:
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
    temp.hbox= hitboxes[(block.blockType, block.rotPos)][0]
    temp.dims= hitboxes[(block.blockType, block.rotPos)][1]
    temp.displace= hitboxes[(block.blockType, block.rotPos)][2]

    if(keys[pygame.K_LEFT]):
        temp.x-=1
        if(not temp.checkCollide()):
            block.x-=1
    elif(keys[pygame.K_RIGHT]):
        temp.x+=1
        if(not temp.checkCollide()):
            block.x+=1

    #Testing
    # elif(keys[pygame.K_UP]):
    #     temp.y-=1
    #     if(not temp.checkCollide()):
    #         block.y-=1
    # elif(keys[pygame.K_DOWN]):
    #     temp.y+=1
    #     if(not temp.checkCollide()):
    #         block.y+=1

def checkEvent():
    global run
    temp= Block(None)
    temp.x= block.x
    temp.y= block.y
    temp.hbox= hitboxes[(block.blockType, block.rotPos)][0]
    temp.dims= hitboxes[(block.blockType, block.rotPos)][1]
    temp.displace= hitboxes[(block.blockType, block.rotPos)][2]

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run= False
        elif(event.type== pygame.KEYDOWN):
            if(event.key== pygame.K_DOWN):
                while(not block.checkFloor()):
                    block.y+=1
                block.set= True
                return True
            if(event.key== pygame.K_a):
                block.rotate(True)
                return False
            elif(event.key== pygame.K_s):
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
        self.hbox= hitboxes[(self.blockType, self.rotPos)][0]
        self.dims= hitboxes[(self.blockType, self.rotPos)][1]
        self.displace= hitboxes[(self.blockType, self.rotPos)][2]
        self.set= False
        self.x= 3
        self.y= 0
        global field

    def checkFloor(self):
        for x in range(len(self.hbox[0])):
            maxY= 0
            for y in range(len(self.hbox)):
                if(self.hbox[y][x]==1):
                    maxY= y
            if(self.y+maxY== 21):
                return True
            if(self.hbox[maxY][x]== 1 and field[self.y+maxY+1][self.x+x]==1):
                return True
        return False


    def rotate(self, ccw): #TODO wall kick
        lastRot= self.rotPos
        ogX= self.x
        ogY= self.y
        tempBool= True
        if(self.blockType!=4 and self.y!= 0):
            if(ccw):
                self.rotPos-=1
                if(self.rotPos<0):
                    self.rotPos= 3
            else: #ie clockwise
                self.rotPos+=1
                if(self.rotPos>3):
                    self.rotPos= 0
            self.hbox= hitboxes[(self.blockType, self.rotPos)][0]
            self.dims= hitboxes[(self.blockType, self.rotPos)][1]
            self.displace= hitboxes[(self.blockType, self.rotPos)][2]
            #Wall kick
            if(self.blockType== 0):
                for i in wallKickLong[(lastRot, self.rotPos)]:
                    self.x+= i[0]
                    self.y+= i[1]
                    if(not self.checkCollide()):
                        tempBool= False
                        break
                    self.x= ogX
                    self.y= ogY
                    
            else:
                for i in wallKick[(lastRot, self.rotPos)]:
                    self.x+= i[0]
                    self.y+= i[1]
                    if(not self.checkCollide()):
                        tempBool= False
                        break
                    self.x= ogX
                    self.y= ogY
            if(tempBool):
                self.rotPos= lastRot
                self.hbox= hitboxes[(self.blockType, self.rotPos)][0]
                self.dims= hitboxes[(self.blockType, self.rotPos)][1]
                self.displace= hitboxes[(self.blockType, self.rotPos)][2]


    def checkCollide(self):
        if((self.x+self.displace[0]+self.dims[0]-1>9 or self.x+self.displace[0]<0) or self.y+self.displace[1]+self.dims[1]-1>21):
            return True
        blockY= self.y 
        for y in self.hbox:
            blockX= self.x
            for x in y:
                if(x==1 and field[blockY][blockX]==1):
                    return True
                blockX+=1
            blockY+=1
        return False

block= Block(None)
last= block.blockType
nextBlock= Block(last)

while run:

    if(play):
        drawWin()
            
        if(block.set):
            block= nextBlock
            last= block.blockType
            nextBlock= Block(last)
        
        keys= pygame.key.get_pressed()

        if(setState):
            frameCount= 1500//t
            if(block.checkFloor()):
                if(frameCounter<frameCount):
                    frameCounter+=1
                    checkKeys(keys)
                    tempBool= checkEvent()
                    if(tempBool):
                        setBlock()
                        if(score== 999999):
                            play= False
                        if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
                            play= False
                        setState= False
                        continue
                else:
                    frameCounter= 0
                    block.set= True
                    setBlock()
                    if(score== 999999):
                        play= False
                    if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
                        play= False
                    setState= False
                    continue
            else:
                setState= False
                frameCounter= 0
                continue
        else:
            checkKeys(keys) 
            tempBool= checkEvent()
            if(tempBool):
                setBlock()
                if(score== 999999):
                    play= False
            if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
                play= False
            if(block.checkFloor()):
                setState= True
                continue
            block.y+=1
    else:
        drawEndScreen()
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False

    pygame.display.update()
    clock.tick(10)

#Testing
# field[19][2]= 1
# field[20][2]= 1
# field[20][3]= 1
# field[21][3]= 1

# block.blockType= 2
# block.rotPos= 3
# block.hbox= hitboxes[(block.blockType, block.rotPos)][0]
# block.dims= hitboxes[(block.blockType, block.rotPos)][1]
# block.displace= hitboxes[(block.blockType, block.rotPos)][2]

# while run:
#     drawWin()
#     keys= pygame.key.get_pressed()
#     checkKeys(keys)
#     checkEvent()
#     pygame.display.update()
#     clock.tick(20)

pygame.quit()
sys.exit()