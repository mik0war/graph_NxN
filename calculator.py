import numpy as np
from scipy.linalg import eig

from buffer import Buffer
from builder import Builder
from visualiser import Visualiser


class Calculator:

    def __init__(self, builder: Builder, buffer: Buffer):
        self.__builder = builder
        self.__buffer = buffer

        # Calculation results
        self.__g_values = None
        self.__p_i = None
        self.__t_values = None
        self.__a = None
        self.__xsi = None

        # Time params
        self.start = 0
        self.end = 0.1
        self.__num = 2000

        # Decorators
        self.visualise = self.check_calculate(self.visualise)
        self.visualise_throughput = self.check_calculate(self.visualise_throughput)

    def set_time_params(self, start, end, num):
        self.__num = num
        self.start = start
        self.end = end

    def calculate(self, matrix, time_start=None, time_end=None, num=None, p=None):
        matrix_size = matrix.__len__()

        if time_start:
            self.start = time_start
        if time_end:
            self.end = time_end
        if num:
            self.__num = num

        p = self.calculate_initial_p(matrix_size, p)

        self.calculate_g_a(matrix)

        ### Вычисление вероятностей P_i(t)
        t_values = np.linspace(self.start, self.end, self.__num)  # Временной интервал
        p_i = np.zeros((len(t_values), matrix_size + 1))  # +1 для суммы вероятностей

        for idx, t in enumerate(t_values):
            m_t = self.compute_m(matrix_size, t - self.start)
            p_i_t = m_t @ p  # Умножение матрицы на вектор начальных условий
            p_i_t = np.where(p_i_t < 0, 0, p_i_t)
            p_i[idx, :matrix_size] = p_i_t
            p_i[idx, matrix_size] = np.sum(p_i_t)  # Сумма вероятностей (должна быть 1)

        if self.__t_values is not None:
            self.__t_values = np.concatenate((self.__t_values, t_values))
        else:
            self.__t_values = t_values
        self.__p_i = p_i

        return p_i

    def set_p(self, p_i):
        self.__p_i = p_i

    def calculate_initial_p(self, matrix_size, p=None):
        # Начальное распределение вероятностей
        if p is None:
            p = np.array([0 for _ in range(matrix_size)])
            p[0] = 1
        return p

    def calculate_g_a(self, matrix):
        ### Вычисление собственных значений и векторов
        self.__g_values, self.__xsi = eig(matrix)  # XSI - матрица правых собственных векторов
        ### Вычисление коэффициентов A (через обратную матрицу)
        self.__a = np.linalg.inv(self.__xsi)

    def compute_m(self, matrix_size, time):
        m = np.zeros((matrix_size, matrix_size))
        for k in range(matrix_size):
            m += np.real(np.outer(self.__xsi[:, k], self.__a[k, :]) * np.exp(self.__g_values[k] * time))
        return m

    def check_calculate(self, func):
        def wrapper(*args, **kwargs):
            if self.__p_i is None:
                raise ValueError('Must call calculate() method before')

            result = func(*args, **kwargs)
            return result

        return wrapper

    def save_throughput(self, style, suffix):
        a_values = self.__builder.build_throughput_values(self.__p_i)

        self.__buffer.add_to_buffer(a_values['$A_1(t)$'], style, rf'$A_1(t)_{{{suffix}}}$')
        self.__buffer.add_to_buffer(a_values['$A_2(t)$'], style, rf'$A_2(t)_{{{suffix}}}$')
        self.__buffer.set_t(self.__t_values)



    def visualise(self, visualiser: Visualiser):
        leg = self.__builder.build_probabilities_legend()

        visualiser.visualise_multiple_graphs(leg, self.__t_values, self.__p_i, 'Probability of SMO')

    def visualise_throughput(self, visualiser: Visualiser):
        a_values = self.__builder.build_throughput_values(self.__p_i)

        p_i_array = np.column_stack(list(a_values.values()))
        visualiser.visualise_multiple_graphs(['$A_1(t)$', '$A_2(t)$'], self.__t_values, p_i_array, 'Throughput')

    def visualise_loss(self, visualiser: Visualiser):
        lose_probabilities = self.__builder.build_lose_probability(self.__p_i)
        visualiser.visualise_single_graph('A(t)', self.__t_values, lose_probabilities, 'Loss')

    def visualise_r(self, visualiser: Visualiser):
        a_values = self.__builder.build_throughput_values(self.__p_i)

        r = (a_values['$A_1(t)$'] - a_values['$A_2(t)$']) / a_values['$A_1(t)$']
        visualiser.visualise_single_graph('R(t)', self.__t_values, r, 'R(t)')

    def calculate_average_count(self, visualiser: Visualiser):
        count = self.__builder.build_average_count(self.__p_i)

        counts = np.column_stack(count)
        visualiser.visualise_multiple_graphs([
            'Count positive packets', 'Count negative packets'
        ], self.__t_values, counts, title='Count of packets')

    def visualise_positive_throughput(self, visualiser: Visualiser):
        throughput = self.__builder.build_positive_throughput(self.__p_i)
        np.column_stack(list(throughput))

        visualiser.visualise_single_graph('A(t)', self.__t_values, throughput, title='Positive throughput')