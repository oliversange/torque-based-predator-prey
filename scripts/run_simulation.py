import argparse
import numpy as np
from pathlib import Path
import yaml
from src.abp.utils.utils import load_config
from src.abp.simulation.simulation import simulate
from src.abp.metrics.proximity import calc_prox_metrics

# Run ABP predator prey simulation
def run_abp_simulation(config: dict, output_dir_name):
        
        # Calculate
        rc = config["abp_model"]["rc"]
        r_c = 2**(1/6)
        R_prey = rc*r_c
        R_prey_pred = 3*r_c

        positions, predator_positions, eatings = simulate(number_of_particles          =config["system"]["number_of_particles"],
                                                            boundary_condition         =config["system"]["boundary_condition"], 
                                                            L                          =config["system"]["L"],
                                                            number_of_steps            =config["simulation"]["number_of_steps"],
                                                            dt                         =config["simulation"]["dt"],
                                                            D                          =config["abp_model"]["D"], 
                                                            D_rot                      =config["abp_model"]["D_rot"], 
                                                            mu                         =config["abp_model"]["mu"], 
                                                            mu_r                       =config["abp_model"]["mu_r"], 
                                                            setup                      =config["prey_parameters"]["setup"], 
                                                            v0                         =config["prey_parameters"]["v0"], 
                                                            T_A                        =config["prey_parameters"]["T_A"], 
                                                            T_0                        =config["prey_parameters"]["T_0"], 
                                                            T_0_predator               =config["predator_parameters"]["T_0_predator"],
                                                            R_prey                     =R_prey, 
                                                            R_prey_pred                =R_prey_pred,
                                                            R_pred_prey                =config["predator_parameters"]["R_pred_prey"],
                                                            v_pred                     =config["predator_parameters"]["v_pred"], 
                                                            predator_introduction_step =config["predator_parameters"]["predator_introduction_step"],
                                                            )
        
        av_particles_in_prox, av_particle_distance = calc_prox_metrics(positions, R=R_prey, boundary_condition=config["system"]["boundary_condition"], L=config["system"]["L"], number_of_steps=config["simulation"]["number_of_steps"])

        # Create output folder
        output_dir = Path("results/") / output_dir_name
        output_dir.mkdir(exist_ok=True)

        # Save config
        output_path = output_dir / "config.yaml"
        with open(output_path, "w") as f:
            yaml.safe_dump(config, f, sort_keys=False)

        # Save results
        np.save(output_dir / "prey.npy", positions)
        np.save(output_dir / "predator.npy", predator_positions)
        np.save(output_dir / "eatings.npy", eatings)

        # Save metrics
        metrics_file = output_dir / "metrics.txt"
        metrics_file.write_text(f"av_particles_in_prox: {av_particles_in_prox}, av_particle_distance: {av_particle_distance}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Config YAML file name (inside configs/)"
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory name (inside results/)"
    )

    args = parser.parse_args()

    config_dict = load_config("configs/"+args.config)

    run_abp_simulation(
        config=config_dict,
        output_dir_name=Path(args.output)
    )