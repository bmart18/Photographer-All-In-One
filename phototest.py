# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:18:03 2021

@author: Brad
"""

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
    
   def pick_newinput():
       dialog = QFileDialog()
       folder_path = dialog.getExistingDirectory(None, "Select Folder")
       textEdit.setText(folder_path)
       getFiles(folder_path)
       
   def getFiles(path):
       arr = os.listdir(path)
       model.removeRows( 0, model.rowCount() )
       model.setStringList(arr)
   def pick_newoutput():
       dialog = QFileDialog()
       folder_path = dialog.getExistingDirectory(None, "Select Folder")
       textEdit_3.setText(folder_path)
       
   app = QApplication(sys.argv)
   w = QWidget()
   w.setGeometry(100,100,887, 590)
   
   model = QStringListModel(w)
   #font
   font = QFont()
   font.setPointSize(18)
   #button to open INPUT directory
   inputDir = QToolButton(w)
   inputDir.setGeometry(180, 120, 61, 41)
   inputDir.setText(". . .")
   #textinput for INPUT directory
   textEdit = QTextEdit(w)
   textEdit.setGeometry(10, 120, 171, 41)
   textEdit.setObjectName("textEdit")
   #textinput for OUTPUT directory
   textEdit_3 = QTextEdit(w)
   textEdit_3.setGeometry(10, 350, 171, 41)
   textEdit_3.setObjectName("textEdit_3")
   #button to open OUTPUT directory
   toolButton_3 = QToolButton(w)
   toolButton_3.setGeometry(180, 350, 61, 41)
   toolButton_3.setObjectName("toolButton_3")
   toolButton_3.setText(". . .")
   #drop down for resolutions
   comboBox = QComboBox(w)
   comboBox.setGeometry(10, 240, 221, 41)
   comboBox.setObjectName("comboBox")
   comboBox.addItem("")
   comboBox.setItemText(0,"1080x720")
   #label above INPUT directory
   label = QLabel(w)
   label.setGeometry(10, 80, 211, 31)
   label.setFont(font)
   label.setObjectName("label")
   label.setText("Input Directory")
   #button to initiate program
   button1 = QPushButton(w)
   button1.setText("Transform Photos")
   button1.move(200,400)
   button1.setGeometry(290, 440, 201, 81)
   #label above OUTPUT directory
   label_2 = QLabel(w)
   label_2.setFont(font)
   label_2.setGeometry(10, 310, 221, 31)
   label_2.setText("Output Directory")
   
   label_3 = QLabel(w)
   label_3.setGeometry(10, 200, 251, 41)
   label_3.setFont(font)
   label_3.setObjectName("label_3")
   
   checkBox = QCheckBox(w)
   checkBox.setGeometry(530, 70, 261, 41)
   font.setPointSize(12)
   checkBox.setFont(font)
   checkBox.setObjectName("checkBox")
   
   checkBox_2 = QCheckBox(w)
   checkBox_2.setGeometry(530, 100, 261, 91)
   checkBox_2.setFont(font)
   checkBox_2.setObjectName("checkBox_2")
   
   listView = QListView(w)
   listView.setGeometry(260, 40, 256, 391)
   listView.setObjectName("listView")
   listView.setModel(model)
   
   checkBox_3 = QCheckBox(w)
   checkBox_3.setGeometry(530, 160, 261, 91)
   checkBox_3.setFont(font)
   checkBox_3.setObjectName("checkBox_3")
   
   checkBox_4 = QCheckBox(w)
   checkBox_4.setGeometry(530, 210, 261, 91)
   checkBox_4.setFont(font)
   checkBox_4.setObjectName("checkBox_4")
   
   comboBox_2 = QComboBox(w)
   comboBox_2.setGeometry(770, 200, 73, 22)
   comboBox_2.setObjectName("comboBox_2")
   comboBox_2.addItem("")
   comboBox_2.addItem("")
   
   plainTextEdit = QPlainTextEdit(w)
   plainTextEdit.setGeometry(530, 270, 231, 31)
   plainTextEdit.setObjectName("plainTextEdit")
   
   comboBox_3 = QComboBox(w)
   comboBox_3.setGeometry(760, 270, 111, 31)
   comboBox_3.setObjectName("comboBox_3")
   comboBox_3.addItem("")
   comboBox_3.addItem("")
   comboBox_3.addItem("")
   comboBox_3.addItem("")
   
   label_4 = QLabel(w)
   label_4.setGeometry(780, 180, 55, 16)
   label_4.setObjectName("label_4")
   
   label_5 = QLabel(w)
   label_5.setGeometry(790, 250, 55, 16)
   label_5.setObjectName("label_5")
   
   checkBox_5 = QCheckBox(w)
   checkBox_5.setGeometry(530, 300, 311, 91)
   font.setPointSize(12)
   checkBox_5.setFont(font)
   checkBox_5.setObjectName("checkBox_5")
   
   checkBox_6 = QCheckBox(w)
   checkBox_6.setGeometry(530, 350, 311, 91)
   checkBox_6.setFont(font)
   checkBox_6.setObjectName("checkBox_6")
   
   checkBox_7 = QCheckBox(w)
   checkBox_7.setGeometry(530, 400, 311, 91)
   checkBox_7.setFont(font)
   checkBox_7.setObjectName("checkBox_7")
   
   checkBox_8 = QCheckBox(w)
   checkBox_8.setGeometry(530, 480, 251, 51)
   checkBox_8.setFont(font)
   checkBox_8.setObjectName("checkBox_8")
   
   
   #### SET TEXTS #########
   label.setText("Input Directory")
   label_2.setText("Output Directory")
   label_3.setText("Output Resolution")
   checkBox.setText("Image to NTSC GrayScale")
   checkBox_2.setText("Log Base 2 Transformation")
   checkBox_3.setText("Gamma Transformation")
   checkBox_4.setText("Add WaterMark")
   comboBox_2.setItemText(0, "0.5")
   comboBox_2.setItemText(1, "1.5")
   comboBox_3.setItemText(0, "Upper Left")
   comboBox_3.setItemText(1, "Lower Left")
   comboBox_3.setItemText(2, "Upper Right")
   comboBox_3.setItemText(3, "Lower Right")
   label_4.setText("Gamma")
   label_5.setText("Position")
   checkBox_5.setText("Histogram/Intensity Equalize")
   checkBox_6.setText("Gaussian Filter")
   checkBox_7.setText("Median Filter")
   checkBox_8.setText("Nonlinear Approach for\n"" Image Enhancement")
   
   inputDir.clicked.connect(pick_newinput)
   toolButton_3.clicked.connect(pick_newoutput)

   w.setWindowTitle("Photographer All in One")
   w.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   window()