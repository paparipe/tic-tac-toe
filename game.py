import pygame as pg
import sys
import time
from pygame.locals import *

pg.init() # Init Engine

# Vars
width = 700
height = 500
line_width = 2


rows = 3
columns = 3

white = (243, 243, 243)
black = (43, 43, 43)
fontSmall = pg.font.Font(None, 20)
fontLarge = pg.font.Font(None, 35)

screen = pg.display.set_mode((width, height)) # Display size
clock = pg.time.Clock() # Set Game Clock
screen.fill(black)


running = True
pause = False
reset = False


def initGame():
    
    pg.display.set_caption("Tic Tac Toe")
    
    # Increment Player Counter
    pg.draw.rect(screen, white, (0, 0, 50, 50))
    for key, p in enumerate(players):
        text = fontSmall.render(p.type + ': ' + str(p.wins), True, black)
        screen.blit(text, (10, 10 * (key*2+1)))
        
    resetGame()

# Game Functions
def resetGame():
    global reset
    reset = False
    
    screen.fill(black)
    
    for i in range(2):
        pg.draw.line(screen, white, (width / 3 * (i+1), 0), (width / 3 * (i+1), height), line_width)
        pg.draw.line(screen, white, (0, height / 3 * (i+1)), (width, height / 3 * (i+1)), line_width)
    
    for column in tiles:
        for tile in column:
            tile.marked = False
            
    # Increment Player Counter
    pg.draw.rect(screen, white, (0, 0, 50, 50))
    for key, p in enumerate(players):
        text = fontSmall.render(p.type + ': ' + str(p.wins), True, black)
        screen.blit(text, (10, 10 * (key*2+1)))
                
    
def checkWin():
    
    if all(tiles[1][1].marked and (tiles[1][1].marked == tiles[i][i].marked) for i in range(3)) : return True
    if all(tiles[1][1].marked and (tiles[1][1].marked == tiles[i][-(i+1)].marked) for i in range(3)) : return True
        
    # if all(tiles[1][1].marked and (tiles[1][1].marked in (tiles[i][i].marked, tiles[i][-(i+1)].marked)) for i in range(3)):
    #     return True
    
    for c, column in enumerate(tiles):
        
        if all(i.marked == column[0].marked and column[0].marked for i in column) or all(tiles[i][c].marked == tiles[0][c].marked and tiles[0][c].marked for i in range(3)):
            return True
    
    return False


def win(player):
    
    player.wins += 1
    
    # Message Player Win
    text = fontLarge.render("Player " + player.type.upper() + " WINS!!!", True, black)
    center = text.get_rect(center=(width // 2, height // 2))
    pg.draw.rect(screen, white, (center[0] - 30, center[1] - 20, center[2] + 60, center[3] + 40))
    screen.blit(text, center)
    
    global activePlayer
    global startingPlayer
    match players.index(player):
        case 0: activePlayer = players[0]
        case 1: activePlayer = players[1]
    startingPlayer = activePlayer
        
    global pause
    pause = True

def checkDraw():
    if all((tiles[i][0].marked and tiles[i][1].marked and tiles[i][2].marked) for i in range(3)) : draw(activePlayer)

def draw(player):
    
    # Message Player Draw
    text = fontLarge.render("Draw :(", True, black)
    center = text.get_rect(center=(width // 2, height // 2))
    pg.draw.rect(screen, white, (center[0] - 30, center[1] - 20, center[2] + 60, center[3] + 40))
    screen.blit(text, center)
    
    global pause
    pause = True
    
    global activePlayer
    global startingPlayer
    match players.index(startingPlayer):
        case 0: startingPlayer = players[0]
        case 1: startingPlayer = players[1]
    activePlayer = startingPlayer
    

# Box Class
class Tile:
    
    def __init__(
        self,
        pos,
        marked = False,
    ):
        self.marked = marked
        self.pos = pos
        self.box = pg.Rect(pos[0], pos[1], width/3, height/3)
    
    def is_clicked(self, mouse_pos):
        return self.box.collidepoint(mouse_pos)
    
    def mark(self):
        if not self.marked :
            self.marked = activePlayer.type
            self.write()
            return True
        return False
    
    def write(self):
        match self.marked:
            case 'x':
                pg.draw.line(screen, white, (self.pos[0] + 50, self.pos[1]+10), (self.pos[0]-50+width/3, self.pos[1]-10+height/3), line_width)
                pg.draw.line(screen, white, (self.pos[0] + 50, self.pos[1]-10+height/3), (self.pos[0]-50+width/3, self.pos[1]+10), line_width)
            case 'o':
                pg.draw.circle(screen, white, (self.pos[0]+width/3/2, self.pos[1]+height/3/2), (height/3/2 - 10), line_width)


class Player:
    def __init__(
        self,
        type,
        wins = 0
    ):
        self.type = type
        self.wins = wins

            
# Define Tiles
tiles = [[Tile([i * width/3, j * height/3]) for i in range(columns)] for j in range(rows)]

# Define Players
players = [Player('x'), Player('o')]
activePlayer = players[0]
startingPlayer = activePlayer


initGame()

while running:

    for event in pg.event.get():
        
        if event.type == pg.QUIT: running = False
        
        if pause :
            
            if event.type == pg.MOUSEBUTTONDOWN:
                reset = True
                pause = False
            
        else :
                
            if event.type == pg.MOUSEBUTTONDOWN:
                
                # Loop Tiles
                for column in (tiles):
                    for tile in (column):
                        if tile.is_clicked(event.pos):
                            play = tile.mark()
                
                # Check For Win
                if checkWin(): win(activePlayer)
                
                # Check For Draw
                elif checkDraw(): draw(activePlayer)
                
                # Switch Player
                if play :
                    match players.index(activePlayer):
                        case 0: activePlayer = players[1]
                        case 1: activePlayer = players[0]
    
    checkWin()
    
    if reset: resetGame()
                    
    pg.display.flip()

    clock.tick(60) # limits FPS to 60

pg.quit()