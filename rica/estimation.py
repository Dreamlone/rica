import numpy as np
from rica.vis_tools import _parse_interval_ids


def local_poly_approximation(input_data, gap_value, degree: int = 2,
                             n_neighbors: int = 5):
    """
    Method allows to restore missing values in an array
    using Savitzky-Golay filter
    :param input_data: array with gaps
    :param gap_value: gap value
    :param degree: degree of a polynomial function
    :param n_neighbors: number of neighboring known elements of the time
    series that the approximation is based on
    :return: array without gaps
    """

    output_data = np.array(input_data)

    i_gaps = np.ravel(np.argwhere(output_data == gap_value))

    # Iterately fill in the gaps in the time series
    for gap_index in i_gaps:
        # Indexes of known elements (updated at each iteration)
        i_known = np.argwhere(output_data != gap_value)
        i_known = np.ravel(i_known)

        # Based on the indexes we calculate how far from the gap
        # the known values are located
        id_distances = np.abs(i_known - gap_index)

        # Now we know the indices of the smallest values in the array,
        # so sort indexes
        sorted_idx = np.argsort(id_distances)
        nearest_values = []
        nearest_indices = []
        for i in sorted_idx[:n_neighbors]:
            time_index = i_known[i]
            nearest_values.append(output_data[time_index])
            nearest_indices.append(time_index)
        nearest_values = np.array(nearest_values)
        nearest_indices = np.array(nearest_indices)

        local_coefs = np.polyfit(nearest_indices, nearest_values, degree)
        est_value = np.polyval(local_coefs, gap_index)
        output_data[gap_index] = est_value

    return output_data


def batch_poly_approximation(input_data, gap_value, degree: int = 3,
                             n_neighbors: int = 10):
    """
    Method allows to restore missing values in an array using
    batch polynomial approximations.
    Approximation is applied not for individual omissions, but for
    intervals of omitted values
    :param input_data: array with gaps
    :param gap_value: gap value
    :param degree: degree of a polynomial function
    :param n_neighbors: the number of neighboring known elements of
    time series that the approximation is based on
    :return: array without gaps
    """

    output_data = np.array(input_data)

    # Gap indices
    gap_list = np.ravel(np.argwhere(output_data == gap_value))
    new_gap_list = _parse_interval_ids(gap_list)

    # Iterately fill in the gaps in the time series
    for gap in new_gap_list:
        # Find the center point of the gap
        center_index = int((gap[0] + gap[-1]) / 2)

        # Indexes of known elements (updated at each iteration)
        i_known = np.argwhere(output_data != gap_value)
        i_known = np.ravel(i_known)

        # Based on the indexes we calculate how far from the gap
        # the known values are located
        id_distances = np.abs(i_known - center_index)

        # Now we know the indices of the smallest values in the array,
        # so sort indexes
        sorted_idx = np.argsort(id_distances)

        # Nearest known values to the gap
        nearest_values = []
        # And their indexes
        nearest_indices = []
        for i in sorted_idx[:n_neighbors]:
            # Getting the index value for the series - output_data
            time_index = i_known[i]
            # Using this index, we get the value of each of the "neighbors"
            nearest_values.append(output_data[time_index])
            nearest_indices.append(time_index)
        nearest_values = np.array(nearest_values)
        nearest_indices = np.array(nearest_indices)

        # Local approximation by an n-th degree polynomial
        local_coefs = np.polyfit(nearest_indices, nearest_values, degree)

        # Estimate our interval according to the selected coefficients
        est_value = np.polyval(local_coefs, gap)
        output_data[gap] = est_value

    return output_data
