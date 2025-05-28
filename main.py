import numpy as np
from scipy.linalg import det, eig
import matplotlib.pyplot as plt

import builder
import visualizer
from visualizer import visualize_state_graph


def calculate_time(g_values: list):
    for i in range(g_values.__len__()):
        g_values[i] = abs(g_values[i])

    g_values.sort()

    g = g_values[1].real
    print(g)
#    print(5 * 1/g)


def calculate(matrix_size, matrix):
    # Начальное распределение вероятностей
    p = np.array([0 for _ in range(matrix_size)])
    p[0] = 1

    Leg = []
    for i in range(matrix_size+1):
        for j in range(matrix_size+1):
            if i+j > matrix_size:
                continue
            Leg.append(f'p{i}{j}')

    Leg.append('1')


    ### Вычисление собственных значений и векторов
    g_values, xsi = eig(matrix)  # XSI - матрица правых собственных векторов
    calculate_time(g_values.copy())
    ### Вычисление коэффициентов A (через обратную матрицу)
    a = np.linalg.inv(xsi)

    ### Вычисление матрицы переходов M(t)
    def compute_M(t):
        m = np.zeros((matrix_size, matrix_size))
        for k in range(matrix_size):
            m += np.real(np.outer(xsi[:, k], a[k, :]) * np.exp(g_values[k] * t))
        return m

    ### Вычисление вероятностей P_i(t)
    t_values = np.linspace(0, 0.01, 1000)  # Временной интервал
    p_i = np.zeros((len(t_values), matrix_size + 1))  # +1 для суммы вероятностей

    for idx, t in enumerate(t_values):
        m_t = compute_M(t)
        p_i_t = m_t @ p  # Умножение матрицы на вектор начальных условий
        p_i[idx, :matrix_size] = p_i_t
        p_i[idx, matrix_size] = np.sum(p_i_t)  # Сумма вероятностей (должна быть 1)

    ### Построение графиков
    plt.figure(figsize=(10, 6))
    for i in range(matrix_size + 1):
        plt.plot(t_values, p_i[:, i], label=Leg[i])

    plt.xlabel('Время (t)')
    plt.ylabel('Вероятность')
    plt.title('Эволюция вероятностей состояний системы')
    plt.grid(True)
    plt.legend()

# Параметры системы
lam1 = 6000
lam2 = 9000
mu1 = 200
mu2 = 700

BUFFER_SIZE = 7

edges = builder.generate_states(BUFFER_SIZE)
states = builder.get_states_array(BUFFER_SIZE)
MATRIX_SIZE = states.__len__()
print(f'Всего состояний: {MATRIX_SIZE}')
kolm = builder.build_equals(states, edges)
matrix = builder.build_matrix(MATRIX_SIZE, kolm, mu1, mu2, lam1, lam2)

mm = np.array(matrix)

calculate(MATRIX_SIZE, mm)

edges_with_labels = builder.generate_states(BUFFER_SIZE)
pos = builder.get_pos_array(BUFFER_SIZE)

visualize_state_graph(BUFFER_SIZE, edges_with_labels)

plt.show()