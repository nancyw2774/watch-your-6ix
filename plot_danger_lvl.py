import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
# speed from -100 to 100 (x-axis)
# distance from 0 to 30 (y-axis)

# Define the ranges for x and y coordinates
x_min = -20
x_max = 0
y_min = 0
y_max = 30
num_points = 1000

# Generate random coordinates
random_coordinates = []
x_coords = []
y_coords = []
for _ in range(num_points):  # Adjust the number of points as needed
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    random_coordinates.append((x, y))
    x_coords.append(x*3.6)
    y_coords.append(y)

# Calculate the squared value of x^2 + y^2
colors = []
for coord in random_coordinates:
    squared_value = coord[1]**2 - coord[0]**2
    colour = "red"
    if squared_value > 300:
        colour = "green"
    elif squared_value > -10:
        colour = "yellow"
    colors.append(colour)

# Create custom legend handles and labels
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Low'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Medium'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='High')
]

# Plot the coordinates with different colors based on squared values
scatter = plt.scatter(x_coords, y_coords, c=colors, cmap='viridis')

# Add the custom legend to the plot
plt.legend(handles=legend_elements, loc='upper right')
plt.title('Danger Level Classification', fontsize = 18)
plt.ylabel('Distance (m)')
plt.xlabel('Speed (km/h)')
plt.grid(True)
plt.show()