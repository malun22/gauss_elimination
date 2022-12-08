from gauss_elimination import GaussElimination
import random
import numpy as np
from pprint import pprint
import sympy as sy


class Testing:
    # Automatic Testing for Gauss Elimination class
    _amount_tests = 0

    def __init__(self, amount_tests: int) -> None:
        self._amount_tests = amount_tests

    def test_solutions(self, print_solutions: bool = False):
        GE = GaussElimination()
        errors = 0
        error_entries = []

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

            solution = GE.solve()

            # Now compute with sympy
            A = sy.Matrix(GE.default_matrix)
            b = sy.Matrix(GE.right_side)

            try:
                # If the matrix is singular, this will raise an error
                sol = A.LUsolve(b).n()
            except:
                continue

            # Compare the solutions
            for i, value in enumerate(solution):
                difference = abs(value - sol[i]) / ((value + sol[i]) / 2) * 100

                if difference > 0.0001:
                    errors += 1
                    error_entries.append((solution, sol))
                    break

            if print_solutions:
                pprint(
                    f"Solution for matrix {i}: {solution} and by Sympy: {sol.n()}")

        print(f"Finished testing with {errors} errors. Error entries:")
        pprint(error_entries)

    def test_for_errors(self, print_steps: bool = False):
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

            if print_steps:
                print("Testing Gauss Elimination for following matrix and right side:")
                pprint(GE.default_matrix)
                pprint(GE.right_side)

            try:
                solution = GE.solve()
            except:
                errors += 1

            if print_steps:
                print(f"Solution for matrix {i}: {solution}")

        print(f"Finished testing with {errors} errors.")


if __name__ == "__main__":
    test = Testing(amount_tests=100000)
    test.test_solutions()
    test.test_for_errors()
