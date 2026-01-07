import geopandas as gpd

# Cargar el archivo Shapefile
archivo_shapefile = "D:/RESPALDO/PRUEBAS_CURT/paco/verificar.shp"
dataframe = gpd.read_file(archivo_shapefile)

# Crear una nueva columna para indicar si la geometría es válida o no
dataframe['es_valida'] = dataframe.geometry.is_valid

# Actualizar el atributo deseado si la geometría es inválida
atributo_actualizado = 'no'
dataframe.loc[~dataframe.es_valida, 'notas'] = atributo_actualizado

# Guardar los cambios en un nuevo archivo Shapefile
nuevo_archivo_shapefile = "D:/RESPALDO/PRUEBAS_CURT/paco/verificar2.shp"
dataframe.to_file(nuevo_archivo_shapefile)

