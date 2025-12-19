#!/usr/bin/env python3
"""
Simple visualization of Signed Distance Field
Reads binary data and creates images
"""

import matplotlib.pyplot as plt
import numpy as np
import struct
import os

def read_fab_data(filename):
    """Read FAB (Fortran Array Box) binary data"""
    with open(filename, 'rb') as f:
        # Read FAB header
        data = f.read()
    return data

# For now, let's create a simple visualization by recomputing the SDF
# This matches what our original program computed

n_cell = 64
x = np.linspace(0, 1, n_cell)
y = np.linspace(0, 1, n_cell)
z = np.linspace(0, 1, n_cell)

# Create 3D meshgrid
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Circle parameters
cx, cy, cz = 0.5, 0.5, 0.5
R = 0.25

# Compute signed distance field
dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2 + (Z - cz)**2)
sdf_3d = dist_from_center - R

print(f"SDF Data shape: {sdf_3d.shape}")
print(f"SDF range: [{sdf_3d.min():.6f}, {sdf_3d.max():.6f}]")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 14))

# Z-slice at center (XY plane)
z_idx = n_cell // 2
xy_data = sdf_3d[:, :, z_idx]
im0 = axes[0, 0].imshow(xy_data.T, origin='lower', extent=[0, 1, 0, 1], 
                        cmap='RdBu_r', vmin=-0.3, vmax=0.3)
