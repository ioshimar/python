from zeep import Client
from zeep import xsd
from PyQt5.QtWidgets import QMessageBox

# URL del servicio WSDL (cambia esto por la URL donde tu servicio está desplegado)
wsdl_url = "http://10.107.12.36:8080/web_service_curt_carta/consutar_carta?wsdl"

# Crear un cliente de Zeep usando la URL del WSDL
client = Client(wsdl=wsdl_url)

# CURT
curt = "215301469710214014171"

# Llamando al método solicitarnomengratura del servicio SOAP
result = client.service.solicitarnomengratura(curt=curt)

# Imprimir el resultado de la llamada al servicio
#print("NOMENGLATURA CARTOGRAFICA:", result)

# Función para mostrar el mensaje en una ventana emergente de QMessageBox
def show_message(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()

# Mostrar el resultado en una ventana emergente de QMessageBox
show_message("NOMENGLATURA CARTOGRAFICA", result)