from networkx.classes import DiGraph

from data_types.labels import Label


class State:
    def __init__(self, index: int, label: str):
        self.__index = index
        self.__label = label

    def get_numeric_index(self) -> int:
        return self.__index

    def get_string_index(self) -> str:
        return self.__label

    def map_to_latex(self):
        return rf'p_{{{self.__label}}}'


class Edge:
    def __init__(self, node_from: State, node_to: State, label: Label):
        self.__node_from = node_from
        self.__node_to = node_to
        self.__label = label

    def add_to_equation_from_node(self, equations):
        equations[self.__node_from].add_value(self.__label, self.__node_from, -1)

    def add_to_equation_to_node(self, equations):
        equations[self.__node_to].add_value(self.__label, self.__node_from, 1)

    def add_to_graph(self, g: DiGraph):
        g.add_edge(self.__node_from.get_string_index(), self.__node_to.get_string_index(),
                   label=rf'${self.__label.get_latex()}$', color=self.__label.get_color())
