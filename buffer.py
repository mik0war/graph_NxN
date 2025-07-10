import numpy as np

from visualiser import Visualiser


class Buffer:
    def __init__(self):
        self.__buffer = {}
        self.__t_values = None

    def add_to_buffer(self, item, style, leg):
        self.__buffer[leg] = (item, style)

    def set_t(self, t_values):
        self.__t_values = t_values

    def visualise_buffer(self, visualiser: Visualiser):
        leg = []
        styles = []
        p_values = []

        for key in self.__buffer.keys():
            leg.append(key)
            styles.append(self.__buffer[key][1])
            p_values.append(self.__buffer[key][0])

        p_values = np.column_stack(p_values)
        visualiser.visualise_multiple_graphs_styled(leg, styles, self.__t_values, p_values, 'Different parameters')
