import pandas as pd
import numpy as np
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.io import write_image
import pickle
import alphashape
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go

### load data

df = pd.read_parquet('../semantics.parquet')
df["cluster"] = df["cluster"].astype('category')

### Compute the enclosing hulls for each island

# Initialize dictionary to store hull points for each cluster
land_polygons_dict = {}

# Compute hull points for each cluster and store in dictionary
for cluster_id, group in df.groupby('cluster', observed=True):
    if group['cluster'].iloc[0].astype(int)>=0:
        alpha = 25 # The highest alpha to try (most reticulated coastline)
        got_hull = False
        while not got_hull:
            # Keep trying consecutively lower alphas until we get a polygon that works
            try:
                points = group[['umap_1', 'umap_2']]
                hull = alphashape.alphashape(points, alpha=alpha)  # Adjust alpha for concavity
                if hull.geom_type == 'Polygon':
                    hull_points = list(zip(*hull.exterior.coords.xy))
                elif hull.geom_type == 'MultiPolygon':  # Handle multiple polygons if needed
                    hull_points = [list(zip(*poly.exterior.coords.xy)) for poly in hull]
                    print('multi')
                else:
                    hull_points = []
                land_polygons_dict[cluster_id] = {"name": f'{group.iloc[0].territory_name} ({group.iloc[0].cluster_topic})',
                                                  "polygon": hull_points}
                got_hull = True
            except:
                alpha = alpha - 1

### functions to create colors
                
                # Map the valence, humanity, and physicality scores to colors

def color_name_to_rgb(name):
    if name == 'orange':
            return [220, 185, 0]
    if name == 'green':
            return [0, 185, 0]
    if name == 'grey':
            return [210, 210, 210]

def map_value_to_color(value, low_color='orange', high_color='green', value_min=1, value_max=5, saturation=1):
    low_color = color_name_to_rgb(low_color)
    high_color = color_name_to_rgb(high_color)

    # Normalize
    normalized_value = (value - value_min) / (value_max - value_min)
    
    # Interpolate
    interpolated_color = [low_color[i] + (high_color[i] - low_color[i]) * normalized_value for i in range(3)]
    
    # Desaturate
    interpolated_color = [int(v*saturation) for v in interpolated_color]

    return '#{:02x}{:02x}{:02x}'.format(*interpolated_color)

def mix_hex_colors(hex1, hex2):
    # Convert hex to RGB
    rgb1 = int(hex1[1:], 16)
    rgb2 = int(hex2[1:], 16)
    
    # Extract RGB components
    r1, g1, b1 = (rgb1 >> 16) & 0xFF, (rgb1 >> 8) & 0xFF, rgb1 & 0xFF
    r2, g2, b2 = (rgb2 >> 16) & 0xFF, (rgb2 >> 8) & 0xFF, rgb2 & 0xFF
    
    # Average the RGB components
    r_avg = (r1 + r2) // 2
    g_avg = (g1 + g2) // 2
    b_avg = (b1 + b2) // 2
    
    # Convert back to hex
    return f'#{r_avg:02x}{g_avg:02x}{b_avg:02x}'

# Placeholder for your hex color function
def hpv_to_color(h, p, v, saturation=1):
    v = (v-1)/3.5 # rescale v to 0 to 1 range
    saturation = saturation * (v+0.75)/1.75
    c1 = map_value_to_color(h, saturation=saturation)
    c2 = map_value_to_color(p, low_color='grey', saturation=saturation)
    
    return mix_hex_colors(c1, c2)
    # return f'#{h:02x}{p:02x}{(h+p):02x}'

# Plot
def add_line_break(text, n):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line) + len(word) + 1 <= n:
            current_line += word + ' '
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    return '<br>'.join(lines)
df['annotation'] = df[['territory_name', 'cluster_topic', 'sfw_term','sfw_definition']].apply(lambda row: f'{row.territory_name} ({row.cluster_topic})<br><br>{add_line_break(f"{row.sfw_term}: {row.sfw_definition}",60)}', axis=1)

def cluster_to_color(cluster, saturation=1):
    row = df[df.cluster==cluster].iloc[0]
    if row.cluster.astype(int)<0:
        return 'rgb(230, 230, 255)'
    humanity = row.humanity
    physicality = row.physicality
    valence = row.valence
    return hpv_to_color(humanity, physicality, valence, saturation)#map_value_to_color(humanity, saturation=saturation)

color_map = {cluster: cluster_to_color(cluster, 0.9) for cluster in df.cluster.unique()}

# marked_cluster = df[df.term == 'fire']['cluster'].to_list()
# for i in marked_cluster:
#     if i!=-1:
#         color_map[i] = 'red'

