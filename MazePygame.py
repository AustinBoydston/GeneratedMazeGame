import pygame as pg
import numpy as np
import sys
import time
import random

MAZE_SIZE = 36
CUBE_SIZE = 10
WALL_SIZE = 20

#initialize pygame
pg.init()

# choose a random start location that is not the outside wall
def chooseRandomStart(size):
    start =  [random.randint(1, size - 2), random.randint(1, size - 2)]
    return start

# initialize the maze with everything set as a wall
# set the outside walls weight value to 1000
def initMaze(size):
    # create the maze 2d array and the maze weights 2d array
    maze = [[1] * size for i in range(size)]
    maze_weights = [[0] * size for i in range(size)]
    # Set the outside wall weights to a high value
    for i in range(size):
        for j in range(size):
            if i == 0 or i == (size - 1):
                maze_weights[i][j] = 1000
            if j == 0 or j == (size - 1):
                maze_weights[i][j] = 1000
    
    #print(maze)
    return maze, maze_weights

# Check if the frontier cell is a valid next cell
def isValidFrontier(maze, maze_weights, x, y):
    path_neighbors = 0
    # is the frontier cell already a path?
    if maze[x][y] == 0:
        return False
    if maze_weights[x][y] > 10:
        return False
    # determine if the frontier wall has exactly one neighbor
    if maze[x+1][y] == 0:
        path_neighbors += 1
    if maze[x][y+1] == 0:
        path_neighbors += 1
    if maze[x-1][y] == 0:
        path_neighbors += 1
    if maze[x][y-1] == 0:
        path_neighbors += 1
    if path_neighbors > 1:
        return False
    return True

# get the frontier cells reletive to the current cell
def getFrontier(maze, maze_weights, x, y):
    frontier = []
    maze_weights
    
    if isValidFrontier(maze, maze_weights, x+1, y):
        frontier.append([x+1, y])
    if isValidFrontier(maze, maze_weights, x, y+1):
        frontier.append([x, y+1])
    if isValidFrontier(maze, maze_weights, x-1, y):
        frontier.append([x-1, y])
    if isValidFrontier(maze, maze_weights, x, y-1):
        frontier.append([x, y-1])
    return frontier
    

# Generate the maze
def generateMaze(size, surface):
    maze, maze_weights = initMaze(size)
    start = chooseRandomStart(size)
    
    # the main cell stack 
    cell_stack = []
    cell_stack.append(start)

    # set path weight of start cell to 500
    maze_weights[start[0]][start[1]] = 500

    # the list of valid frontier cells
    frontier = getFrontier(maze, maze_weights, start[0], start[1])
    # main generation loop
    while True:
        time.sleep(.001)
        # set current cell to a path cell
        maze[cell_stack[-1][0]][cell_stack[-1][1]] = 0

        # get the frontier of the current path cell
        frontier = getFrontier(maze, maze_weights, cell_stack[-1][0], cell_stack[-1][1])
        
        # check if the frontier is empty
        if len(frontier) == 0:
            # write back tracking code here
            
            #pop off current cell and get last cell
            cell_stack.pop()
            #if the cell stack is empty (backtracking is done) stop the generating loop
            if len(cell_stack) == 0:
                break
            #print("size of cell stack during back track: ", len(cell_stack))
            #Get the current maze coordinates after back tracking once
            back_x, back_y = cell_stack[-1][0], cell_stack[-1][1]
            #decrement last cell's frontier weights in a copy of maze_wieghts so that the actual values are not changed
            #maze_weights_copy1 = maze_weights
            
            if maze[back_x+1][back_y] == 1:
                maze_weights[back_x+1][back_y] -= 1
            if maze[back_x-1][back_y] == 1:
                maze_weights[back_x-1][back_y] -= 1
            if maze[back_x][back_y+1] == 1:
                maze_weights[back_x][back_y+1] -= 1
            if maze[back_x][back_y-1] == 1:
                maze_weights[back_x][back_y-1] -= 1
            #get valid frontier of current cell
            frontier = getFrontier(maze, maze_weights, back_x, back_y)
            print("current position: ", back_x, ", ", back_y, "Valid Frontier: ", frontier)
            #time.sleep(.2)
            #check if there are any valid frontier items
            if len(frontier) == 0:
                # if not, do nothing and let the next loop back track again
                pass
            else:
                # if yes, get a random valid one and push it onto the cell stack
                # get random valid frontier item
                random_frontier = random.randint(0, len(frontier) - 1)
                # push chosen frontier item onto the path stack
                cell_stack.append([frontier[random_frontier][0],frontier[random_frontier][1]] )
                # increment frontier weights (set path weight to 500) to say there is an additional neighbor path cell
                for i in range(len(frontier)):
                    if i == random_frontier:
                        maze_weights[frontier[i][0]][frontier[i][1]] = 500    
                    else:
                        maze_weights[frontier[i][0]][frontier[i][1]] += 1
        else:
            # get random valid frontier item
            random_frontier = random.randint(0, len(frontier) - 1)
            # push chosen frontier item onto the path stack
            cell_stack.append([frontier[random_frontier][0],frontier[random_frontier][1]] )
            # increment frontier weights (set path weight to 500) to say there is an additional neighbor path cell
            for i in range(len(frontier)):
                if i == random_frontier:
                    maze_weights[frontier[i][0]][frontier[i][1]] = 500    
                else:
                    maze_weights[frontier[i][0]][frontier[i][1]] += 1
        drawGeneratingMaze(maze, surface)
        # if we have back tracked to the start, stop carving out paths
        if len(cell_stack) == 0:
            break

    return maze, start

