from qgis.core import *
import qgis.utils
from qgis.gui import *
from PyQt5.QtCore import *
import math
from datetime import datetime
from pyproj import Proj, transform
from osgeo import ogr

# ITERAR

print ("     ¡validando campos!")

capa = iface.activeLayer()

count=capa.fields().count()

if(count>7):
    print("el shape contiene mas de los campos necesarios")
else:

    nombre = []
    
    for campo in capa.fields().names():
        nombre.append(campo)
        #print(campo)
        
    if(nombre[0]!="cve_ent") or (nombre[1]!="cve_mun") or (nombre[2]!="cve_loc") or (nombre[3]!="id_cat"):
        print("estructura incorrecta")
    else:
        #for field in capa.fields():
#    print(field.name(), field.typeName(), field.length())

        def validaCampo (campos, capa, tipo):
        # tipo = 1 campo entero
        # tipo = 2 campo entero
            capa.updateFields()
            posicionCampo = 0
            for campo in capa.fields(): 
                if (QgsField(campo).name().upper() == campos.upper()):
                    print("     campo "+campos+" correcto") 
        
                            
        capa = iface.activeLayer()
        validaCampo("cve_ent",capa,1)
        validaCampo("cve_mun",capa,1)
        validaCampo("cve_loc",capa,1)
        validaCampo("id_cat",capa,1)


        def validaCampo (campoNuevo, capa, tipo):
                # tipo = 1 campo entero
                # tipo = 2 campo entero
                capa.updateFields()
                posicionCampo = 0
                for campo in capa.fields(): 
                    if (QgsField(campo).name().upper() == campoNuevo.upper()):
                        print("     campo "+campoNuevo+" ya existe, limpiando valores")
                        fList = list()
                        fList.append(posicionCampo)
                        capa.dataProvider().deleteAttributes(fList)
                        capa.updateFields()
                        break
                    posicionCampo +=1
                
                capa.commitChanges()
                print("     agregando campo "+campoNuevo)
                if (tipo==1):
                    capa.dataProvider().addAttributes([QgsField(campoNuevo,  QVariant.String, "string", 21)])
                else:
                    capa.dataProvider().addAttributes([QgsField(campoNuevo,  QVariant.String, "string", 21)])
                capa.commitChanges()
                capa.updateFields()


        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Inicio =", current_time)

        capa = iface.activeLayer()
        validaCampo("longitud",capa,1)
        validaCampo("latitud",capa,1)
        iface.mapCanvas().currentLayer().reload() 
        capa = iface.activeLayer()

        print(" ")
        print ("     calculando curt")

        crsi = capa.crs()
        #crsDest = capa.crs().authid()
        #print(crsi)

        capa.startEditing()
        for feat in capa.getFeatures():
            geom = feat.geometry()                   
            # Calcular el centroide de la geometría
            
            centroid = geom.centroid()
            cen = centroid.asPoint()
            points = [cen]
            c = QgsGeometry.fromPolygonXY([points])
            #print(c)
            #print(points)
            #centroid = QgsGeometry.fromPolygonXY(centroide)
            # Verificar si el centroide se encuentra dentro de la geometría
           
            if not centroid.intersects(geom): 
                #print("no")
                centroid = geom.nearestPoint(QgsGeometry.fromPointXY(cen))
                #print(centroid)
                # Usar el punto más cercano como el nuevo centroide
                #centroid = QgsGeometry.fromPointXY(nearest_point)   
            
            
            #print(centroid.asPoint())
            #cen = transform(crsi, centroide.asPoint().x(), centroide.asPoint().y())
            #centroide.transform()
            longitud = centroid.asPoint().x()
            latitud = centroid.asPoint().y()
            
            #longi = centroid.asPoint().x() * -1
            #latitud_dms = curtv1_decimal_dmsc_lat_round()
            #longitud_dms = curtv1_decimal_dmsc_lon_round()
            

            CURT_latitud = f'{latitud}'
            CURT_longitud = f'{longitud}'
           
            #print(centroide.asPoint().x(), centroide.asPoint().y())
            feat['latitud'] = CURT_latitud
            feat['longitud'] = CURT_longitud
            capa.updateFeature(feat)
        capa.commitChanges()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Termino :", current_time)

print("     CREANDO SHAPE DE PUNTOS     ")

puntos = r"D:\prueba_centroid\p.shp"

# Crear el archivo shape y agregar los campos necesarios
crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
fields = QgsFields()
#fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('x', QVariant.String))
fields.append(QgsField('y', QVariant.String))
writer = QgsVectorFileWriter(puntos, 'UTF-8', fields, QgsWkbTypes.Point, crs, 'ESRI Shapefile')

puntos.startEditing()
for feat in puntos.getFeatures():
    feat['x'] = CURT_longitud
    feat['y'] = CURT_latitud
    
    puntos.updateFeature(feat)
puntos.commitChanges()
