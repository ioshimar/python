from osgeo import ogr
from osgeo import osr
from osgeo import gdal
from qgis._core import QgsFeatureRequest
from shapely.wkt import loads
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsGeometry, QgsPointXY, QgsField, QgsProject, edit
from qgis.utils import iface
from datetime import datetime
import operator
from qgis.core import Qgis
from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsProject
import os
from pathlib import Path
import re


path = 'D:/RESPALDO/PRUEBAS_CURT/geometrias/parcela.shp'
rut = os.path.basename(path)
tabla = Path(rut).stem

dataSource1 = ogr.Open(path, 1)
#dataSource2 = ogr.Open(path, 1)


    
layer = dataSource1.GetLayer()
#layer2= dataSource2.GetLayer()
layerDefinition = layer.GetLayerDefn()
    
    # Prepare a transformation between projections
src_srs = layer.GetSpatialRef()
tgt_srs = osr.SpatialReference()
epsg = src_srs.GetAttrValue('AUTHORITY',1)

if epsg == '6365' or epsg == '4326':
    print('si')
    print(epsg)    
else:
    print('no')
    print(epsg)

#print(src_srs)