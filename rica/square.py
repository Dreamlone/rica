import numpy as np
import pandas as pd
from rica.vis_tools import plot_points, find_x_borders


def water_in_section(dataframe: pd.DataFrame, river_level: int, points: int = 5000,
                     vis: bool = False):
    """ Calculate water amount in cross section by level using Monte-Carlo
    method
    """
    left_border_x = min(dataframe['x'])
    right_border_x = max(dataframe['x'])
    lower_border_h = min(dataframe['Height_m'])
    upper_border_h = max(dataframe['Height_m'])

    x_coords = np.random.uniform(left_border_x, right_border_x, points)
    h_coords = np.random.uniform(lower_border_h, upper_border_h, points)

    if vis:
        plot_points(dataframe, river_level, x_coords, h_coords)

    # Calculate square
    known_sq = (right_border_x - left_border_x) * (upper_border_h - lower_border_h)

    # How many points are in the "flooded part"
    flood_points = calculate_flood_points(dataframe=dataframe, river_level=river_level,
                                          x_coords=x_coords, h_coords=h_coords)

    flood_ratio = flood_points/points

    section_square = flood_ratio * known_sq
    return section_square


def calculate_flood_points(dataframe, river_level, x_coords, h_coords):
    """ Calculate number of flooded points in the section """

    # TODO make it more efficient
    flood_count = 0
    for point in range(0, len(x_coords)):
        current_level = h_coords[point]
        # Potentially flood point
        if current_level < river_level:
            current_x = x_coords[point]
            # Find appropriate x coords
            x_range, _ = find_x_borders(dataframe, current_level)
            if current_x > x_range[0] and current_x < x_range[-1]:
                flood_count += 1

    return flood_count
