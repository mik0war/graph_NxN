import numpy as np
import matplotlib.pyplot as plt

import builder
from calculator import Calculator
from visualiser import Visualiser


def calculate_time(g_values: list):
    for i in range(g_values.__len__()):
        g_values[i] = abs(g_values[i])

    g_values.sort()

    g = g_values[1].real
    print(g)
#    print(5 * 1/g)

# Параметры системы
lam1 = 750
lam2 = 500
mu1 = 960
mu2 = 530

BUFFER_SIZE = 3

parameters = builder.Parameters(lam1, lam2, mu1, mu2)
builder = builder.Builder(parameters)
calculator = Calculator(builder)
visualiser = Visualiser()

matrix_coefficients = builder.build_matrix(BUFFER_SIZE)

MATRIX_SIZE = matrix_coefficients.__len__()

print(f'Всего состояний: {MATRIX_SIZE}')
mm = np.array(matrix_coefficients)

calculator.calculate(mm)
calculator.visualise(visualiser)
calculator.visualise_throughput(visualiser)
calculator.visualise_loss(visualiser)
calculator.visualise_r(visualiser)

visualiser.visualise_graph(builder)
matrix_latex = builder.build_matrix_latex()
visualiser.display_latex_text(matrix_latex)

equation_system = builder.build_latex_evaluation_system()
visualiser.display_latex_text(equation_system)

plt.show()