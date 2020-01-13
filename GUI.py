import sys, pygame, math
import PathFinder
from PathFinder import PathManager
pygame.init()

#set up screen
screenSize = width, height = 800, 850
speed = [2, 2]
screen = pygame.display.set_mode(screenSize)
font = pygame.font.Font('freesansbold.ttf', 32) 

#Colour constants
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 50)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#grid constants
SIZE = 50
BLOCKSIZE = 16

#game state for button events
GAMESTATE = 1
#button hold for barrier select
buttonDown = False

#on screen text
font = pygame.font.Font('freesansbold.ttf', 28) 
helpText = font.render('', True, WHITE, BLACK)
helpTextRect = helpText.get_rect()
helpTextRect.center = (10, 825)

#setup path finder
newPathFinder = PathManager(SIZE)


def drawPoint(point, colour):
    pointRect = pygame.Rect(point.coordinates[0]*BLOCKSIZE+1, point.coordinates[1]*BLOCKSIZE+1, BLOCKSIZE-1, BLOCKSIZE-1)
    pygame.draw.rect(screen, colour, pointRect)

def drawGrid(manager):
    
    for x in range(0, SIZE):
        for y in range(0, SIZE):
            if (manager.grid[x][y].active == False):
                drawPoint(manager.grid[x][y], BLACK)
            else:
                if manager.startPoint == (x,y) or manager.endPoint == (x,y):
                    drawPoint(manager.grid[x][y], GREEN)
                elif manager.grid[x][y].path == True:
                    drawPoint(manager.grid[x][y], BLUE)
                else:
                    drawPoint(manager.grid[x][y], WHITE)

def getMouseCoords():
    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    Mouse_x = math.floor(Mouse_x / BLOCKSIZE)
    Mouse_y = math.floor(Mouse_y / BLOCKSIZE)

    return (Mouse_x, Mouse_y)

def clickEvent(button):
    global GAMESTATE
    global newPathFinder
    global buttonDown
    #   Set start point
    if GAMESTATE == 1 and button == 1:
        if newPathFinder.setStartPoint(getMouseCoords()):
            GAMESTATE += 1
        return
    #   Set end point
    if GAMESTATE == 2 and button == 1:
        if newPathFinder.setEndPoint(getMouseCoords()):
            GAMESTATE += 1
            buttonDown = False
        return
    #   find path
    if GAMESTATE == 3 and button == 3:
        newPathFinder.findPath()
        GAMESTATE += 1
        return
    #   reset path
    if GAMESTATE == 4 and button == 3:
        newPathFinder = PathManager(SIZE)
        GAMESTATE = 1

def setBarriers():
    if GAMESTATE == 3 and buttonDown == True:
        newPathFinder.deactivatePoint(getMouseCoords())

def updateHelpText():
    global GAMESTATE
    global helpText
    switcher={
        1:'[Left Click] Select start point',
        2:'[Left Click] Select end point',
        3:'[Left Click] Add barrier   [Right Click] Find path',
        4:'[Right Click] Reset the grid',
        }
    text = switcher.get(GAMESTATE,"error")


    helpText = font.render(text, True, WHITE, BLACK)

updateHelpText()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonDown = True
            clickEvent(event.button)
            updateHelpText()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            buttonDown = False

    setBarriers()        
       


    screen.fill(BLACK) 

    drawGrid(newPathFinder)

    screen.blit(helpText, helpTextRect)

    pygame.display.flip()


