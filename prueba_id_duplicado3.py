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

path = 'D:/RESPALDO/PRUEBAS_CURT/zayna/curt_a (2)/curt_a/caracteres1.shp'

dataSource1 = ogr.Open(path, 1)
layer = dataSource1.GetLayer()

nameField = ogr.FieldDefn('notas14', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)

capa = QgsVectorLayer(path, "curt", "ogr")
    #capa.dataProvider().addAttributes([QgsField('igual_cve',  QVariant.String)])

with edit(capa):
    registros = capa.getFeatures()
    for registro in registros:
        id_actual = registro.id()
        clave_actual = registro['id_cat']
        ids = str(clave_actual)
        #print(clave_actual)
        if(clave_actual != NULL):
            #print(clave_actual)
            idc = ids.isalnum()
            print(idc)
           
            if(idc == True):
                print(clave_actual)
                expresion_filtro = 'id_cat=\''+clave_actual+'\'';
                        
                request = QgsFeatureRequest().setFilterExpression(expresion_filtro)
                               
                for feature in capa.getFeatures(request):
                    id_compara = feature.id()            
                    if (id_actual!=id_compara):
                        registro.setAttribute(registro.fieldNameIndex('notas14'), '14,')
                        capa.updateFeature(registro)
                        feature.setAttribute(feature.fieldNameIndex('notas14'),'14,')
                        capa.updateFeature(feature)
                        