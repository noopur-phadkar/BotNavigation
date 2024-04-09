import heapq
import numpy as np
import matplotlib.pyplot as plt

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in neighbors(graph, current):
            new_cost = cost_so_far[current] + graph[next[0]][next[1]]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
                
    return came_from, cost_so_far

def neighbors(graph, current):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
    (x, y) = current
    results = []
    for (dx, dy) in directions:
        next = (x + dx, y + dy)
        if 0 <= next[0] < len(graph) and 0 <= next[1] < len(graph[0]) and graph[next[0]][next[1]] == 0:
            results.append(next)
    return results

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path

def visualize_warehouse_updated(warehouse, path):
    # Create a color map: 0 (available space) in white, 1 (obstacle) in black
    colored_warehouse = np.zeros((warehouse.shape[0], warehouse.shape[1], 3))
    for i in range(warehouse.shape[0]):
        for j in range(warehouse.shape[1]):
            if warehouse[i][j] == 1:  # Obstacle
                colored_warehouse[i][j] = [0, 0, 0]  # Black
            else:  # Available space
                colored_warehouse[i][j] = [1, 1, 1]  # White

    # Convert path points to red
    for point in path:
        colored_warehouse[point[0], point[1]] = [1, 0, 0]  # Red

    fig, ax = plt.subplots()
    ax.imshow(colored_warehouse, interpolation='nearest')

    plt.show()

# Example warehouse layout and pathfinding
warehouse_layout = np.array([
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

start = (0, 4)  # Starting position
goal = (9, 9)  # Goal position

came_from, cost_so_far = a_star_search(warehouse_layout, start, goal)
path = reconstruct_path(came_from, start, goal)
visualize_warehouse(warehouse_layout, path)