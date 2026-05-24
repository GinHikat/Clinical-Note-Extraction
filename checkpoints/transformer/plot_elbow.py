import pandas as pd
import matplotlib.pyplot as plt

# Load data
csv_path = '/home/hngoc/gin/Clinical-Note-Extraction/checkpoints/transformer/clustering_sweep_patient_summary.csv'
df = pd.read_csv(csv_path)

# Set up beautiful aesthetic style
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)

# Sleek and premium color palette
primary_color = '#4361EE'    # Royal Indigo for Inertia
secondary_color = '#F72585'  # Vivid Coral/Pink for Silhouette
grid_color = '#E9ECEF'       # Light grey gridlines

# Plot Inertia (SSE) on ax1 (Left Y-axis)
ax1.set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('Inertia (Within-Cluster Sum of Squares)', color=primary_color, fontsize=12, fontweight='bold', labelpad=10)
line1 = ax1.plot(df['K'], df['Inertia'], marker='o', color=primary_color, linewidth=2.5, markersize=8, label='Inertia (SSE)', linestyle='-')
ax1.tick_params(axis='y', labelcolor=primary_color)
ax1.grid(True, linestyle='--', alpha=0.5, color=grid_color)

# Plot Silhouette Score on ax2 (Right Y-axis, Dual Axis)
ax2 = ax1.twinx()
ax2.set_ylabel('Silhouette Score', color=secondary_color, fontsize=12, fontweight='bold', labelpad=10)
line2 = ax2.plot(df['K'], df['Silhouette'], marker='s', color=secondary_color, linewidth=2.5, markersize=8, label='Silhouette Score', linestyle='--')
ax2.tick_params(axis='y', labelcolor=secondary_color)
ax2.grid(False)  # Avoid overlapping gridlines

# Title and Design
plt.title('Optimal K Selection: Elbow Method & Silhouette Analysis', fontsize=14, fontweight='bold', pad=15)

# Align and display legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', frameon=True, facecolor='white', edgecolor=grid_color)

# Ensure clean layout
plt.tight_layout()

# Save image
output_path = '/home/hngoc/gin/Clinical-Note-Extraction/checkpoints/transformer/elbow_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot successfully saved to {output_path}")
