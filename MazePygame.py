import pygame as pg
import sys
import time
import random


############################################ Class Definitions #############################

class Config:
    """
    A configuration class to store constants used in the maze game.

    This class defines parameters that control the maze's properties, 
    player attributes, and gameplay dynamics.

    Attributes:
        MAZE_SIZE (int): The size of the maze grid (number of cells per side).
        CUBE_SIZE (int): The size of the player rectangle in pixels.
        WALL_SIZE (int): The size of each wall block in pixels.
        PLAYER_SPEED (int): The movement speed of the player in pixels per frame.
        GENERATE_SPEED (float): The delay in seconds for maze generation animation.
        OUTER_WALL_WEIGHT (int): The weight value assigned to the outer walls.
        PATH_WEIGHT (int): The weight value assigned to the path cells.
        PATH (int): The identifier for path cells in the maze.
        WALL (int): The identifier for wall cells in the maze.
        EXIT (int): The identifier for the maze exit cell.
    """
    MAZE_SIZE = 36 #* 2 # Maze height and width
    CUBE_SIZE = 10 #// 2# Player
    WALL_SIZE = 20 #// 2# Walls
    PLAYER_SPEED = 3
    GENERATE_SPEED = 0.00001 # time for the sleep function to wait when generating maze
    # weight varibales
    OUTER_WALL_WEIGHT = 1000
    PATH_WEIGHT = 500
    PATH = 0
    WALL = 1
    EXIT = 2


class Maze:
    """
    A class to represent a procedurally generated maze.

    The Maze class creates a 2D grid maze using a randomized algorithm.
    It handles the generation of the maze layout, including setting up walls, paths, 
    the start position, and the exit. The maze can also be visualized on a given Pygame surface.

    Attributes:
        config (Config): Configuration object containing maze parameters.
        size (int): The size of the maze grid.
        wall_size (int): The size of each maze cell in pixels.
        surface (pygame.Surface): The Pygame surface on which the maze is drawn.
        maze (list[list[int]]): A 2D grid representing the maze layout (0 = path, 1 = wall, 2 = exit).
        maze_weights (list[list[int]]): A 2D grid for tracking maze generation states.
        start (tuple[int, int]): The starting position in the maze.

    Methods:
        chooseRandomStart(size):
            Randomly selects a starting point inside the maze grid.
        initMaze(size):
            Initializes the maze grid with walls and sets boundary weights.
        chooseExit(maze, start_x, start_y):
            Selects a random path cell as the exit point far from the start.
        isValidFrontier(maze, maze_weights, x, y):
            Checks if a cell is a valid candidate for path expansion.
        getFrontier(maze, maze_weights, x, y):
            Finds valid frontier cells around a given cell.
        digPath(maze, maze_weights, cell_stack, frontier):
            Converts a wall into a path and updates the frontier list.
        backTrack(maze, maze_weights, cell_stack):
            Reverts to the previous cell when no valid frontier exists.
        generateMaze(maze, maze_weights, size, surface):
            Generates the maze using a randomized algorithm and visualizes it.
    """
    #config = Config()
    def __init__(self, size_n, size_wall, surface, config):
        self.size = size_n
        self.wall_size = size_wall
        self.surface = surface
        self.config = config
        self.maze, self.maze_weights = self.initMaze(self.size)
        self.maze, self.maze_weights, self.start = self.generateMaze(self.maze, self.maze_weights, self.size, self.surface)
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
        maze = [[self.config.WALL] * size for i in range(size)]
        maze_weights = [[0] * size for i in range(size)]
        # Set the outside wall weights to a high value
        for i in range(size):
            for j in range(size):
                if i == 0 or i == (size - 1):
                    maze_weights[i][j] = self.config.OUTER_WALL_WEIGHT
                if j == 0 or j == (size - 1):
                    maze_weights[i][j] = self.config.OUTER_WALL_WEIGHT
    
        #print(maze)
        return maze, maze_weights


    # choose a random path cell as the maze exit
    def chooseExit(self, maze, start_x, start_y):
        counter = 0
        while True:
            endx = random.randint(1, self.config.MAZE_SIZE - 2)
            endy = random.randint(1, self.config.MAZE_SIZE - 2) 
            if abs((start_x - endx)) >= self.config.MAZE_SIZE - (self.config.MAZE_SIZE/2) -1 and abs((start_y - endy)) >= self.config.MAZE_SIZE - (self.config.MAZE_SIZE/2) - 1:  
                if maze[endx][endy] == 0:
                    break
            counter += 1
            if counter == 1000:
                print("ERROR: CHOOSE EXIT TIMEOUT, EXITING PROGRAM")
                exit()
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
                maze_weights[frontier[i][0]][frontier[i][1]] = self.config.PATH_WEIGHT   
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
        #print("current position: ", back_x, ", ", back_y, "Valid Frontier: ", frontier)
        #time.sleep(.2)
        #check if there are any valid frontier items
        if len(frontier) == 0:
            # if not, do nothing and let the next loop back track again
            pass
        else:
           maze, maze_weights, cell_stack = self.digPath(maze, maze_weights, cell_stack, frontier)
        return maze, maze_weights, cell_stack, 1

    # Generate the maze
    def generateMaze(self, maze, maze_weights, size, surface):
        start = self.chooseRandomStart(size)

        # the main cell stack 
        cell_stack = []
        cell_stack.append(start)

        # set path weight of start cell to 500
        maze_weights[start[0]][start[1]] = self.config.PATH_WEIGHT

        # the list of valid frontier cells
        frontier = self.getFrontier(maze, maze_weights, start[0], start[1])
        # main generation loop
        while True:
            #time.sleep(GENERATE_SPEED)


            # set current cell to a path cell
            maze[cell_stack[-1][0]][cell_stack[-1][1]] = 0
            drawMaze(maze, surface, True, self.config)
            # get the frontier of the current path cell
            frontier = self.getFrontier(maze, maze_weights, cell_stack[-1][0], cell_stack[-1][1])

            # check if the frontier is empty
            if len(frontier) == 0:
                # write back tracking code here
                maze, maze_weights, cell_stack, failed = self.backTrack(maze, maze_weights, cell_stack)
                
            else:
                # stage new cell for path digging
                maze, maze_weights, cell_stack = self.digPath(maze, maze_weights, cell_stack, frontier)
                
         
            # if we have back tracked to the start, stop carving out paths
            if len(cell_stack) == 0:
                break
        
        return maze, maze_weights, start



