import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 15, 7

from rica.vis_tools import plot_section, find_x_borders
from rica.square import water_in_section
from rica.estimation import batch_poly_approximation


def imitate_problem(dataframe, river_level):
    """ Imitate lack of information about the depths """
    # Remove all information about depths
    heights = np.array(dataframe['Height_m'])
    xs = np.array(dataframe['x'])

    x_range, indices = find_x_borders(dataframe, river_level)
    # Flag unknown part with -100.0 value
    heights[indices] = -100.0

    recovered = batch_poly_approximation(heights, -100.0, degree=2, n_neighbors=15)

    plt.plot(xs, recovered, c='red', label='Estimated depths')
    plot_section(df, river_level)

    # Calculate new square
    dataframe['Height_m'] = recovered
    square_water = water_in_section(dataframe, river_level, vis=False)
    square_ga = square_water/10000
    print(f'Estimated water amount in the cross section (hectares): {square_ga:.2f}')


if __name__ == '__main__':
    df = pd.read_csv('data/Крестовский Лесоучасток.csv', sep=';')
    river_level = 300

    # Calculate water amount in the section
    square_water = water_in_section(df, river_level, vis=False)
    square_ga = square_water/10000
    print(f'Actual water amount in the cross section (hectares): {square_ga:.2f}')

    imitate_problem(df, river_level)
