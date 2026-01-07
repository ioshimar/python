import requests
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
from zeep import Client

import geopandas as gpd

client = Client('http://10.106.12.118:8080/web_serv/insertUE?wsdl')

path = 'D:/RESPALDO/PRUEBAS_RNIC/rnic.shp'

dataSource1 = ogr.Open(path, 1)

layer = dataSource1.GetLayer()
layerDefinition = layer.GetLayerDefn()

for campos in layer:
    geom = campos.GetGeometryRef()
    #print(geom)
    cve_catast = campos.GetField("cve_catast")
    folio_real = campos.GetField("folio_real")
    cve_edo = campos.GetField("cve_edo")
    cve_mun = campos.GetField("cve_mun")
    cve_loc = campos.GetField("cve_loc")
    id_asent = campos.GetField("id_asent")
    nivel = campos.GetField("nivel")
    tipo_tenen = campos.GetField("tipo_tenen")
    tipo_ambit = campos.GetField("tipo_ambit")
    uso_suelo = campos.GetField("uso_suelo")
    valor_terr = campos.GetField("valor_terr")
    valor_cons = campos.GetField("valor_cons")
    tipo_insti = campos.GetField("tipo_insti")
    result = client.service.insertar(cve_catast,folio_real,cve_edo,cve_mun,cve_loc,id_asent,nivel,tipo_tenen,tipo_ambit,uso_suelo,valor_terr,valor_cons,tipo_insti,geom)   
    #print(geom)

QMessageBox.information(iface.mainWindow(), "PROCESO", 'Envío finalizado ')


