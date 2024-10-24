# Importar las librerías necesarias
import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Cargar el dataset con coordenadas
df_coordenadas = pd.read_csv('dataset_con_coordenadas.csv')

# Eliminar duplicados basados en el nombre del distrito y las coordenadas
df_unique = df_coordenadas.drop_duplicates(subset=['DISTRITO', 'Latitude', 'Longitude'])

# Crear un grafo vacío
G = nx.Graph()

# Añadir nodos al grafo (cada distrito único)
for i, row in df_unique.iterrows():
    G.add_node(row['DISTRITO'], pos=(row['Latitude'], row['Longitude']))

# Función para calcular la distancia geodésica (Haversine)
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# Conectar los distritos que estén cerca (por ejemplo, a menos de 50 km)
threshold_distance_km = 50

for i, row1 in df_unique.iterrows():
    for j, row2 in df_unique.iterrows():
        if i != j:
            coord1 = (row1['Latitude'], row1['Longitude'])
            coord2 = (row2['Latitude'], row2['Longitude'])
            distance = calculate_distance(coord1, coord2)
            if distance <= threshold_distance_km:
                G.add_edge(row1['DISTRITO'], row2['DISTRITO'], weight=distance)

# Visualizar las conexiones
pos = nx.spring_layout(G)  # Usamos un layout para organizar los nodos

# Dibujar el grafo
plt.figure(figsize=(10,10))

# Dibujar los nodos con sus nombres
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold')

# Mostrar el grafo
plt.show()
