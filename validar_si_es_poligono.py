from osgeo import ogr
from shapely.wkt import loads
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
import geopandas as gpd
from pathlib import Path
import re
import math

# Abre el shapefile y obtén la capa de polígonos
path = 'D:/RESPALDO/CASO_NUEVO_LEON/01_abasolov2/01_CURT_V2.shp'

dataSource1 = ogr.Open(path, 1)
layer = dataSource1.GetLayer()
layerDefinition = layer.GetLayerDefn()

for campos in layer:
    geom = campos.GetGeometryRef()
    typegeom = geom.GetGeometryName()
    if typegeom != "POLYGON" and typegeom != "MULTIPOLYGON":
        notas = campos.GetFieldIndex("notas8")
        print("EXISTEN")
    else:
        print("NO EXISTEN")