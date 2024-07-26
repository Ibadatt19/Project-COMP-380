import tkinter as tk
import random

# Define the Grassfire algorithm 


def grassfire_algorithm(start, goal, obstacles, grid_size, app):
    # Initialize the grid with 'inf' for empty cells and -1 for obstacles
    grid = [[float('inf') if (r, c) not in obstacles else -1 for c in range(grid_size[1])] for r in range(grid_size[0])]
    grid[start[0]][start[1]] = 0  # Set the starting position to 0

    # List to keep track of cells to visit in ths queue, starting with the start cell
    Start_by_visiting = [start]

    def spread_fire():
        if Start_by_visiting:
            r, c = Start_by_visiting.pop(0)
            for dir_row, dir_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: Up, Down, Left, Right (No digonal direction should be used here)
                rr, cc = r + dir_row, c + dir_col
                if 0 <= rr < grid_size[0] and 0 <= cc < grid_size[1]:
                    if grid[rr][cc] == float('inf'):
                        grid[rr][cc] = grid[r][c] + 1
                        Start_by_visiting.append((rr, cc))
                        app.visualize_fire(rr, cc, grid[rr][cc])
            app.after(100, spread_fire)
        else:
            app.retrace_path(grid, start, goal)

    # Start the fire spreading process
    spread_fire()


# GUI Application
class GrassfireApp(tk.Tk):
    def __init__(self): # dunder used for intitialising the attributes of an object when instance of a class is created.
        super().__init__()
        self.title('Grassfire Algorithm Simulation')

        # Initialize the application variables
        self.grid_size = (8, 8)  # Default grid size
        self.start = (0, 0)  # Default starting position
        self.goal = (7, 7)  # Default goal position
        self.obstacles = []  # List to hold obstacle coordinates
        self.cells = {}  # Dictionary to hold cell widgets

        # Set up user input fields for grid size, obstacles, start, and goal
        self.setup_input_fields()

        # Button to generate grid and run algorithm
        self.run_button = tk.Button(self, text='Run', command=self.run_simulation)
        self.run_button.pack()

        # Canvas to draw the grid
        self.canvas = tk.Canvas(self, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.after(100, self.update_canvas_size)  # Delay to update canvas size based on window

    def setup_input_fields(self):
        # Create input fields for grid size, obstacle percentage, start, and goal
        self.size_entry = self.create_entry('8x8', 'Grid Size')
        self.obstacle_entry = self.create_entry('15%', 'Obstacle % ')
        self.start_entry = self.create_entry('0,0', 'Start Position ')
        self.goal_entry = self.create_entry('7,7', 'Goal Position ')

    def create_entry(self, default, label):
        # Helper function to create labeled entry fields
        frame = tk.Frame(self)
        label = tk.Label(frame, text=label)
        label.pack(side=tk.LEFT, padx=50)
        entry = tk.Entry(frame, width=70)
        entry.insert(0, default)
        entry.pack(side=tk.LEFT)
        frame.pack()
        return entry

    def update_canvas_size(self):
        self.canvas.config(width=self.winfo_width(), height=self.winfo_height())
        self.cell_width = self.canvas.winfo_width() // self.grid_size[1] 
        self.cell_height = self.canvas.winfo_height() // self.grid_size[0] 
        self.draw_grid()


    def visualize_fire(self, r, c, value):
        if (r, c) != self.start and (r, c) != self.goal:
            cell = self.cells[(r, c)]
            self.canvas.itemconfig(cell, fill='black')
            # Update text on the cell
            self.canvas.itemconfig(self.cell_texts[(r, c)], text=str(value), fill='white')
        self.canvas.update()


    def retrace_path(self, grid, start, goal):
        # Backtrack from the goal to the start to find the shortest path
        path = []
        r, c = goal
        if grid[r][c] == float('inf'):
            print("No path found")
            return  # No path found
        while (r, c) != start:
            path.append((r, c))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.grid_size[0] and 0 <= cc < self.grid_size[1] and grid[rr][cc] == grid[r][c] - 1:
                    r, c = rr, cc
                    break
        path.append(start)
        path.reverse()  # The path is reversed so that it starts from the start node

        # Visualize the shortest path
        for r, c in path:
            self.visualize_path(r, c)
        self.canvas.update()  # Update the canvas to show the path

    def visualize_path(self, r, c):
        # Change the color of the cells in the path to visualize it
        # Avoid changing the color of the start and goal nodes
        if (r, c) != self.start and (r, c) != self.goal:
            cell = self.cells[(r, c)]
            self.canvas.itemconfig(cell, fill='magenta')  # Blue color for the shortest path

    def run_simulation(self):
    # Parse user input and set up the grid and obstacles
        self.parse_user_input()
        self.canvas.delete('all')  # Clear the canvas before drawing a new grid
        self.draw_grid()

        # Check if the start and goal positions are valid according to the assignment's requirements
        if self.start[0] != 0:
            print("Start position must be in the first row.")
            return
        if self.goal[0] <= self.grid_size[0] // 2 or self.goal[1] <= (2 * self.grid_size[1]) // 3:
            print("Goal position must be greater than half the number of rows and two-thirds the number of columns.")
            return

        # Avoid placing obstacles in the start and goal cells
        self.obstacles = [obst for obst in self.obstacles if obst != self.start and obst != self.goal]

        # Run the Grassfire algorithm
        grassfire_algorithm(self.start, self.goal, self.obstacles, self.grid_size, self)

    def parse_user_input(self):
        # Convert user input into usable data
        self.grid_size = tuple(map(int, self.size_entry.get().split('x')))
        obstacle_percentage = float(self.obstacle_entry.get().strip('%')) / 100
        self.start = tuple(map(int, self.start_entry.get().split(',')))
        self.goal = tuple(map(int, self.goal_entry.get().split(',')))

        # Generate obstacles based on the user-defined percentage
        num_obstacles = int(self.grid_size[0] * self.grid_size[1] * obstacle_percentage)
        self.obstacles = [(random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1)) for _ in range(num_obstacles)]

    def draw_grid(self):
        # Calculate cell width and height based on the canvas size and grid size
        self.cell_width = self.canvas.winfo_width() // self.grid_size[1]
        self.cell_height = self.canvas.winfo_height() // self.grid_size[0]
        self.cell_texts = {}  # Initialize dictionary to store text objects for updating later

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                # Calculate coordinates for each cell
                x1, y1 = col * self.cell_width, row * self.cell_height
                x2, y2 = x1 + self.cell_width, y1 + self.cell_height
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill='pink', tags='cell')
                self.cells[(row, col)] = cell

                # Set default text content and color
                text_content = ''
                text_color = 'red'

                # Update the cell color and text if it's the start or goal cell
                if (row, col) == self.start:
                    self.canvas.itemconfig(cell, fill='green')
                    text_content = 'START'
                    text_color = 'white'
                elif (row, col) == self.goal:
                    self.canvas.itemconfig(cell, fill='red')
                    text_content = 'GOAL'
                    text_color = 'white'
                elif (row, col) in self.obstacles:
                    self.canvas.itemconfig(cell, fill='grey')

                # Create text in the cell
                text = self.canvas.create_text(
                    x1 + self.cell_width / 2, 
                    y1 + self.cell_height / 2,
                    text=text_content, fill=text_color)
                self.cell_texts[(row, col)] = text


if __name__ == '__main__':
    GrassfireApp().mainloop()