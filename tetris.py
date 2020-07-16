import random
import pygame
import time 
pygame.init()
win=pygame.display.set_mode((420, 840))
clock= pygame.time.Clock()

score= 0
level= 0
lines= 0
field= [[1]*10 for _ in range(22)]


run= True
play= True
setState= False
t= 48
frameCounter= 0
font= pygame.font.SysFont('arial', 30)


hitboxes= {
    '0':[[1, 1, 1, 1]],
    '1':[[0, 1, 0], [1, 1, 1]],
    '2':[[0, 1, 1], [1, 1, 0]],
    '3':[[1, 1, 0], [0, 1, 1]],
    '4':[[1, 1], [1, 1]],
    '5':[[0, 0, 1], [1, 1, 1]],
    '6':[[1, 0, 0], [1, 1, 1]],
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
    tempY= 40
    for y in range(len(field)):
        tempX= 10
        for x in field[y]:
            if(x==1):
                win.fill((255, 255, 255), (tempX, tempY, 40, 40))
                pygame.draw.rect(win, (0, 0, 255), (tempX, tempY, 40, 40), 5)
            tempX+=40
        tempY+=40
    pygame.draw.rect(win, (255, 255, 255), (10, 40, 400, 800), 2)
    text= font.render('Score: '+ str(score)+ '\nLevel: '+ str(level), 1, (255, 255, 255))
    blockY= 40+block.y*20
    for y in range(len(block.hbox)):
        blockX= 10+block.x*20
        for x in block.hbox[y]:
            win.fill((255, 255, 255), (tempX, tempY, 40, 40))
            pygame.draw.rect(win, (0, 0, 255), (tempX, tempY, 40, 40), 5)
            blockX+=40
        blockY+=40

    win.blit(text, (0, 0))

def drawEndScreen():
    text= font.render('Score: '+ str(score)+ '\nLevel: '+ str(level), 1, (255, 255, 255))
    win.blit(text, (0, 0))

def checkKeys(keys): 
    temp= block
    if(keys[pygame.K_LEFT]):
        temp.x-=1
        if(temp.checkCollide()):
            block.x-=1
        return False
    elif(keys[pygame.K_RIGHT]):
        temp.x+=1
        if(temp.checkCollide()):
            block.x+=1
        return False
    elif(keys[pygame.K_DOWN]):
        while(not block.checkFloor()):
            block.y+=1
        block.set= True
        clear()
        return True
    elif(keys[pygame.K_a]):
        temp.rotate(True)
        if(temp.checkCollide()):
            block.rotate(True)
        return False
    elif(keys[pygame.K_s]):
        temp.rotate(False)
        if(temp.checkCollide()):
            block.rotate(False)
        return False

class Block:
    def __init__(self, last):
        self.blockType= blockTypeInit(last)
        self.hbox= hitboxes[str(self.blockType)]
        self.set= False
        self.x= 3
        if(self.blockType== 0):
            self.y=1
        else:
            self.y= 0
        global field

    def checkFloor(self): 
        floorY= self.y+len(self.hbox)-1
        if(floorY== 21):
            return True
        count= 0
        for i in self.hbox[len(self.hbox)-1]: #ERROR
            floorX= self.x+count
            if(i==1 and field[floorY+1][floorX]==1): #ERROR
                return True
            count+=1 
        return False

    def rotate(self, ccw):
        if(self.blockType!= 3):
            temp= [[]*1 for _ in range(len(self.hbox[0]))]
            if(ccw):
                for x in range(len(self.hbox[0])-1, 0, -1):
                    for y in self.hbox:
                        temp[x].append(y[x]) 
                self.hbox= temp
            else:
                for x in range(len(self.hbox[0])):
                    for y in self.hbox.reverse():
                        temp[x].append(y[x])
                self.hbox= temp

    def checkCollide(self): 
        for i in range(block.y, block.y+ len(block.hbox)):
            for j in range(block.x, block.x+ len(block.hbox[0])):
                if(block.hbox[i-block.y][j-block.x]==1 and field[i][j]==1):
                    return True
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
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
        
        keys= pygame.key.get_pressed()

        if(setState):
            frameCount= 3000//t
            if(block.checkFloor()):
                if(frameCounter<frameCount):
                    frameCounter+=1
                    tempBool= checkKeys(keys)
                    if(tempBool):
                        setState= False
                        continue
                else:
                    frameCounter= 0
                    block.set= True
                    #DOUBLE CHECK THAT FOR LOOP HERE MAKES SENSE
                    for i in range(block.y, block.y+ len(block.hbox)):
                        for j in range(block.x, block.x+ len(block.hbox[0])):
                            if(block.hbox[i-block.y][j-block.x]==1):
                                field[i][j]= block.hbox[i-block.y][j-block.x]
                    clear()
                    if(field[0].count(1)>0 or field[1].count(1)>0): #checks if game is over
                        play= False
                    setState= False
                    continue
            else:
                setState= False
                frameCounter= 0
                continue
        else:
            if(block.checkFloor()):
                setState= True
                continue
            else:
                checkKeys(keys)
                block.y+=1
    else:
        drawEndScreen()


    clock.tick(30)

pygame.quit()