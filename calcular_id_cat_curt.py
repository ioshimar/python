from qgis.core import QgsProject, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils

# Obtener la capa activa desde el panel de capas de QGIS
layer = QgsProject.instance().mapLayersByName('CURT_ICES_001_011')[0]

# Inicializar un número consecutivo
numero_consecutivo = 1

# Comenzar la edición de la capa
layer.startEditing()

# Recorrer todos los registros de la capa
for feature in layer.getFeatures():
    # Obtener los valores de los campos a concatenar
    cve_ent = feature['Cve_ent']
    cve_mun = feature['Cve_mun']
    cve_loc = feature['Cve_loc']

    # Generar el nuevo valor para id_cat
    id_cat = f"{cve_ent}{cve_mun}{cve_loc}{numero_consecutivo:05d}"  # El número consecutivo con 5 dígitos

    # Actualizar el valor del campo id_cat
    layer.changeAttributeValue(feature.id(), layer.fields().indexFromName('id_cat'), id_cat)

    # Incrementar el número consecutivo
    numero_consecutivo += 1

# Guardar los cambios
layer.commitChanges()

print("El campo id_cat ha sido actualizado exitosamente.")