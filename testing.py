from gauss_elimination import GaussElimination
import random
import numpy as np
from pprint import pprint


class Testing:
    # Automatic Testing for Gauss Elimination class
    _amount_tests = 0

    def __init__(self, amount_tests: int, print_matrix: bool = False) -> None:
        self._amount_tests = amount_tests
        self._print_matrix = print_matrix

    def test(self):
        GE = GaussElimination()
        errors = 0

        for i in range(self._amount_tests):
            # Select random amount of unknowns
            GE.n = random.randrange(2, 11)

            # Create random matrix
            GE.default_matrix = np.random.randint(
                low=-200,
                high=200,
                size=(GE.n, GE.n)
            )

            # Create random right side
            GE.right_side = np.random.randint(low=-200, high=200, size=(GE.n))

            if self._print_matrix:
                print("Testing Gauss Elimination for following matrix and right side:")
                pprint(GE.default_matrix)
                pprint(GE.right_side)

            try:
                solution = GE.solve()
            except:
                errors += 1

            if self._print_matrix:
                print(f"Solution for matrix {i}: {solution}")

        print(f"Finished testing with {errors} errors.")


if __name__ == "__main__":
    test = Testing(amount_tests=100000)
    test.test()
