from osgeo import ogr
from shapely.wkt import loads
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsGeometry, QgsPointXY, QgsField, QgsProject
from qgis.utils import iface
from datetime import datetime

path = 'D:/RESPALDO/PRUEBAS_CURT/curt_campos.shp'

dataSource1 = ogr.Open(path, 1)
layer = dataSource1.GetLayer()

nameField = ogr.FieldDefn('curt', ogr.OFTString)        # create new field of type string called Name to store the country names
nameField.SetWidth(21)
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas1', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas2', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas3', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas4', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas5', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas6', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
nameField = ogr.FieldDefn('notas7', ogr.OFTString)        # create new field of type string called Name to store the country names
layer.CreateField(nameField)
def valcve_ent():
    for campos in layer:
        if (campos.GetField("cve_ent")=='') or (campos.GetField("cve_ent")==NULL):
            notas = campos.GetFieldIndex("notas1")
            campos.SetField(notas, '1,')
            layer.SetFeature(campos)
        if(operator.length_hint(campos.GetField("cve_ent"))!= 2):
            notas = campos.GetFieldIndex("notas2")
            campos.SetField(notas, '2,')
            layer.SetFeature(campos)
            
def valcve_mun():
    for campos in layer:
        if(campos.GetField("cve_mun")=='') or (campos.GetField("cve_mun")==NULL):
            notas = campos.GetFieldIndex("notas3")
            campos.SetField(notas, '3,')
            layer.SetFeature(campos)
        if(operator.length_hint(campos.GetField("cve_mun"))!= 3):
            notas = campos.GetFieldIndex("notas4")
            campos.SetField(notas, '4,')
            layer.SetFeature(campos)
def valcve_loc():
    for campos in layer:
        if(campos.GetField("cve_loc")=='') or (campos.GetField("cve_loc")==NULL):
            notas = campos.GetFieldIndex("notas5")
            campos.SetField(notas, '5,')
            layer.SetFeature(campos)
        if(operator.length_hint(campos.GetField("cve_loc"))!= 4):
            notas = campos.GetFieldIndex("notas6")
            campos.SetField(notas, '6,')
            layer.SetFeature(campos)
def valid_cat():
    for campos in layer:
        if(campos.GetField("id_cat")=='') or (campos.GetField("id_cat")==NULL):
            notas = campos.GetFieldIndex("notas7")
            campos.SetField(notas, '7,')
            layer.SetFeature(campos)
def concat_field():
    nameField = ogr.FieldDefn('notas', ogr.OFTString)        # create new field of type string called Name to store the country names
    layer.CreateField(nameField)
    for campos in layer:
        if(campos.GetField("notas1")==None):
            n1 = ''
            #print(n1)
        else:
            n1 = campos.GetField("notas1")
        if(campos.GetField("notas2")==None):
            n2 = ''
            
        else:
            n2 = campos.GetField("notas2")
        if(campos.GetField("notas3")==None):
            n3 = ''
            
        else:
            n3 = campos.GetField("notas3")
        if(campos.GetField("notas4")==None):
            n4 = ''
            
        else:
            n4 = campos.GetField("notas4")
        if(campos.GetField("notas5")==None):
            n5 = ''
            
        else:
            n5 = campos.GetField("notas5")
        if(campos.GetField("notas6")==None):
            n6 = ''
            
        else:
            n6 = campos.GetField("notas6")
        if(campos.GetField("notas7")==None):
            n7 = ''
            
        else:
            n7 = campos.GetField("notas7")
            
        nota = ''.join([n1, n2, n3, n4, n5, n6, n7])
        notas = campos.GetFieldIndex("notas")
        campos.SetField(notas, nota)
        layer.SetFeature(campos)
        #print(nota)
        
def gen_curt():
    for campos in layer:
        if(campos.GetField("notas")=='') or (campos.GetField("notas")==NULL):
            geom = campos.GetGeometryRef()
            #pt = loads(geom.ExportToWkt()).centroid
            pt = loads(geom.ExportToWkt()).representative_point() #Igual a Point On Surface
            longi = (loads(geom.ExportToWkt()).representative_point().x)*-1
            latitu = loads(geom.ExportToWkt()).representative_point().y
                            
            def calcula(lat):
                grados = int(lat)
                minutos = int((lat - grados) * 60)
                segundos = round((((lat - grados) * 60) - minutos) * 60 * 100000)
                if segundos == 600000:
                    segundos = 0
                    minutos += 1
                elif segundos >= 1000000:
                    segundos -= 1000000
                    minutos += 1
                if minutos >= 60:
                    minutos = 0
                    grados += 1
                return "{:0>2}{:0>2}{:0>6}".format(grados, minutos, segundos)

            latit = latitu

            latitud = calcula(latit)
                                    
            def calculalon(lon):
                grados = int(lon)
                minutos = int((lon - grados) * 60)
                segundos = round((((lon - grados) * 60) - minutos) * 60 * 100000)
                if segundos == 600000:
                    segundos = 0
                    minutos += 1
                elif segundos >= 1000000:
                    segundos -= 1000000
                    minutos += 1
                if minutos >= 60:
                    minutos = 0
                    grados += 1
                return "{:0>3}{:0>2}{:0>6}".format(grados, minutos, segundos)

            longitu = longi

            longitud = calculalon(longitu)
                                    
            CURT_conc = f'{latitud}{longitud}'
            #print(CURT_conc)
            clave = campos.GetFieldIndex("curt")
            campos.SetField(clave, CURT_conc)
            layer.SetFeature(campos)
        
valcve_ent()
valcve_mun()
valcve_loc()
valid_cat()
concat_field()
gen_curt()