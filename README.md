# repeated-a-star

## Three different implementations of the A* search algorithm in Python with a PyGame GUI

### Overview

- Generates a random maze with coordinates for Agent and Goal cell. 
- Chosen algorithm will run with a newly generated maze, solve the maze from Agent to the Target, and save a screenshot of the final solved maze. 
- Highlights all cells discovered on the A* path as well as the final chosen path taken by the AI. 
- Generates a log of the number of cells discovered per run


### A* Variations

- Forward A* calculates the path from the Agent to the target cell
- Backward A* calculates the path from the Target to the Agent
- Adaptive A* uses known history of previously calculated path to make a prediction on the next possible step

