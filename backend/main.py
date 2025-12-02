import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

from builder import Builder, Parameters
import buffer
from calculator import Calculator
from data_types.parameters import Interval
from visualiser import Visualiser


def calculate_time(g_values: list):
    for i in range(g_values.__len__()):
        g_values[i] = abs(g_values[i])

    g_values.sort()

    g = g_values[1].real
    print(g)
#    print(5 * 1/g)

# Параметры системы
lam1 = 250
lam2 = 100
mu1 = 960
mu2 = 100

parameters_list = [
   Interval(0.1, 0.2, Parameters(250, 800, 960, 100)),
   Interval(0.2, 0.6, Parameters(250, 1000, 960, 100)),
   Interval(0.6, 1, Parameters(250, 100, 960, 100)),
    # Interval(0.6, 1, Parameters(750, 500, 960, 530)),
]

BUFFER_SIZE = 3

parameters = Parameters(lam1, lam2, mu1, mu2)
builder = Builder(parameters)
buffer = buffer.Buffer()

calculator = Calculator(builder, buffer)
visualiser = Visualiser()

matrix_coefficients = builder.build_matrix(BUFFER_SIZE)
MATRIX_SIZE = matrix_coefficients.__len__()

first = Interval(0.0, 0.1, parameters)

p_i = calculator.calculate(matrix_coefficients, 0.0, 0.1, 10000)
for interval in parameters_list:
    parameters.change_value(interval.parameters)
    matrix = builder.build_matrix(BUFFER_SIZE, False)

    init_p = p_i[-1, :MATRIX_SIZE]
    p_new = calculator.calculate(matrix, interval.time_start, interval.time_end, 10000, init_p)
    p_i = np.vstack((p_i, p_new))

calculator.set_p(p_i)
calculator.start = 0.0
calculator.end = 1

calculator.visualise(visualiser)
calculator.visualise_throughput(visualiser, [first] + parameters_list)

t_start = 0.1  # начальное время
t_end = 0.61    # конечное время

# Находим индексы соответствующих временных точек
start_idx = np.argmin(np.abs(calculator.get_t_values() - t_start))
end_idx = np.argmin(np.abs(calculator.get_t_values() - t_end))

# Вычисляем интеграл на заданном интервале
integral = np.trapezoid(builder.build_throughput_values(p_i)['$A_1(t)$'][start_idx:end_idx+1],
                    calculator.get_t_values()[start_idx:end_idx+1])

print(f"Интеграл от t={t_start} до t={t_end}: {integral}")

# m2 = builder.build_matrix(BUFFER_SIZE, False)
#
# MATRIX_SIZE = matrix_coefficients.__len__()
#
# print(f'Всего состояний: {MATRIX_SIZE}')
# mm = np.array(matrix_coefficients)

# calculator.calculate(mm)
# calculator.visualise(visualiser)

# calculator.visualise_loss(visualiser)
# calculator.visualise_r(visualiser)
calculator.calculate_average_count(visualiser)
calculator.calculate_average_time(visualiser)
calculator.visualise_spoof(visualiser)
#
# calculator.save_throughput('-', 'first')
# parameters = Parameters(lam1, lam2, mu1, 1600)
#
# builder.change_params(parameters)
#
# matrix_coefficients = builder.build_matrix(BUFFER_SIZE)
#
# mm = np.array(matrix_coefficients)
# calculator.calculate(mm)
# calculator.save_throughput('-.', 'second')
# #buffer.visualise_buffer(visualiser)
# visualiser.visualise_graph(builder)
matrix_latex = builder.build_matrix_latex()
visualiser.display_latex_text(matrix_latex, '', '', '')
visualiser.visualise_graph(builder)
# equation_system = builder.build_latex_evaluation_system()
# visualiser.display_latex_text(equation_system)
#
plt.show()