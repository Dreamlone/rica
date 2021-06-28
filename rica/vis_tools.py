import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 15, 7


def plot_section(dataframe: pd.DataFrame, river_level: int = None):
    """ Simple cross section visualisation """
    if river_level is None:
        plt.plot(dataframe['x'], dataframe['Height_m'], c='blue')
        plt.ylabel('Height')
        plt.xlabel('Meters')
        plt.grid()
        plt.show()
    else:
        x_range, _ = find_x_borders(dataframe, river_level)
        plt.plot(dataframe['x'], dataframe['Height_m'], c='blue',
                 label='Cross section')
        plt.plot(x_range, np.full(len(x_range), river_level), c='orange',
                 label='River level')
        plt.legend()
        plt.ylabel('Height')
        plt.xlabel('Meters')
        plt.grid()
        plt.show()


def plot_points(dataframe: pd.DataFrame, river_level: int, x_coords: np.array,
                h_coords: np.array):
    plt.scatter(x_coords, h_coords, c='black', s=2.5)
    plot_section(dataframe, river_level)


def find_x_borders(dataframe, river_level):
    """ Calculate x range for river level line visualisation """
    if max(dataframe['Height_m']) <= river_level:
        x_range = [min(dataframe['x']), max(dataframe['x'])]
        indices = None
    else:
        heights = np.ravel(np.array(dataframe['Height_m']))
        xs = np.ravel(np.array(dataframe['x']))

        # Find ids of points, which lower than river level
        ids_flooded = np.ravel(np.argwhere(heights <= river_level))
        ids_flooded_intervals = _parse_interval_ids(ids_flooded)
        if len(ids_flooded_intervals) == 1:
            indices = ids_flooded_intervals[0]
            x_range = xs[indices]
        elif len(ids_flooded_intervals) > 1:
            # Find the longest interval
            lens = [len(i) for i in ids_flooded_intervals]
            lens = np.array(lens)
            max_len_id = int(np.argmax(lens))

            # Get ids of "flooded" part
            indices = ids_flooded_intervals[max_len_id]
            x_range = xs[indices]
        else:
            raise ValueError(f'River level is not valid')

    return x_range, indices


def _parse_interval_ids(ids_flooded: np.array) -> list:
    """
    Method allows parsing source array with flooded indexes
    :param ids_flooded: array with indexes of gaps in array
    :return: a list with separated points in continuous intervals
    """

    new_flooded_list = []
    local_floods = []
    for index, point in enumerate(ids_flooded):
        if index == 0:
            local_floods.append(point)
        else:
            prev_point = ids_flooded[index - 1]
            if point - prev_point > 1:
                # There is a "gap" between gaps
                new_flooded_list.append(local_floods)

                local_floods = []
                local_floods.append(point)
            else:
                local_floods.append(point)
    new_flooded_list.append(local_floods)

    return new_flooded_list
