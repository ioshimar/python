from qgis.core import QgsVectorFileWriter, QgsProject

# Obtiene la capa activa en QGIS
capa_activa = iface.activeLayer()

if capa_activa:
    # Define la ruta de destino para el nuevo Shapefile
    ruta_destino = 'D:/RESPALDO/PRUEBAS_CURT/CURT_PRODRUCCION/curt_produccion.shp'

    # Crea un objeto QgsVectorFileWriter y configura las opciones
    writer = QgsVectorFileWriter(ruta_destino, "UTF-8", capa_activa.dataProvider().fields(), capa_activa.wkbType(), capa_activa.crs())

    if writer.hasError() == QgsVectorFileWriter.NoError:
        # Copia todas las características de la capa activa al nuevo Shapefile
        for feat in capa_activa.getFeatures():
            writer.addFeature(feat)

        # Finaliza la escritura y cierra el archivo
        del writer

        print("Capa exportada con éxito.")
    else:
        print(f"Error al exportar la capa: {writer.errorMessage()}")
else:
    print("No hay una capa activa en QGIS.")