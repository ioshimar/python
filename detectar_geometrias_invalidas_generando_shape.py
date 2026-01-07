from qgis.core import QgsProject, QgsGeometry, QgsPointXY, QgsVectorLayer, QgsField, QgsFeature
from qgis.PyQt.QtCore import QVariant

# Cargar la capa original
layer = QgsProject.instance().mapLayersByName('Ejemplo_Cuernavaca')[0]

# Crear una nueva capa de puntos para almacenar los vértices problemáticos
crs = layer.crs().toWkt()
point_layer = QgsVectorLayer(f'Point?crs={crs}', 'Vertices_Problematicos', 'memory')
point_provider = point_layer.dataProvider()

# Agregar campos a la nueva capa
point_provider.addAttributes([QgsField('Feature_ID', QVariant.Int), QgsField('Error_Desc', QVariant.String)])
point_layer.updateFields()

# Iterar sobre cada característica en la capa original
for feature in layer.getFeatures():
    geom = feature.geometry()
    if not geom.isGeosValid():
        validity = geom.validateGeometry()
        for error in validity:
            # Obtener la descripción del error
            error_desc = error.what()

            # Obtener la ubicación del error
            error_location = error.where()
            if error_location.isEmpty():
                continue

            # Crear una nueva característica para el punto problemático
            point_feature = QgsFeature(point_layer.fields())
            point_feature.setGeometry(QgsGeometry.fromPointXY(error_location))
            point_feature.setAttributes([feature.id(), error_desc])

            # Agregar la nueva característica a la capa de puntos
            point_provider.addFeature(point_feature)

# Agregar la nueva capa al proyecto
QgsProject.instance().addMapLayer(point_layer)

# Guardar la nueva capa en un archivo shapefile
output_path = 'C:/path/to/save/Vertices_Problematicos.shp'  # Cambia esta línea a la ruta deseada
error = QgsVectorFileWriter.writeAsVectorFormat(point_layer, output_path, 'UTF-8', point_layer.crs(), 'ESRI Shapefile')

if error == QgsVectorFileWriter.NoError:
    print(f'Shapefile guardado exitosamente en {output_path}')
else:
    print(f'Error al guardar el shapefile: {error}')