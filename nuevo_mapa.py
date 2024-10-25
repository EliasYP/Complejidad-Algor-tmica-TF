import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame
from tkinter import simpledialog

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

# Función para mostrar el grafo original
def show_graph():
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold')
    plt.show()

# Función para aplicar Dijkstra
def apply_dijkstra():
    start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:")
    end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")
    if start_node and end_node:
        try:
            path = nx.dijkstra_path(G, source=start_node, target=end_node)
            pos = nx.spring_layout(G)
            plt.figure(figsize=(10, 10))
            nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold')
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
            plt.show()
        except nx.NetworkXNoPath:
            print("No hay camino entre los nodos especificados.")

# Función para aplicar Bellman-Ford
def apply_bellman_ford():
    start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:")
    end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")
    if start_node and end_node:
        try:
            path = nx.bellman_ford_path(G, source=start_node, target=end_node)
            pos = nx.spring_layout(G)
            plt.figure(figsize=(10, 10))
            nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold')
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='g', width=2)
            plt.show()
        except nx.NetworkXNoPath:
            print("No hay camino entre los nodos especificados.")

# Crear la interfaz gráfica
root = Tk()
root.title("Visualización de Grafos")

frame = Frame(root)
frame.pack(pady=20)

btn_show_graph = Button(frame, text="Mostrar Grafo Original", command=show_graph)
btn_show_graph.pack(side="left", padx=10)

btn_dijkstra = Button(frame, text="Aplicar Dijkstra", command=apply_dijkstra)
btn_dijkstra.pack(side="left", padx=10)

btn_bellman_ford = Button(frame, text="Aplicar Bellman-Ford", command=apply_bellman_ford)
btn_bellman_ford.pack(side="left", padx=10)

root.mainloop()