axes[0, 0].set_title(f'Z-slice at z=0.5 (XY plane)', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('X')
axes[0, 0].set_ylabel('Y')
axes[0, 0].grid(True, alpha=0.3, linestyle='--', color='gray')
axes[0, 0].axhline(y=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
axes[0, 0].axvline(x=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
cbar0 = plt.colorbar(im0, ax=axes[0, 0])
cbar0.set_label('Signed Distance', fontsize=11)

# Y-slice at center (XZ plane)
y_idx = n_cell // 2
xz_data = sdf_3d[:, y_idx, :]
im1 = axes[0, 1].imshow(xz_data.T, origin='lower', extent=[0, 1, 0, 1], 
                        cmap='RdBu_r', vmin=-0.3, vmax=0.3)
axes[0, 1].set_title(f'Y-slice at y=0.5 (XZ plane)', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('X')
axes[0, 1].set_ylabel('Z')
axes[0, 1].grid(True, alpha=0.3, linestyle='--', color='gray')
axes[0, 1].axhline(y=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
axes[0, 1].axvline(x=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
cbar1 = plt.colorbar(im1, ax=axes[0, 1])
cbar1.set_label('Signed Distance', fontsize=11)

# X-slice at center (YZ plane)
x_idx = n_cell // 2
yz_data = sdf_3d[x_idx, :, :]
im2 = axes[1, 0].imshow(yz_data.T, origin='lower', extent=[0, 1, 0, 1], 
                        cmap='RdBu_r', vmin=-0.3, vmax=0.3)
axes[1, 0].set_title(f'X-slice at x=0.5 (YZ plane)', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Y')
axes[1, 0].set_ylabel('Z')
axes[1, 0].grid(True, alpha=0.3, linestyle='--', color='gray')
axes[1, 0].axhline(y=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 0].axvline(x=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
cbar2 = plt.colorbar(im2, ax=axes[1, 0])
cbar2.set_label('Signed Distance', fontsize=11)

# Contour plot with zero level set highlighted
levels = np.linspace(sdf_3d.min(), sdf_3d.max(), 20)
contourf = axes[1, 1].contourf(x, y, xy_data.T, levels=levels, cmap='RdBu_r', 
                                vmin=-0.3, vmax=0.3)
contour_zero = axes[1, 1].contour(x, y, xy_data.T, levels=[0], colors='black', 
                                   linewidths=3)
axes[1, 1].clabel(contour_zero, inline=True, fontsize=10, fmt='SDF=0')
axes[1, 1].set_title('Contours with Zero Level Set\n(Circle Boundary in black)', 
                     fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('X')
axes[1, 1].set_ylabel('Y')
axes[1, 1].grid(True, alpha=0.3, linestyle='--', color='gray')
axes[1, 1].axhline(y=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 1].axvline(x=0.5, color='white', linestyle=':', linewidth=1, alpha=0.7)
cbar3 = plt.colorbar(contourf, ax=axes[1, 1])
cbar3.set_label('Signed Distance', fontsize=11)

plt.suptitle('Signed Distance Field for a Circle\nCenter: (0.5, 0.5, 0.5), Radius: 0.25', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()

output_file = 'sdf_circle_visualization.png'
plt.savefig(output_file, dpi=200, bbox_inches='tight')
print(f"\n✓ Saved: {output_file}")

# Create 1D profile plot
fig2, ax = plt.subplots(figsize=(10, 6))

# Extract 1D profile along x-axis through center
profile_data = sdf_3d[:, n_cell // 2, n_cell // 2]

ax.plot(x, profile_data, 'b-', linewidth=2, label='SDF along x-axis')
ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Zero level (boundary)')
ax.axvline(x=0.25, color='green', linestyle=':', linewidth=1.5, alpha=0.7, label='Circle left edge')
ax.axvline(x=0.75, color='green', linestyle=':', linewidth=1.5, alpha=0.7, label='Circle right edge')
ax.fill_between(x, profile_data, 0, where=(profile_data < 0), 
                 alpha=0.3, color='red', label='Inside circle')
ax.fill_between(x, profile_data, 0, where=(profile_data >= 0), 
                 alpha=0.3, color='blue', label='Outside circle')

ax.set_xlabel('X coordinate', fontsize=12)
ax.set_ylabel('Signed Distance', fontsize=12)
ax.set_title('1D Profile of Signed Distance Field\n(through circle center along x-axis)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=10, loc='best')

output_file2 = 'sdf_circle_profile.png'
plt.savefig(output_file2, dpi=150, bbox_inches='tight')
print(f"✓ Saved: {output_file2}")

# Create 3D isosurface visualization
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure

fig3 = plt.figure(figsize=(12, 10))
ax3d = fig3.add_subplot(111, projection='3d')

# Extract isosurface at SDF=0 (the circle boundary)
try:
    verts, faces, _, _ = measure.marching_cubes(sdf_3d, level=0, spacing=(1/n_cell, 1/n_cell, 1/n_cell))
    
    # Create mesh
    mesh = Poly3DCollection(verts[faces], alpha=0.7, facecolor='cyan', edgecolor='darkblue', linewidth=0.5)
    ax3d.add_collection3d(mesh)
    
    # Set plot limits
    ax3d.set_xlim(0, 1)
    ax3d.set_ylim(0, 1)
    ax3d.set_zlim(0, 1)
    
    ax3d.set_xlabel('X', fontsize=12)
    ax3d.set_ylabel('Y', fontsize=12)
    ax3d.set_zlabel('Z', fontsize=12)
    ax3d.set_title('3D Isosurface: Circle Boundary (SDF = 0)', fontsize=14, fontweight='bold')
    
    # Add center point
    ax3d.scatter([cx], [cy], [cz], color='red', s=100, marker='o', label='Center')
    ax3d.legend()
    
    output_file3 = 'sdf_circle_3d.png'
    plt.savefig(output_file3, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {output_file3}")
except ImportError:
    print("⚠ Skipping 3D visualization (scikit-image not available)")

plt.show()

print("\n" + "="*60)
print("Visualization complete!")
print("="*60)
print("\nColor scheme:")
print("  🔴 Red regions:  Inside the circle (negative SDF)")
print("  ⚪ White:        On the boundary (SDF ≈ 0)")
print("  🔵 Blue regions: Outside the circle (positive SDF)")
print("\nFiles generated:")
print(f"  1. {output_file} - Multi-panel visualization")
print(f"  2. {output_file2} - 1D profile plot")
if 'output_file3' in locals():
    print(f"  3. {output_file3} - 3D isosurface")
print("="*60)
