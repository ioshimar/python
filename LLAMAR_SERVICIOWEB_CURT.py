from zeep import Client
from zeep import xsd

# URL del servicio WSDL (cambia esto por la URL donde tu servicio está desplegado)
wsdl_url = "http://10.107.12.36:8080/web_service_curt/consultar_curt?wsdl"

# Crear un cliente de Zeep usando la URL del WSDL
client = Client(wsdl=wsdl_url)

# Geometría en formato WKT para probar: un MULTIPOLYGON
wkt_geometry = "MULTIPOLYGON (((-102.002957123953 22.0237930041669,-102.003017764166 22.0237655496861,-102.003036284298 22.0238007089507,-102.002975642412 22.0238281602479,-102.002957123953 22.0237930041669)))"

# Llamando al método convertirCurt del servicio SOAP
result = client.service.convertirCurt(wkt=wkt_geometry)

# Imprimir el resultado de la llamada al servicio
#print("Resultado de la conversión CURT:", result)

# Función para mostrar el mensaje en una ventana emergente de QMessageBox
def show_message(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()

# Mostrar el resultado en una ventana emergente de QMessageBox
show_message("Resultado de la conversión CURT", result)