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
    "^": "one group",
}

_FONTSIZE = 14


def _parse_dir_name(name: str):
    """Return (T_A, rc) from a directory name like 'T_A_0.1_rc_2.0'."""
    m = re.fullmatch(r"T_A_([\d.]+)_rc_([\d.]+)", name)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def plot_eatings_vs_parameters(sweep_dir):
    """Plot number of eating events across the (T_A, rc) parameter space.

    Marker shape encodes the clustering state; marker size encodes the
    total number of eating events.

    Parameters
    ----------
    sweep_dir:
        Directory containing subdirectories named ``T_A_<value>_rc_<value>``.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes.
    """
    sweep_dir = Path(sweep_dir)

    rows = []  # (T_A, rc, n_eatings)
    for entry in sorted(sweep_dir.iterdir()):
        parsed = _parse_dir_name(entry.name)
        if parsed is None or not entry.is_dir():
            continue
        t_a, rc = parsed
        n_eatings = np.size(np.load(entry / "eatings.npy"))
        rows.append((t_a, rc, n_eatings))

    rc_values = sorted({r[1] for r in rows})

    fig, ax = plt.subplots(figsize=(7, 5))
    seen_shapes = set()

    for t_a, rc, n_eatings in rows:
        rc_idx = rc_values.index(rc)
        shape = _SHAPE_DICT.get(t_a, ["^"] * len(rc_values))[rc_idx]
        label = _LABEL_DICT[shape] if shape not in seen_shapes else None
        seen_shapes.add(shape)

        ax.scatter(
            t_a, rc,
            marker=shape,
            c=[_COLOR_DICT[shape]],
            s=n_eatings ** 3 / 1000,
            label=label,
        )

    # Phase boundary lines
    ax.plot([0.4, 0.4,  4,  4      ], [6, 3.5, 3.5,  1      ], c=_CMAP(0.8))
    ax.plot([4,   4,   40           ], [6, 2.5,  2.5         ], c=_CMAP(0.6))
    ax.plot([4,   4,   25, 25,   60 ], [5, 3.5,  3.5, 2.5, 2.5], c=_CMAP(0.4))

    ax.set_xscale("log")
    ax.set_xlim(0.08, 50)
    ax.set_ylim(1.8, 5.2)
    ax.set_xlabel(
        r"prey-prey interaction torque $T_{\mathrm{A}}$", fontsize=_FONTSIZE
    )
    ax.set_ylabel(
        r"prey-prey interaction radius $R_{\mathrm{pp}}$ in $r_{\mathrm{c}}$",
        fontsize=_FONTSIZE,
    )
    ax.legend(
        loc="upper center", fontsize=_FONTSIZE,
        bbox_to_anchor=(0.5, 1.25), ncol=2,
    )
    plt.subplots_adjust(top=0.85)

    return fig, ax