def drawGeneratingMaze(maze, surf):
    drawMaze(maze, surf)
    pg.display.flip()


# draw the maze given a MAZE_SIZE x MAZE_SIZE maze and a surface
def drawMaze(maze, surface_):
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            r = (WALL_SIZE*i, WALL_SIZE*j, WALL_SIZE, WALL_SIZE)
            
            if maze[i][j] == 0:
                pg.draw.rect(surface_, (0, 0, 0), r)
            elif maze[i][j] == 1:
                pg.draw.rect(surface_, (255, 0, 255), r)
            elif maze[i][j] == 2:
                pg.draw.rect(surface_, (0, 255, 0), r)
            elif maze[i][j] == 3:
                pg.draw.rect(surface_, (0, 0, 255), r)
            else:
                exit()
    
    
# detect collision based off of the four corners of the player model
def colliding(maze, playerx, playery):
    # top left of player
    newx_tl = (playerx)//WALL_SIZE
    newy_tl = (playery)//WALL_SIZE
    
    # bottom left of player
    newx_bl = (playerx)//WALL_SIZE
    newy_bl = (playery + CUBE_SIZE - 1)//WALL_SIZE
    
    # top right of player
    newx_tr = (playerx + CUBE_SIZE - 1)//WALL_SIZE
    newy_tr = (playery)//WALL_SIZE
    
    # botom right of player
    newx_br = (playerx+ CUBE_SIZE - 1)//WALL_SIZE
    newy_br = (playery+ CUBE_SIZE - 1)//WALL_SIZE
    
    
    
    if newx_tl + 1> MAZE_SIZE or newy_tl+1 > MAZE_SIZE:
        return False
    if maze[newx_tl][newy_tl] or maze[newx_bl][newy_bl] or maze[newx_tr][newy_tr] or maze[newx_br][newy_br]:
        return True
    else:
        return False



# Screen dimensions
WIDTH, HEIGHT = 720, 720
# Create the display
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("maze game")

maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]



# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pg.display.set_mode((WIDTH, HEIGHT))
disp = pg.display.set_caption("Basic pg Game")

# Clock for controlling frame rate
clock = pg.time.Clock()
FPS = 60

#set the maze to a generated one instead of the hardcoded one above
maze, player_start = generateMaze(MAZE_SIZE, screen)

# Player properties
player_width, player_height = CUBE_SIZE, CUBE_SIZE
player_x, player_y = player_start[0] * WALL_SIZE+ 3, player_start[1] * WALL_SIZE + 3 #WIDTH // 2, HEIGHT // 2
player_speed = 3



# attempt to draw maze
drawMaze(maze, screen)



# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    
    new_x, new_y = player_x, player_y
    # Get keys pressed
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        new_y -= player_speed
    if keys[pg.K_DOWN]:
        new_y += player_speed
    if keys[pg.K_LEFT]:
        new_x -= player_speed
    if keys[pg.K_RIGHT]:
        new_x += player_speed

    # Detect collision
    if not colliding(maze, new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_width, player_x))
    player_y = max(0, min(HEIGHT - player_height, player_y))

    # Draw everything
    screen.fill(BLACK)  # Clear the screen
    
    drawMaze(maze, screen)

    pg.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))



    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pg
pg.quit()
sys.exit()