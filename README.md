# A* Path finding algorithm

The **A\* star** is a technique that is used in path finding and graph traversal. Unlike other traversal techniques, it has "brains", i.e. a smart algorithm that helps to find the shortest path by considering only the optimal paths without considering all options. 

![GIF of the A* algorith](https://media.giphy.com/media/Bge04c1SH5as4HZrMZ/giphy.gif)

The blue is the start node and the orange is the end node with the black representing the obstacles. The green are the open nodes we can travel to while the red are the closed one, i.e. already visited. It uses a Manhattan Distance heuristic funciton to best determine the optimal path without having to consider all possible paths.

---

# Run the program

1. Clone the repository
2. Install Python and run <code>pip install -r requirements.txt</code> to install the requirements
3. Double click main.py OR open your command line and type <code>python main.py</code>