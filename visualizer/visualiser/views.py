from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

def index(request):
    months_data = {
    'February': np.array([
        [1, 2, 1, 2, 1, 2, 2],
        [2, 2, 1, 2, 2, 1, 2],
        [2, 2, 1, 2, 2, 2, 1],
        [2, 2, 2, 2, 2, 2, 2],
        [2, 1, 2, 2, 2, 2, 2],
        [1, 2, 2, 2, 2, 2, 2]
    ]),
    'April': np.array([
        [2, 2, 1, 2, 2, 1, 2],
        [2, 2, 2, 1, 1, 2, 2],
        [1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 2, 1, 2, 2],
        [2, 2, 2, 1, 2, 2, 1],
        [1, 2, 1, 2, 2, 2, 2]
    ]),
    'June': np.array([
        [2, 1, 2, 2, 1, 2, 2],
        [1, 2, 2, 2, 2, 1, 2],
        [2, 2, 2, 1, 1, 2, 2],
        [2, 2, 1, 2, 2, 1, 2],
        [1, 2, 2, 2, 1, 2, 2],
        [2, 1, 2, 1, 2, 2, 2]
    ]),
    'August': np.array([
        [2, 2, 2, 1, 2, 2, 1],
        [2, 1, 2, 2, 1, 2, 2],
        [2, 2, 1, 2, 2, 1, 2],
        [1, 2, 2, 2, 1, 2, 2],
        [2, 2, 2, 1, 2, 2, 1],
        [2, 1, 2, 2, 2, 1, 2]
    ]),
    'October': np.array([
        [2, 2, 2, 1, 2, 2, 1],
        [2, 1, 2, 2, 1, 2, 2],
        [2, 2, 1, 2, 2, 1, 2],
        [1, 2, 2, 2, 1, 2, 2],
        [2, 2, 2, 1, 2, 2, 1],
        [1, 2, 1, 2, 2, 2, 2]
    ]),
    'December': np.array([
        [2, 2, 2, 1, 2, 2, 1],
        [2, 1, 2, 2, 1, 2, 2],
        [2, 2, 1, 2, 2, 1, 2],
        [1, 2, 2, 2, 1, 2, 2],
        [2, 2, 2, 1, 2, 2, 1],
        [2, 1, 2, 1, 2, 2, 2]
    ]),
}


    plot_divs = {}
    for month, matrix in months_data.items():
        fig = go.Figure()

        rows, cols = matrix.shape
        cell_size = 1  # Base cell size normalized to 1
        width = cols * cell_size
        height = rows * cell_size
        margin = 0.05

        # Define colors for server and coolant
        colors = {1: '#ADD8E6', 2: '#808080'}  # Light blue and grey

        for i in range(rows):
            for j in range(cols):
                value = matrix[i, j]
                fig.add_shape(
                    type="rect",
                    x0=j * cell_size,
                    y0=(rows - i - 1) * cell_size,
                    x1=(j + 1) * cell_size,
                    y1=(rows - i) * cell_size,
                    fillcolor=colors[value],
                    line=dict(color="black", width=1)
                )

                fig.add_annotation(
                    x=(j * cell_size + cell_size / 2),
                    y=((rows - i - 1) * cell_size + cell_size / 2),
                    text="Cooler" if value == 1 else "Server",
                    showarrow=False,
                    font=dict(size=14, color="black"),
                    # Center-align the text within the shape
                    xanchor="center",
                    yanchor="middle",
                )

        fig.update_layout(
            title=f"{month}",
            title_font=dict(size=18),
            title_x=0.5,
            title_xanchor='center',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-margin, width + margin]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-margin, height + margin]),
            width=(cols*80),  # Fixed width
            height=(rows*80),  # Fixed height
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            margin=dict(l=30, r=30, t=50, b=30),  # Small margins
        )

        plot_divs[month] = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'plot_divs': plot_divs,
    }
    return render(request, 'visualizer/index.html', context)