def draw_lexiconia_map():
    fig = go.Figure()

    for cluster in land_polygons_dict:
        polygon = land_polygons_dict[cluster]["polygon"]
        # fig.add_trace(go.Scatter(x=[p[0] for p in polygon], y=[p[1] for p in polygon], mode='lines', fill='toself'))
        color = cluster_to_color(cluster)
        fig.add_trace(go.Scatter(
                                x=[v[0] for v in polygon], 
                                y=[v[1] for v in polygon], 
                                mode='lines', 
                                fill='toself',
                                text=land_polygons_dict[cluster]["name"],
                                fillcolor=color, # fill color
                                line=dict(color=color)  # outline color
                            ))

    # draw the lands
    land_df = df[df['cluster'].astype('int')>=0]
    land_df["cluster"] = land_df["cluster"].astype('int').astype('category')
    scatter_plot = px.scatter(land_df, x='umap_1', y='umap_2',
                                    color='cluster',
                                    hover_name='annotation',
                                    hover_data={'umap_1': False, 'umap_2': False, 'cluster': False},
                                    color_discrete_map=color_map)
    scatter_plot.update_traces(marker={'size': 2.5}, hoverinfo='skip', hovertemplate=None)
    for trace in scatter_plot.data:
        fig.add_trace(trace)

    # draw the seas
    sea_df = df[df['cluster'].astype('int')<0]
    sea_df["cluster"] = sea_df["cluster"].astype('int').astype('category')
    scatter_plot = px.scatter(sea_df, x='umap_1', y='umap_2',
                                    color='cluster',
                                    hover_name='annotation',
                                    hover_data={'umap_1': False, 'umap_2': False, 'cluster': False},
                                    color_discrete_map=color_map)
    scatter_plot.update_traces(marker={'size': 2.5})
    for trace in scatter_plot.data:
        fig.add_trace(trace)

    fig.update_layout(title={'text': '<b>Lexiconia</b><br><a href="https://github.com/jjdhunt/lexiconia">https://github.com/jjdhunt/lexiconia</a>',
                            'y':0.97,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                    autosize=True,
                    plot_bgcolor='skyblue',
                    showlegend=False,
                    xaxis=dict(showgrid=False,
                                showticklabels=False,
                                zeroline=False,
                                scaleanchor='y',  # This makes x-axis scale depend on y-axis
                                scaleratio=1),  # This ensures the scale ratio is 1:1),
                    yaxis=dict(showgrid=False,
                                showticklabels=False,
                                zeroline=False),
                    dragmode='pan')
    return fig

base_fig = draw_lexiconia_map()

config = {
    'scrollZoom': True,
    'responsive': True,  # Make plot responsive to window size
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
        'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 
        'hoverCompareCartesian', 'toggleSpikelines'
    ]
}

##### Dash App #####

current_word = df[df['cluster'].astype('int')>=0].sample(1).iloc[0]
goal_word = df[df['cluster'].astype('int')>=0].sample(1).iloc[0]
history_words = None

n_submissions = 0
max_travel_distance = 1

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='lexiconia-plot',
        figure=base_fig,
        config=config,
        style={'height': '90vh'}
    ),
    dcc.Input(id='term-input', type='text', placeholder='Enter term...', debounce=True)
])

@app.callback(
    Output('lexiconia-plot', 'figure'),
    Input('term-input', 'value'),
    [State('lexiconia-plot', 'figure')]
)
def update_plot(input_value, cur_fig):
    global current_word
    global history_words
    fig = go.Figure(base_fig)
    fig.update_layout(cur_fig['layout'])
    if input_value:
        filtered_df = df[df['term'] == input_value]
        if filtered_df.shape[0]>0:
            scatter_trace = go.Scattergl(
                x=filtered_df['umap_1'],
                y=filtered_df['umap_2'],
                mode='markers',
                hoverinfo='text',
                text=filtered_df['annotation'],
                marker=dict(color='darkred',size=10)
            )
            fig.add_trace(scatter_trace)

            #move to the closest point if it is close enough
            x0 = current_word['umap_1']
            y0 = current_word['umap_2']
            filtered_df['distance'] = filtered_df[['umap_1', 'umap_2']].apply(lambda row: np.sqrt((row['umap_1'] - x0)**2 + (row['umap_2'] - y0)**2), axis=1)
            closest_row = filtered_df.loc[filtered_df['distance'].idxmin()]
            if closest_row['cluster'].astype('int') >= 0 and closest_row['distance'] <= max_travel_distance:
                history_words = pd.concat([history_words, current_word.to_frame().T])
                current_word = closest_row

    # add history words
    if history_words is not None:
        scatter_trace = go.Scattergl(
                x=history_words['umap_1'],
                y=history_words['umap_2'],
                mode='markers',
                hoverinfo='text',
                text=history_words['annotation'],
                marker=dict(color='darkgoldenrod',size=10)
            )
        fig.add_trace(scatter_trace)

    # add current word
    scatter_trace = go.Scattergl(
            x=[current_word['umap_1']],
            y=[current_word['umap_2']],
            mode='markers',
            hoverinfo='text',
            text=[current_word['annotation']],
            marker=dict(color='gold',size=10)
        )
    fig.add_trace(scatter_trace)

    # add goal word
    scatter_trace = go.Scattergl(
            x=[goal_word['umap_1']],
            y=[goal_word['umap_2']],
            mode='markers',
            hoverinfo='text',
            text=[goal_word['annotation']],
            marker=dict(color='limegreen',size=10)
        )
    fig.add_trace(scatter_trace)

    return fig

if __name__ == '__main__':
    app.run(debug=True)