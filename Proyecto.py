

import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
from sklearn.cluster import KMeans
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv('Indicadores_de_Cobertura_en_el_Servicio_de_Agua_Potable_en_el_Departamento_de_Cusco_2016_2019.csv')

# Add fictitious columns for additional analysis
df['Tiempo_Respuesta'] = np.random.randint(1, 10, df.shape[0])
df['Frecuencia_Mantenimiento'] = np.random.randint(1, 5, df.shape[0])

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3)
df['Cluster'] = kmeans.fit_predict(df[['Tiempo_Respuesta', 'Frecuencia_Mantenimiento']])

# Create graph
G = nx.Graph()

# Add nodes
for distrito in df['DISTRITO'].unique():
    G.add_node(distrito)

# Add edges (example: based on same province)
for _, row in df.iterrows():
    for _, row2 in df.iterrows():
        if row['PROVINCIA'] == row2['PROVINCIA'] and row['DISTRITO'] != row2['DISTRITO']:
            G.add_edge(row['DISTRITO'], row2['DISTRITO'])

# Visualize graph using Plotly
pos = nx.spring_layout(G)
edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Network Graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False))
                )

fig.show()