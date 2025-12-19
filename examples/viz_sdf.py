#!/usr/bin/env python3
"""
Simple visualization of the signed distance field
"""
import numpy as np
import matplotlib.pyplot as plt

# Create data matching our SDF calculation
n = 64
x = np.linspace(0, 1, n)
y = np.linspace(0, 1, n)

# Circle parameters
cx, cy, cz = 0.5, 0.5, 0.5
radius = 0.25

# Create 2D slice at z=0.5 (middle of domain)
X, Y = np.meshgrid(x, y)
Z_slice = 0.5
dist = np.sqrt((X - cx)**2 + (Y - cy)**2 + (Z_slice - cz)**2)
sdf_slice = dist - radius

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Signed distance field
im1 = axes[0].contourf(X, Y, sdf_slice, levels=20, cmap='RdBu_r')
axes[0].contour(X, Y, sdf_slice, levels=[0], colors='black', linewidths=2)
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].set_title('Signed Distance Field (z=0.5 slice)')
axes[0].set_aspect('equal')
plt.colorbar(im1, ax=axes[0], label='Distance')

# Plot 2: Binary (inside/outside)
binary = np.where(sdf_slice < 0, 1, 0)
im2 = axes[1].contourf(X, Y, binary, levels=[0, 0.5, 1], cmap='RdYlGn')
axes[1].contour(X, Y, sdf_slice, levels=[0], colors='black', linewidths=2)
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
axes[1].set_title('Inside (green) vs Outside (red)')
axes[1].set_aspect('equal')
plt.colorbar(im2, ax=axes[1], label='Region')

plt.tight_layout()
plt.savefig('sdf_circle_visualization.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualization saved to: sdf_circle_visualization.png")
print("\nThe visualization shows:")
print("  - Left: Signed distance field (blue=inside, red=outside)")
print("  - Right: Binary regions (green=inside circle, red=outside)")
print("  - Black contour: Circle boundary (SDF=0)")
print("\nStatistics:")
print(f"  Min SDF: {sdf_slice.min():.4f}")
print(f"  Max SDF: {sdf_slice.max():.4f}")
print(f"  Cells inside: {np.sum(sdf_slice < 0)} ({100*np.sum(sdf_slice < 0)/sdf_slice.size:.1f}%)")
print(f"  Cells outside: {np.sum(sdf_slice > 0)} ({100*np.sum(sdf_slice > 0)/sdf_slice.size:.1f}%)")
