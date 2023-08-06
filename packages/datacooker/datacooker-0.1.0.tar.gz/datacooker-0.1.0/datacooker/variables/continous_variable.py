"""
Continous variable module
"""

import numpy as np
from scipy.stats import rv_continuous, norm

from .variable import Variable


class ContinousVariable(Variable):
    """
    A continous variable defined by a distribution
    """

    def __init__(self,
                 label: str,
                 distribution: rv_continuous = norm(),
                 missing_values_fraction: float = 0) -> None:
        super().__init__(label, missing_values_fraction)
        self.__values: list = []
        self.__distribtuion: rv_continuous = distribution

    def simulate_values(self, size: int) -> np.ndarray:
        self.__values = self.__distribtuion.rvs(size=size)
        return self.__values
