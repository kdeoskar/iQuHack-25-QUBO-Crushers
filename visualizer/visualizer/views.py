from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

def index(request):
    seasons_data = {
        'Winter': np.array([
            [1, 2, 2, 2],
            [2, 2, 1, 2],
            [2, 2, 1, 2],
            [2, 2, 2, 1],
            [2, 1, 2, 2]
        ]),
        'Spring': np.array([
            [2, 2, 1, 2],
            [2, 2, 2, 1],
            [1, 2, 2, 2],
            [2, 1, 2, 2],
            [2, 2, 2, 1]
        ]),
        'Summer': np.array([
            [2, 1, 2, 2],
            [1, 2, 2, 2],
            [2, 2, 2, 1],
            [2, 2, 1, 2],
            [1, 2, 2, 2]
        ]),
        'Fall': np.array([
            [2, 2, 2, 1],
            [2, 1, 2, 2],
            [2, 2, 1, 2],
            [1, 2, 2, 2],
            [2, 2, 2, 1]
        ]),
    }

    plot_divs = {}
    for season, matrix in seasons_data.items():
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
            title=f"Optimal - {season}",
            title_font=dict(size=18),
            title_x=0.5,
            title_xanchor='center',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-margin, width + margin]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-margin, height + margin]),
            width=450,  # Fixed width
            height=450,  # Fixed height
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            margin=dict(l=30, r=30, t=50, b=30),  # Small margins
        )

        plot_divs[season] = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'plot_divs': plot_divs,
    }
    return render(request, 'visualizer/index.html', context)
