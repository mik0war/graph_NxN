import numpy as np
from scipy.linalg import eig

from builder import Builder
from visualiser import Visualiser


class Calculator:

    def __init__(self, builder : Builder):
        self.__builder = builder

        #Calculation results
        self.__g_values = None
        self.__p_i = None
        self.__t_values = None

        #Time params
        self.__start = 0
        self.__end = 0.025
        self.__num = 2000

        #Decorators
        self.visualise = self.check_calculate(self.visualise)
        self.visualise_throughput = self.check_calculate(self.visualise_throughput)

    def set_time_params(self, start, end, num):
        self.__num = num
        self.__start = start
        self.__end = end

    def calculate(self, matrix, p = None):
        matrix_size = matrix.__len__()

        # Начальное распределение вероятностей
        if not p:
            p = np.array([0 for _ in range(matrix_size)])
            p[0] = 1

        ### Вычисление собственных значений и векторов
        self.__g_values, xsi = eig(matrix)  # XSI - матрица правых собственных векторов
        ### Вычисление коэффициентов A (через обратную матрицу)
        a = np.linalg.inv(xsi)

        ### Вычисление матрицы переходов M(t)
        def compute_m(time):
            m = np.zeros((matrix_size, matrix_size))
            for k in range(matrix_size):
                m += np.real(np.outer(xsi[:, k], a[k, :]) * np.exp(self.__g_values[k] * time))
            return m

        ### Вычисление вероятностей P_i(t)
        self.__t_values = np.linspace(self.__start, self.__end, self.__num)  # Временной интервал
        p_i = np.zeros((len(self.__t_values), matrix_size + 1))  # +1 для суммы вероятностей

        for idx, t in enumerate(self.__t_values):
            m_t = compute_m(t)
            p_i_t = m_t @ p  # Умножение матрицы на вектор начальных условий
            p_i[idx, :matrix_size] = p_i_t
            p_i[idx, matrix_size] = np.sum(p_i_t)  # Сумма вероятностей (должна быть 1)

        self.__p_i = p_i

    def check_calculate(self, func):
        def wrapper(*args, **kwargs):

            if self.__p_i is None:
                raise ValueError('Must call calculate() method before')

            result = func(*args, **kwargs)
            return result

        return wrapper

    def visualise(self, visualiser : Visualiser):
        self.__builder.visualise_probabilities(visualiser, self.__t_values, self.__p_i)


    def visualise_throughput(self, visualiser: Visualiser):
        self.__builder.visualise_loss(visualiser, self.__t_values, self.__p_i)

