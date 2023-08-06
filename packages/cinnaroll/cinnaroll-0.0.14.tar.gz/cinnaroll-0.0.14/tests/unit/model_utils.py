import numpy as np
from typing import Tuple


def generate_random_data(
        num_samples: int, num_features: int) -> Tuple[np.ndarray, np.ndarray]:  # type: ignore
    """Generate random data of specified dimension. Returns numpy.arrays."""
    X = np.random.rand(num_samples, num_features)
    Y = np.random.rand(num_samples)

    return X, Y
