import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

_LINESTYLE_DICT = {
    0.1:  [":", ":", ":", ":"],
    1.0:  [":", ":", "-.", "-."],
    10.0: ["-.", "--", "-", "-"],
    20.0: ["-.", "--", "-", "-"],
    30.0: ["-.", "-", "-", "-"],
    40.0: ["-.", "-", "-", "-"],
}

_LINESTYLE_LABELS = {
    ":":  "cloud",
    "-.": "multiple loose groups",
    "--": "multiple cohesive groups",
    "-":  "one cohesive group",
}

_FONTSIZE = 15
_CMAP = plt.cm.viridis


def _parse_dir_name(name: str):
    """Return (T_A, rc) parsed from a directory name like 'T_A_0.1_rc_2.0'."""
    m = re.fullmatch(r"T_A_([\d.]+)_rc_([\d.]+)", name)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def _load_n_particles(run_dir: Path) -> int:
    config_path = run_dir / "config.yaml"
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    return cfg["system"]["number_of_particles"]


def _survival_curve(
    run_dirs: list[Path],
    n_particles_per_run: int,
    n_bins: int = 100_000,
) -> tuple[np.ndarray, np.ndarray]:
    """Aggregate eatings across runs and return (times, survivorship)."""
    all_eatings = np.concatenate(
        [np.load(d / "eatings.npy") for d in run_dirs]
    )
    total_prey = n_particles_per_run * len(run_dirs)

    hist, bin_edges = np.histogram(all_eatings, bins=n_bins)
    survivorship = (total_prey - np.cumsum(hist)) / len(run_dirs)
    return bin_edges[:-1], survivorship


def plot_survivor_histogram(sweep_dir):
    """Plot survivorship functions for every (T_A, rc) combination in sweep_dir.

    Parameters
    ----------
    sweep_dir:
        Directory containing subdirectories named ``T_A_<value>_rc_<value>``.

    Returns
    -------
    fig, ax : matplotlib Figure and array of Axes (shape 2×3).
    """
    sweep_dir = Path(sweep_dir)

    # Collect run directories grouped by (T_A, rc)
    runs: dict[tuple[float, float], list[Path]] = {}
    for entry in sweep_dir.iterdir():
        parsed = _parse_dir_name(entry.name)
        if parsed is not None and entry.is_dir():
            runs.setdefault(parsed, []).append(entry)

    t_a_values = sorted({k[0] for k in runs})
    rc_values = sorted({k[1] for k in runs})

    n_cols = 3
    n_rows = int(np.ceil(len(t_a_values) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 10))
    axes_flat = np.array(axes).flatten()

    # Read n_particles from any available config
    n_particles = _load_n_particles(next(iter(runs.values()))[0])

    rc_colors = {rc: _CMAP(0.3 * (i + 1)) for i, rc in enumerate(rc_values)}

    for subplot_idx, t_a in enumerate(t_a_values):
        ax = axes_flat[subplot_idx]
        linestyles = _LINESTYLE_DICT.get(t_a, ["-"] * len(rc_values))

        for rc_idx, rc in enumerate(rc_values):
            run_dirs = runs.get((t_a, rc), [])
            if not run_dirs:
                continue

            times, survivorship = _survival_curve(run_dirs, n_particles)
            color = rc_colors[rc]
            linestyle = linestyles[rc_idx] if rc_idx < len(linestyles) else "-"

            ax.plot(times, survivorship, c=color, linestyle=linestyle)

        ax.set_ylim(0, 100)
        ax.set_xlabel(
            r"time $t$ in units of $\tau_{\mathrm{r}}$", fontsize=_FONTSIZE
        )
        ax.set_ylabel(r"Survivorship function $S(t)$", fontsize=_FONTSIZE)
        ax.set_title(
            r"$T_{\mathrm{A}}$ = " + str(t_a), fontsize=_FONTSIZE
        )

    # Hide unused subplots
    for ax in axes_flat[len(t_a_values):]:
        ax.set_visible(False)

    _add_legend(fig, rc_values, rc_colors)
    plt.tight_layout()

    return fig, axes


def _add_legend(fig, rc_values: list[float], rc_colors: dict[float, tuple]):
    linestyle_handles = [
        Line2D([0], [0], color="black", linestyle=ls, label=label)
        for ls, label in _LINESTYLE_LABELS.items()
    ]
    color_handles = [
        Patch(
            color=rc_colors[rc],
            label=rf"$R_{{\mathrm{{pp}}}} = {int(rc)}r_{{\mathrm{{c}}}}$",
        )
        for rc in rc_values
    ]
    fig.legend(
        handles=linestyle_handles + color_handles,
        loc="lower center",
        ncol=4,
        fontsize=_FONTSIZE,
    )
    plt.subplots_adjust(bottom=0.15)
