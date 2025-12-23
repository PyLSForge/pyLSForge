#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signed Distance Field for a Circle using pyAMReX

This program computes the signed distance field for a circle in 3D space.
The signed distance function (SDF) gives:
- Negative values inside the circle
- Zero on the circle boundary
- Positive values outside the circle

For a circle centered at (cx, cy, cz) with radius R:
SDF(x, y, z) = sqrt((x-cx)^2 + (y-cy)^2 + (z-cz)^2) - R

Author: TanishyadavNSUT
Date: December 2025
"""

import amrex.space3d as amr
import numpy as np


def compute_signed_distance_field(n_cell=64, max_grid_size=32, 
                                   center=(0.5, 0.5, 0.5), radius=0.25):
    """
    Compute signed distance field for a circle.
    
    Parameters:
    -----------
    n_cell : int
        Number of cells in each direction
    max_grid_size : int
        Maximum size of each grid block
    center : tuple
        Center of the circle (cx, cy, cz)
    radius : float
        Radius of the circle
    """
    xp = np
    
    # Setup computational domain
    dom_lo = amr.IntVect(*amr.d_decl(0, 0, 0))
    dom_hi = amr.IntVect(*amr.d_decl(n_cell-1, n_cell-1, n_cell-1))
    domain = amr.Box(dom_lo, dom_hi)
    
    # Create BoxArray and break into chunks
    ba = amr.BoxArray(domain)
    ba.max_size(max_grid_size)
    
    # Define physical domain [0, 1]^3
    real_box = amr.RealBox([*amr.d_decl(0., 0., 0.)], [*amr.d_decl(1., 1., 1.)])
    
    # Create geometry (Cartesian, non-periodic)
    coord = 0  # Cartesian coordinates
    is_per = [*amr.d_decl(0, 0, 0)]  # Non-periodic
    geom = amr.Geometry(domain, real_box, coord, is_per)
    
    # Get cell spacing
    dx = geom.data().CellSize()
    
    # Create MultiFab to store the signed distance field
    Nghost = 0  # No ghost cells needed for this calculation
    Ncomp = 1   # One component (signed distance)
    dm = amr.DistributionMapping(ba)
    
    sdf_mf = amr.MultiFab(ba, dm, Ncomp, Nghost)
    
    # Extract circle parameters
    cx, cy, cz = center
    R = radius
    
    amr.Print(f'\n{"="*60}\n')
    amr.Print(f'Computing Signed Distance Field for a Circle\n')
    amr.Print(f'{"="*60}\n')
    amr.Print(f'Domain: [{n_cell}^3] cells\n')
    amr.Print(f'Physical domain: [0, 1]^3\n')
    amr.Print(f'Circle center: ({cx:.3f}, {cy:.3f}, {cz:.3f})\n')
    amr.Print(f'Circle radius: {R:.3f}\n')
    amr.Print(f'Cell size: dx = {dx[0]:.6f}\n')
    amr.Print(f'{"="*60}\n\n')
    
    # Compute signed distance field
    amr.Print('Computing SDF values...\n')
    
    for mfi in sdf_mf:
        bx = mfi.validbox()
        sdf_array = xp.array(sdf_mf.array(mfi), copy=False)
        
        # Get cell-centered coordinates
        x = (xp.arange(bx.small_end[0], bx.big_end[0]+1, 1) + 0.5) * dx[0]
        y = (xp.arange(bx.small_end[1], bx.big_end[1]+1, 1) + 0.5) * dx[1]
        z = (xp.arange(bx.small_end[2], bx.big_end[2]+1, 1) + 0.5) * dx[2]
        
        # Create 3D meshgrid
        # Note: AMReX arrays are indexed as [component, z, y, x]
        zz = z[:, xp.newaxis, xp.newaxis]
        yy = y[xp.newaxis, :, xp.newaxis]
        xx = x[xp.newaxis, xp.newaxis, :]
        
        # Compute distance from circle center
        dist_from_center = xp.sqrt((xx - cx)**2 + (yy - cy)**2 + (zz - cz)**2)
        
        # Signed distance: negative inside, positive outside
        sdf_array[0, :, :, :] = dist_from_center - R
    
    # Compute statistics
    sdf_min = sdf_mf.min(0)
    sdf_max = sdf_mf.max(0)
    sdf_sum = sdf_mf.sum(0)
    sdf_norm = sdf_mf.norm0(0, 0, False, False)
    
    amr.Print('SDF computation complete!\n\n')
    amr.Print(f'Statistics:\n')
    amr.Print(f'  Min SDF value: {sdf_min:.6f} (deepest inside)\n')
    amr.Print(f'  Max SDF value: {sdf_max:.6f} (farthest outside)\n')
    amr.Print(f'  Sum of SDF values: {sdf_sum:.6f}\n')
    amr.Print(f'  L-infinity norm: {sdf_norm:.6f}\n\n')
    
    # Write plotfile for visualization
    pltfile = 'plt_sdf_circle'
    varnames = amr.Vector_string(['signed_distance'])
    amr.write_single_level_plotfile(pltfile, sdf_mf, varnames, geom, 0.0, 0)
    
    amr.Print(f'Plotfile written to: {pltfile}\n')
    amr.Print(f'Visualize with VisIt or ParaView\n\n')
    
    # Count cells inside, on boundary, and outside
    count_inside = 0
    count_boundary = 0
    count_outside = 0
    tolerance = 2 * dx[0]  # Boundary thickness (2 cells)
    
    for mfi in sdf_mf:
        sdf_array = xp.array(sdf_mf.array(mfi), copy=False)
        count_inside += xp.sum(sdf_array[0] < -tolerance)
        count_boundary += xp.sum(xp.abs(sdf_array[0]) <= tolerance)
        count_outside += xp.sum(sdf_array[0] > tolerance)
    
    total_cells = n_cell**3
    amr.Print(f'Cell distribution:\n')
    amr.Print(f'  Inside circle: {count_inside} cells ({100*count_inside/total_cells:.2f}%)\n')
    amr.Print(f'  On boundary: {count_boundary} cells ({100*count_boundary/total_cells:.2f}%)\n')
    amr.Print(f'  Outside circle: {count_outside} cells ({100*count_outside/total_cells:.2f}%)\n')
    amr.Print(f'{"="*60}\n')
    
    return sdf_mf, geom


def main():
    """
    Main function to run the signed distance field computation.
    """
    # Parameters
    n_cell = 64           # Grid resolution
    max_grid_size = 32    # Max grid block size
    center = (0.5, 0.5, 0.5)  # Circle center
    radius = 0.25         # Circle radius
    
    # Compute SDF
    sdf_mf, geom = compute_signed_distance_field(
        n_cell=n_cell,
        max_grid_size=max_grid_size,
        center=center,
        radius=radius
    )
    
    amr.Print('\nProgram completed successfully!\n\n')


if __name__ == '__main__':
    # Initialize AMReX
    amr.initialize([])
    
    # Run main computation
    main()
    
    # Finalize AMReX
    amr.finalize()
