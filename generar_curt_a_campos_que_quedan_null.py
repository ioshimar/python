from osgeo import ogr
from shapely.wkt import loads
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsGeometry, QgsPointXY, QgsField, QgsProject
from qgis.utils import iface
from datetime import datetime


path = 'D:/RESPALDO/PRUEBAS_CURT/cei/Recorte_Delicias_EPSG_4326.shp'

dataSource = ogr.Open(path, 1)  # Abre el shapefile en modo de escritura
if dataSource is None:
    print("No se pudo abrir el shapefile")
else:
    layer = dataSource.GetLayer()
    campo_curt = "curt"
    
    contador = 0

    for feature in layer:
        contador += 1  # Incrementa el contador en cada iteración
        valor_curt = feature.GetField(campo_curt)
        notas = feature.GetField("notas")
        id_cat = feature.GetField("id_cat")
        print("Procesando registro:", contador)
        print("ID_CAT:", id_cat)
        
        # Verifica si el campo 'curt' está vacío y si hay un valor en 'id_cat'
        if ((not valor_curt or valor_curt == "") and (not notas or notas == "")) and id_cat:
            geom = feature.GetGeometryRef()
            # Cálculos para 'curt' (reemplaza esta parte con tu lógica)
            pt = loads(geom.ExportToWkt()).representative_point() #Igual a Point On Surface
            longi = (loads(geom.ExportToWkt()).representative_point().x)*-1
            latitu = loads(geom.ExportToWkt()).representative_point().y
            
            g = int(latitu)
            grados = str(g)
            tam_grad = len(grados)
            if tam_grad == 1:
                grados = '0'+ grados
            else:
                grados = grados
            m = (latitu - g)*60
            min = int(m)
            minutos = str(min)
            tam_min = len(minutos)
            if tam_min == 1:
                minutos = '0'+ minutos
            else:
                minutos = minutos
            s = round(((m-min)*60),6)
            se = str(s)
            see = se[0:8]
            si = se[7:8]
            
            if si == 5:
               si = int(si)-1
               sii = str(si)
               siii = se[0:6] 
               see = siii + sii
            
            seee = float(see)
            seeee = round((seee*10000))
            seg = int(seeee)
            segundos = str(seg)
            tam_seg = len(segundos)
            if tam_seg==1:
                segundos = '00000'+ segundos
            elif tam_seg==2:
                segundos = '0000'+ segundos
            elif tam_seg==3:
                segundos = '000'+ segundos
            elif tam_seg==4:
                segundos = '00'+ segundos
            elif tam_seg==5:
                segundos = '0'+ segundos
            else:
                segundos = segundos
            
            latitud = grados+minutos+segundos
            
            #LONGITUD
            gl = int(longi)
            grados_lon = str(gl)
            tam_gradlon = len(grados_lon)
            if tam_gradlon == 1:
                grados_lon = '00'+ grados_lon
            elif tam_gradlon == 2:
                grados_lon = '0'+ grados_lon
            else:
                grados_lon = grados_lon
            ml = (longi - gl)*60
            minlon = int(ml)
            minutos_lon = str(minlon)
            tam_minlon = len(minutos_lon)
            if tam_minlon == 1:
                minutos_lon = '0'+ minutos_lon
            else:
                minutos_lon = minutos_lon
            s1 = round(((ml-minlon)*60),6)
            se1 = str(s1)
            see1 = se1[0:8]
            si1 = se1[7:8]
            
            if si == 5:
               si1 = int(si1)-1
               sii1 = str(si1)
               siii1 = se1[0:6] 
               see1 = siii1 + sii1
            
            seee1 = float(see1)
            seeee1 = round((seee1*10000))
            seg1 = int(seeee1)
            segundos_lon = str(seg1)
            tam_seglon = len(segundos_lon)
            if tam_seglon==1:
                segundos_lon = '00000'+ segundos_lon
            elif tam_seglon==2:
                segundos_lon = '0000'+ segundos_lon
            elif tam_seglon==3:
                segundos_lon = '000'+ segundos_lon
            elif tam_seglon==4:
                segundos_lon = '00'+ segundos_lon
            elif tam_seglon==5:
                segundos_lon = '0'+ segundos_lon
            else:
                segundos_lon = segundos_lon
            
            longitud = grados_lon+minutos_lon+segundos_lon 
            
            curt = latitud+longitud
            
            campos.SetField('curt', curt)  # Asigna el valor calculado a 'curt'
            layer.SetFeature(campos)
            
            # Asigna el valor calculado a 'curt'
            feature.SetField(campo_curt, curt)
            
            # Actualiza el registro en la capa de datos
            if layer.SetFeature(feature) != 0:
                print("Error al asignar valor a 'curt' en el registro con ID_CAT:", id_cat)
            else:
                print("Se asignó el valor calculado a 'curt' en el registro con ID_CAT:", id_cat)
    
    # Imprime el total de registros procesados
    print("Total de registros procesados:", contador)
    
    
                