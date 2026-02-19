"""
Mandelbrot Set Visualization
============================

The Mandelbrot set is the set of complex numbers c for which the sequence:

    z_0 = 0
    z_{n+1} = z_n^2 + c

remains bounded (|z| never exceeds 2) as n → ∞.

Points inside the set are colored black. Points outside the set are colored
by how quickly they escape — fewer iterations to escape means farther from
the set boundary, producing the vivid gradient exterior.

Usage:
    uv run python src/mandelbrot.py

Output:
    output/mandelbrot.png
"""

import os
import sys

# ---------------------------------------------------------------------------
# Auto-install dependencies if they're missing (makes the script self-contained)
# ---------------------------------------------------------------------------
try:
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "numpy", "matplotlib"],
        stdout=subprocess.DEVNULL,
    )
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

# ---------------------------------------------------------------------------
# Configuration — tweak these constants to explore different views / quality
# ---------------------------------------------------------------------------
WIDTH = 1200          # Output image width in pixels
HEIGHT = 800          # Output image height in pixels
MAX_ITER = 50         # Max iterations before declaring a point "stable"

REAL_MIN, REAL_MAX = -2.0, 1.0    # Real-axis range of the complex plane
IMAG_MIN, IMAG_MAX = -1.2, 1.2    # Imaginary-axis range of the complex plane

COLORMAP = "inferno"  # Matplotlib colormap used to color escape speed
OUTPUT_PATH = "output/mandelbrot.png"

# ---------------------------------------------------------------------------
# Step 1 — Build the grid of complex numbers c
#
# We sample WIDTH points along the real axis and HEIGHT points along the
# imaginary axis, then combine them with meshgrid to get a 2-D array of
# complex numbers — one for every pixel.
# ---------------------------------------------------------------------------
real_axis = np.linspace(REAL_MIN, REAL_MAX, WIDTH)   # 1-D array of real parts
imag_axis = np.linspace(IMAG_MIN, IMAG_MAX, HEIGHT)  # 1-D array of imag parts

# meshgrid produces two (HEIGHT × WIDTH) arrays; combining them gives c
real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
c = real_grid + 1j * imag_grid  # shape: (HEIGHT, WIDTH), dtype: complex128

# ---------------------------------------------------------------------------
# Step 2 — Vectorized Mandelbrot iteration
#
# Strategy:
#   - z starts at 0 for every point.
#   - Each step updates all "still active" points together.
#   - When |z| > 2 for a point, it has escaped: record the iteration count,
#     then freeze that point (mask it from future updates to save computation).
# ---------------------------------------------------------------------------
z = np.zeros_like(c)                           # z_0 = 0 for every pixel
iteration_count = np.full(c.shape, MAX_ITER)   # assume stable; overwrite on escape
active = np.ones(c.shape, dtype=bool)          # True = still iterating

for i in range(MAX_ITER):
    # Update z only for points that haven't escaped yet
    z[active] = z[active] ** 2 + c[active]

    # Detect newly escaped points (|z| > 2, still marked as active)
    escaped = active & (np.abs(z) > 2.0)

    # Record the iteration at which these points escaped
    iteration_count[escaped] = i

    # Remove escaped points from the active set so they're no longer updated
    active[escaped] = False

    # Early exit: if nothing left to iterate, stop
    if not active.any():
        break

# ---------------------------------------------------------------------------
# Step 3 — Build the color image
#
# Stable points (iteration_count == MAX_ITER) → pure black.
# Escaped points → mapped through a colormap based on their escape speed.
#   Normalizing to [0, 1] first lets matplotlib apply the colormap evenly.
# ---------------------------------------------------------------------------
# Normalize escape iteration counts to [0, 1]
norm = mcolors.Normalize(vmin=0, vmax=MAX_ITER - 1)
cmap = plt.get_cmap(COLORMAP)

# Apply the colormap: result is an (HEIGHT × WIDTH × 4) RGBA array
rgba_image = cmap(norm(iteration_count))

# Force stable points (never escaped) to solid black regardless of colormap
stable_mask = (iteration_count == MAX_ITER)
rgba_image[stable_mask] = [0.0, 0.0, 0.0, 1.0]  # RGBA black, fully opaque

# ---------------------------------------------------------------------------
# Step 4 — Save to PNG and display
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)
ax.imshow(
    rgba_image,
    extent=[REAL_MIN, REAL_MAX, IMAG_MIN, IMAG_MAX],  # axis labels in math coords
    origin="lower",   # imag_axis increases upward, matching standard math convention
    aspect="auto",
)
ax.set_title("Mandelbrot Set", fontsize=14, color="white", pad=10)
ax.set_xlabel("Re(c)", color="white")
ax.set_ylabel("Im(c)", color="white")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_edgecolor("white")

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=100, bbox_inches="tight", facecolor="black")
print(f"Image saved to: {OUTPUT_PATH}")

plt.show()
