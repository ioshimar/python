import geopandas as gpd
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
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
from qgis.core import QgsProject
import os
from pathlib import Path
import re
from zeep import Client

def show_error_message(message):
    # Mostrar cuadro de diálogo con el mensaje de error
    QMessageBox.critical(None, "Error", message)

    # Imprimir el mensaje en la consola
    print(f"Error: {message}")

def normalize_text(text):
    # Normalizar texto para ignorar diferencias de acentos y convertirlo a minúsculas
    normalized_text = unicodedata.normalize("NFKD", text).casefold()
    return normalized_text

def validate_shapefile(path):
    try:
        # Cargamos el Shapefile con geopandas
        gdf = gpd.read_file(path)

        # Validamos que el Shapefile contenga geometrías
        if gdf.empty:
            raise ValueError("El Shapefile está vacío o no contiene geometrías.")

        # Validamos los nombres de los campos
        valid_field_names = ["cve_catast", "folio_real", "cve_edo", "cve_mun", "cve_loc", "id_asent", "nivel", "tipo_tenen", "tipo_ambit", "uso_suelo", "valor_terr", "valor_cons", "tipo_insti"]
        for field_name in valid_field_names:
            if field_name not in gdf.columns:
                raise ValueError(f"El campo '{field_name}' no se encuentra en el Shapefile.")

        # Validamos que los campos "valor_terr" y "valor_cons" sean numéricos
        numeric_fields = ["valor_terr", "valor_cons"]
        for field_name in numeric_fields:
            if not pd.api.types.is_numeric_dtype(gdf[field_name]):
                raise ValueError(f"El campo '{field_name}' debe ser de tipo numérico.")

        # Validamos que los demás campos sean de tipo texto o string
        text_fields = set(gdf.columns) - set(numeric_fields) - {"geometry"}
        for field_name in text_fields:
            if not pd.api.types.is_string_dtype(gdf[field_name]):
                raise ValueError(f"El campo '{field_name}' debe ser de tipo texto o string.")
                
        # Validamos los campos cve_edo, cve_mun, cve_loc, id_asent
        for field_name in ["cve_edo", "cve_mun", "cve_loc", "id_asent"]:
            if gdf[field_name].isnull().any():
                raise ValueError(f"El campo '{field_name}' no puede estar vacío.")
            if field_name == "cve_edo" and ~gdf["cve_edo"].astype(str).str.match(r"^\d{2}$").all():
                raise ValueError("El campo 'cve_edo' debe tener un tamaño de dos caracteres y contener solo dígitos.")
            if field_name == "cve_mun" and ~gdf["cve_mun"].astype(str).str.match(r"^\d{3}$").all():
                raise ValueError("El campo 'cve_mun' debe tener un tamaño de tres caracteres y contener solo dígitos.")
            if field_name == "cve_loc" and ~gdf["cve_loc"].astype(str).str.match(r"^\d{4}$").all():
                raise ValueError("El campo 'cve_loc' debe tener un tamaño de cuatro caracteres y contener solo dígitos.")
            if field_name == "id_asent" and ~gdf["id_asent"].astype(str).str.match(r"^\d{2}\d{3}\d{4}$").all():
                raise ValueError("El campo 'id_asent' debe contener nueve dígitos (cve_edo, cve_mun, cve_loc).")
                

        # Validamos tipo_tenen, tipo_ambit, tipo_insti
        valid_tipo_tenen = ["Privada", "Pública"]
        valid_tipo_ambit = ["Urbano", "Rural", "Semiurbano"]
        valid_tipo_insti = ["Federal", "Estatal", "Municipal centralizada", "Municipal autónoma"]
        if ~gdf["tipo_tenen"].isin(valid_tipo_tenen).all():
            raise ValueError("El campo 'tipo_tenen' solo puede contener 'Privada' o 'Pública'.")
        if ~gdf["tipo_ambit"].isin(valid_tipo_ambit).all():
            raise ValueError("El campo 'tipo_ambit' solo puede contener 'Urbano', 'Rural' o 'Semiurbano'.")
        if ~gdf["tipo_insti"].isin(valid_tipo_insti).all():
            raise ValueError("El campo 'tipo_insti' solo puede contener 'Federal', 'Estatal', 'Municipal centralizada' o 'Municipal autónoma'.")

        # Mostramos los nombres de los campos y sus tipos
        print("Nombres de los campos y sus tipos:")
        for field_name, field_type in zip(gdf.columns, gdf.dtypes):
            print(f"{field_name}: {field_type}")

        print("Validación exitosa: El Shapefile contiene geometrías y los campos son válidos.")
        
        client = Client('http://10.106.12.118:8080/web_serv/insertUE?wsdl')

        #path = 'D:/RESPALDO/PRUEBAS_RNIC/rnic.shp'

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

    except ValueError as e:
        show_error_message(str(e))
    except Exception as e:
        print(f"Error: {e}")

# Ruta del Shapefile a validar
path = "D:/RESPALDO/PRUEBAS_RNIC/rnic.shp"

# Llamamos a la función para validar el Shapefile
validate_shapefile(path)
