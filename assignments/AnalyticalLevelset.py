import amrex.space2d as amr
import numpy as np
import matplotlib.pyplot as plt


def main():
    # ------------------------------------------------------------
    # 1. Initialize AMReX
    # ------------------------------------------------------------
    amr.initialize([])

    if amr.Config.spacedim != 2:
        print("ERROR: pyAMReX not built in 2D")
        amr.finalize()
        return

    # ------------------------------------------------------------
    # 2. Grid & Geometry
    # ------------------------------------------------------------
    n = 128
    max_grid_size = 64

    prob_lo = [0.0, 0.0]
    prob_hi = [1.0, 1.0]

    real_box = amr.RealBox(prob_lo, prob_hi)

    domain = amr.Box(
        np.array([0, 0]),
        np.array([n - 1, n - 1])
    )

    geom = amr.Geometry(domain, real_box, 0, [0, 0])

    ba = amr.BoxArray(domain)
    ba.max_size(max_grid_size)
    dm = amr.DistributionMapping(ba)

    # ------------------------------------------------------------
    # 3. MultiFab (1 component, no ghost cells)
    # ------------------------------------------------------------
    sdf = amr.MultiFab(ba, dm, 1, 0)
    sdf.set_val(0.0)

    dx = geom.data().CellSize()

    # ------------------------------------------------------------
    # 4. Analytical Circle SDF
    # ------------------------------------------------------------
    center = np.array([0.5, 0.5])
    radius = 0.25

    print("Computing analytical SDF for circle...")

    for mfi in sdf:
        arr = sdf.array(mfi).to_numpy()  # shape: (ny, nx, 1, 1)
        bx = mfi.validbox()

        i_lo, j_lo = bx.lo_vect
        i_hi, j_hi = bx.hi_vect

        i = np.arange(i_lo, i_hi + 1)
        j = np.arange(j_lo, j_hi + 1)

        x = (i + 0.5) * dx[0]
        y = (j + 0.5) * dx[1]

        Y, X = np.meshgrid(y, x, indexing="ij")

        sdf_vals = np.sqrt(
            (X - center[0])**2 + (Y - center[1])**2
        ) - radius

        # Write into MultiFab
        arr[:, :, 0, 0] = sdf_vals

    # ------------------------------------------------------------
    # 5. Gather full image for plotting
    # ------------------------------------------------------------
    full = np.zeros((n, n))

    for mfi in sdf:
        arr = sdf.array(mfi).to_numpy()
        bx = mfi.validbox()

        i_lo, j_lo = bx.lo_vect
        i_hi, j_hi = bx.hi_vect

        full[j_lo:j_hi + 1, i_lo:i_hi + 1] = arr[:, :, 0, 0]

    print("SDF min/max:", full.min(), full.max())

    # ------------------------------------------------------------
    # 6. Plot
    # ------------------------------------------------------------
    plt.figure(figsize=(7, 6))

    lim = np.max(np.abs(full))
    if lim == 0:
        lim = 1e-6

    im = plt.imshow(
        full,
        origin="lower",
        extent=[0, 1, 0, 1],
        cmap="seismic",
        vmin=-lim,
        vmax=lim
    )

    plt.colorbar(im, label="Signed Distance")

    # Zero level set (circle)
    plt.contour(
        full,
        levels=[0.0],
        colors="black",
        linewidths=2,
        extent=[0, 1, 0, 1]
    )

    plt.title("Analytical Signed Distance Function\nCircle centered at (0.5, 0.5)")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig("circle_sdf_2d.png", dpi=150)
    plt.show()

    print("Saved: circle_sdf_2d.png")

    # ------------------------------------------------------------
    # 7. Finalize
    # ------------------------------------------------------------
    amr.finalize()


if __name__ == "__main__":
    main()
