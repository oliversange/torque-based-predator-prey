from src.abp.visualization.survivor_histogram import plot_survivor_histogram
from src.abp.visualization.eatings_vs_metrics import plot_eatings_vs_metrics
from src.abp.visualization.eatings_vs_parameters import plot_eatings_vs_parameters
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

def run_plot_survivor_histogram(sweep_dir, save_dir):

    fig, ax = plot_survivor_histogram(sweep_dir)

    fig.savefig(save_dir / "survivor_histogram.png", bbox_inches="tight")

    plt.show()

def run_plot_eatings_vs_metrics(sweep_dir, save_dir):

    fig, ax = plot_eatings_vs_metrics(sweep_dir)

    fig.savefig(save_dir / "eatings_vs_metrics.png", bbox_inches="tight")

    plt.show()

def run_plot_eatings_vs_parameters(sweep_dir, save_dir="figures"):
    
    fig, ax = plot_eatings_vs_parameters(sweep_dir)

    fig.savefig(save_dir / "eatings_vs_parameters.png", bbox_inches="tight")

    plt.show()

if __name__=="__main__":


    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--sweep_name",
        type=str,
        required=True,
        help="Name of the sweep save dir in (results/)"
    )

    args = parser.parse_args()

    sweep_dir = Path("results") / args.sweep_name
    save_dir = sweep_dir / "plots"
    save_dir.mkdir(exist_ok=True)
    run_plot_survivor_histogram(sweep_dir, save_dir)
    run_plot_eatings_vs_metrics(sweep_dir, save_dir)
    run_plot_eatings_vs_parameters(sweep_dir, save_dir)