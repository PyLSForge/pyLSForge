#!/usr/bin/env python3
"""
Visualize the Signed Distance Field for a Circle
Creates 2D slice visualizations directly from AMReX plotfile
"""

import matplotlib.pyplot as plt
import numpy as np
import amrex.space3d as amr

# Initialize AMReX
amr.initialize([])

# Read the plotfile
print("Loading plotfile...")
pltfile = "plt_sdf_circle"
ds = amr.PlotFileData(pltfile)

# Get geometry info
geom = ds.probDomain()
prob_lo = ds.probLo()
prob_hi = ds.probHi()

print(f"Domain: {prob_lo} to {prob_hi}")
print(f"Variables: {ds.varNames()}")

# Get the MultiFab data
mf = ds.get(0, 0)  # level 0, component 0
ba = mf.box_array()
dm = mf.dm()

# Extract data into numpy array
n_cell = 64
data_3d = np.zeros((n_cell, n_cell, n_cell))

for mfi in mf:
    bx = mfi.validbox()
    arr = np.array(mf.array(mfi), copy=True)
    
    # Get box bounds
    lo = bx.small_end
    hi = bx.big_end
    
    # Copy data
    data_3d[lo[2]:hi[2]+1, lo[1]:hi[1]+1, lo[0]:hi[0]+1] = arr[0, :, :, :]

print(f"Data shape: {data_3d.shape}")
print(f"Data range: [{data_3d.min():.6f}, {data_3d.max():.6f}]")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 14))

# Z-slice at center (XY plane)
z_idx = n_cell // 2
im0 = axes[0, 0].imshow(data_3d[z_idx, :, :], origin='lower', extent=[0, 1, 0, 1], 
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
im1 = axes[0, 1].imshow(data_3d[:, y_idx, :], origin='lower', extent=[0, 1, 0, 1], 
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
im2 = axes[1, 0].imshow(data_3d[:, :, x_idx], origin='lower', extent=[0, 1, 0, 1], 
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
xy_data = data_3d[z_idx, :, :]
levels = np.linspace(data_3d.min(), data_3d.max(), 20)
contourf = axes[1, 1].contourf(xy_data, levels=levels, cmap='RdBu_r', 
                                vmin=-0.3, vmax=0.3, extent=[0, 1, 0, 1])
contour_zero = axes[1, 1].contour(xy_data, levels=[0], colors='black', 
                                   linewidths=3, extent=[0, 1, 0, 1])
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
profile_y_idx = n_cell // 2
profile_z_idx = n_cell // 2
profile_data = data_3d[profile_z_idx, profile_y_idx, :]
x_coords = np.linspace(0, 1, n_cell)

ax.plot(x_coords, profile_data, 'b-', linewidth=2, label='SDF along x-axis')
ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Zero level (boundary)')
ax.axvline(x=0.25, color='green', linestyle=':', linewidth=1.5, alpha=0.7, label='Circle left edge')
ax.axvline(x=0.75, color='green', linestyle=':', linewidth=1.5, alpha=0.7, label='Circle right edge')
ax.fill_between(x_coords, profile_data, 0, where=(profile_data < 0), 
                 alpha=0.3, color='red', label='Inside circle')
ax.fill_between(x_coords, profile_data, 0, where=(profile_data >= 0), 
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
print("="*60)

# Finalize AMReX
amr.finalize()
