Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import random
from queue import PriorityQueue

class GridWorld:
    def __init__(self, size):
        self.size = size
        self.initial_pos = (1, 1)
        self.goal_pos = (1, 1)
        self.wumpus = None
        self.pit = None
        self.found_wumpus = False
        self.found_pit = False
        self.wumpus_position = None
        self.pit_position = None
        self.actions = []

    def initialize_world(self):
        # Set random positions for wumpus and pit
        self.wumpus = (random.randint(1, self.size), random.randint(1, self.size))
        self.pit = (random.randint(1, self.size), random.randint(1, self.size))

    def heuristic(self, pos):
        # Manhattan distance heuristic
        return abs(self.goal_pos[0] - pos[0]) + abs(self.goal_pos[1] - pos[1])

    def construct_path(self, start, goal, came_from):
        path = []
        current = goal
        while current != start:
            path.append(came_from[current])
            current = came_from[current]
        path.reverse()
        return path

    def search(self):
        # Run A* search
        open_set = PriorityQueue()
        open_set.put((0, self.initial_pos))
        came_from = {}
        g_score = {self.initial_pos: 0}
        f_score = {self.initial_pos: self.heuristic(self.initial_pos)}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == self.goal_pos:
                self.actions.extend(self.construct_path(self.initial_pos, self.goal_pos, came_from))
                break

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    open_set.put((f_score[neighbor], neighbor))

            # Check if the wumpus or pit is found
            if current == self.wumpus:
                self.found_wumpus = True
                self.wumpus_position = current
            elif current == self.pit:
                self.found_pit = True
                self.pit_position = current

            # If either wumpus or pit is found, return to the initial position and stop searching
            if self.found_wumpus or self.found_pit:
                self.actions.append("TurnAround")  # Turn around to face the opposite direction
                self.actions.extend(self.construct_path(current, self.initial_pos, came_from))  # Go back to the initial position
                break

    def get_neighbors(self, pos):
        neighbors = []
        x, y = pos
        if x > 1:
...             neighbors.append((x - 1, y))
...         if x < self.size:
...             neighbors.append((x + 1, y))
...         if y > 1:
...             neighbors.append((x, y - 1))
...         if y < self.size:
...             neighbors.append((x, y + 1))
...         return neighbors
... 
...     def execute_actions(self):
...         for action in self.actions:
...             print(action)
... 
...     def visualize_path(self):
...         grid = [['-' for _ in range(self.size)] for _ in range(self.size)]
...         for action in self.actions:
...             if action == "GoForward":
...                 grid[self.initial_pos[0] - 1][self.initial_pos[1] - 1] = 'A'
...                 self.move_forward()
...             elif action == "TurnLeft":
...                 self.turn_left()
...             elif action == "TurnRight":
...                 self.turn_right()
...             elif action == "TurnAround":
...                 self.turn_around()
... 
...         grid[self.initial_pos[0] - 1][self.initial_pos[1] - 1] = 'A'
...         grid[self.goal_pos[0] - 1][self.goal_pos[1] - 1] = 'G'
...         if self.found_wumpus:
...             grid[self.wumpus[0] - 1][self.wumpus[1] - 1] = 'W'
...         if self.found_pit:
...             grid[self.pit[0] - 1][self.pit[1] - 1] = 'P'
... 
...         for row in grid:
...             print(' '.join(row))
... 
...     def move_forward(self):
...         if self.initial_pos[1] < self.size:
...             self.initial_pos = (self.initial_pos[0], self.initial_pos[1] + 1)
... 
    def turn_left(self):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        current_direction = directions.index((1, 0))
        new_direction = (current_direction + 1) % 4
        self.initial_pos = (self.initial_pos[0] + directions[new_direction][0], self.initial_pos[1] + directions[new_direction][1])

    def turn_right(self):
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        current_direction = directions.index((1, 0))
        new_direction = (current_direction - 1) % 4
        self.initial_pos = (self.initial_pos[0] + directions[new_direction][0], self.initial_pos[1] + directions[new_direction][1])

    def turn_around(self):
        self.turn_left()
        self.turn_left()


# Initialize and run the search
world = GridWorld(4)
world.initialize_world()
world.search()
world.execute_actions()
