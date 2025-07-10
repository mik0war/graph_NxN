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
        # В Plotly стили линий задаются по-другому, преобразуем matplotlib styles в plotly
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

        edge_x = []
        edge_y = []
        edge_colors = []
        edge_labels = []
        for u, v in g.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_colors.append(g[u][v]['color'])
            edge_labels.append(g[u][v]['label'])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='gray'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        for node in g.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle center",
            hoverinfo='text',
            marker=dict(
                showscale=False,
                colorscale='Blues',
                size=20,
                color='lightblue',
                line=dict(width=2, color='black'))
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Graph Visualization',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        # Добавляем подписи к ребрам
        middle_node_trace = go.Scatter(
            x=[], y=[],
            text=[],
            mode='text',
            hoverinfo='none',
            textfont=dict(size=14)
        )

        for edge in g.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            middle_node_trace['x'] += tuple([(x0 + x1) / 2])
            middle_node_trace['y'] += tuple([(y0 + y1) / 2])
            middle_node_trace['text'] += tuple([g.edges[edge]['label']])

        fig.add_trace(middle_node_trace)
        fig.show()

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