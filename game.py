import pygame as pg
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

# Write Centered Text Box
def centerText(message):
    text = fontLarge.render(message, True, black)
    center = text.get_rect(center=(width // 2, height // 2))
    pg.draw.rect(screen, white, (center[0] - 30, center[1] - 20, center[2] + 60, center[3] + 40))
    screen.blit(text, center)
    
# Draw and Write Player Win Counter
def drawCounter(players):
    pg.draw.rect(screen, white, (0, 0, 50, 50))
    for key, p in enumerate(players):
        text = fontSmall.render(p.type + ': ' + str(p.wins), True, black)
        screen.blit(text, (10, 10 * (key*2+1)))

# Game Class
class Game:
    
    # Init Game
    def __init__(self,
        players=False, activePlayer=False, startingPlayer=False,
        running = True, pause = False, reset = False
    ):
        
        # Define Players
        self.players = [Player('x'), Player('o')]
        self.activePlayer = self.players[0]
        self.startingPlayer = self.activePlayer
        
        # Game Status
        self.running = running  # Set Game Running Status
        self.pause = pause      # Set Game Pause Status
        self.reset = reset      # Set Game Reset 
        
        pg.display.set_caption("Tic Tac Toe") # Set Game Tab Name
        
        drawCounter(self.players)
        
        self.resetGame()
    
    # Reset Game
    def resetGame(self):
        self.reset = False
        
        screen.fill(black)
        
        # Redraw Game Lines
        for i in range(2):
            pg.draw.line(screen, white, (width / 3 * (i+1), 0), (width / 3 * (i+1), height), line_width)
            pg.draw.line(screen, white, (0, height / 3 * (i+1)), (width, height / 3 * (i+1)), line_width)
        
        # Remove Mark Values
        for column in tiles:
            for tile in column:
                tile.marked = False
                
        # Increment Player Counter
        drawCounter(self.players)
    
    # Check for Win
    def checkWin(self):
    
        if all(tiles[1][1].marked and (tiles[1][1].marked == tiles[i][i].marked) for i in range(3)) : return True
        if all(tiles[1][1].marked and (tiles[1][1].marked == tiles[i][-(i+1)].marked) for i in range(3)) : return True
        
        for c, column in enumerate(tiles):
            
            if all(i.marked == column[0].marked and column[0].marked for i in column) or all(tiles[i][c].marked == tiles[0][c].marked and tiles[0][c].marked for i in range(3)):
                return True
        
        return False

    # Win Event
    def win(self):
        self.activePlayer.wins += 1
        
        centerText("Player " + self.activePlayer.type.upper() + " WINS!!!")
        
        self.startingPlayer = self.switchPlayer(self.activePlayer)
        self.activePlayer = self.startingPlayer
        
        self.pause = True
    
    # Check for Draw
    def checkDraw(self):
        return all((tiles[i][0].marked and tiles[i][1].marked and tiles[i][2].marked) for i in range(3))
    
    # Draw Event
    def draw(self):
        
        centerText("Draw :(")
        
        self.pause = True
        
        self.startingPlayer = self.switchPlayer(self.startingPlayer)
        self.activePlayer = self.startingPlayer
        
    # Switch Player
    def switchPlayer(self, player):
        match self.players.index(player):
            case 0: return self.players[1]
            case 1: return self.players[0]
              
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
    
    def mark(self):
        if not self.marked :
            self.marked = game.activePlayer.type
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

# Player Class
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

# Start Game
game = Game()
while game.running:
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT: game.running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            
            # Game Paused
            if game.pause :
                game.reset = True
                game.pause = False
            
            # Game Running
            else :
                
                for column in (tiles):
                    for tile in (column):
                        if tile.box.collidepoint(event.pos):
                            play = tile.mark()
                
                
                if game.checkWin(): game.win()      # Check For Win
                elif game.checkDraw(): game.draw()  # Check For Draw
                elif play : game.activePlayer = game.switchPlayer(game.activePlayer)
    
    # Reset Game
    if game.reset: game.resetGame()
       
    pg.display.flip()
    clock.tick(60) # Set FPS to 60

pg.quit()