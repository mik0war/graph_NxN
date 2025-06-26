import networkx as nx
from matplotlib import pyplot as plt


class Visualiser:

    def __init__(self, use_latex=True):
        plt.rcParams.update({
            "text.usetex": use_latex,
            "text.latex.preamble": r"\usepackage{amsmath}"
        })

    @staticmethod
    def visualise_probability(leg, t_values, p_i):
        plt.figure(figsize=(10, 6))
        for i in range(leg.__len__()):
            plt.plot(t_values, p_i[:, i], label=leg[i])

        plt.xlabel('Time (t)')
        plt.ylabel('Probability')
        plt.title('Probability of SMO')
        plt.grid(True)
        plt.legend()

    @staticmethod
    def visualise_loss(leg, t_values, p_i):
        plt.figure(figsize=(14, 8))
        plt.plot(t_values, p_i, label=leg)

        plt.xlabel('Time (t)')
        plt.ylabel('Probability')
        plt.title('Probability of loss')
        plt.grid(True)
        plt.legend()

    @staticmethod
    def visualise_graph(builder):
        g = nx.DiGraph()

        pos = builder.build_graph_positions(g)

        fig, ax = plt.subplots(figsize=(12, 6))

        # Рисуем узлы
        nx.draw_networkx_nodes(g, pos, node_size=1000,
                               node_color='lightblue', edgecolors='black', ax=ax)

        # Рисуем все рёбра сначала
        nx.draw_networkx_edges(
            g, pos,
            edge_color=[g[u][v]['color'] for u, v in g.edges()],
            arrowsize=20,
            width=2,
            arrowstyle='->',
            connectionstyle='arc3,rad=0.2',
            ax=ax
        )

        edge_labels = nx.get_edge_attributes(g, 'label')

        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels,
                                     label_pos=0.3, font_size=7, connectionstyle='arc3,rad=0.2')

        nx.draw_networkx_labels(g, pos, font_size=12, font_weight='bold', ax=ax)

        plt.axis('off')
        plt.tight_layout()

    @staticmethod
    def display_latex_text(latex_code, font_size=8):
        fig, ax = plt.subplots(figsize=(5, 2))
        ax.axis('off')
        ax.text(0.5, 0.5, latex_code, fontsize=font_size, ha='center', va='center')
