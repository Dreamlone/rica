import numpy as np
import pandas as pd

from rica.vis_tools import plot_section, find_x_borders
from rica.square import water_in_section


def imitate_problem(dataframe, river_level):
    """ Imitate lack of information about the depths """
    # Remove all information about depths
    heights = np.array(dataframe['Height_m'])
    x_range = find_x_borders(dataframe, river_level)


if __name__ == '__main__':
    df = pd.read_csv('data/Крестовский Лесоучасток.csv', sep=';')
    river_level = 300
    # Section visualisation
    plot_section(df, river_level)

    # Calculate water amount in the section
    square_water = water_in_section(df, river_level, vis=False)
    square_ga = square_water/10000
    print(f'Actual water amount in the cross section (hectares): {square_ga:.2f}')

    imitate_problem(df, river_level)
