import argparse
from pathlib import Path
from src.abp.utils.utils import load_config, generate_configs
from scripts.run_simulation import run_abp_simulation


def run_abp_simulation_sweep(sweep_config_name, output_dir_name):
    sweep_cfg = load_config(Path("configs") / sweep_config_name)
    base_config = load_config(Path("configs") / sweep_cfg["base_config"])
    sweep_dict = sweep_cfg["sweep"]
    for i, config in enumerate(generate_configs(base_config, sweep_dict)):
        
        output_name = f"T_A_{config['prey_parameters']['T_A']}_rc_{config['abp_model']['rc']}"

        print(f"Running {output_name}")

        run_abp_simulation(config, Path(output_dir_name) / output_name)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to config YAML file"
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory name (inside results/)"
    )

    args = parser.parse_args()

    run_abp_simulation_sweep(
        sweep_config_name=args.config,
        output_dir_name=args.output
    )