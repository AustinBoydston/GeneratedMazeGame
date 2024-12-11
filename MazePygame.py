import pygame as pg
import sys
import time
import random


############################################ Global Variables ########################
MAZE_SIZE = 36 * 2 # Maze height and width
CUBE_SIZE = 10 // 2# Player
WALL_SIZE = 20 // 2# Walls
GENERATE_SPEED = 0.00001 # time for the sleep function to wait when generating maze

############################################ Class Definitions #############################


class Maze:
    def __init__(self, size_n, size_wall, ):
        self.size = size_n
        self.wall_size = size_wall
        self.maze, self.maze_weights = self.initMaze(self.size)
        self.maze, self.maze_weights, self.start = self.generateMaze(self.maze, self.maze_weights, self.size)
        self.maze = self.chooseExit(self.maze, self.start[0], self.start[1])



    ########## Getter Methods #########


    
        # choose a random start location that is not the outside wall
    def chooseRandomStart(self, size):
        start =  [random.randint(1, size - 2), random.randint(1, size - 2)]
        return start

    
    # initialize the maze with everything set as a wall
    # set the outside walls weight value to 1000
    def initMaze(self, size):
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


    # choose a random path cell as the maze exit
    def chooseExit(self, maze, start_x, start_y):
        while True:
            endx = random.randint(1, MAZE_SIZE - 2)
            endy = random.randint(1, MAZE_SIZE - 2) 
            if ((start_x - endx)**2)**(1/2) >= MAZE_SIZE - (MAZE_SIZE/2) -1 and ((start_y - endy)**2)**(1/2) >= MAZE_SIZE - (MAZE_SIZE/2) - 1:  
                if maze[endx][endy] == 0:
                    break
        maze[endx][endy] = 2
        return maze


    

    # Check if the frontier cell is a valid next cell
    def isValidFrontier(self, maze, maze_weights, x, y):
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
    def getFrontier(self, maze, maze_weights, x, y):
        frontier = []
        maze_weights

        if self.isValidFrontier(maze, maze_weights, x+1, y):
            frontier.append([x+1, y])
        if self.isValidFrontier(maze, maze_weights, x, y+1):
            frontier.append([x, y+1])
        if self.isValidFrontier(maze, maze_weights, x-1, y):
            frontier.append([x-1, y])
        if self.isValidFrontier(maze, maze_weights, x, y-1):
            frontier.append([x, y-1])
        return frontier

    # create the next path cell in the maze
    def digPath(self, maze, maze_weights, cell_stack, frontier):
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
        return maze, maze_weights, cell_stack



    #Back track the function by one cell
    def backTrack(self, maze, maze_weights, cell_stack):
        #pop off current cell and get last cell
        cell_stack.pop()
        #if the cell stack is empty (backtracking is done) stop the generating loop
        if len(cell_stack) == 0:
            return maze, maze_weights, cell_stack, 0
        #print("size of cell stack during back track: ", len(cell_stack))
        #Get the current maze coordinates after back tracking once
        back_x, back_y = cell_stack[-1][0], cell_stack[-1][1]
        #decrement last cell's frontier weights in a copy of maze_wieghts so that the actual values are not changed
        #maze_weights_copy1 = maze_weight
        if maze[back_x+1][back_y] == 1:
            maze_weights[back_x+1][back_y] -= 1
        if maze[back_x-1][back_y] == 1:
            maze_weights[back_x-1][back_y] -= 1
        if maze[back_x][back_y+1] == 1:
            maze_weights[back_x][back_y+1] -= 1
        if maze[back_x][back_y-1] == 1:
            maze_weights[back_x][back_y-1] -= 1
        #get valid frontier of current cell
        frontier = self.getFrontier(maze, maze_weights, back_x, back_y)
        print("current position: ", back_x, ", ", back_y, "Valid Frontier: ", frontier)
        #time.sleep(.2)
        #check if there are any valid frontier items
        if len(frontier) == 0:
            # if not, do nothing and let the next loop back track again
            pass
        else:
           maze, maze_weights, cell_stack = self.digPath(maze, maze_weights, cell_stack, frontier)
        return maze, maze_weights, cell_stack, 1

    # Generate the maze
    def generateMaze(self, maze, maze_weights, size):
        start = self.chooseRandomStart(size)

        # the main cell stack 
        cell_stack = []
        cell_stack.append(start)

        # set path weight of start cell to 500
        maze_weights[start[0]][start[1]] = 500

        # the list of valid frontier cells
        frontier = self.getFrontier(maze, maze_weights, start[0], start[1])
        # main generation loop
        while True:
            #time.sleep(GENERATE_SPEED)
            # set current cell to a path cell
            maze[cell_stack[-1][0]][cell_stack[-1][1]] = 0

            # get the frontier of the current path cell
            frontier = self.getFrontier(maze, maze_weights, cell_stack[-1][0], cell_stack[-1][1])

            # check if the frontier is empty
            if len(frontier) == 0:
                # write back tracking code here
                maze, maze_weights, cell_stack, failed = self.backTrack(maze, maze_weights, cell_stack)
                
            else:
                # stage new cell for path digging
                maze, maze_weights, cell_stack = self.digPath(maze, maze_weights, cell_stack, frontier)
                
            #drawGeneratingMaze(maze, surface)
            # if we have back tracked to the start, stop carving out paths
            if len(cell_stack) == 0:
                break
        
        return maze, maze_weights, start



