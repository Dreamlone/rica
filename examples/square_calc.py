import pandas as pd

from rica.vis_tools import plot_section
from rica.square import water_in_section

if __name__ == '__main__':
    df = pd.read_csv('data/Батамай.csv', sep=';')
    river_level = 110
    # Section visualisation
    plot_section(df, river_level)

    # Calculate water amount in the section using 5000 points
    square_water = water_in_section(df, river_level, vis=True, points=5000)

    print(f'Water amount in the cross section (square metres): {square_water}')
