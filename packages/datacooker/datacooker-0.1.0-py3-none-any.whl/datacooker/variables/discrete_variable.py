"""
Discrete variable module
"""

import numpy as np
from scipy.stats import rv_discrete, poisson

from .variable import Variable


class DiscreteVariable(Variable):
    """
    A discrete variable defined by a distribution
    """

    def __init__(self,
                 label: str,
                 distribution: rv_discrete = poisson(1),
                 missing_values_fraction: float = 0) -> None:
        super().__init__(label, missing_values_fraction)
        self.__values = []
        self.__distribtuion: rv_discrete = distribution

    def simulate_values(self, size: int) -> np.ndarray:
        self.__values = self.__distribtuion.rvs(size=size)
        return self.__values
