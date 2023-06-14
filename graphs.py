import plotly.graph_objects as go
import os

# Create the 'graphs' directory if it doesn't exist
if not os.path.exists('static/graphs'):
    os.makedirs('static/graphs')


def create_scatter_plot(x, y, x_label, y_label, filename):
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.write_image(f"static/graphs/{filename}.png")
    return filename+'.png'


def create_line_chart(x, y, x_label, y_label, filename):
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.write_image(f"static/graphs/{filename}.png")
    return filename+'.png'



def create_bar_chart(x, y, x_label, y_label, filename):
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.write_image(f"static/graphs/{filename}.png")
    return filename+'.png'



def create_heatmap(z, x_labels, y_labels, x_label, y_label, filename):
    fig = go.Figure(data=go.Heatmap(z=z, x=x_labels, y=y_labels))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.write_image(f"static/graphs/{filename}.png")
    return filename+'.png'



def create_bubble_chart(x, y, size, x_label, y_label, filename):
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers', marker=dict(size=size)))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.write_image(f"static/graphs/{filename}.png")
    return filename+'.png'



# Example usage:
x_values = [1, 2, 3, 4, 5]
y_values = [10, 5, 7, 8, 12]
z_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
x_labels = ['A', 'B', 'C']
y_labels = ['X', 'Y', 'Z']

create_scatter_plot(x_values, y_values, 'X-axis', 'Y-axis', 'scatter_plot')
create_line_chart(x_values, y_values, 'X-axis', 'Y-axis', 'line_chart')
create_bar_chart(x_values, y_values, 'X-axis', 'Y-axis', 'bar_chart')
create_heatmap(z_values, x_labels, y_labels, 'X-axis', 'Y-axis', 'heatmap')
create_bubble_chart(x_values, y_values, [20, 30, 40, 50, 60], 'X-axis', 'Y-axis', 'bubble_chart')
