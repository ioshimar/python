from qgis.core import (
    QgsProject, 
    QgsVectorLayer, 
    QgsVectorFileWriter,
    QgsGeometry,
    QgsFeature,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QVariant
import os

# Función para corregir geometría inválida
def fix_invalid_geometry(geom):
    if not geom.isGeosValid():
        return geom.makeValid()
    else:
        return geom

# Cargar la capa original
layer = QgsProject.instance().mapLayersByName('Ejemplo_Cuernavaca_Corregidogeo')[0]

# Verificar que la capa se cargó correctamente
if not layer:
    raise Exception('No se pudo cargar la capa Ejemplo_Cuernavaca')

# Crear una nueva capa para almacenar las geometrías corregidas
crs = layer.crs()
corrected_layer = QgsVectorLayer(QgsWkbTypes.displayString(QgsWkbTypes.MultiPolygon) + '?crs=' + crs.authid(), 'Ejemplo_Cuernavaca_Corregido', 'memory')
corrected_provider = corrected_layer.dataProvider()

# Verificar que el CRS se definió correctamente
print(f'CRS de la capa original: {crs.toWkt()}')

# Copiar los campos de la capa original a la capa corregida
corrected_provider.addAttributes(layer.fields())
corrected_layer.updateFields()

# Iniciar edición de la capa corregida
corrected_layer.startEditing()

# Iterar sobre cada característica en la capa original
num_features_added = 0
for feature in layer.getFeatures():
    geom = feature.geometry()
    fixed_geom = fix_invalid_geometry(geom)

    # Crear una nueva característica con la geometría corregida
    new_feature = QgsFeature(corrected_layer.fields())
    new_feature.setGeometry(fixed_geom)
    new_feature.setAttributes(feature.attributes())
    
    # Agregar la nueva característica a la capa corregida
    if corrected_provider.addFeature(new_feature):
        num_features_added += 1
        print(f'Característica {feature.id()} agregada con éxito')
    else:
        print(f'Error al agregar la característica {feature.id()}')

# Forzar la actualización de la capa corregida
corrected_layer.updateExtents()

# Finalizar edición de la capa corregida
corrected_layer.commitChanges()

# Verificar si se han agregado características a la capa corregida
print(f'Número de características agregadas a la capa corregida: {num_features_added}')

# Asignar el CRS correctamente
corrected_layer.setCrs(crs)

# Agregar la nueva capa corregida al proyecto
QgsProject.instance().addMapLayer(corrected_layer)

# Guardar la nueva capa en un archivo shapefile
output_path = 'D:/PES/Ejemplo_Cuernavaca_Corregido.shp'  # Cambia esta línea a la ruta deseada

# Asegúrate de que el directorio de salida existe
output_directory = os.path.dirname(output_path)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Guardar el shapefile
error = QgsVectorFileWriter.writeAsVectorFormat(corrected_layer, output_path, 'UTF-8', crs, 'ESRI Shapefile')

# Imprimir mensajes detallados sobre el proceso de escritura
print(f'Intentando guardar el shapefile en: {output_path}')
print(f'Directorio de salida: {output_directory}')
print(f'CRS de la capa corregida: {corrected_layer.crs().authid()}')
print(f'Número de características en la capa corregida: {corrected_layer.featureCount()}')

if error == QgsVectorFileWriter.NoError:
    print(f'Shapefile guardado exitosamente en {output_path}')
else:
    print(f'Error al guardar el shapefile: {error}')