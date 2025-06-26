import numpy as np
from numpy import ndarray

from data_types.equations_type import EquationSystem, MatrixElement
from data_types.labels import *
from data_types.state import State, Edge
from visualiser import Visualiser


class Parameters:
    def __init__(self, lam1: int, lam2: int, mu1: int, mu2: int):
        self.lam_one = LambdaOne(lam1)
        self.lam_two = LambdaTwo(lam2)
        self.mu_one = MuOne(mu1)
        self.mu_two = MuTwo(mu2)


class Builder:
    def __init__(self, parameters: Parameters):
        self.__parameters = parameters
        self.__states: dict[str | int, State] | None = None
        self.__edges: list[Edge] | None = None
        self.__kolm_system: EquationSystem | None = None
        self.__matrix: list[list[MatrixElement]] | None = None
        self.__buffer_size: int = 0

    def build_states(self, buffer_size: int):

        states = {}
        index = 0
        for i in range(buffer_size + 1):
            for j in range(buffer_size + 1):
                if i + j > buffer_size:
                    continue

                states[index] = State(index, i, j)
                states[f'{i}{j}'] = states[index]
                index += 1

        self.__states = states
        return self.__states

    def build_edges(self, buffer_size: int):
        if not self.__states:
            self.build_states(buffer_size)

        edges_with_labels = []

        for i in range(buffer_size + 1):
            for j in range(buffer_size + 1):

                if i + j > buffer_size:
                    continue

                conditions = [
                    [j + 1 + i <= buffer_size, f'{i}{j + 1}', self.__parameters.lam_one],
                    [i + j <= buffer_size and j - 1 >= 0, f'{i + 1}{j - 1}', self.__parameters.lam_two],
                    [j == 0 and i + 1 <= buffer_size, f'{i + 1}{j}', self.__parameters.lam_two],
                    [i - 1 >= 0, f'{i - 1}{j}', self.__parameters.mu_two],
                    [j - 1 >= 0, f'{i}{j - 1}', self.__parameters.mu_one],
                ]

                for condition in conditions:
                    if condition[0]:
                        edges_with_labels.append(Edge(self.__states[f'{i}{j}'],
                                                      self.__states[condition[1]],
                                                      condition[2]))

        self.__edges = edges_with_labels
        return edges_with_labels

    def build_equation_system(self, buffer_size: int):
        if not self.__edges:
            self.build_edges(buffer_size)

        self.__kolm_system = EquationSystem(buffer_size, self.__states)
        self.__kolm_system.fill_equations(self.__edges)

        return self.__kolm_system

    def build_matrix(self, buffer_size: int):
        if not self.__kolm_system:
            self.build_equation_system(buffer_size)

        self.__matrix = self.__kolm_system.map_to_matrix()
        self.__buffer_size = buffer_size

        matrix = [[0 for _ in range(self.__matrix.__len__())]
                  for _ in range(self.__matrix.__len__())]

        for i in range(self.__matrix.__len__()):
            for j in range(self.__matrix.__len__()):
                matrix[i][j] = self.__matrix[i][j].get_value()

        return matrix

    def build_probabilities_legend(self):

        leg = []
        for state in self.__states:
            if isinstance(state, int):
                leg.append(rf'${self.__states[state].map_to_latex()}$')
        leg.append('1')

        return leg

    def build_lose_probability(self, p_values: ndarray):
        lose_probabilities = [
            p_values[:, self.__states[state].get_numeric_index()]
            for state in self.__states
            if isinstance(state, int) and self.__states[state].get_state_sum() == self.__buffer_size
        ]

        return np.sum(lose_probabilities, axis=0)

    def build_throughput_values(self, p_values: ndarray):
        throughput_values: ndarray = self.build_lose_probability(p_values)

        lam_one = self.__parameters.lam_one.get_value()
        lam_two = self.__parameters.lam_two.get_value()

        a_values = {
            '$A_1(t)$': lam_one * (1 - throughput_values),
            '$A_2(t)$': lam_two * (1 - throughput_values)
        }

        return a_values

    def build_graph_positions(self, g) -> dict[str, tuple[int, int]]:
        for edge in self.__edges:
            edge.add_to_graph(g)

        pos = {}
        for i in range(self.__buffer_size + 1):
            for j in range(self.__buffer_size + 1):
                if i + j > self.__buffer_size:
                    break

                pos[f'{i}{j}'] = (j, self.__buffer_size - i)
        return pos

    def build_matrix_latex(self):
        if not self.__matrix:
            return r""

        n_cols = len(self.__matrix) if self.__matrix else 0
        cols = "c" * n_cols
        latex_rows = []
        for row in self.__matrix:
            processed_row = [item.get_latex_value() for item in row]
            latex_rows.append(" & ".join(processed_row))

        latex_body = " \\\\ ".join(latex_rows)
        return rf"$\left[\begin{{array}}{{{cols}}} {latex_body} \end{{array}}\right]$"

    def build_latex_evaluation_system(self, ):
        return self.__kolm_system.map_to_latex()
