import geopandas as gpd
import pandas as pd

def merge_data_to_shapefile(shapefile_path, excel_path, common_field, output_path):
    # Leer el shapefile y el archivo Excel
    gdf = gpd.read_file(shapefile_path)
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # Verificar si el campo común existe en ambos conjuntos de datos
    if common_field not in gdf.columns or common_field not in df.columns:
        print(f"El campo común '{common_field}' no existe en ambos conjuntos de datos.")
        return
    
    # Convertir la columna del archivo Excel al tipo de dato object
    df[common_field] = df[common_field].astype(str)
    
    # Fusionar los datos usando el campo común como clave
    merged_gdf = gdf.merge(df, left_on=common_field, right_on=common_field)
    
    # Guardar el resultado en un nuevo shapefile
    merged_gdf.to_file(output_path)
    print(f"Los datos se han pegado al shapefile y se ha guardado en {output_path}.")

# Ejemplo de uso:
shapefile_path = 'D:/RESPALDO/PRUEBAS_PROYECTO_CONSULCURT/DatosAbiertos_Marzo2016/unido.shp'
excel_path = 'D:/RESPALDO/PRUEBAS_PROYECTO_CONSULCURT/DatosAbiertos_Marzo2016/coloniasyfracc.xlsx'
common_field = 'd_cp'
output_path = 'D:/RESPALDO/PRUEBAS_PROYECTO_CONSULCURT/DatosAbiertos_Marzo2016/salida.shp'
merge_data_to_shapefile(shapefile_path, excel_path, common_field, output_path)