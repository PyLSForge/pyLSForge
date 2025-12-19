#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 The AMReX Community
#
# This file is part of AMReX.
#
# License: BSD-3-Clause-LBNL
# Authors: Revathi Jambunathan, Edoardo Zoni, Olga Shapoval, David Grote, Axel Huebl

import amrex.space3d as amr
import numpy as np

def main():
    """
    Simple heat diffusion test
    """
    xp = np
    
    # Setup domain: 32x32x32 cells
    n_cell = 32
    max_grid_size = 16
    nsteps = 10  # Just 10 steps for testing
    plot_int = 5
    dt = 1e-5

    dom_lo = amr.IntVect(*amr.d_decl(       0,        0,        0))
    dom_hi = amr.IntVect(*amr.d_decl(n_cell-1, n_cell-1, n_cell-1))
    domain = amr.Box(dom_lo, dom_hi)

    ba = amr.BoxArray(domain)
    ba.max_size(max_grid_size)

    real_box = amr.RealBox([*amr.d_decl( 0., 0., 0.)], [*amr.d_decl( 1., 1., 1.)])
    coord = 0
    is_per = [*amr.d_decl(1,1,1)]
    geom = amr.Geometry(domain, real_box, coord, is_per)
    dx = geom.data().CellSize()

    Nghost = 1
    Ncomp = 1
    dm = amr.DistributionMapping(ba)

    phi_old = amr.MultiFab(ba, dm, Ncomp, Nghost)
    phi_new = amr.MultiFab(ba, dm, Ncomp, Nghost)
    phi_old.set_val(0.)
    phi_new.set_val(0.)

    time = 0.
    ng = phi_old.n_grow_vect
    ngx, ngy, ngz = ng[0], ng[1], ng[2]

    # Initialize: phi = 1 + e^(-(r-0.5)^2/0.01)
    for mfi in phi_old:
        bx = mfi.validbox()
        phiOld = xp.array(phi_old.array(mfi), copy=False)
        x = (xp.arange(bx.small_end[0], bx.big_end[0]+1, 1) + 0.5) * dx[0]
        y = (xp.arange(bx.small_end[1], bx.big_end[1]+1, 1) + 0.5) * dx[1]
        z = (xp.arange(bx.small_end[2], bx.big_end[2]+1, 1) + 0.5) * dx[2]
        rsquared = ((z[:         , xp.newaxis, xp.newaxis] - 0.5)**2
                  + (y[xp.newaxis, :         , xp.newaxis] - 0.5)**2
                  + (x[xp.newaxis, xp.newaxis, :         ] - 0.5)**2) / 0.01
        phiOld[:, ngz:-ngz, ngy:-ngy, ngx:-ngx] = 1. + xp.exp(-rsquared)

    amr.Print('Heat equation simulation initialized\n')
    amr.Print(f'Domain: {n_cell}^3 cells\n')
    amr.Print(f'Steps: {nsteps}, dt: {dt}\n')

    # Time stepping
    for step in range(1, nsteps+1):
        phi_old.fill_boundary(geom.periodicity())

        for mfi in phi_old:
            phiOld = xp.array(phi_old.array(mfi), copy=False)
            phiNew = xp.array(phi_new.array(mfi), copy=False)
            hix, hiy, hiz = phiOld.shape[3], phiOld.shape[2], phiOld.shape[1]
            
            phiNew[:, ngz:-ngz, ngy:-ngy, ngx:-ngx] = (
                phiOld[:, ngz:-ngz, ngy:-ngy, ngx:-ngx]
                + dt*((   phiOld[:, ngz:-ngz, ngy:-ngy, ngx+1:hix-ngx+1]
                       -2*phiOld[:, ngz:-ngz, ngy:-ngy, ngx  :-ngx     ]
                         +phiOld[:, ngz:-ngz, ngy:-ngy, ngx-1:hix-ngx-1]) / dx[0]**2
                     +(   phiOld[:, ngz:-ngz, ngy+1:hiy-ngy+1, ngx:-ngx]
                       -2*phiOld[:, ngz:-ngz, ngy  :-ngy     , ngx:-ngx]
                         +phiOld[:, ngz:-ngz, ngy-1:hiy-ngy-1, ngx:-ngx]) / dx[1]**2
                     +(   phiOld[:, ngz+1:hiz-ngz+1, ngy:-ngy, ngx:-ngx]
                       -2*phiOld[:, ngz  :-ngz     , ngy:-ngy, ngx:-ngx]
                         +phiOld[:, ngz-1:hiz-ngz-1, ngy:-ngy, ngx:-ngx]) / dx[2]**2))

        time += dt
        amr.copy_mfab(dst=phi_old, src=phi_new, srccomp=0, dstcomp=0, numcomp=1, nghost=0)
        amr.Print(f'Advanced step {step}\n')

    amr.Print('Heat equation simulation completed successfully!\n')

if __name__ == '__main__':
    amr.initialize([])
    main()
    amr.finalize()
