from qgis.core import QgsProject, QgsGeometry

# Cargar la capa
layer = QgsProject.instance().mapLayersByName('Ejemplo_Cuernavaca')[0]

# Iterar sobre cada característica (polígono) en la capa
for feature in layer.getFeatures():
    geom = feature.geometry()
    if not geom.isGeosValid():
        print(f'Feature ID {feature.id()} tiene una geometría inválida.')
        # Obtener detalles del problema de geometría
        validity = geom.validateGeometry()
        for error in validity:
            print(f'  Error de geometría: {error}')

# Alternativamente, podrías exportar los resultados a un archivo de texto
with open('geometria_invalida.txt', 'w') as file:
    for feature in layer.getFeatures():
        geom = feature.geometry()
        if not geom.isGeosValid():
            file.write(f'Feature ID {feature.id()} tiene una geometría inválida.\n')
            validity = geom.validateGeometry()
            for error in validity:
                file.write(f'  Error de geometría: {error}\n')