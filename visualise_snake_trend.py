import pandas as pd
import matplotlib.pyplot as plt

# Load data from Excel
df = pd.read_excel("C:/Code/SnakeAI-master/snake_fitness_log.xlsx")

# Set up figure and axes
fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot Best Fitness and Average Fitness on log scale
ax1.set_yscale("log")
ax1.plot(df["Generation"], df["Best Fitness"], label="Best Fitness", color="green", marker="o", markersize=3)
ax1.plot(df["Generation"], df["Average Fitness"], label="Average Fitness", color="blue", marker="s", markersize=3)
ax1.set_xlabel("Generation")
ax1.set_ylabel("Fitness (Log Scale)")
ax1.grid(True, which="both", linestyle='--', linewidth=0.5)

# Create secondary y-axis for Best Score (linear scale)
ax2 = ax1.twinx()
ax2.plot(df["Generation"], df["Best Score"], label="Best Score", color="orange", marker="^", markersize=3)
ax2.set_ylabel("Best Score (Linear Scale)")

# Add title and adjust layout
fig.suptitle("Snake AI Training Progress")
fig.tight_layout()
fig.subplots_adjust(top=0.9)

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# Show the plot
plt.show()
