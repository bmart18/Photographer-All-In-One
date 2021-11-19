# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:18:03 2021

@author: Brad
"""

import sys
import os
import numpy as np
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def startProgram(path,NTSC,Log,Gamma,GammaVar,Watermark,WatermarkText,WatermarkPosition,Histogram,Gaussian,Median,NonLinear,OutputDirectory):
    font = cv2.FONT_HERSHEY_COMPLEX
    color = (255, 255, 255)
    thickness = 4

    def process_image(working_image, watermark, pos,path):
        text_length = len(watermark)
        width = len(working_image) #im.size[1]
        height = len(working_image[1])
        #print("width: "+ str(width))
        #print("shape[0]: "+ str(working_image.shape[0]))
        #print("height: "+ str(height))
        #print("shape[1]: "+ str(working_image.shape[1]))
        new_image = working_image
        if watermark != "":
            if working_image.shape[0] >= 4000:
                avg_char = 120
                text_width = text_length * avg_char
                fontScale = 6
                image_ul = (0, 150)
                image_ur = (working_image.shape[1] - text_width, 150)
                image_ll = (0, working_image.shape[0] - 50)
                image_lr = (working_image.shape[1] - text_width, working_image.shape[0] - 50)
            else:
                avg_char = 80
                text_width = text_length * avg_char
                fontScale = 4
                image_ul = (0, 100)
                image_ur = (working_image.shape[1] - text_width, 100)
                image_ll = (0, working_image.shape[0] - 50)
                image_lr = (working_image.shape[1] - text_width, working_image.shape[0] - 50)
 
            if pos == 'UL':
                new_image = cv2.putText(working_image, watermark, image_ul, font, fontScale, color, thickness, cv2.LINE_AA)
 
            if pos == 'UR':
                new_image = cv2.putText(working_image, watermark, image_ur, font, fontScale, color, thickness, cv2.LINE_AA)
 
            if pos == 'LL':
                new_image = cv2.putText(working_image, watermark, image_ll, font, fontScale, color, thickness, cv2.LINE_AA)
 
            if pos == 'LR':
                new_image = cv2.putText(working_image, watermark, image_lr, font, fontScale, color, thickness, cv2.LINE_AA)

        if(OutputDirectory == ""): #check is user sepcified output path
            temppath = path
        else:
            temppath = OutputDirectory
        if not os.path.exists(temppath + '\\Processed'): #if there isnt a processed directory make one
            os.mkdir(temppath + '\\Processed')
        newpath = temppath + '\\' + 'Processed' + '\\' + file #make the full path for writing
        cv2.imwrite(newpath, new_image)

    def medianFilter(matrix):
        outputMatrix = matrix.copy()
        matrix = np.pad(matrix, ((1, 1), (1, 1)), 'constant') #pad matrix with 0's
        matrixRows = len(matrix)
        matrixColumns = len(matrix[0])
        for i in range(1, matrixRows - 1):
            for j in range(1, matrixColumns - 1):

                MiddleInt = matrix[i][j]
                TopRightInt = matrix[i - 1][j + 1]
                MiddleRightInt = matrix[i][j + 1]
                BottomRightInt = matrix[i + 1][j + 1]
                TopLeftInt = matrix[i - 1][j-1]
                MiddleLeftInt = matrix[i][j - 1]
                BottomLeftInt = matrix[i - 1][j + 1]
                TopInt = matrix[i+1][j]
                BottomInt = matrix[i-1][j]
                matrixOfInts = [MiddleRightInt,TopRightInt,TopInt,TopLeftInt,MiddleInt,MiddleLeftInt,BottomLeftInt,BottomInt,BottomRightInt]
                matrixOfInts.sort() # sort array
                outputMatrix[i-1][j-1] = matrixOfInts[5]  # there will always be 9 elements so index 5 will be median 100% of the time
        return outputMatrix


    def ntsc_grayscale(img):

        b, g, r = cv2.split(img)
        rows = len(r)  # grab rows and cols of any single channel matrix
        cols = len(r[0])
        unnormalized = b.copy()  # need a one channel matrix to copy, we will overwrite all the values
        normalized = b.copy()
        for i in range(rows):
            for j in range(cols):
                unnormalized[i][j] = ((76.245 * r[i][j] + 149.685 * g[i][j] + 29.071 * b[i][j]) / 255)  # NTSC method
                normalized[i][j] = unnormalized[i][j] / 255  # incase we need a lil normalized one
        return unnormalized

    def getHistogramAndEqualize(img):
        newimg = img.copy()
        array = [None]*256            # Two empty arrays with 256 spots 0-255
        probability = [None]*256      # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        rows = len(img)               # Use len instead of img.shape() because of pixel size
        cols = len(img[0])            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        pixels = rows*cols
        for i in range(rows):
            for j in range(cols):
                if array[img[i][j]] is None:  # if this is the first time we have see this intensity value, set it to one
                    array[img[i][j]] = 1
                else:                          # else increment it by one (cant increment a none value)
                    array[img[i][j]] += 1
        count = 0
        for k in array:
            if k is None:  # if we did not find any intensity for that value, set it to equal instead of none
                probability[count] = 0
                array[count] = 0
            else:           # else find the probability of that intensity
                probability[count] = k/pixels
            count += 1
        # ship the array off to the distribution function but let the function know the level
        equalizedarray = cumulativeDistribution(256,probability)

        for i in range(rows):
            for j in range(cols):
                # iterate through the array and give our equalized image the new value
                newimg[i][j] = equalizedarray[img[i][j]]
        return newimg
        # plt.hist(array,bins='auto')    # for testing
        # plt.show()


    def cumulativeDistribution(Level,probability):
        newarray = [None]*Level           # similar to above we make two empty arrays with the level
        probabilityadd = [None]*Level
        count = 0
        for i in probability:
            if count == 0: # if this is the first probability, just take the level-1 and times it by the probability
                newarray[count] = round((Level - 1) * i)
                probabilityadd[count] = i # start a tally of the probability so we dont need to do recursive functions
            else:
                # add the last probability to the current to keep the running tally
                probabilityadd[count] = probabilityadd[count-1] + i
                # take the probability total and multiply by the level - 1 and set it to that count.
                newarray[count] = round((Level-1) * (probabilityadd[count]))
            count += 1
        return newarray # send the equalized array back

    def equalizecolor(img):
        ycrcb = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB) # convert to a nice color scheme
        channels = cv2.split(ycrcb) # use split to give us the nice color channels
        cv2.equalizeHist(channels[0],channels[0]) # use a nice function to nicely equalize the channels
        cv2.merge(channels,ycrcb) # nicely merge the channels back
        cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
        return img
    
    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            working_image = cv2.imread(path + '\\' + file)
            cv2.waitKey(100)

            if NTSC:
                working_image = ntsc_grayscale(working_image)
                # cv2.imshow('grayscale',working_image)  # testing
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            if False:
                if NTSC:  # if its already gray ya cant gray it again
                    working_image = getHistogramAndEqualize(working_image)
                else:  # gray it before equalizing
                    working_image = ntsc_grayscale(working_image)
                    working_image = getHistogramAndEqualize(working_image)
            if Histogram:
                working_image = equalizecolor(working_image)
            if Median:
                if NTSC:  # if its already gray ya cant gray it again
                    working_image = medianFilter(working_image)
                else:  # gray it before filtering
                    working_image = ntsc_grayscale(working_image)
                    working_image = medianFilter(working_image)
            process_image(working_image, WatermarkText, WatermarkPosition,path)
    ###############################################################################


def window():
               
   def startTransformation():
       NTSC = False
       Log = False
       Gamma = False
       GammaVar = ""
       Watermark = False
       WatermarkText = ""
       WatermarkPosition = ""
       OutputDirectory = ""
       Histogram = False
       Gaussian = False
       Median = False
       NonLinear = True
       path = textEdit.toPlainText()
       if checkBox.checkState() == 2:
           NTSC = True
       if checkBox_2.checkState() == 2:    
           Log = True
       if checkBox_3.checkState() == 2:
           Gamma = True
           GammaVar = str(comboBox_2.currentText())
           print(GammaVar)
           print(str(Gamma))
       if checkBox_4.checkState() == 2:
           Watermark = True
           WatermarkText = plainTextEdit.toPlainText()
           WatermarkPosition = str(comboBox_3.currentText())
       if checkBox_5.checkState() == 2:
           Histogram = True
       if checkBox_6.checkState() == 2:
           Gaussian = True
       if checkBox_7.checkState() == 2:
           Median = True
       if checkBox_8.checkState() == 2:
           NonLinear = True
       #start program
       startProgram(path,NTSC,Log,Gamma,GammaVar,Watermark,WatermarkText,WatermarkPosition,Histogram,Gaussian,Median,NonLinear,OutputDirectory)
       
       
   def pick_newinput():
       dialog = QFileDialog()
       folder_path = dialog.getExistingDirectory(None, "Select Folder")
       textEdit.setText(folder_path)
       getFiles(folder_path)
       
   def getFiles(path):
       model.removeRows(0, model.rowCount())
       if path!= "":
        arr = os.listdir(path)
        temp = []
        for i in arr:
            if i.endswith('.jpg') or i.endswith('.png'):
                #print(i)  #  testing
                temp.append(i)
        model.setStringList(temp)
       
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
   button1 = QToolButton(w)
   button1.setText("Transform Photos")
   button1.move(200,400)
   button1.setGeometry(290, 440, 201, 81)
   button1.setObjectName("button1")
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
   comboBox_3.setItemText(0, "UL")
   comboBox_3.setItemText(1, "LL")
   comboBox_3.setItemText(2, "UR")
   comboBox_3.setItemText(3, "LR")
   label_4.setText("Gamma")
   label_5.setText("Position")
   checkBox_5.setText("Histogram/Intensity Equalize")
   checkBox_6.setText("Gaussian Filter")
   checkBox_7.setText("Median Filter")
   checkBox_8.setText("Nonlinear Approach for\n"" Image Enhancement")
   
   button1.clicked.connect(startTransformation)
   inputDir.clicked.connect(pick_newinput)
   toolButton_3.clicked.connect(pick_newoutput)

   
   
   w.setWindowTitle("Photographer All in One")
   w.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   window()