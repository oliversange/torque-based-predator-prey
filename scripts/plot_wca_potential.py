from src.abp.visualization.wca_potential import plot_wca_potential
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def run_wca_plot(save_path="figures"):
    
    fig, ax = plot_wca_potential(r=np.linspace(0.1, 3, 500), 
                         x=[2**(1/6), 2**(1/6)], 
                         y=[0, 200], 
                         x_1=[1, 1], 
                         y_1=[0, 200])
    
    fig.savefig(Path(save_path) / "wca_potential.png", bbox_inches="tight")

    plt.show()

if __name__=="__main__":

    run_wca_plot()