import os
import geopandas as gpd
import pandas as pd  # Importante agregar esta línea


def merge_shapefiles(input_folder, output_file, target_crs=None):
    # Lista de todos los archivos .shp en la carpeta de entrada
    shapefile_list = [file for file in os.listdir(input_folder) if file.endswith('.shp')]
    
    # Si no hay archivos .shp en la carpeta de entrada, salimos del programa
    if not shapefile_list:
        print("No se encontraron archivos .shp en la carpeta especificada.")
        return
    
    # Leer el primer shapefile para inicializar el GeoDataFrame que contendrá la fusión
    gdf_merged = gpd.read_file(os.path.join(input_folder, shapefile_list[0]))
    
    # Si se proporciona un CRS de destino, transformar todas las geometrías a ese CRS
    if target_crs:
        gdf_merged = gdf_merged.to_crs(target_crs)
    
    # Unir los demás shapefiles al GeoDataFrame
    for shapefile in shapefile_list[1:]:
        gdf_to_merge = gpd.read_file(os.path.join(input_folder, shapefile))
        
        # Si se proporciona un CRS de destino, transformar las geometrías a ese CRS
        if target_crs:
            gdf_to_merge = gdf_to_merge.to_crs(target_crs)
        
        gdf_merged = gpd.GeoDataFrame(
            pd.concat([gdf_merged, gdf_to_merge], ignore_index=True),
            crs=gdf_merged.crs
        )
    
    # Guardar el resultado en un nuevo shapefile
    gdf_merged.to_file(output_file)
    print(f"Se han unido {len(shapefile_list)} shapefiles en {output_file}.")

# Ejemplo de uso:
input_folder = 'D:/RESPALDO/PRUEBAS_PROYECTO_CONSULCURT/DatosAbiertos_Marzo2016'
output_file = 'D:/RESPALDO/PRUEBAS_PROYECTO_CONSULCURT/DatosAbiertos_Marzo2016/unido.shp'
target_crs = 'EPSG:4326'  # Por ejemplo, WGS 84
merge_shapefiles(input_folder, output_file, target_crs)
