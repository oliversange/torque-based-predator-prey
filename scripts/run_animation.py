import argparse
import numpy as np
from pathlib import Path
from src.abp.utils.utils import load_config
from src.abp.visualization.animation import animate_simulation

def run_animation(result_path, interval=50):
    
    # Load coordinates
    result_dir = Path("results/"+result_path)
    positions = np.load(result_dir / "prey.npy")
    predator_positions = np.load(result_dir / "predator.npy")

    # Load config
    config = load_config(result_dir / "config.yaml")

    animate_simulation(positions=positions,
                       predator_positions=predator_positions,
                       box_size=config["system"]["L"],
                       interval=interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--result",
        type=str,
        required=True,
        help="Results folder name (inside results/)"
    )

    parser.add_argument(
        "--interval",
        type=int,
        required=False,
        help="Data animation inteval"
    )

    args = parser.parse_args()

    run_animation(
        result_path=args.result,
        interval=args.interval
    )