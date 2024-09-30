# cifer_aggregation/aggregation.py

from typing import List
import numpy as np

def average_parameters(parameters_list: List[List[float]]) -> List[float]:
    """
    Aggregate parameters by calculating the average

    :param parameters_list: List of parameters from multiple clients
    :return: Aggregated parameters
    """
    if not parameters_list:
        raise ValueError("Parameter list is empty")
    
    num_parameters = len(parameters_list[0])
    averaged_parameters = [sum(p[i] for p in parameters_list) / len(parameters_list) for i in range(num_parameters)]
    
    return averaged_parameters

def weighted_average_parameters(parameters_list: List[List[float]], weights: List[float]) -> List[float]:
    """
    Aggregate parameters using a weighted average

    :param parameters_list: List of parameters from multiple clients
    :param weights: Weights used for each client
    :return: Aggregated parameters
    """
    if not parameters_list or not weights:
        raise ValueError("Parameter list or weights list is empty")
    if len(parameters_list) != len(weights):
        raise ValueError("Parameter list and weights list have different lengths")
    
    num_parameters = len(parameters_list[0])
    weighted_sum = [0] * num_parameters
    total_weight = sum(weights)
    
    for i in range(len(parameters_list)):
        for j in range(num_parameters):
            weighted_sum[j] += parameters_list[i][j] * weights[i]
    
    averaged_parameters = [ws / total_weight for ws in weighted_sum]
    
    return averaged_parameters

def geometric_median_parameters(parameters_list: List[List[float]]) -> List[float]:
    """
    Aggregate parameters using a geometric median

    :param parameters_list: List of parameters from multiple clients
    :return: Aggregated parameters
    """
    def geometric_median(data: np.ndarray, eps: float = 1e-5) -> np.ndarray:
        """
        Calculate the geometric median of the data

        :param data: Data used for calculation
        :param eps: Desired precision
        :return: Geometric median of the data
        """
        data = np.array(data)
        median = np.mean(data, axis=0)
        while True:
            distances = np.linalg.norm(data - median, axis=1)
            nonzero_distances = distances > 0
            if np.any(nonzero_distances):
                weights = 1 / distances[nonzero_distances]
                weights /= weights.sum()
                new_median = np.average(data[nonzero_distances], axis=0, weights=weights)
                if np.linalg.norm(new_median - median) < eps:
                    return new_median
                median = new_median
            else:
                return median
    
    parameters_array = np.array(parameters_list)
    median_parameters = geometric_median(parameters_array)
    
    return median_parameters.tolist()
