from src.abp.visualization.state_diagram import plot_state_diagram
from pathlib import Path
import matplotlib.pyplot as plt

def run_plot_state_diagram(save_path='figures'):

    fig, ax = plot_state_diagram()

    fig.savefig(Path(save_path) / "state_diagram.png", bbox_inches="tight")

    plt.show()

if __name__=='__main__':

    run_plot_state_diagram()
