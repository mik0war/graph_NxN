import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt


class Visualiser:

    def __init__(self, use_latex=True):
        plt.rcParams.update({
            "text.usetex": use_latex,
            "text.latex.preamble": r"\usepackage{amsmath}"
        })

    @staticmethod
    def visualise_multiple_graphs(leg, t_values, p_i, title, x_label='Time (t)', y_label='Probability'):
        fig = go.Figure()
        for i in range(len(leg)):
            fig.add_trace(go.Scatter(
                x=t_values,
                y=p_i[:, i],
                name=leg[i],
                mode='lines',
                hovertemplate=f'<b>{leg[i]}</b><br>t: %{{x}}<br>p: %{{y}}<extra></extra>'
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            hovermode='x unified',
            showlegend=True
        )
        fig.show()

    @staticmethod
    def visualise_multiple_graphs_styled(leg, styles, t_values, p_i, title, x_label='Time (t)', y_label='Probability'):
        line_styles = {
            '-': 'solid',
            '--': 'dash',
            ':': 'dot',
            '-.': 'dashdot'
        }

        fig = go.Figure()
        for i in range(len(leg)):
            fig.add_trace(go.Scatter(
                x=t_values,
                y=p_i[:, i],
                name=leg[i],
                mode='lines',
                line=dict(dash=line_styles.get(styles[i], 'solid')),
                hovertemplate=f'<b>{leg[i]}</b><br>t: %{{x}}<br>p: %{{y}}<extra></extra>'
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            hovermode='x unified',
            showlegend=True
        )
        fig.show()

    @staticmethod
    def visualise_single_graph(leg, t_values, p_i, title, x_label='Time (t)', y_label='Probability'):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=t_values,
            y=p_i,
            name=leg,
            mode='lines',
            hovertemplate=f'<b>{leg}</b><br>t: %{{x}}<br>p: %{{y}}<extra></extra>'
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            hovermode='x unified',
            showlegend=True
        )
        fig.show()

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
                                     label_pos=0.3, font_size=14, connectionstyle='arc3,rad=0.2')

        nx.draw_networkx_labels(g, pos, font_size=14, font_weight='bold', ax=ax)

        plt.axis('off')
        plt.tight_layout()


    @staticmethod
    def display_latex_text(latex_code, font_size=8):
        fig = go.Figure()
        fig.add_annotation(
            text=latex_code,
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=font_size),
            align="center"
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="white"
        )
        fig.show()