class Player:
    """
    A class to represent the player in the maze game.

    The Player class handles the player's position, movement, and interactions
    with the maze, such as collision detection and detecting the maze exit.

    Attributes:
        player_x (int): The current x-coordinate of the player in pixels.
        player_y (int): The current y-coordinate of the player in pixels.
        width (int): The width of the player's rectangle.
        height (int): The height of the player's rectangle.
        speed (int): The speed of the player's movement in pixels per frame.
        config (Config): Configuration object containing maze parameters.

    Methods:
        detectExit(maze, playerx, playery):
            Checks if the player's current position corresponds to the maze's exit cell.
        colliding(maze, playerx, playery):
            Detects if the player's current position would result in a collision with a wall.
    """

    def __init__(self, x, y, width, height, speed, config):
        self.player_x = x
        self.player_y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.config = config


    def getCorners(self, playerx, playery):
        corners = [
            (playerx//self.config.WALL_SIZE, playery//self.config.WALL_SIZE),
            (((playerx + self.config.CUBE_SIZE)//self.config.WALL_SIZE), playery//self.config.WALL_SIZE),
            (playerx//self.config.WALL_SIZE, (playery + self.config.CUBE_SIZE)//self.config.WALL_SIZE),
            ((playerx + self.config.CUBE_SIZE)//self.config.WALL_SIZE, (playery + self.config.CUBE_SIZE)//self.config.WALL_SIZE)
        ]
        return corners


    def detectExit(self, maze, playerx, playery):
        corners = self.getCorners(playerx, playery)
        if maze[corners[0][0]][corners[0][1]] == 2 and maze[corners[1][0]][corners[1][1]] == 2 and maze[corners[2][0]][corners[2][1]] == 2 and maze[corners[3][0]][corners[3][1]] == 2:
            return True
        else:
            return False




    # detect collision based off of the four corners of the player model
    def colliding(self, maze, playerx, playery):
        corners = self.getCorners(playerx, playery)
        if maze[corners[0][0]][corners[0][1]] == 1 or maze[corners[1][0]][corners[1][1]] == 1 or maze[corners[2][0]][corners[2][1]] == 1 or maze[corners[3][0]][corners[3][1]] == 1:
            return True  
        else:
            return False

######################################### Function Definitions





# draw the maze given a MAZE_SIZE x MAZE_SIZE maze and a surface
def drawMaze(maze, surface_, generating, config):
    for i in range(config.MAZE_SIZE):
        for j in range(config.MAZE_SIZE):
            r = (config.WALL_SIZE*i, config.WALL_SIZE*j, config.WALL_SIZE, config.WALL_SIZE)
            
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
            #If the maze is generating, animate the generation
            if generating:
                pg.display.update(r)
    
    



##################################### Main ################################## 
def main():
    # Screen dimensions
    WIDTH, HEIGHT = 720, 720
    # Create the display
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("maze game")


    # instantiate config object
    config = Config()

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
    maze_ = Maze(config.MAZE_SIZE, config.WALL_SIZE, screen, config)
    # Player properties
    player_width, player_height = config.CUBE_SIZE, config.CUBE_SIZE
    player_x, player_y = maze_.start[0] * config.WALL_SIZE + 3, maze_.start[1] * config.WALL_SIZE + 3 #WIDTH // 2, HEIGHT // 2
    player_speed = config.PLAYER_SPEED

    player1 = Player(player_x, player_y, player_width, player_height, player_speed, config)



    # attempt to draw maze
    drawMaze(maze_.maze, screen, False, config)



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

        drawMaze(maze_.maze, screen, False, config)

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

