import numpy as np
from typing import List, Union


class GaussElimination:
    _default_matrix = [[3, 0, 1], [1, 2, 0], [0, 1, 1]]
    _right_side = [0] * len(_default_matrix)
    _n = len(_default_matrix[0])

    def __init__(
        self,
        default_matrix: List[List[float]] = None,
        right_side: List[float] = None
    ) -> None:
        self._default_matrix = default_matrix if default_matrix else self._default_matrix
        self._right_side = right_side if right_side else self._right_side
        self._n = len(self._default_matrix[0])

    @property
    def default_matrix(self):
        return self._default_matrix

    @default_matrix.setter
    def default_matrix(self, matrix: List[List[float]]):
        self._default_matrix = matrix

    @property
    def right_side(self):
        return self._right_side

    @right_side.setter
    def right_side(self, right_side: List[float]):
        self._right_side = right_side

    def solve(self, algorithm: str = "forward_elimination"):
        if algorithm == "forward_elimination":
            res = self.forward_elimination_back_substitution(
                self.default_matrix, self.right_side)

            return res
        else:
            raise ValueError("Invalid algorithm!")

    def forward_elimination_back_substitution(
        self,
        matrix: List[List[float]],
        right_side: List[float]
    ):
        np_matrix = self.convert_matrix_to_numpy_array(matrix)
        np_right_side = self.convert_right_side_to_numpy_array(right_side)

        np_matrix, np_right_side = self.forward_elimination(
            np_matrix, np_right_side)

        solution = self.back_substitution(
            np_matrix, np_right_side)

        return solution

    def convert_matrix_to_numpy_array(self, matrix: List[List[float]]) -> np.ndarray:
        x = np.zeros((len(matrix), len(matrix[0])))

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                x[i][j] = matrix[i][j]

        return x

    def convert_right_side_to_numpy_array(self, right_side: List[float]) -> np.ndarray:
        x = np.zeros(len(right_side))

        for i in range(len(right_side)):
            x[i] = right_side[i]

        return x

    def forward_elimination(
        self,
        matrix: np.ndarray,
        right_side: np.ndarray
    ) -> Union[np.ndarray, np.ndarray]:
        for i in range(self._n - 1):
            for j in range(i + 1, self._n):
                m = matrix[j][i] / matrix[i][i]
                right_side[j] -= m * right_side[i]
                for k in range(i + 1, self._n):
                    matrix[j][k] -= m * matrix[i][k]

        return matrix, right_side

    def not_working_forward_elimination(self, matrix: np.ndarray, right_side: np.ndarray) -> Union[np.ndarray, np.ndarray]:
        n = len(matrix[0]) - 1

        for k in range(n - 1):
            for i in range(k + 1, n):
                mik = matrix[i][k] / matrix[k][k]
                for j in range(k + 1, n):
                    matrix[i][j] = matrix[i][j] - mik * matrix[k][j]

                right_side[i] -= mik * right_side[k]

        return matrix, right_side

    def back_substitution(
        self,
        matrix: np.ndarray,
        right_side: np.ndarray
    ) -> np.ndarray:
        x = np.zeros(self._n)

        x[self._n - 1] = right_side[self._n - 1] / \
            matrix[self._n - 1][self._n - 1]

        for i in range(self._n - 2, -1, -1):
            temp = right_side[i]

            for j in range(i + 1, self._n):
                temp -= matrix[i][j] * x[j]

            x[i] = temp / matrix[i][i]

        return x

    def not_working_back_substitution(self, matrix: np.ndarray, right_side: np.ndarray) -> np.ndarray:
        n = len(matrix[0]) - 1
        r = len(matrix) - 1

        # Create solution vector
        x = np.zeros(n + 1)

        x[n] = matrix[r][n] / \
            matrix[r][n]

        for i in range(r - 1, -1, -1):
            x[i] = matrix[i][r]

            for j in range(i + 1, r):
                x[i] = x[i] - matrix[i][j] * x[j]

            x[i] = x[i] / matrix[i][i]

        return x
