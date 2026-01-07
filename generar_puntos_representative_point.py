from qgis.core import *
import qgis.utils
from qgis.gui import *
from PyQt5.QtCore import *
import numpy as np
from shapely.geometry import shape
import fiona

shapefile_path = 'D:/RESPALDO/PRUEBAS_CURT/comparar_curt/no_coinciden.shp'

vl = QgsVectorLayer("Point?crs=epsg:4326&field=id:integer", "centroid", "memory")
pr = vl.dataProvider()

with fiona.open(shapefile_path, "r") as src:
    for feature in src:
        geom = shape(feature["geometry"])
        punto = geom.representative_point()
        longitud = punto.x
        print(longitud)
        latitud = punto.y
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(longitud, latitud)))
        fet.setAttributes([1])
        pr.addFeature(fet)

vl.updateExtents()
QgsProject.instance().addMapLayer(vl)