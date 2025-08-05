import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1, 2, 3],
    y=[1, 2, 3],
    name='$A_1(t)$'  # Будет рендериться в легенде
))

fig.update_layout(
    title='График $A_1(t)$',  # LaTeX в заголовке
    xaxis_title='$t$',
    yaxis_title='$A_1$'
)

fig.show()