from io import RawIOBase
import pygame
import math
from queue import PriorityQueue

# Initialise the window width and title
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding using the A* algorithm")

# Initialise the different color RGB variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node: each individual block on the grid 
class Node:
    # On initialisation, keep track of few values so we can draw and operate on  it
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = WHITE
        self.neighbours = []
        self.total_rows =total_rows

    # Return the node object's position (x and y value in the grid)
    def get_pos(self):
        return self.row, self.col
    
    """
        Checker funciton: The color of the node determine what it is:
            - RED: Closed
            - GREEN - Open
            - BLACK - Barrier/Obstacle
            - ORANGE - Start
            - PURLE - End
            - WHITE - Default
    """
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    """
        Change the value of the current node to the different color, i.e change its functionality
    """
    def reset(self):
        self.color = WHITE
    
    def make_open(self):
        self.color = GREEN

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    # Returns neighbours of the node that are not a barrier 
    def get_neighbours(self, grid):
        self.neighbours = []
        
        # Look DOWN a row
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        # Look UP a row
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        # Look LEFT a row
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])
        # Look RIGHT a row
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

    # Draw the rectangle node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def __lt__(self, other):
        return False


# Heuristic function using the Manhattan Distance (distance between two points measured along axes at right angles)
def heuristic_function(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)

# Reconstruct the path once the end node has been reached using the came_from variable
def backtrack(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# Main A start algorithm function
def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic_function(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            backtrack(came_from, end, draw)
            start.make_start()
            end.make_end()
            
            return True

        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic_function(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

# Create the grid with the individuals nodes (width X width)
def create_grid(row, width):
    grid = []
    gap = width // row

    for i in range(row):
        grid.append([])
        
        for j in range(row):
            node = Node(i, j, gap, row)
            grid[i].append(node)
    
    return grid

# Draw the grid lines
def draw_grid_lines(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Initial draw to fill the nodes with the default white
def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid_lines(win, rows, width)
    pygame.display.update()

# Get the position (x and y) that the user clicked
def pos_click(pos, row, width):
    gap = width //row
    y, x = pos

    row = y // gap
    col = x // gap
    
    return row, col

# Main function that runs to create grid and update on various events
def main(win, width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        # Get all events, i.e. if something has been clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # LEFT button click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = pos_click(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()
                
                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = pos_click(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.get_neighbours(grid)
                            
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()

# Run the main function to run the program
main(WIN, WIDTH)