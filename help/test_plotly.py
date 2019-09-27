import plotly
import plotly.plotly as py
import plotly.graph_objs as go


title = 'Graphical representation of the report'

# data
x_data_f = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
y_data_f = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]

x_data_g = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]
y_data_g = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]

traces = []

# Create and style traces
fFunction = go.Scatter(
    x = x_data_f,
    y = y_data_f,
    mode='lines+markers',
    name = 'f(x)',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 3,
        shape='spline')
)
gFunction = go.Scatter(
    x = x_data_g,
    y = y_data_g,
    mode='lines+markers',
    name = 'g(x)',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 3,
        shape='spline')
)

traces = [fFunction, gFunction]


# Edit the layout
layout = dict(title = title)

fig = dict(data=traces, layout=layout)
plotly.offline.plot(fig, filename='report_example.html')
