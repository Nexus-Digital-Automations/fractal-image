# Fractal Image — Mandelbrot Set Visualizer

Renders the [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) to a PNG using NumPy vectorized iteration and a matplotlib colormap.

![Mandelbrot set rendered with inferno colormap](output/mandelbrot.png)

---

## What it produces

A 1200×800 PNG of the Mandelbrot set:

- **Black** — points stable under iteration (inside the set)
- **Colored** — points that escape, colored by how many iterations it took (escape-time coloring with the `inferno` colormap)

---

## Prerequisites

- [Python 3.x](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) — fast Python package manager

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Setup

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/Nexus-Digital-Automations/fractal-image.git
cd fractal-image
uv venv
uv pip install numpy matplotlib
```

---

## Generate the image

```bash
uv run python src/mandelbrot.py
```

The script will:
1. Compute the Mandelbrot set for a 1200×800 grid of complex numbers
2. Save the result to `output/mandelbrot.png`
3. Open an interactive preview window

---

## Configuration

All tunable parameters are constants at the top of `src/mandelbrot.py`:

| Constant | Default | Description |
|---|---|---|
| `WIDTH` | `1200` | Image width in pixels |
| `HEIGHT` | `800` | Image height in pixels |
| `MAX_ITER` | `50` | Max iterations before a point is declared stable |
| `REAL_MIN / REAL_MAX` | `-2.0 / 1.0` | Real-axis range of the complex plane |
| `IMAG_MIN / IMAG_MAX` | `-1.2 / 1.2` | Imaginary-axis range |
| `COLORMAP` | `"inferno"` | Any [matplotlib colormap](https://matplotlib.org/stable/gallery/color/colormap_reference.html) |
| `OUTPUT_PATH` | `"output/mandelbrot.png"` | Where to save the image |

**Example — higher detail with a different colormap:**

```python
WIDTH, HEIGHT = 2400, 1600
MAX_ITER = 200
COLORMAP = "plasma"
```

**Example — zoom into the seahorse valley:**

```python
REAL_MIN, REAL_MAX = -0.76, -0.72
IMAG_MIN, IMAG_MAX = 0.08, 0.12
MAX_ITER = 200
```

---

## How it works

The Mandelbrot set is the set of complex numbers `c` for which the sequence

```
z₀ = 0
zₙ₊₁ = zₙ² + c
```

never diverges (i.e. `|z|` never exceeds 2).

The script builds a 2-D grid of complex numbers covering the configured range, one per pixel, then iterates the recurrence in **vectorized NumPy** — all pixels are updated simultaneously per iteration step. Points that escape have their iteration count recorded and are masked out of further computation. The escape counts are then mapped through a matplotlib colormap to produce the final image.

---

## Project structure

```
fractal-image/
├── src/
│   └── mandelbrot.py   # Visualization script
├── output/             # Generated images (gitignored)
├── .gitignore
└── README.md
```
