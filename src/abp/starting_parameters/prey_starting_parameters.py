import numpy as np

def calculate_prey_starting_parameters(number_of_particles, setup, rc=2**(1/6)):

    if setup=="circle":
        x = np.zeros(number_of_particles)
        y = np.zeros(number_of_particles)
        theta = np.zeros(number_of_particles)
        r0 = 87.5
        x[0] = r0
        y[0] = r0
        theta[0] = 0
        num = 1
        for r in range(1, 19):
            for i in range(6 * r):
                if num < number_of_particles:
                    x[num] = r0 + r * rc * np.cos(i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6)
                    y[num] = r0 + r * rc * np.sin(i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6)
                    theta[num] = (i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6) - np.pi
                    num += 1
                else:
                    break
        theta = (theta + np.pi) % (2 * np.pi) - np.pi

    if setup=="grid":
        grid_size=10
        spacing=2
        center=175 / 2
        x = np.linspace(center - (grid_size // 2) * spacing, center + (grid_size // 2) * spacing, grid_size)
        y = np.linspace(center - (grid_size // 2) * spacing, center + (grid_size // 2) * spacing, grid_size)
        x, y = np.meshgrid(x, y)
        theta = np.random.uniform(0, 2 * np.pi, 100)
    
    return x.flatten(), y.flatten(), theta