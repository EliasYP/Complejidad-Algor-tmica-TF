import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# Cargar el dataset
df = pd.read_csv('Indicadores_de_Cobertura_en_el_Servicio_de_Agua_Potable_en_el_Departamento_de_Cusco_2016_2019.csv')
print("se lee el archivo")
# Preparar las columnas necesarias para formar las consultas a Nominatim
df['Location_Query'] = df['DISTRITO'] + ', ' + df['PROVINCIA'] + ', ' + df['DEPARTAMENTO'] + ', Peru'

# Inicializar el geolocalizador de Nominatim con un user_agent único
geolocator = Nominatim(user_agent="my_unique_geocoder_application", timeout=10)

# Diccionario para almacenar coordenadas ya consultadas (evitar duplicados)
cache = {}

# Función para obtener coordenadas con reintentos
def get_coordinates(query, retries=3):
    if query in cache:
        return cache[query]
    for attempt in range(retries):
        try:
            location = geolocator.geocode(query)
            if location:
                cache[query] = (location.latitude, location.longitude)
                return location.latitude, location.longitude
            else:
                print(f"No se encontraron coordenadas para: {query}")
                return None, None
        except Exception as e:
            print(f"Error al obtener coordenadas para {query}: {e}")
            if attempt < retries - 1:
                print(f"Reintentando... ({attempt+1}/{retries})")
                sleep(2)  # Pausa antes de reintentar
            else:
                print(f"Error definitivo después de {retries} intentos.")
                return None, None

# Crear nuevas columnas para latitud y longitud
df['Latitude'] = None
df['Longitude'] = None

# Obtener coordenadas para cada fila (distrito)
for i, row in df.iterrows():
    lat, lon = get_coordinates(row['Location_Query'])
    df.at[i, 'Latitude'] = lat
    df.at[i, 'Longitude'] = lon
    print(f"Fila {i+1} procesada: {row['Location_Query']} - Coordenadas: {lat}, {lon}")
    sleep(2)  # Pausa entre solicitudes para no sobrecargar el servicio

# Eliminar la columna de Location_Query que solo era auxiliar
df = df.drop(columns=['Location_Query'])

# Guardar el dataset actualizado
df.to_csv('dataset_con_coordenadas.csv', index=False)

print("Proceso completado. Archivo guardado como 'dataset_con_coordenadas.csv'.")
