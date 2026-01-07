# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from qgis.gui import QgsMessageBar
import output_file_dialog_base
from PyQt5.QtGui import *
from os import chdir
from PyQt5.QtWidgets import QApplication, QDialog
from importlib import reload
 
class OutputFile(QDialog):
     
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing:
        # self.<objectname>
        self.ui = output_file_dialog.Ui_Dialog()
        self.ui.setupUi(self)
 
#        #As in a QGIS plugin
#        self.ui.lineEdit.clear()
#        self.ui.pushButton.clicked.connect(self.select_output_file)
 
    def select_output_file(self):
        chdir('c:/Users')
        filename = QFileDialog.getSaveFileName(self, "Select output file ","", '*.txt')
        self.ui.lineEdit.setText(filename)
        self.save_file()
 
    def save_file(self):
        filename = self.ui.lineEdit.text()
        output_file = open(filename, 'w')
        output_file.write("My text")
        output_file.close()
 
# Create the dialog and keep reference
reload(output_file_dialog_base)
 
dlg = OutputFile()      #create Dialog object
dlg.show()                 #show Dialog object
 
dlg.ui.lineEdit.clear()   #clear text in lineEdit object
dlg.ui.pushButton.clicked.connect(dlg.select_output_file)   #send signal if pushButton is clicked