class Player:
    def __init__(self, x, y, width, height, speed):
        self.player_x = x
        self.player_y = y
        self.height = height
        self.width = width
        self.speed = speed

    def detectExit(self, maze, playerx, playery):
        
        
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


        if maze[newx_tl][newy_tl] == 2 and maze[newx_bl][newy_bl] == 2 and maze[newx_tr][newy_tr] == 2 and maze[newx_br][newy_br] == 2:
            return True
        else:
            return False




    # detect collision based off of the four corners of the player model
    def colliding(self, maze, playerx, playery):
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
        if maze[newx_tl][newy_tl] == 1 or maze[newx_bl][newy_bl] == 1 or maze[newx_tr][newy_tr] == 1 or maze[newx_br][newy_br] == 1:
            return True
        else:
            return False

######################################### Function Definitions










    


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
    
    



##################################### Main ################################## 
def main():
    # Screen dimensions
    WIDTH, HEIGHT = 720, 720
    # Create the display
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("maze game")

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
    #maze, player_start = generateMaze(MAZE_SIZE, screen)
    maze_ = Maze(MAZE_SIZE, WALL_SIZE)
    # Player properties
    player_width, player_height = CUBE_SIZE, CUBE_SIZE
    player_x, player_y = maze_.start[0] * WALL_SIZE+ 3, maze_.start[1] * WALL_SIZE + 3 #WIDTH // 2, HEIGHT // 2
    player_speed = 3

    player1 = Player(player_x, player_y, player_width, player_height, player_speed)



    # attempt to draw maze
    drawMaze(maze_.maze, screen)



    # Game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        new_x, new_y = player1.player_x, player1.player_y
        # Get keys pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            new_y -= player1.speed
        if keys[pg.K_DOWN]:
            new_y += player1.speed
        if keys[pg.K_LEFT]:
            new_x -= player1.speed
        if keys[pg.K_RIGHT]:
            new_x += player1.speed

        # Detect collision
        if not player1.colliding(maze_.maze, new_x, new_y):
            player1.player_x = new_x
            player1.player_y = new_y
        #Exit the main function if escape is successful. Generate a new maze.
        if player1.detectExit(maze_.maze, new_x, new_y):
            return 1

        # Keep player within screen bounds
        player1.player_x = max(0, min(WIDTH - player_width, player1.player_x))
        player1.player_y = max(0, min(HEIGHT - player_height, player1.player_y))

        # Draw everything
        screen.fill(BLACK)  # Clear the screen

        drawMaze(maze_.maze, screen)

        pg.draw.rect(screen, RED, (player1.player_x, player1.player_y, player1.width, player1.height))



        # Update the display
        pg.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


#############################################Running Code##########################

#initialize pygame
pg.init()

#infinite game loop
while True:
    main()

# Quit pg
pg.quit()
sys.exit()

