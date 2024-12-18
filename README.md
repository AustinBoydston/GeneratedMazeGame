# Generated Maze Game - Procedural Maze Generator and Player Navigation

 A procedurally generated maze game created using Python and Pygame.
---
### Prerequisites
- Python 3.8 or higher
- Pygame library installed (`pip install pygame`)

### Running the Game
1. Clone the repository:
   ```bash
   git clone https://github.com/AustinBoydston/GeneratedMazeGame.git
   cd maze-game
   ```
2. Install the dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python maze_game.py
   ```

### Controls
- **Arrow Keys**: Move the player through the maze.
- Reach the green exit to win the game, which will regenerate a new maze.
- After completing 3 mazes, the game exits.

---
### Code Highlights
- **`Config` Class**: Centralized configuration for all game settings (maze size, speed, etc.).
- **`Maze` Class**: Handles procedural generation and maze data storage.
- **`Player` Class**: Manages player position, movement, collision, and exit detection.
- **Procedural Generation Algorithm**: Follows similar patterns to Prim's Algorithm for maze generation, but implements a weight matrix instead of a visited list to carve out paths dynamically.
---

## Customization

You can modify the game's configuration by editing the `Config` class:

- **Maze Size**: Change `Config.MAZE_SIZE` to increase or decrease the maze's complexity.
- **Player Speed**: Modify `Config.PLAYER_SPEED` to adjust player movement speed.
- **Generation Speed**: Adjust `Config.GENERATE_SPEED` to speed up or slow down maze generation visualization.

Example:
```python
class Config:
    MAZE_SIZE = 50  # Larger maze
    PLAYER_SPEED = 5  # Faster movement
    GENERATE_SPEED = 0.1  # Slower generation animation
```

# The Maze Generation Algorithm 
### (Weight Matrix DFS Implementation, Nicknamed "Boydston's Maze Algorithm" [*I've yet to see anything like this ¯\\_(ツ)_/¯*])
This generation algorithm is similar to Prim's Algorithm in that it starts with a maze full of walls and uses the concept of a "frontier" to randomly choose the next path cell. It is different in that there is no global frontier list like in classic Prim's and it has a DFS style generation rather than a BFS. There is a second matrix the same size and dimension as the maze that tracks "weights" of each cell in the maze. My reason for this approach is that this framework allows a lot of flexibility and features to be added on to this basic maze game post generation, and also more control over the generation process. For more on this, see the next section on future work. The generation algorithm is as follows.
 1. Initialize the maze matrix to all 1s (walls) and the wieght matrix to all 0s except set the outside wall weights to 1000 (1000 chosen by arbitrary convention)
 2. Randomly choose a starting cell that is not on the outside border and push it onto the stack.
 3. If the stack is empty, return the Maze (else proceed)
 4. Set the cell on the top of the stack in the maze matrix to 0 (saying its a path cell), and the weight of this cell to 500 (500 chosen by arbitrary convention)
 5. Get the list of neighbors from the current cell (The "frontier": cells to the immediate left, right, up, and down)
 6. Check each neighbor in the frontier to see if it is a valid choice for us to make the next current cell (criteria is: not a cell on the outside border, and not a cell that has already been seen by the algorithm. I.E. the neighbor cell has a weight of 0)
 7. Remove the neighbor cells from the valid frontier list that do not meet the criteria in step 6.
 8. Randomly choose a cell from the remaining list of valid frontier cells. (If the list is empty backtrack. See A. below.)
 9. Increment the weights of all the neighbor cells by 1 (basically saying we have seen these cells an amount of times eqaul to the weight value, thus increment it by one for seeing them this time).
 10. Set the chosen frontier cell in the maze matrix to 0 (saying its a path cell)
 11. Push the chosen cell onto the stack making it the next current cell

 A. (back track implementation)
 1. pop the current cell off the stack
 2. Get the new current cells neighbors and decrement their weights by 1 (When this cell was first made a path, it saw all these neighbors once already, decrementing here makes us forget seeing the neighbor cells when that happened for this cell, while still remembering if the neighbors were seen by other path cells)
 3. Remove the neighbor cells from the valid frontier list that do not meet the criteria in step 6 above.
 4. Randomly choose a cell from the remaining list of valid frontier cells. (If the list is empty, do nothing and let the main loop repeat back to step 3 above)
 5. Increment the weights of all the neighbor cells by 1 (recording the fact that we saw all these neighbors here).
 6. Push the chosen cell onto the stack making it the next current cell

## Future Features (or, why this algorithm?)
The weight matrix of this maze can be used to keep track of further cell types asides from wall, path and exit. This second 2d matrix, in the context of games, can allow a path to be an enemy spawn path cell, a loot/chest having cell, an npc encounter cell, or any other kind of path cell that needs its own sub type. For the specific implementation, a number scheme will need to be chosen to translate the wieght to it's proper subtype, but will still allow the implementation of thousands of sub types while still maintaining O(1) time complexity to process them. Another valuable benefit of this weighted matrix, is it can be preconfigured with a custom weight matrix before the maze is generated to control how the maze carves paths. Tracing out weights of 1000 in weight matrix in the above algorithm will garuntee that no path will be created on cell with those weights allowing great control over the final layout. This could even be used to make "Maze art" where the layout of the maze creates the impression of an image. More use cases likely exist than what was mentioned here!
## Acknowledgments

- **Pygame**: The library used for creating the game visuals and handling input.
- **Procedural Generation**: Inspired by algorithms like Prim's Algorithm and DFS.


All Rights Reserved

