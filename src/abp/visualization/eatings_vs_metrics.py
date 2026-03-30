import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

_SHAPE_DICT = {
    0.1:  ["h", "h", "h", "h"],
    1.0:  ["h", "h", "p", "p"],
    10.0: ["p", "s", "^", "^"],
    20.0: ["p", "s", "^", "^"],
    30.0: ["p", "^", "^", "^"],
    40.0: ["p", "^", "^", "^"],
}

_CMAP = plt.cm.viridis
_COLOR_DICT = {
    "h": _CMAP(0.8),
    "p": _CMAP(0.6),
    "s": _CMAP(0.4),
    "^": _CMAP(0.2),
}
_LABEL_DICT = {
    "h": "cloud",
    "p": "multiple loose groups",
    "s": "multiple cohesive groups",
    "^": "one cohesive group",
}

_FONTSIZE = 13
_MARKER_SIZE = 75


def _parse_dir_name(name: str):
    """Return (T_A, rc) from a directory name like 'T_A_0.1_rc_2.0'."""
    m = re.fullmatch(r"T_A_([\d.]+)_rc_([\d.]+)", name)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def _parse_metrics(metrics_path: Path) -> dict:
    """Parse 'key: value, key: value' from metrics.txt into a dict."""
    text = metrics_path.read_text()
    return {k.strip(): float(v) for k, v in (pair.split(":") for pair in text.split(","))}


def _load_run(run_dir: Path) -> tuple:
    """Return (n_eatings, av_proximity, av_distance) for one run directory."""
    n_eatings = np.size(np.load(run_dir / "eatings.npy"))
    metrics = _parse_metrics(run_dir / "metrics.txt")
    proximity = metrics["av_particles_in_prox"]
    distance = metrics["av_particle_distance"]
    return n_eatings, proximity, distance


def _scatter_panel(ax, x_vals, eatings, shapes, xlabel):
    seen = set()
    for x, y, shape in zip(x_vals, eatings, shapes):
        label = _LABEL_DICT[shape] if shape not in seen else None
        seen.add(shape)
        ax.scatter(x, y, c=[_COLOR_DICT[shape]], marker=shape,
                   s=_MARKER_SIZE, label=label)
    ax.set_ylabel(r"total number of eating events $N_{\mathrm{E}}$", fontsize=_FONTSIZE)
    ax.set_xlabel(xlabel, fontsize=_FONTSIZE)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=_FONTSIZE)
    ax.grid()


def plot_eatings_vs_metrics(sweep_dir):
    """Plot eating events vs proximity and distance metrics for all runs in sweep_dir.

    Parameters
    ----------
    sweep_dir:
        Directory containing subdirectories named ``T_A_<value>_rc_<value>``.

    Returns
    -------
    fig, ax : matplotlib Figure and array of two Axes.
    """
    sweep_dir = Path(sweep_dir)

    # Collect data grouped by (T_A, rc)
    rows: list[tuple] = []  # (T_A, rc, n_eatings, proximity, distance)
    for entry in sorted(sweep_dir.iterdir()):
        parsed = _parse_dir_name(entry.name)
        if parsed is None or not entry.is_dir():
            continue
        t_a, rc = parsed
        n_eatings, proximity, distance = _load_run(entry)
        rows.append((t_a, rc, n_eatings, proximity, distance))

    rc_values = sorted({r[1] for r in rows})

    eatings, proximity_vals, distance_vals, shapes = [], [], [], []
    for t_a, rc, n_eatings, proximity, distance in rows:
        rc_idx = rc_values.index(rc)
        shape = _SHAPE_DICT.get(t_a, ["^"] * len(rc_values))[rc_idx]
        eatings.append(n_eatings)
        proximity_vals.append(proximity)
        distance_vals.append(distance)
        shapes.append(shape)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    _scatter_panel(
        ax1, proximity_vals, eatings, shapes,
        xlabel=r"proximity parameter $P$",
    )
    _scatter_panel(
        ax2, distance_vals, eatings, shapes,
        xlabel=r"average particle distance $D$ in units of $\sigma$",
    )

    plt.tight_layout()
    return fig, np.array([ax1, ax2])
