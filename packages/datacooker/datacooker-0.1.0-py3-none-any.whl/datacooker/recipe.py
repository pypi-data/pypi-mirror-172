"""Recipe module"""

from typing import Dict
from numpy import ndarray
from numpy.random import choice
from pandas import DataFrame, get_dummies
from datacooker.variables.nominal_variable import NominalVariable

from datacooker.variables.variable import Variable


class Recipe:
    """
    A Recipe is a class holding steps to build data
    based on selected model and variables descriptions
    """

    def __init__(self, model_function: callable, result_label: str = 'result') -> None:
        self.__model: callable = model_function
        self.__result_label: str = result_label
        self.__variables: Dict[str, Variable] = {}
        self.__corr_variables: list[tuple[str, callable]] = []
        self.__error: callable = None
        self.__data: Dict[str, ndarray] = {}

    def add_variable(self, variable: Variable) -> None:
        """Adds an independent variable to the recipe

        Args:
            variable (Variable): variable
        """
        self.__variables.update({variable.label: variable})

    def add_variables(self, variables: list[Variable]) -> None:
        """Adds a list of independent variables to the recipe

        Args:
            variables (list[Variable]): list of variables
        """
        for variable in variables:
            self.add_variable(variable)

    def add_corr_variable(self, label: str, lambda_fn: callable) -> None:
        """Adds a correlated variable to the recipe.
        The correlation function defines how its values depend on indepedent variables
        added to the model.

        Args:
            label (str): variable name
            lambda_fn (callable): function that defines correlated variable values taking
            dictionary of variables as argument
            other variables in the recipe.
        """
        self.__corr_variables.append((label, lambda_fn))

    def add_corr_variables(self, labels: list[str], variable_fn: list[callable]) -> None:
        """Adds a list of correlated variables to the recipe.
        The correlation function defines how its values depend on indepedent variables
        added to the model.

        Args:
            labels (list[str]): list of names for each added correlated variable
            lambda_fns (list[callable]): list of function that defines correlated variable values
            taking dictionary of variables as argument
            other variables in the recipe.
        """
        if len(labels) != len(variable_fn):
            error_msg = invalid_labels_and_functions_length_msg(
                len(labels), len(variable_fn))
            raise ValueError(error_msg)

        for index, label in enumerate(labels):
            self.add_corr_variable(label, variable_fn[index])

    def add_error(self, lambda_fn: callable) -> None:
        """Adds an error component that directly influences the resulting variable

        Args:
            label (str): noise variable name
            lambda_fn (callable): _description_
        """
        self.__error = lambda_fn

    def cook(self, size: int = 100) -> DataFrame:
        """Cooks the recipe!
        Generates values for independent, correlated, noise and result variables.
        Stores data in a dataframe

        Args:
            size (int, optional): How many entries should be generated. Defaults to 100.

        Returns:
            pd.DataFrame: dataframe containing all variables
        """
        self.__generate_indepedent_var_values(size)
        self.__generate_corr_var_values()
        self.__generate_result_values(size)
        self.__apply_missing_data_fraction(size)
        return DataFrame.from_dict(self.__data)

    def __apply_missing_data_fraction(self, size: int) -> None:
        for label, variable in self.__variables.items():
            fraction = variable.missing_values_fraction
            if fraction:
                choices_count = int(fraction * size)
                chosen_indexes = choice(size, choices_count, replace=False)
                if isinstance(variable, NominalVariable):
                    self.__update_nominal_missing_data(label, chosen_indexes)
                else:
                    values = self.__data[label]
                    values[chosen_indexes] = None
                    self.__data.update({label: values})

    def __update_nominal_missing_data(self, label: str, chosen_indexes: ndarray) -> None:
        for category, values in self.__data.items():
            if category.startswith(f"{label}."):
                values = values.astype(float)
                values[chosen_indexes] = None
                self.__data.update({category: values})

    def __generate_error_values(self, size: int) -> int | ndarray:
        if not self.__error:
            return 0

        return self.__error(self.__data, size)

    def __generate_result_values(self, size: int) -> None:
        error_values = self.__generate_error_values(size)
        results = self.__apply_model(error_values)
        self.__data.update({self.__result_label: results})

    def __generate_corr_var_values(self) -> None:
        if bool(self.__corr_variables):
            for (label, corr_fn) in self.__corr_variables:
                self.__data.update({label: corr_fn(self.__data)})

    def __generate_indepedent_var_values(self, size: int) -> None:
        if not self.__variables:
            raise ValueError(NO_VARIABLES_ERROR_MSG)

        for label, variable in self.__variables.items():
            if isinstance(variable, NominalVariable):
                dummies_dataframe = get_dummies(variable.simulate_values(size))
                for column in dummies_dataframe:
                    self.__data.update(
                        {f"{label}.{column}": dummies_dataframe[column].values})
            else:
                self.__data.update({label: variable.simulate_values(size)})

    def __apply_model(self, error_values):
        return self.__model(self.__data, error_values)


def invalid_labels_and_functions_length_msg(length_labels: int, length_functions: int) -> str:
    """Builds error message for labels and functions lenghts mismatch

    Args:
        length_labels (int): length of labels list
        length_functions (int): length of functions list

    Returns:
        str: error message
    """

    return f"""
        Labels and Functions lists must have the same length: Labels legth: {length_labels}, \
            functions length: {length_functions}.
    """


NO_VARIABLES_ERROR_MSG = "No variables have been included in the recipe"
