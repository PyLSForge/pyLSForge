
#

#python -m pip install yt
import yt
from yt.frontends.boxlib.api import AMReXDataset

def save_slice(pltfile, step):
    # Load AMReX plotfile
    ds = AMReXDataset(pltfile)

    print("Loaded:", pltfile)
    print("Fields:", ds.field_list)

    # Z-direction slice (axis=2 for 3D)
    sl = yt.SlicePlot(
        ds,
        2,                       # axis: 0=x, 1=y, 2=z
        ("boxlib", "phi")        # field name
    )

    # Optional: annotate AMR grids
    sl.annotate_grids()

    # Optional: colorbar + limits
    sl.set_cmap(("boxlib", "phi"), "inferno")

    # Save PNG
    outname = f"phi_slice_{step:05d}.png"
    sl.save(outname)

    print("Saved:", outname)


if __name__ == "__main__":
    save_slice("plt00000", 0)
    save_slice("plt01000", 1000)
