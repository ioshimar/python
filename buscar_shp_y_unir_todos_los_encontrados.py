import geopandas as gpd
import os
import pandas as pd

# Directorio principal donde se buscarán los archivos shapefile
directorio_principal = 'D:/RESPALDO/RAN'

# Nombre del shapefile que deseas buscar y unir
nombre_shapefile = 'PARCELA'

# Función para buscar y unir los archivos shapefile por nombre
def unir_shapefiles_por_nombre(directorio, nombre):
    shapefiles = []  # Una lista para almacenar los GeoDataFrames con el nombre especificado

    # Recorre el directorio y sus subdirectorios
    for ruta, carpetas, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith('.shp'):
                nombre_archivo = os.path.splitext(archivo)[0]
                if nombre_archivo == nombre:
                    ruta_completa = os.path.join(ruta, archivo)
                    gdf = gpd.read_file(ruta_completa)
                    if not gdf.empty:  # Verifica si el GeoDataFrame no está vacío
                        shapefiles.append(gdf)

    if shapefiles:
        # Unir todos los GeoDataFrames en uno solo
        gdf_final = gpd.GeoDataFrame(pd.concat(shapefiles, ignore_index=True), crs=shapefiles[0].crs)
        return gdf_final, len(shapefiles)
    else:
        return None, 0

# Llama a la función para buscar y unir los shapefiles por nombre
shapefile_unido, num_archivos_encontrados = unir_shapefiles_por_nombre(directorio_principal, nombre_shapefile)

if shapefile_unido:
    # Guarda el GeoDataFrame final en un nuevo archivo shapefile
    shapefile_unido.to_file(f'{nombre_shapefile}_unido.shp')
    print(f'Se encontraron {num_archivos_encontrados} archivos con el nombre {nombre_shapefile}.')
    print(f'Shapefile {nombre_shapefile} unido y guardado como {nombre_shapefile}_unido.shp')
else:
    print(f'No se encontraron archivos con el nombre {nombre_shapefile}.')