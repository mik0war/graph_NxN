from data_types.labels import Label
from data_types.state import Edge, State


class Coefficient:

    def __init__(self, value: Label, sign: int):
        self.__values = value
        self.__sign = sign

    def map_to_matrix_coefficient(self) -> tuple[list[Label], int]:
        return [self.__values], self.__sign

    def get_latex_value(self) -> str:
        return rf'{self.__values.get_latex()}'


class MatrixElement:
    def __init__(self):
        self.__values: list[Label] = []
        self.__sign = 1

    def add_element(self, coefficient: Coefficient) -> None:
        coefficients_list, sign = coefficient.map_to_matrix_coefficient()
        self.__values += coefficients_list
        self.__sign = sign

    def get_value(self) -> int:
        sum_values = 0
        for value in self.__values:
            sum_values = value.add_value(sum_values)

        return sum_values * self.__sign

    def get_latex_value(self) -> str:
        if self.__values.__len__() == 0:
            return r'0'

        latex = r''

        for value in self.__values:
            latex += rf' + {value.get_latex()}'

        latex = latex[2:]

        if self.__sign == -1:
            latex = rf'-({latex})'
        return latex


class Equation:
    def __init__(self):
        self.__coefficients: dict[State, list[Coefficient]] = {}

    def add_value(self, value: Label, index: State, sign: int) -> None:
        self.__coefficients.setdefault(index, []).append(Coefficient(value, sign))

    def fill_matrix_line(self, matrix_line: list[MatrixElement]) -> None:
        for index in self.__coefficients.keys():
            for coefficient in self.__coefficients[index]:
                matrix_line[index.get_numeric_index()].add_element(coefficient)

    def map_to_latex(self, state: State):
        equal = rf'\frac{{d{state.map_to_latex()} (t)}}{{dt}} &='
        coefficient_latex = r''
        for value in self.__coefficients[state]:
            coefficient_latex += rf' + {value.get_latex_value()}'
        coefficient_latex = coefficient_latex[2:]
        equal += rf'-({coefficient_latex}) \frac{{d{state.map_to_latex()} (t)}}{{dt}}'

        for coefficient_state in self.__coefficients:
            if coefficient_state != state:
                for value in self.__coefficients[coefficient_state]:
                    equal += rf' + {value.get_latex_value()} \frac{{d{coefficient_state.map_to_latex()} (t)}}{{dt}}'
        return equal


class EquationSystem:

    def __init__(self, buffer_size: int, states_list: dict[int | str, State]):
        self.__equations: dict[State, Equation] = {}
        for i in range(buffer_size + 1):
            for j in range(buffer_size + 1):
                if i + j > buffer_size:
                    break
                self.__equations[states_list[f'{i}{j}']] = Equation()

    def fill_equations(self, edges: list[Edge]) -> None:
        for edge in edges:
            edge.add_to_equation_from_node(self.__equations)
            edge.add_to_equation_to_node(self.__equations)

    def map_to_matrix(self) -> list[list[MatrixElement]]:
        matrix = [[MatrixElement() for _ in range(self.__equations.__len__())]
                  for _ in range(self.__equations.__len__())]

        for index, state in enumerate(self.__equations):
            self.__equations[state].fill_matrix_line(matrix[index])

        return matrix

    def map_to_latex(self) -> str:
        equals = r''
        for state in self.__equations:
            equal_latex = self.__equations[state].map_to_latex(state)
            equals += rf'{equal_latex} \\'

        return rf'\begin{{align*}}\begin{{cases}} {equals} \end{{cases}}\end{{align*}}'
