#!/usr/bin/env python3
"""
Create animation of heat diffusion simulation
Shows how heat diffuses over time
"""

import yt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
import glob
import os

# Find all plotfiles
plotfiles = sorted(glob.glob("plt[0-9]*"))
if not plotfiles:
    print("No plotfiles found!")
    exit(1)

print(f"Found {len(plotfiles)} plotfiles: {plotfiles[0]} to {plotfiles[-1]}")

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Get initial data for setup
ds0 = yt.load(plotfiles[0])
slc0 = ds0.slice('z', 0.5)
frb0 = slc0.to_frb((1.0, 'code_length'), 256)
data0 = np.array(frb0[('boxlib', 'phi')])

# Find min/max for colorbar across all timesteps
vmin, vmax = data0.min(), data0.max()

im = ax.imshow(data0.T, origin='lower', extent=[0, 1, 0, 1], 
               cmap='hot', vmin=vmin, vmax=vmax)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
cbar = plt.colorbar(im, ax=ax, label='Temperature')
title = ax.set_title('Heat Diffusion - Step 0', fontsize=14, fontweight='bold')

def update(frame):
    """Update function for animation"""
    ds = yt.load(plotfiles[frame])
    slc = ds.slice('z', 0.5)
    frb = slc.to_frb((1.0, 'code_length'), 256)
    data = np.array(frb[('boxlib', 'phi')])
    
    im.set_array(data.T)
    title.set_text(f'Heat Diffusion - Step {frame * 100}')
    return [im, title]

# Create animation
print("Creating animation...")
ani = FuncAnimation(fig, update, frames=len(plotfiles), 
                   interval=200, blit=True, repeat=True)

# Save as GIF
output_file = 'heat_diffusion_animation.gif'
writer = PillowWriter(fps=5)
ani.save(output_file, writer=writer)
print(f"Animation saved as: {output_file}")
print(f"Total frames: {len(plotfiles)}")

plt.close()

# Create a comparison figure showing start and end
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Initial state
ds_start = yt.load(plotfiles[0])
slc_start = ds_start.slice('z', 0.5)
frb_start = slc_start.to_frb((1.0, 'code_length'), 256)
data_start = np.array(frb_start[('boxlib', 'phi')])

im0 = axes[0].imshow(data_start.T, origin='lower', extent=[0, 1, 0, 1], 
                     cmap='hot', vmin=1, vmax=data_start.max())
axes[0].set_title(f'Initial State (Step 0)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('X')
axes[0].set_ylabel('Y')
axes[0].grid(True, alpha=0.3)
plt.colorbar(im0, ax=axes[0], label='Temperature')

# Middle state
mid_idx = len(plotfiles) // 2
ds_mid = yt.load(plotfiles[mid_idx])
slc_mid = ds_mid.slice('z', 0.5)
frb_mid = slc_mid.to_frb((1.0, 'code_length'), 256)
data_mid = np.array(frb_mid[('boxlib', 'phi')])

im1 = axes[1].imshow(data_mid.T, origin='lower', extent=[0, 1, 0, 1], 
                     cmap='hot', vmin=1, vmax=data_start.max())
axes[1].set_title(f'Middle State (Step {mid_idx * 100})', fontsize=14, fontweight='bold')
axes[1].set_xlabel('X')
axes[1].set_ylabel('Y')
axes[1].grid(True, alpha=0.3)
plt.colorbar(im1, ax=axes[1], label='Temperature')

# Final state
ds_end = yt.load(plotfiles[-1])
slc_end = ds_end.slice('z', 0.5)
frb_end = slc_end.to_frb((1.0, 'code_length'), 256)
data_end = np.array(frb_end[('boxlib', 'phi')])

im2 = axes[2].imshow(data_end.T, origin='lower', extent=[0, 1, 0, 1], 
                     cmap='hot', vmin=1, vmax=data_start.max())
axes[2].set_title(f'Final State (Step {(len(plotfiles)-1) * 100})', 
                  fontsize=14, fontweight='bold')
axes[2].set_xlabel('X')
axes[2].set_ylabel('Y')
axes[2].grid(True, alpha=0.3)
plt.colorbar(im2, ax=axes[2], label='Temperature')

plt.suptitle('Heat Diffusion Simulation - Evolution Over Time', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('heat_diffusion_comparison.png', dpi=150, bbox_inches='tight')
print("Saved: heat_diffusion_comparison.png")
print("\nVisualization complete!")
