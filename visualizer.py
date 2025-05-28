import networkx as nx
import matplotlib.pyplot as plt

import builder


def visualize_state_graph(n, graph):
    G = nx.DiGraph()

    for edge in graph:
        G.add_edge(edge[0], edge[1], label=edge[2]['label'], color=edge[2]['color'])

    pos = builder.get_pos_array(n)


    fig, ax = plt.subplots(figsize=(12, 6))

    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_size=1000,
                           node_color='lightblue', edgecolors='black', ax=ax)

    # Рисуем все рёбра сначала
    edges = nx.draw_networkx_edges(
        G, pos,
        edge_color=[G[u][v]['color'] for u, v in G.edges()],
        arrowsize=20,
        width=2,
        arrowstyle='->',
        connectionstyle='arc3,rad=0.2',
        ax=ax
    )

    # Теперь добавляем подписи точно по центру
    edge_labels = nx.get_edge_attributes(G, 'label')

    # Для каждого ребра находим точное положение середины
    for i, (u, v) in enumerate(G.edges()):
        edge = edges[i]
        path = edge.get_path()
        verts = path.vertices

        if len(verts) > 2:
            mid_idx = 1
            x, y = verts[mid_idx]

        else:  # Для прямых рёбер
            x = (verts[0][0] + verts[1][0]) / 2
            y = (verts[0][1] + verts[1][1]) / 2

        # Добавляем подпись
        text = ax.text(x, y, edge_labels[(u, v)],
                       fontsize=10, ha='center', va='center',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.0),
                       zorder=10)

    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)

    plt.axis('off')
    plt.tight_layout()

def display_latex(latex_code, font_size=8):
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('off')
    ax.text(0.5, 0.5, latex_code, fontsize=font_size, ha='center', va='center')


def matrix_to_latex(matrix):
    if not matrix:
        return r""

    n_cols = len(matrix[0]) if matrix else 0
    cols = "c" * n_cols
    latex_rows = []
    for row in matrix:
        processed_row = [str(item) for item in row]
        latex_rows.append(" & ".join(processed_row))

    latex_body = " \\\\ ".join(latex_rows)
    return rf"$\left[\begin{{array}}{{{cols}}} {latex_body} \end{{array}}\right]$"


def kolm_to_latex(kolm, states_array):

    kolm_equations = {}
    for state in states_array:
        kolm_equations[state] = dict()

    for state in states_array:
        for variable in kolm[states_array.index(state)]:
            if variable['sign'] == 1:
                if states_array[variable['state']] in kolm_equations[state]:
                    kolm_equations[state][states_array[variable['state']]] += rf'+{variable['value']}'
                else:
                    kolm_equations[state][states_array[variable['state']]] = rf'{variable['value']}'
            else:
                if state in kolm_equations[state]:
                    kolm_equations[state][state] += rf'+{variable['value']}'
                else:
                    kolm_equations[state][state] = rf'{variable['value']}'

    equals = r''
    for state in states_array:
        equal = rf'\frac{{dp_{{{state}}} (t)}}{{dt}} &='
        equal += rf'-({kolm_equations[state][state]}) \frac{{dp_{{{state}}} (t)}}{{dt}}'
        states = kolm_equations[state].keys()
        for inner_state in states:
            if inner_state != state:
                equal += rf'+ {kolm_equations[state][inner_state]} \frac{{dp_{{{inner_state}}} (t)}}{{dt}}'
        equals += rf'{equal} \\'

    kolm_latex = rf'\begin{{align*}}\begin{{cases}} {equals}\end{{cases}}\end{{align*}}'
    return kolm_latex





