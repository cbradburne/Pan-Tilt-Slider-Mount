#macOS
#python3 -m pip install pyqt5
#python3 -m pip install pyjoystick
#python3 -m pip install pyserial
#python3 -m pip install pyinstaller
#python3 -m pip install pysdl2-dll
#python3 -m pip install pynput

#pyinstaller --additional-hooks-dir=. --onefile --windowed --icon PTSApp-Icon.icns --name PTSApp-QT PTSQT5.py

#Windows
#python -m pip install pyqt5
#python -m pip install pyjoystick
#python -m pip install pyserial
#python -m pip install pyinstaller
#python -m pip install pysdl2-dll

#pyinstaller --additional-hooks-dir=. --onefile --windowed --icon PTSApp-Icon.ico --name PTSApp-QT PTSQT5.py
#pyinstaller --paths 'C:\Users\Music\AppData\Local\Programs\Python\Python39\Lib\site-packages\sdl2' --hidden-import=pkg_resources.py2_warn --additional-hooks-dir=. --onefile --windowed --icon PTSApp-Icon.ico --name PTSApp-QT PTSQT5.py

#cd 'C:\Users\Music\Documents\GitHub\Pan-Tilt-Slider-Mount\Code\App\Source\Experimental\5 way - 10 positions\PyQt5'
#pyinstaller PTSApp-QT.spec
#pyuic5 -x ptsui5.ui -o ptsui5.py
#pyuic5 -x serialPage.ui -o serialPage.py

from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QFileDialog
from serial.tools import list_ports
from serial import Serial
import sys, time, os, subprocess, re, json, pkg_resources, pyjoystick
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from sys import platform
from pathlib import Path

#from qt_thread_updater import ThreadUpdater
#updater = ThreadUpdater()

#os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path('C:\\Users\\Music\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PyQt5\\Qt5\\plugins\\platforms') #join(sys._MEIPASS, 'PyQt5', 'plugins', 'platforms')
#plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
#os.environ["PYSDL2_DLL_PATH"] = "C:\\Users\\Music\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\sdl2dll\\dll"

#if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):

debug = False

serial_port = None

device_name = ""
serialLoop = False
msg = ""
sendData = ""

manualMove = ""

config = {}
cam1Label = 'Cam1'
cam2Label = 'Cam2'
cam3Label = 'Cam3'
cam4Label = 'Cam4'
cam5Label = 'Cam5'

btn_scan_show = False

flashTick = False
resetButtons = False
isConnected = False

whichCamRead = 1
whichCamSerial = 1
SetPosToggle = False

serialText = ""

message = ""

newText = ""
editButton = 0
editToggle = False

slideToggle = False

arr = []
oldAxisX = 0
oldAxisY = 0
oldAxisZ = 0
oldAxisW = 0
axisX = 0
axisY = 0
axisZ = 0
axisW = 0
data = bytearray(8)

previousTime = time.time()
currentMillisMoveCheck = time.time()
previousMillisMoveCheck = time.time()

moveCheckInterval = 0.8

Cam1TextColour = '55FF55'
Cam2TextColour = '9DDDFF'
Cam3TextColour = 'FFFF55'
Cam4TextColour = 'FF55FF'
Cam5TextColour = '55FFFF'

Cam1ButColour = '#208020'
Cam2ButColour = '#405C80'
Cam3ButColour = '#807100'
Cam4ButColour = '#008071'
Cam5ButColour = '#710080'

NotConnectedColour = '#751010'
ConnectedColour = '#107510'

cam1Pos1Set = False
cam1Pos2Set = False
cam1Pos3Set = False
cam1Pos4Set = False
cam1Pos5Set = False
cam1Pos6Set = False
cam1Pos7Set = False
cam1Pos8Set = False
cam1Pos9Set = False
cam1Pos10Set = False
cam1Pos1Run = False
cam1Pos2Run = False
cam1Pos3Run = False
cam1Pos4Run = False
cam1Pos5Run = False
cam1Pos6Run = False
cam1Pos7Run = False
cam1Pos8Run = False
cam1Pos9Run = False
cam1Pos10Run = False
cam1AtPos1 = False
cam1AtPos2 = False
cam1AtPos3 = False
cam1AtPos4 = False
cam1AtPos5 = False
cam1AtPos6 = False
cam1AtPos7 = False
cam1AtPos8 = False
cam1AtPos9 = False
cam1AtPos10 = False

cam2Pos1Set = False
cam2Pos2Set = False
cam2Pos3Set = False
cam2Pos4Set = False
cam2Pos5Set = False
cam2Pos6Set = False
cam2Pos7Set = False
cam2Pos8Set = False
cam2Pos9Set = False
cam2Pos10Set = False
cam2Pos1Run = False
cam2Pos2Run = False
cam2Pos3Run = False
cam2Pos4Run = False
cam2Pos5Run = False
cam2Pos6Run = False
cam2Pos7Run = False
cam2Pos8Run = False
cam2Pos9Run = False
cam2Pos10Run = False
cam2AtPos1 = False
cam2AtPos2 = False
cam2AtPos3 = False
cam2AtPos4 = False
cam2AtPos5 = False
cam2AtPos6 = False
cam2AtPos7 = False
cam2AtPos8 = False
cam2AtPos9 = False
cam2AtPos10 = False

cam3Pos1Set = False
cam3Pos2Set = False
cam3Pos3Set = False
cam3Pos4Set = False
cam3Pos5Set = False
cam3Pos6Set = False
cam3Pos7Set = False
cam3Pos8Set = False
cam3Pos9Set = False
cam3Pos10Set = False
cam3Pos1Run = False
cam3Pos2Run = False
cam3Pos3Run = False
cam3Pos4Run = False
cam3Pos5Run = False
cam3Pos6Run = False
cam3Pos7Run = False
cam3Pos8Run = False
cam3Pos9Run = False
cam3Pos10Run = False
cam3AtPos1 = False
cam3AtPos2 = False
cam3AtPos3 = False
cam3AtPos4 = False
cam3AtPos5 = False
cam3AtPos6 = False
cam3AtPos7 = False
cam3AtPos8 = False
cam3AtPos9 = False
cam3AtPos10 = False

cam4Pos1Set = False
cam4Pos2Set = False
cam4Pos3Set = False
cam4Pos4Set = False
cam4Pos5Set = False
cam4Pos6Set = False
cam4Pos7Set = False
cam4Pos8Set = False
cam4Pos9Set = False
cam4Pos10Set = False
cam4Pos1Run = False
cam4Pos2Run = False
cam4Pos3Run = False
cam4Pos4Run = False
cam4Pos5Run = False
cam4Pos6Run = False
cam4Pos7Run = False
cam4Pos8Run = False
cam4Pos9Run = False
cam4Pos10Run = False
cam4AtPos1 = False
cam4AtPos2 = False
cam4AtPos3 = False
cam4AtPos4 = False
cam4AtPos5 = False
cam4AtPos6 = False
cam4AtPos7 = False
cam4AtPos8 = False
cam4AtPos9 = False
cam4AtPos10 = False

cam5Pos1Set = False
cam5Pos2Set = False
cam5Pos3Set = False
cam5Pos4Set = False
cam5Pos5Set = False
cam5Pos6Set = False
cam5Pos7Set = False
cam5Pos8Set = False
cam5Pos9Set = False
cam5Pos10Set = False
cam5Pos1Run = False
cam5Pos2Run = False
cam5Pos3Run = False
cam5Pos4Run = False
cam5Pos5Run = False
cam5Pos6Run = False
cam5Pos7Run = False
cam5Pos8Run = False
cam5Pos9Run = False
cam5Pos10Run = False
cam5AtPos1 = False
cam5AtPos2 = False
cam5AtPos3 = False
cam5AtPos4 = False
cam5AtPos5 = False
cam5AtPos6 = False
cam5AtPos7 = False
cam5AtPos8 = False
cam5AtPos9 = False
cam5AtPos10 = False

OLDcam1Pos1Set = False
OLDcam1Pos2Set = False
OLDcam1Pos3Set = False
OLDcam1Pos4Set = False
OLDcam1Pos5Set = False
OLDcam1Pos6Set = False
OLDcam1Pos7Set = False
OLDcam1Pos8Set = False
OLDcam1Pos9Set = False
OLDcam1Pos10Set = False
OLDcam1AtPos1 = False
OLDcam1AtPos2 = False
OLDcam1AtPos3 = False
OLDcam1AtPos4 = False
OLDcam1AtPos5 = False
OLDcam1AtPos6 = False
OLDcam1AtPos7 = False
OLDcam1AtPos8 = False
OLDcam1AtPos9 = False
OLDcam1AtPos10 = False
OLDcam1Pos1Run = False
OLDcam1Pos2Run = False
OLDcam1Pos3Run = False
OLDcam1Pos4Run = False
OLDcam1Pos5Run = False
OLDcam1Pos6Run = False
OLDcam1Pos7Run = False
OLDcam1Pos8Run = False
OLDcam1Pos9Run = False
OLDcam1Pos10Run = False

OLDcam2Pos1Set = False
OLDcam2Pos2Set = False
OLDcam2Pos3Set = False
OLDcam2Pos4Set = False
OLDcam2Pos5Set = False
OLDcam2Pos6Set = False
OLDcam2Pos7Set = False
OLDcam2Pos8Set = False
OLDcam2Pos9Set = False
OLDcam2Pos10Set = False
OLDcam2AtPos1 = False
OLDcam2AtPos2 = False
OLDcam2AtPos3 = False
OLDcam2AtPos4 = False
OLDcam2AtPos5 = False
OLDcam2AtPos6 = False
OLDcam2AtPos7 = False
OLDcam2AtPos8 = False
OLDcam2AtPos9 = False
OLDcam2AtPos10 = False
OLDcam2Pos1Run = False
OLDcam2Pos2Run = False
OLDcam2Pos3Run = False
OLDcam2Pos4Run = False
OLDcam2Pos5Run = False
OLDcam2Pos6Run = False
OLDcam2Pos7Run = False
OLDcam2Pos8Run = False
OLDcam2Pos9Run = False
OLDcam2Pos10Run = False

OLDcam3Pos1Set = False
OLDcam3Pos2Set = False
OLDcam3Pos3Set = False
OLDcam3Pos4Set = False
OLDcam3Pos5Set = False
OLDcam3Pos6Set = False
OLDcam3Pos7Set = False
OLDcam3Pos8Set = False
OLDcam3Pos9Set = False
OLDcam3Pos10Set = False
OLDcam3AtPos1 = False
OLDcam3AtPos2 = False
OLDcam3AtPos3 = False
OLDcam3AtPos4 = False
OLDcam3AtPos5 = False
OLDcam3AtPos6 = False
OLDcam3AtPos7 = False
OLDcam3AtPos8 = False
OLDcam3AtPos9 = False
OLDcam3AtPos10 = False
OLDcam3Pos1Run = False
OLDcam3Pos2Run = False
OLDcam3Pos3Run = False
OLDcam3Pos4Run = False
OLDcam3Pos5Run = False
OLDcam3Pos6Run = False
OLDcam3Pos7Run = False
OLDcam3Pos8Run = False
OLDcam3Pos9Run = False
OLDcam3Pos10Run = False

OLDcam4Pos1Set = False
OLDcam4Pos2Set = False
OLDcam4Pos3Set = False
OLDcam4Pos4Set = False
OLDcam4Pos5Set = False
OLDcam4Pos6Set = False
OLDcam4Pos7Set = False
OLDcam4Pos8Set = False
OLDcam4Pos9Set = False
OLDcam4Pos10Set = False
OLDcam4AtPos1 = False
OLDcam4AtPos2 = False
OLDcam4AtPos3 = False
OLDcam4AtPos4 = False
OLDcam4AtPos5 = False
OLDcam4AtPos6 = False
OLDcam4AtPos7 = False
OLDcam4AtPos8 = False
OLDcam4AtPos9 = False
OLDcam4AtPos10 = False
OLDcam4Pos1Run = False
OLDcam4Pos2Run = False
OLDcam4Pos3Run = False
OLDcam4Pos4Run = False
OLDcam4Pos5Run = False
OLDcam4Pos6Run = False
OLDcam4Pos7Run = False
OLDcam4Pos8Run = False
OLDcam4Pos9Run = False
OLDcam4Pos10Run = False

OLDcam5Pos1Set = False
OLDcam5Pos2Set = False
OLDcam5Pos3Set = False
OLDcam5Pos4Set = False
OLDcam5Pos5Set = False
OLDcam5Pos6Set = False
OLDcam5Pos7Set = False
OLDcam5Pos8Set = False
OLDcam5Pos9Set = False
OLDcam5Pos10Set = False
OLDcam5AtPos1 = False
OLDcam5AtPos2 = False
OLDcam5AtPos3 = False
OLDcam5AtPos4 = False
OLDcam5AtPos5 = False
OLDcam5AtPos6 = False
OLDcam5AtPos7 = False
OLDcam5AtPos8 = False
OLDcam5AtPos9 = False
OLDcam5AtPos10 = False
OLDcam5Pos1Run = False
OLDcam5Pos2Run = False
OLDcam5Pos3Run = False
OLDcam5Pos4Run = False
OLDcam5Pos5Run = False
OLDcam5Pos6Run = False
OLDcam5Pos7Run = False
OLDcam5Pos8Run = False
OLDcam5Pos9Run = False
OLDcam5Pos10Run = False

cam1SliderSpeed = 0
cam2SliderSpeed = 0
cam3SliderSpeed = 0
cam4SliderSpeed = 0
cam5SliderSpeed = 0

oldcam1Speed = 9
oldcam2Speed = 9
oldcam3Speed = 9
oldcam4Speed = 9
oldcam5Speed = 9

cam1PTSpeed = 0
cam2PTSpeed = 0
cam3PTSpeed = 0
cam4PTSpeed = 0
cam5PTSpeed = 0

cam1ZoomLimit = 0
cam2ZoomLimit = 0
cam3ZoomLimit = 0
cam4ZoomLimit = 0
cam5ZoomLimit = 0

oldcam1PTSpeed = 9
oldcam2PTSpeed = 9
oldcam3PTSpeed = 9
oldcam4PTSpeed = 9
oldcam5PTSpeed = 9

cam1isZooming = False
cam1isRecording = False
cam2isZooming = False
cam2isRecording = False
cam3isZooming = False
cam3isRecording = False
cam4isZooming = False
cam4isRecording = False
cam5isZooming = False
cam5isRecording = False

cam1ptAccel = ''
cam1slAccel = ''
cam1ptSpeed1 = ''
cam1ptSpeed2 = ''
cam1ptSpeed3 = ''
cam1ptSpeed4 = ''
cam1slSpeed1 = ''
cam1slSpeed2 = ''
cam1slSpeed3 = ''
cam1slSpeed4 = ''

cam2ptAccel = ''
cam2slAccel = ''
cam2ptSpeed1 = ''
cam2ptSpeed2 = ''
cam2ptSpeed3 = ''
cam2ptSpeed4 = ''
cam2slSpeed1 = ''
cam2slSpeed2 = ''
cam2slSpeed3 = ''
cam2slSpeed4 = ''

cam3ptAccel = ''
cam3slAccel = ''
cam3ptSpeed1 = ''
cam3ptSpeed2 = ''
cam3ptSpeed3 = ''
cam3ptSpeed4 = ''
cam3slSpeed1 = ''
cam3slSpeed2 = ''
cam3slSpeed3 = ''
cam3slSpeed4 = ''

cam4ptAccel = ''
cam4slAccel = ''
cam4ptSpeed1 = ''
cam4ptSpeed2 = ''
cam4ptSpeed3 = ''
cam4ptSpeed4 = ''
cam4slSpeed1 = ''
cam4slSpeed2 = ''
cam4slSpeed3 = ''
cam4slSpeed4 = ''

cam5ptAccel = ''
cam5slAccel = ''
cam5ptSpeed1 = ''
cam5ptSpeed2 = ''
cam5ptSpeed3 = ''
cam5ptSpeed4 = ''
cam5slSpeed1 = ''
cam5slSpeed2 = ''
cam5slSpeed3 = ''
cam5slSpeed4 = ''


cam1AF = False
cam2AF = False
cam3AF = False
cam4AF = False
cam5AF = False

oldcam1AF = False
oldcam2AF = False
oldcam3AF = False
oldcam4AF = False
oldcam5AF = False

class Ui_SettingsWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        #super(Ui_SettingsWindow, self).__init__()

 #   def setupUi(self):

#class Ui_SettingsWindow(QMainWindow):
#    def __init__(self):
#        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

    def setupUi(self):
        global whichCamSerial

        self.setObjectName("settingsWindow")
        self.resize(1980, 1080)
        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 1311, 1001))
        self.groupBox.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButtonZoomLimit = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelZoomLimit.setFocus())
        self.pushButtonZoomLimit.setGeometry(QtCore.QRect(30, 650, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonZoomLimit.setFont(font)
        self.pushButtonZoomLimit.setStyleSheet("border: 5px solid grey; background-color: #40805C; border-radius: 30px;")
        self.pushButtonZoomLimit.setObjectName("pushButtonZoomLimit")
        self.pushButtonPTS4 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed4.setFocus())
        self.pushButtonPTS4.setGeometry(QtCore.QRect(30, 210, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonPTS4.setFont(font)
        self.pushButtonPTS4.setStyleSheet("border: 5px solid grey; background-color: #405C80; border-radius: 30px;")
        self.pushButtonPTS4.setObjectName("pushButtonPTS4")
        self.pushButtonPTS3 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed3.setFocus())
        self.pushButtonPTS3.setGeometry(QtCore.QRect(30, 300, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonPTS3.setFont(font)
        self.pushButtonPTS3.setStyleSheet("border: 5px solid grey; background-color: #405C80; border-radius: 30px;")
        self.pushButtonPTS3.setObjectName("pushButtonPTS3")
        self.pushButtonPTS2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed2.setFocus())
        self.pushButtonPTS2.setGeometry(QtCore.QRect(30, 390, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonPTS2.setFont(font)
        self.pushButtonPTS2.setStyleSheet("border: 5px solid grey; background-color: #405C80; border-radius: 30px;")
        self.pushButtonPTS2.setObjectName("pushButtonPTS2")
        self.pushButtonPTS1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed1.setFocus())
        self.pushButtonPTS1.setGeometry(QtCore.QRect(30, 480, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonPTS1.setFont(font)
        self.pushButtonPTS1.setStyleSheet("border: 5px solid grey; background-color: #405C80; border-radius: 30px;")
        self.pushButtonPTS1.setObjectName("pushButtonPTS1")
        self.pushButtonSS4 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed4.setFocus())
        self.pushButtonSS4.setGeometry(QtCore.QRect(710, 210, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonSS4.setFont(font)
        self.pushButtonSS4.setStyleSheet("border: 5px solid grey; background-color: #807100; border-radius: 30px;")
        self.pushButtonSS4.setObjectName("pushButtonSS4")
        self.pushButtonSS3 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed3.setFocus())
        self.pushButtonSS3.setGeometry(QtCore.QRect(710, 300, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonSS3.setFont(font)
        self.pushButtonSS3.setStyleSheet("border: 5px solid grey; background-color: #807100; border-radius: 30px;")
        self.pushButtonSS3.setObjectName("pushButtonSS3")
        self.pushButtonSS2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed2.setFocus())
        self.pushButtonSS2.setGeometry(QtCore.QRect(710, 390, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonSS2.setFont(font)
        self.pushButtonSS2.setStyleSheet("border: 5px solid grey; background-color: #807100; border-radius: 30px;")
        self.pushButtonSS2.setObjectName("pushButtonSS2")
        self.pushButtonSS1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed1.setFocus())
        self.pushButtonSS1.setGeometry(QtCore.QRect(710, 480, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonSS1.setFont(font)
        self.pushButtonSS1.setStyleSheet("border: 5px solid grey; background-color: #807100; border-radius: 30px;")
        self.pushButtonSS1.setObjectName("pushButtonSS1")
        self.pushButtonSA = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLaccel.setFocus())
        self.pushButtonSA.setGeometry(QtCore.QRect(710, 70, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonSA.setFont(font)
        self.pushButtonSA.setStyleSheet("border: 5px solid grey; background-color: #807100; border-radius: 30px;")
        self.pushButtonSA.setObjectName("pushButtonSA")
        self.pushButtonPTA = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTaccel.setFocus())
        self.pushButtonPTA.setGeometry(QtCore.QRect(30, 70, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonPTA.setFont(font)
        self.pushButtonPTA.setStyleSheet("border: 5px solid grey; background-color: #405C80; border-radius: 30px;")
        self.pushButtonPTA.setObjectName("pushButtonPTA")
        self.labelPTaccel = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTaccel.setGeometry(QtCore.QRect(360, 70, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelPTaccel.setFont(font)
        self.labelPTaccel.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTaccel.setText("")
        self.labelPTaccel.setObjectName("labelPTaccel")
        self.labelZoomLimit = QtWidgets.QLineEdit(self.groupBox)
        self.labelZoomLimit.setGeometry(QtCore.QRect(360, 650, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelZoomLimit.setFont(font)
        self.labelZoomLimit.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelZoomLimit.setText("")
        self.labelZoomLimit.setObjectName("labelZoomLimit")
        self.labelPTspeed4 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed4.setGeometry(QtCore.QRect(360, 210, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelPTspeed4.setFont(font)
        self.labelPTspeed4.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed4.setText("")
        self.labelPTspeed4.setObjectName("labelPTspeed4")
        self.labelPTspeed3 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed3.setGeometry(QtCore.QRect(360, 300, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelPTspeed3.setFont(font)
        self.labelPTspeed3.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed3.setText("")
        self.labelPTspeed3.setObjectName("labelPTspeed3")
        self.labelPTspeed2 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed2.setGeometry(QtCore.QRect(360, 390, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelPTspeed2.setFont(font)
        self.labelPTspeed2.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed2.setText("")
        self.labelPTspeed2.setObjectName("labelPTspeed2")
        self.labelPTspeed1 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed1.setGeometry(QtCore.QRect(360, 480, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelPTspeed1.setFont(font)
        self.labelPTspeed1.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed1.setText("")
        self.labelPTspeed1.setObjectName("labelPTspeed1")
        self.labelSLaccel = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLaccel.setGeometry(QtCore.QRect(1040, 70, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelSLaccel.setFont(font)
        self.labelSLaccel.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLaccel.setText("")
        self.labelSLaccel.setObjectName("labelSLaccel")
        self.labelSLspeed4 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed4.setGeometry(QtCore.QRect(1040, 210, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelSLspeed4.setFont(font)
        self.labelSLspeed4.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed4.setText("")
        self.labelSLspeed4.setObjectName("labelSLspeed4")
        self.labelSLspeed2 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed2.setGeometry(QtCore.QRect(1040, 390, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelSLspeed2.setFont(font)
        self.labelSLspeed2.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed2.setText("")
        self.labelSLspeed2.setObjectName("labelSLspeed2")
        self.labelSLspeed1 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed1.setGeometry(QtCore.QRect(1040, 480, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelSLspeed1.setFont(font)
        self.labelSLspeed1.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed1.setText("")
        self.labelSLspeed1.setObjectName("labelSLspeed1")
        self.labelSLspeed3 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed3.setGeometry(QtCore.QRect(1040, 300, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        self.labelSLspeed3.setFont(font)
        self.labelSLspeed3.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed3.setText("")
        self.labelSLspeed3.setObjectName("labelSLspeed3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(1350, 670, 551, 341))
        self.groupBox_2.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButtonNum1 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('1'))
        self.pushButtonNum1.setGeometry(QtCore.QRect(10, 20, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum1.setFont(font)
        self.pushButtonNum1.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum1.setObjectName("pushButtonNum1")
        self.pushButtonNum1.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum2 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('2'))
        self.pushButtonNum2.setGeometry(QtCore.QRect(130, 20, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum2.setFont(font)
        self.pushButtonNum2.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum2.setObjectName("pushButtonNum2")
        self.pushButtonNum2.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum3 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('3'))
        self.pushButtonNum3.setGeometry(QtCore.QRect(250, 20, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum3.setFont(font)
        self.pushButtonNum3.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum3.setObjectName("pushButtonNum3")
        self.pushButtonNum3.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum4 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('4'))
        self.pushButtonNum4.setGeometry(QtCore.QRect(10, 100, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum4.setFont(font)
        self.pushButtonNum4.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum4.setObjectName("pushButtonNum4")
        self.pushButtonNum4.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum5 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('5'))
        self.pushButtonNum5.setGeometry(QtCore.QRect(130, 100, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum5.setFont(font)
        self.pushButtonNum5.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum5.setObjectName("pushButtonNum5")
        self.pushButtonNum5.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum6 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('6'))
        self.pushButtonNum6.setGeometry(QtCore.QRect(250, 100, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum6.setFont(font)
        self.pushButtonNum6.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum6.setObjectName("pushButtonNum6")
        self.pushButtonNum6.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum7 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('7'))
        self.pushButtonNum7.setGeometry(QtCore.QRect(10, 180, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum7.setFont(font)
        self.pushButtonNum7.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum7.setObjectName("pushButtonNum7")
        self.pushButtonNum7.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum8 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('8'))
        self.pushButtonNum8.setGeometry(QtCore.QRect(130, 180, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum8.setFont(font)
        self.pushButtonNum8.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum8.setObjectName("pushButtonNum8")
        self.pushButtonNum8.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum9 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('9'))
        self.pushButtonNum9.setGeometry(QtCore.QRect(250, 180, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum9.setFont(font)
        self.pushButtonNum9.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum9.setObjectName("pushButtonNum9")
        self.pushButtonNum9.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum0 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('0'))
        self.pushButtonNum0.setGeometry(QtCore.QRect(130, 260, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonNum0.setFont(font)
        self.pushButtonNum0.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNum0.setObjectName("pushButtonNum0")
        self.pushButtonNum0.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNumBS = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.keyBackSpace())
        self.pushButtonNumBS.setGeometry(QtCore.QRect(410, 20, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(28)
        self.pushButtonNumBS.setFont(font)
        self.pushButtonNumBS.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNumBS.setObjectName("pushButtonNumBS")
        self.pushButtonNumBS.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNumEnt = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.keyEnter())
        self.pushButtonNumEnt.setGeometry(QtCore.QRect(390, 260, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(48)
        self.pushButtonNumEnt.setFont(font)
        self.pushButtonNumEnt.setStyleSheet("border: 5px solid grey; background-color: #008071; border-radius: 30px;")
        self.pushButtonNumEnt.setObjectName("pushButtonNumEnt")
        self.pushButtonNumEnt.setFocusPolicy(Qt.NoFocus)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(1380, 10, 291, 581))
        self.groupBox_3.setStyleSheet("color: #FFFFFF; background-color: #1e252a; border: 4px solid #262d32;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButtonCam1 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam1GetSettings())
        self.pushButtonCam1.setGeometry(QtCore.QRect(60, 30, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonCam1.setFont(font)
        self.pushButtonCam1.setStyleSheet("color:black; border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam1.setFlat(False)
        self.pushButtonCam1.setObjectName("pushButtonCam1")
        self.pushButtonCam2 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam2GetSettings())
        self.pushButtonCam2.setGeometry(QtCore.QRect(60, 140, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonCam2.setFont(font)
        self.pushButtonCam2.setStyleSheet("color:black; border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam2.setFlat(False)
        self.pushButtonCam2.setObjectName("pushButtonCam2")
        self.pushButtonCam3 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam3GetSettings())
        self.pushButtonCam3.setGeometry(QtCore.QRect(60, 250, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonCam3.setFont(font)
        self.pushButtonCam3.setStyleSheet("color:black; border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam3.setFlat(False)
        self.pushButtonCam3.setObjectName("pushButtonCam3")
        self.pushButtonCam4 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam4GetSettings())
        self.pushButtonCam4.setGeometry(QtCore.QRect(60, 360, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonCam4.setFont(font)
        self.pushButtonCam4.setStyleSheet("color:black; border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam4.setFlat(False)
        self.pushButtonCam4.setObjectName("pushButtonCam4")
        self.pushButtonCam5 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam5GetSettings())
        self.pushButtonCam5.setGeometry(QtCore.QRect(60, 470, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonCam5.setFont(font)
        self.pushButtonCam5.setStyleSheet("color:black; border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")
        self.pushButtonCam5.setFlat(False)
        self.pushButtonCam5.setObjectName("pushButtonCam5")
        self.pushButtonClose = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.pushToClose())
        self.pushButtonClose.setGeometry(QtCore.QRect(1720, 40, 181, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setStyleSheet("border: 4px solid red; background-color: #aa4c4C; border-radius: 40px;")
        self.pushButtonClose.setFlat(False)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.pushButtonStore = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.sendStoreEEPROM())
        self.pushButtonStore.setGeometry(QtCore.QRect(1720, 480, 181, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushButtonStore.setFont(font)
        self.pushButtonStore.setStyleSheet("border: 4px solid red; background-color: #4caa4C; border-radius: 40px;")
        self.pushButtonStore.setFlat(False)
        self.pushButtonStore.setObjectName("pushButtonStore")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1980, 24))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        global whichCamSerial

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("settingsWindow", "MainWindow"))
        self.pushButtonZoomLimit.setText(_translate("settingsWindow", "Zoom Limit"))
        self.pushButtonPTS4.setText(_translate("settingsWindow", "Pan/Tilt Speed - Fastest"))
        self.pushButtonPTS3.setText(_translate("settingsWindow", "Pan/Tilt Speed - Fast"))
        self.pushButtonPTS2.setText(_translate("settingsWindow", "Pan/Tilt Speed - Slow"))
        self.pushButtonPTS1.setText(_translate("settingsWindow", "Pan/Tilt Speed - Slowest"))
        self.pushButtonSS4.setText(_translate("settingsWindow", "Slider Speed - Fastest"))
        self.pushButtonSS3.setText(_translate("settingsWindow", "Slider Speed - Fast"))
        self.pushButtonSS2.setText(_translate("settingsWindow", "Slider Speed - Slow"))
        self.pushButtonSS1.setText(_translate("settingsWindow", "Slider Speed - Slowest"))
        self.pushButtonSA.setText(_translate("settingsWindow", "Slider Base Accel"))
        self.pushButtonPTA.setText(_translate("settingsWindow", "Pan/Tilt Base Accel"))
        self.pushButtonNum1.setText(_translate("settingsWindow", "1"))
        self.pushButtonNum2.setText(_translate("settingsWindow", "2"))
        self.pushButtonNum3.setText(_translate("settingsWindow", "3"))
        self.pushButtonNum4.setText(_translate("settingsWindow", "4"))
        self.pushButtonNum5.setText(_translate("settingsWindow", "5"))
        self.pushButtonNum6.setText(_translate("settingsWindow", "6"))
        self.pushButtonNum7.setText(_translate("settingsWindow", "7"))
        self.pushButtonNum8.setText(_translate("settingsWindow", "8"))
        self.pushButtonNum9.setText(_translate("settingsWindow", "9"))
        self.pushButtonNum0.setText(_translate("settingsWindow", "0"))
        self.pushButtonNumBS.setText(_translate("settingsWindow", "⌫"))
        self.pushButtonNumEnt.setText(_translate("settingsWindow", "↩"))
        self.pushButtonCam1.setText(_translate("settingsWindow", "Cam1"))
        self.pushButtonCam2.setText(_translate("settingsWindow", "Cam2"))
        self.pushButtonCam3.setText(_translate("settingsWindow", "Cam3"))
        self.pushButtonCam4.setText(_translate("settingsWindow", "Cam4"))
        self.pushButtonCam5.setText(_translate("settingsWindow", "Cam5"))
        self.pushButtonClose.setText(_translate("settingsWindow", "Close"))
        self.pushButtonStore.setText(_translate("settingsWindow", "Store"))

        #self.show()
        self.showFullScreen()

        self.getSettings()

    def getSettings(self):
        self.sendSerial('&1K')
        self.sendSerial('&2K')
        self.sendSerial('&3K')
        self.sendSerial('&4K')
        self.sendSerial('&5K')


    def emulateKey(self, key):
        widget = QtWidgets.QApplication.focusWidget()
        widget.setText(widget.text() + key)

    def keyBackSpace(self):
        widget = QtWidgets.QApplication.focusWidget()
        widgetText = widget.text()
        widget.setText(widgetText[:-1])

    def keyEnter(self):
        widget = QtWidgets.QApplication.focusWidget()

        if widget.objectName() == "labelPTaccel":
            self.sendSerial('&' + str(whichCamSerial) + 'L' + widget.text())
        elif widget.objectName() == "labelSLaccel":
            self.sendSerial('&' + str(whichCamSerial) + 'l' + widget.text())
        elif widget.objectName() == "labelPTspeed1":
            self.sendSerial('&' + str(whichCamSerial) + 'F' + widget.text())
        elif widget.objectName() == "labelPTspeed2":
            self.sendSerial('&' + str(whichCamSerial) + 'f' + widget.text())
        elif widget.objectName() == "labelPTspeed3":
            self.sendSerial('&' + str(whichCamSerial) + 'G' + widget.text())
        elif widget.objectName() == "labelPTspeed4":
            self.sendSerial('&' + str(whichCamSerial) + 'g' + widget.text())
        elif widget.objectName() == "labelSLspeed1":
            self.sendSerial('&' + str(whichCamSerial) + 'H' + widget.text())
        elif widget.objectName() == "labelSLspeed2":
            self.sendSerial('&' + str(whichCamSerial) + 'h' + widget.text())
        elif widget.objectName() == "labelSLspeed3":
            self.sendSerial('&' + str(whichCamSerial) + 'J' + widget.text())
        elif widget.objectName() == "labelSLspeed4":
            self.sendSerial('&' + str(whichCamSerial) + 'j' + widget.text())
        elif widget.objectName() == "labelZoomLimit":
            self.sendSerial('&' + str(whichCamSerial) + 'w' + widget.text())


            

    def sendStoreEEPROM(self):
        self.sendSerial('&' + str(whichCamSerial) + 'U')

    def pushToClose(self):
        self.close()

    def cam1GetSettings(self):
        global whichCamSerial
        global cam1ptAccel
        global cam1slAccel
        global cam1ptSpeed1
        global cam1ptSpeed2
        global cam1ptSpeed3
        global cam1ptSpeed4
        global cam1slSpeed1
        global cam1slSpeed2
        global cam1slSpeed3
        global cam1slSpeed4
        global cam1ZoomLimit

        whichCamSerial = 1
        self.sendSerial('&1K')

        self.labelPTaccel.setText(str(cam1ptAccel))
        self.labelSLaccel.setText(str(cam1slAccel))
        self.labelPTspeed1.setText(str(cam1ptSpeed1))
        self.labelPTspeed2.setText(str(cam1ptSpeed2))
        self.labelPTspeed3.setText(str(cam1ptSpeed3))
        self.labelPTspeed4.setText(str(cam1ptSpeed4))
        self.labelSLspeed1.setText(str(cam1slSpeed1))
        self.labelSLspeed2.setText(str(cam1slSpeed2))
        self.labelSLspeed3.setText(str(cam1slSpeed3))
        self.labelSLspeed4.setText(str(cam1slSpeed4))
        self.labelZoomLimit.setText(str(cam1ZoomLimit))

        self.pushButtonCam1.setStyleSheet("color: black; border: 4px solid red; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam2.setStyleSheet("color: black; border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam3.setStyleSheet("color: black; border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam4.setStyleSheet("color: black; border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam5.setStyleSheet("color: black; border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def cam2GetSettings(self):
        global whichCamSerial
        global cam2ptAccel
        global cam2slAccel
        global cam2ptSpeed1
        global cam2ptSpeed2
        global cam2ptSpeed3
        global cam2ptSpeed4
        global cam2slSpeed1
        global cam2slSpeed2
        global cam2slSpeed3
        global cam2slSpeed4
        global cam2ZoomLimit

        whichCamSerial = 2
        self.sendSerial('&2K')

        self.labelPTaccel.setText(str(cam2ptAccel))
        self.labelSLaccel.setText(str(cam2slAccel))
        self.labelPTspeed1.setText(str(cam2ptSpeed1))
        self.labelPTspeed2.setText(str(cam2ptSpeed2))
        self.labelPTspeed3.setText(str(cam2ptSpeed3))
        self.labelPTspeed4.setText(str(cam2ptSpeed4))
        self.labelSLspeed1.setText(str(cam2slSpeed1))
        self.labelSLspeed2.setText(str(cam2slSpeed2))
        self.labelSLspeed3.setText(str(cam2slSpeed3))
        self.labelSLspeed4.setText(str(cam2slSpeed4))
        self.labelZoomLimit.setText(str(cam2ZoomLimit))

        self.pushButtonCam1.setStyleSheet("color: black; border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam2.setStyleSheet("color: black; border: 4px solid red; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam3.setStyleSheet("color: black; border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam4.setStyleSheet("color: black; border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam5.setStyleSheet("color: black; border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def cam3GetSettings(self):
        global whichCamSerial
        global cam3ptAccel
        global cam3slAccel
        global cam3ptSpeed1
        global cam3ptSpeed2
        global cam3ptSpeed3
        global cam3ptSpeed4
        global cam3slSpeed1
        global cam3slSpeed2
        global cam3slSpeed3
        global cam3slSpeed4
        global cam3ZoomLimit

        whichCamSerial = 3
        self.sendSerial('&3K')

        self.labelPTaccel.setText(str(cam3ptAccel))
        self.labelSLaccel.setText(str(cam3slAccel))
        self.labelPTspeed1.setText(str(cam3ptSpeed1))
        self.labelPTspeed2.setText(str(cam3ptSpeed2))
        self.labelPTspeed3.setText(str(cam3ptSpeed3))
        self.labelPTspeed4.setText(str(cam3ptSpeed4))
        self.labelSLspeed1.setText(str(cam3slSpeed1))
        self.labelSLspeed2.setText(str(cam3slSpeed2))
        self.labelSLspeed3.setText(str(cam3slSpeed3))
        self.labelSLspeed4.setText(str(cam3slSpeed4))
        self.labelZoomLimit.setText(str(cam3ZoomLimit))

        self.pushButtonCam1.setStyleSheet("color: black; border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam2.setStyleSheet("color: black; border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam3.setStyleSheet("color: black; border: 4px solid red; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam4.setStyleSheet("color: black; border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam5.setStyleSheet("color: black; border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def cam4GetSettings(self):
        global whichCamSerial
        global cam4ptAccel
        global cam4slAccel
        global cam4ptSpeed1
        global cam4ptSpeed2
        global cam4ptSpeed3
        global cam4ptSpeed4
        global cam4slSpeed1
        global cam4slSpeed2
        global cam4slSpeed3
        global cam4slSpeed4
        global cam4ZoomLimit

        whichCamSerial = 4
        self.sendSerial('&4K')

        self.labelPTaccel.setText(str(cam4ptAccel))
        self.labelSLaccel.setText(str(cam4slAccel))
        self.labelPTspeed1.setText(str(cam4ptSpeed1))
        self.labelPTspeed2.setText(str(cam4ptSpeed2))
        self.labelPTspeed3.setText(str(cam4ptSpeed3))
        self.labelPTspeed4.setText(str(cam4ptSpeed4))
        self.labelSLspeed1.setText(str(cam4slSpeed1))
        self.labelSLspeed2.setText(str(cam4slSpeed2))
        self.labelSLspeed3.setText(str(cam4slSpeed3))
        self.labelSLspeed4.setText(str(cam4slSpeed4))
        self.labelZoomLimit.setText(str(cam4ZoomLimit))

        self.pushButtonCam1.setStyleSheet("color: black; border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam2.setStyleSheet("color: black; border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam3.setStyleSheet("color: black; border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam4.setStyleSheet("color: black; border: 4px solid red; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam5.setStyleSheet("color: black; border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def cam5GetSettings(self):
        global whichCamSerial
        global cam5ptAccel
        global cam5slAccel
        global cam5ptSpeed1
        global cam5ptSpeed2
        global cam5ptSpeed3
        global cam5ptSpeed4
        global cam5slSpeed1
        global cam5slSpeed2
        global cam5slSpeed3
        global cam5slSpeed4
        global cam5ZoomLimit

        whichCamSerial = 5
        self.sendSerial('&5K')

        self.labelPTaccel.setText(str(cam5ptAccel))
        self.labelSLaccel.setText(str(cam5slAccel))
        self.labelPTspeed1.setText(str(cam5ptSpeed1))
        self.labelPTspeed2.setText(str(cam5ptSpeed2))
        self.labelPTspeed3.setText(str(cam5ptSpeed3))
        self.labelPTspeed4.setText(str(cam5ptSpeed4))
        self.labelSLspeed1.setText(str(cam5slSpeed1))
        self.labelSLspeed2.setText(str(cam5slSpeed2))
        self.labelSLspeed3.setText(str(cam5slSpeed3))
        self.labelSLspeed4.setText(str(cam5slSpeed4))
        self.labelZoomLimit.setText(str(cam5ZoomLimit))

        self.pushButtonCam1.setStyleSheet("color: black; border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam2.setStyleSheet("color: black; border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam3.setStyleSheet("color: black; border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam4.setStyleSheet("color: black; border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam5.setStyleSheet("color: black; border: 4px solid red; background-color: #8D5395; border-radius: 10px;")

    def sendSerial(self, toSendData):
        global sendData
        sendData = toSendData

class Ui_editWindow(QMainWindow):
    def __init__(self):
        super(Ui_editWindow, self).__init__()

    def setupUi(self):
        self.setObjectName("editWindow")
        self.resize(332, 185)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #7593BC;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 30, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("border: 10px solid grey; background-color: #cccccc; border-radius: 40px;")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.editSet())
        self.pushButton.setGeometry(QtCore.QRect(200, 50, 91, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #cccccc;")
        self.pushButton.setObjectName("pushButton")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 332, 24))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()
        self.move(780, 150)

        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)  
        self.lineEdit.setFocus()

    def editSet(self):
        global newText
        newText = self.lineEdit.text()
        self.close()
        if sys.platform == "win32":
            os.system('wmic process where name="osk.exe" delete')
        elif sys.platform == "linux" or sys.platform == "linux2":
            os.system('/usr/bin/toggle-keyboard.sh')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.editSet()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("editWindow", "Edit Name"))
        self.pushButton.setText(_translate("editWindow", "Set"))


class Ui_MoverWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(861, 801)
        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushUP10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.up10())
        self.pushUP10.setGeometry(QtCore.QRect(240, 0, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(48)
        self.pushUP10.setFont(font)
        self.pushUP10.setStyleSheet("border: 10px solid grey; background-color: #33aa33; border-radius: 50px;")
        self.pushUP10.setObjectName("pushUP10")
        self.pushUP1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.up1())
        self.pushUP1.setGeometry(QtCore.QRect(240, 130, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(48)
        self.pushUP1.setFont(font)
        self.pushUP1.setStyleSheet("border: 10px solid grey; background-color: #77ff77; border-radius: 50px;")
        self.pushUP1.setObjectName("pushUP1")
        self.pushDOWN1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.down1())
        self.pushDOWN1.setGeometry(QtCore.QRect(240, 350, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushDOWN1.setFont(font)
        self.pushDOWN1.setStyleSheet("border: 10px solid grey; background-color: #77ff77; border-radius: 50px;")
        self.pushDOWN1.setObjectName("pushDOWN1")
        self.pushDOWN10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.down10())
        self.pushDOWN10.setGeometry(QtCore.QRect(240, 480, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushDOWN10.setFont(font)
        self.pushDOWN10.setStyleSheet("border: 10px solid grey; background-color: #33aa33; border-radius: 50px;")
        self.pushDOWN10.setObjectName("pushDOWN10")
        self.pushLEFT10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.left10())
        self.pushLEFT10.setGeometry(QtCore.QRect(0, 240, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushLEFT10.setFont(font)
        self.pushLEFT10.setStyleSheet("border: 10px solid grey; background-color: #aaaa33; border-radius: 50px;")
        self.pushLEFT10.setObjectName("pushLEFT10")
        self.pushLEFT1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.left1())
        self.pushLEFT1.setGeometry(QtCore.QRect(130, 240, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushLEFT1.setFont(font)
        self.pushLEFT1.setStyleSheet("border: 10px solid grey; background-color: #ffff77; border-radius: 50px;")
        self.pushLEFT1.setObjectName("pushLEFT1")
        self.pushRIGHT1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.right1())
        self.pushRIGHT1.setGeometry(QtCore.QRect(350, 240, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushRIGHT1.setFont(font)
        self.pushRIGHT1.setStyleSheet("border: 10px solid grey; background-color: #ffff77; border-radius: 50px;")
        self.pushRIGHT1.setObjectName("pushRIGHT1")
        self.pushRIGHT10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.right10())
        self.pushRIGHT10.setGeometry(QtCore.QRect(480, 240, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushRIGHT10.setFont(font)
        self.pushRIGHT10.setStyleSheet("border: 10px solid grey; background-color: #aaaa33; border-radius: 50px;")
        self.pushRIGHT10.setObjectName("pushRIGHT10")
        self.pushSlideLeft100 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideLeft100())
        self.pushSlideLeft100.setGeometry(QtCore.QRect(0, 640, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushSlideLeft100.setFont(font)
        self.pushSlideLeft100.setStyleSheet("border: 10px solid grey; background-color: #aa3333; border-radius: 50px;")
        self.pushSlideLeft100.setObjectName("pushSlideLeft100")
        self.pushSlideLeft10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideLeft10())
        self.pushSlideLeft10.setGeometry(QtCore.QRect(130, 640, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushSlideLeft10.setFont(font)
        self.pushSlideLeft10.setStyleSheet("border: 10px solid grey; background-color: #ff7777; border-radius: 50px;")
        self.pushSlideLeft10.setObjectName("pushSlideLeft10")
        self.pushSlideRight10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideRight10())
        self.pushSlideRight10.setGeometry(QtCore.QRect(350, 640, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushSlideRight10.setFont(font)
        self.pushSlideRight10.setStyleSheet("border: 10px solid grey; background-color: #ff7777; border-radius: 50px;")
        self.pushSlideRight10.setObjectName("pushSlideRight10")
        self.pushSlideRight100 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideRight100())
        self.pushSlideRight100.setGeometry(QtCore.QRect(480, 640, 121, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushSlideRight100.setFont(font)
        self.pushSlideRight100.setStyleSheet("border: 10px solid grey; background-color: #aa3333; border-radius: 50px;")
        self.pushSlideRight100.setObjectName("pushSlideRight100")
        self.pushZoomInFast = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(6), released= lambda: self.zoomMove(0))
        self.pushZoomInFast.setGeometry(QtCore.QRect(740, 50, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushZoomInFast.setFont(font)
        self.pushZoomInFast.setStyleSheet("border: 10px solid grey; background-color: #3333aa; border-radius: 50px;")
        self.pushZoomInFast.setObjectName("pushZoomInFast")
        self.pushZoomInSlow = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(1), released= lambda: self.zoomMove(0))
        self.pushZoomInSlow.setGeometry(QtCore.QRect(740, 180, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushZoomInSlow.setFont(font)
        self.pushZoomInSlow.setStyleSheet("border: 10px solid grey; background-color: #7777ff; border-radius: 50px;")
        self.pushZoomInSlow.setObjectName("pushZoomInSlow")
        self.pushZoomOutSlow = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(-1), released= lambda: self.zoomMove(0))
        self.pushZoomOutSlow.setGeometry(QtCore.QRect(740, 400, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushZoomOutSlow.setFont(font)
        self.pushZoomOutSlow.setStyleSheet("border: 10px solid grey; background-color: #7777ff; border-radius: 50px;")
        self.pushZoomOutSlow.setObjectName("pushZoomOutSlow")
        self.pushZoomOutFast = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(-6), released= lambda: self.zoomMove(0))
        self.pushZoomOutFast.setGeometry(QtCore.QRect(740, 530, 121, 121))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(36)
        self.pushZoomOutFast.setFont(font)
        self.pushZoomOutFast.setStyleSheet("border: 10px solid grey; background-color: #3333aa; border-radius: 50px;")
        self.pushZoomOutFast.setObjectName("pushZoomOutFast")
        self.pushClose = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.pushToClose())
        self.pushClose.setGeometry(QtCore.QRect(10, 0, 101, 101))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(48)
        self.pushClose.setFont(font)
        self.pushClose.setStyleSheet("border: 10px solid grey; background-color: #cc7777; border-radius: 50px;")
        self.pushClose.setObjectName("pushClose")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 603, 24))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()
    
        ag = QDesktopWidget().availableGeometry()       # 1920 x 1080
        sg = QDesktopWidget().screenGeometry()          # 1920 x 1080
        widget = self.geometry()                        # 
        x = (ag.width() / 2) - (widget.width() / 2)
        y = 2 * ag.height() - sg.height() - widget.height() - 50
        x = int(x)
        y = int(y)
        self.move(x, y)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Mover"))
        self.pushUP10.setText(_translate("MainWindow", "10"))
        self.pushUP1.setText(_translate("MainWindow", "1"))
        self.pushDOWN10.setText(_translate("MainWindow", "10"))
        self.pushDOWN1.setText(_translate("MainWindow", "1"))
        self.pushLEFT10.setText(_translate("MainWindow", "10"))
        self.pushLEFT1.setText(_translate("MainWindow", "1"))
        self.pushRIGHT1.setText(_translate("MainWindow", "1"))
        self.pushRIGHT10.setText(_translate("MainWindow", "10"))
        self.pushZoomInFast.setText(_translate("MainWindow", "Z++"))
        self.pushZoomInSlow.setText(_translate("MainWindow", "Z+"))
        self.pushZoomOutSlow.setText(_translate("MainWindow", "Z-"))
        self.pushZoomOutFast.setText(_translate("MainWindow", "Z--"))
        self.pushSlideLeft100.setText(_translate("MainWindow", "100"))
        self.pushSlideLeft10.setText(_translate("MainWindow", "10"))
        self.pushSlideRight10.setText(_translate("MainWindow", "10"))
        self.pushSlideRight100.setText(_translate("MainWindow", "100"))
        self.pushClose.setText(_translate("MainWindow", "X"))
        

    def pushToClose(self):
        self.close()

    def zoomMove(self, speed):
        global manualMove
        global whichCamSerial

        zoomSerial = "&"
        
        if whichCamSerial == 1: zoomSerial = zoomSerial + "1"
        elif whichCamSerial == 2: zoomSerial = zoomSerial + "2"
        elif whichCamSerial == 3: zoomSerial = zoomSerial + "3"
        elif whichCamSerial == 4: zoomSerial = zoomSerial + "4"
        elif whichCamSerial == 5: zoomSerial = zoomSerial + "5"

        if speed == -8: self.sendSerial(zoomSerial + 'a8')
        elif speed == -7: self.sendSerial(zoomSerial + 'a7')
        elif speed == -6: self.sendSerial(zoomSerial + 'a6')
        elif speed == -5: self.sendSerial(zoomSerial + 'a5')
        elif speed == -4: self.sendSerial(zoomSerial + 'a4')
        elif speed == -3: self.sendSerial(zoomSerial + 'a3')
        elif speed == -2: self.sendSerial(zoomSerial + 'a2')
        elif speed == -1: self.sendSerial(zoomSerial + 'a1')
        elif speed == 1: self.sendSerial(zoomSerial + 'A1')
        elif speed == 2: self.sendSerial(zoomSerial + 'A2')
        elif speed == 3: self.sendSerial(zoomSerial + 'A3')
        elif speed == 4: self.sendSerial(zoomSerial + 'A4')
        elif speed == 5: self.sendSerial(zoomSerial + 'A5')
        elif speed == 6: self.sendSerial(zoomSerial + 'A6')
        elif speed == 7: self.sendSerial(zoomSerial + 'A7')
        elif speed == 8: self.sendSerial(zoomSerial + 'A8')
        else: self.sendSerial(zoomSerial + 'q')

        #manualMove = "z" + str(speed)

    def up10(self):
        global manualMove
        manualMove = "u10"

    def up1(self):
        global manualMove
        manualMove = "u1"

    def down1(self):
        global manualMove
        manualMove = "d1"

    def down10(self):
        global manualMove
        manualMove = "d10"

    def left10(self):
        global manualMove
        manualMove = "l10"

    def left1(self):
        global manualMove
        manualMove = "l1"

    def right1(self):
        global manualMove
        manualMove = "r1"

    def right10(self):
        global manualMove
        manualMove = "r10"



    def slideLeft100(self):
        global manualMove
        manualMove = "sl100"

    def slideLeft10(self):
        global manualMove
        manualMove = "sl10"

    def slideRight10(self):
        global manualMove
        manualMove = "sr10"

    def slideRight100(self):
        global manualMove
        manualMove = "sr100"

    

    def sendSerial(self, toSendData):
        global sendData
        sendData = toSendData


class PTSapp(QMainWindow):
    def __init__(self, txt):
        self.text = txt
        super(PTSapp, self).__init__()
        self.setupUi()
    
    def openEditWindow(self, text):
        self.ui2 = Ui_editWindow()
        self.ui2.setupUi()
        self.ui2.lineEdit.setText(text)
        
        if sys.platform == "win32":
            os.startfile("C:\\\Windows\\System32\\osk.exe")
        elif sys.platform == "linux" or sys.platform == "linux2":
            os.system('/usr/bin/toggle-keyboard.sh')

    
    def openMoverWindow(self):
        self.ui3 = Ui_MoverWindow()
        self.ui3.setupUi()
        self.setPos(3)

    
    def openSettingsWindow(self):

        self.sendSerial('&1K')
        time.sleep(0.1)
        self.sendSerial('&2K')
        time.sleep(0.1)
        self.sendSerial('&3K')
        time.sleep(0.1)
        self.sendSerial('&4K')
        time.sleep(0.1)
        self.sendSerial('&5K')

        self.setPos(3)
        self.ui4 = Ui_SettingsWindow()
        self.ui4.setupUi()


    def setupUi(self):
        self.setObjectName("PTSapp")
        self.resize(1920, 1080)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 140, 1881, 160))
        self.groupBox.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32; ")
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")

        self.serial_port = None
        self.thread = None

        def handle_key_event(key):
            #print(key, '-', key.keytype, '-', key.number, '-', key.value)
            #keytest = key[1]
            #print(key.number)

            global whichCamSerial

            global axisX
            global axisY
            global axisZ
            global axisW
            
            #updater.now_call_latest()
            joyName = str(key.joystick)
            joyName = joyName.lower()

            joyType = str(key)
            #print(joyType[-6:])

            deadRange = 0.1

            if re.search('xbox', joyName):
                #print(key.number)
                if joyType[-6:] == "Axis 3":
                    if (key.value < -deadRange):
                        axisX = int(self.scale(key.value, (-1, -deadRange), (-255, 0)))
                    elif (key.value > deadRange):
                        axisX = int(self.scale(key.value, (1, deadRange), (255, 0)))
                    else:
                        axisX = 0
                    
                    #axisX = int(self.scale(key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 4":
                    if (key.value < -deadRange):
                        axisY = int(self.scale(key.value, (-1, -deadRange), (-255, 0)))
                    elif (key.value > deadRange):
                        axisY = int(self.scale(key.value, (1, deadRange), (255, 0)))
                    else:
                        axisY = 0

                    #axisY = int(self.scale(key.value, (-1, 1), (255,-255)))
                elif joyType[-6:] == "Axis 0":
                    if (key.value < -deadRange):
                        axisZ = int(self.scale(key.value, (-1, -deadRange), (-255, 0)))
                    elif (key.value > deadRange):
                        axisZ = int(self.scale(key.value, (1, deadRange), (255, 0)))
                    else:
                        axisZ = 0

                    #axisZ = int(self.scale(key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 1":
                    if (key.value < -deadRange):
                        axisW = int(self.scale(key.value, (-1, -(deadRange*2)), (-8, 0)))
                    elif (key.value > deadRange):
                        axisW = int(self.scale(key.value, (1, (deadRange*2)), (8, 0)))
                    else:
                        axisW = 0

                    #axisW = int(self.scale(key.value, (-1, 1), (8,-8)))
                elif joyType[-6:] == "tton 0" and (key.value == 0):
                    if whichCamSerial == 1:
                        if cam1AF:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                        else:
                            self.sendSerial('&' + str(whichCamSerial) + 'p')
                    elif whichCamSerial == 2:
                        if cam2AF:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                        else:
                            self.sendSerial('&' + str(whichCamSerial) + 'p')
                    elif whichCamSerial == 3:
                        if cam3AF:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                        else:
                            self.sendSerial('&' + str(whichCamSerial) + 'p')
                    elif whichCamSerial == 4:
                        if cam4AF:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                        else:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                    elif whichCamSerial == 5:
                        if cam5AF:
                            self.sendSerial('&' + str(whichCamSerial) + 'P')
                        else:
                            self.sendSerial('&' + str(whichCamSerial) + 'p')


            
            else:
                if joyType[-6:] == "Axis 3":
                    axisX = int(self.scale(key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 2":
                    axisY = int(self.scale(key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 0":
                    axisZ = int(self.scale(key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 1":
                    axisW = int(self.scale(key.value, (-1, 1), (-8,8)))


        mngr = pyjoystick.ThreadEventManager(event_loop=run_event_loop, handle_key_event=handle_key_event)
        mngr.start()

        self.pushButton11 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go1())
        self.pushButton11.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton11.setFont(font)
        self.pushButton11.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton11.setFlat(False)
        self.pushButton11.setObjectName("pushButton11")
        self.pushButton12 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go2())
        self.pushButton12.setGeometry(QtCore.QRect(160, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton12.setFont(font)
        self.pushButton12.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton12.setFlat(False)
        self.pushButton12.setObjectName("pushButton12")
        self.pushButton13 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go3())
        self.pushButton13.setGeometry(QtCore.QRect(300, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton13.setFont(font)
        self.pushButton13.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton13.setFlat(False)
        self.pushButton13.setObjectName("pushButton13")
        self.pushButton14 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go4())
        self.pushButton14.setGeometry(QtCore.QRect(440, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton14.setFont(font)
        self.pushButton14.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton14.setFlat(False)
        self.pushButton14.setObjectName("pushButton14")
        self.pushButton15 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go5())
        self.pushButton15.setGeometry(QtCore.QRect(580, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton15.setFont(font)
        self.pushButton15.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton15.setFlat(False)
        self.pushButton15.setObjectName("pushButton15")
        self.pushButton16 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go6())
        self.pushButton16.setGeometry(QtCore.QRect(720, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton16.setFont(font)
        self.pushButton16.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton16.setFlat(False)
        self.pushButton16.setObjectName("pushButton16")
        self.pushButton17 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go7())
        self.pushButton17.setGeometry(QtCore.QRect(860, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton17.setFont(font)
        self.pushButton17.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton17.setFlat(False)
        self.pushButton17.setObjectName("pushButton17")
        self.pushButton18 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go8())
        self.pushButton18.setGeometry(QtCore.QRect(1000, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton18.setFont(font)
        self.pushButton18.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton18.setFlat(False)
        self.pushButton18.setObjectName("pushButton18")
        self.pushButton19 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go9())
        self.pushButton19.setGeometry(QtCore.QRect(1140, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton19.setFont(font)
        self.pushButton19.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton19.setFlat(False)
        self.pushButton19.setObjectName("pushButton19")
        self.pushButton10 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go10())
        self.pushButton10.setGeometry(QtCore.QRect(1280, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton10.setFont(font)
        self.pushButton10.setStyleSheet("border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;")
        self.pushButton10.setFlat(False)
        self.pushButton10.setObjectName("pushButton10")
        self.dial1p = QtWidgets.QDial(self.groupBox, sliderPressed= lambda: self.setDials(1, 1, self.dial1p.value()))
        self.dial1p.setGeometry(QtCore.QRect(1500, 10, 140, 140))
        self.dial1p.setStyleSheet("background: black;")
        self.dial1p.setMinimum(1)
        self.dial1p.setMaximum(4)
        self.dial1p.setInvertedAppearance(False)
        self.dial1p.setInvertedControls(False)
        self.dial1p.setWrapping(False)
        self.dial1p.setNotchTarget(11.7)
        self.dial1p.setNotchesVisible(True)
        self.dial1p.setObjectName("dial1p")
        self.dial1s = QtWidgets.QDial(self.groupBox, sliderPressed= lambda: self.setDials(1, 2, self.dial1s.value()))
        self.dial1s.setGeometry(QtCore.QRect(1670, 10, 140, 140))
        self.dial1s.setStyleSheet("background: black;")
        self.dial1s.setMinimum(1)
        self.dial1s.setMaximum(4)
        self.dial1s.setNotchTarget(11.7)
        self.dial1s.setNotchesVisible(True)
        self.dial1s.setObjectName("dial1s")
        self.line1p = QtWidgets.QFrame(self.groupBox)
        self.line1p.setGeometry(QtCore.QRect(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        self.line1p.setStyleSheet("border: 10px solid #aaaa00;")
        self.line1p.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line1p.setLineWidth(20)
        self.line1p.setFrameShape(QtWidgets.QFrame.VLine)
        self.line1p.setObjectName("line1p")
        self.line1s = QtWidgets.QFrame(self.groupBox)
        self.line1s.setGeometry(QtCore.QRect(1820, 115, 20, 36))
        self.line1s.setStyleSheet("border: 10px solid #aaaa00;")
        self.line1s.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line1s.setLineWidth(20)
        self.line1s.setFrameShape(QtWidgets.QFrame.VLine)
        self.line1s.setObjectName("line1s")

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 310, 1881, 160))
        self.groupBox_2.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton21 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go1())
        self.pushButton21.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton21.setFont(font)
        self.pushButton21.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton21.setFlat(False)
        self.pushButton21.setObjectName("pushButton21")
        self.pushButton22 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go2())
        self.pushButton22.setGeometry(QtCore.QRect(160, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton22.setFont(font)
        self.pushButton22.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton22.setFlat(False)
        self.pushButton22.setObjectName("pushButton22")
        self.pushButton23 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go3())
        self.pushButton23.setGeometry(QtCore.QRect(300, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton23.setFont(font)
        self.pushButton23.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton23.setFlat(False)
        self.pushButton23.setObjectName("pushButton23")
        self.pushButton24 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go4())
        self.pushButton24.setGeometry(QtCore.QRect(440, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton24.setFont(font)
        self.pushButton24.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton24.setFlat(False)
        self.pushButton24.setObjectName("pushButton24")
        self.pushButton25 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go5())
        self.pushButton25.setGeometry(QtCore.QRect(580, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton25.setFont(font)
        self.pushButton25.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton25.setFlat(False)
        self.pushButton25.setObjectName("pushButton25")
        self.pushButton26 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go6())
        self.pushButton26.setGeometry(QtCore.QRect(720, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton26.setFont(font)
        self.pushButton26.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton26.setFlat(False)
        self.pushButton26.setObjectName("pushButton26")
        self.pushButton27 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go7())
        self.pushButton27.setGeometry(QtCore.QRect(860, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton27.setFont(font)
        self.pushButton27.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton27.setFlat(False)
        self.pushButton27.setObjectName("pushButton27")
        self.pushButton28 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go8())
        self.pushButton28.setGeometry(QtCore.QRect(1000, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton28.setFont(font)
        self.pushButton28.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton28.setFlat(False)
        self.pushButton28.setObjectName("pushButton28")
        self.pushButton29 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go9())
        self.pushButton29.setGeometry(QtCore.QRect(1140, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton29.setFont(font)
        self.pushButton29.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton29.setFlat(False)
        self.pushButton29.setObjectName("pushButton29")
        self.pushButton20 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go10())
        self.pushButton20.setGeometry(QtCore.QRect(1280, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton20.setFont(font)
        self.pushButton20.setStyleSheet("border: 10px solid grey; background-color: #405C80; border-radius: 40px;")
        self.pushButton20.setFlat(False)
        self.pushButton20.setObjectName("pushButton20")
        self.dial2p = QtWidgets.QDial(self.groupBox_2, sliderPressed= lambda: self.setDials(2, 1, self.dial2p.value()))
        self.dial2p.setGeometry(QtCore.QRect(1500, 10, 140, 140))
        self.dial2p.setStyleSheet("background: black;")
        self.dial2p.setMinimum(1)
        self.dial2p.setMaximum(4)
        self.dial2p.setTracking(True)
        self.dial2p.setInvertedAppearance(False)
        self.dial2p.setInvertedControls(False)
        self.dial2p.setWrapping(False)
        self.dial2p.setNotchTarget(11.7)
        self.dial2p.setNotchesVisible(True)
        self.dial2p.setObjectName("dial2p")
        self.dial2s = QtWidgets.QDial(self.groupBox_2, sliderPressed= lambda: self.setDials(2, 2, self.dial2s.value()))
        self.dial2s.setGeometry(QtCore.QRect(1670, 10, 140, 140))
        self.dial2s.setStyleSheet("background: black;")
        self.dial2s.setMinimum(1)
        self.dial2s.setMaximum(4)
        self.dial2s.setNotchTarget(11.7)
        self.dial2s.setNotchesVisible(True)
        self.dial2s.setObjectName("dial2s")
        self.line2p = QtWidgets.QFrame(self.groupBox_2)
        self.line2p.setGeometry(QtCore.QRect(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        self.line2p.setStyleSheet("border: 10px solid #aaaa00;")
        self.line2p.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line2p.setLineWidth(20)
        self.line2p.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2p.setObjectName("line2p")
        self.line2s = QtWidgets.QFrame(self.groupBox_2)
        self.line2s.setGeometry(QtCore.QRect(1820, 115, 20, 36))
        self.line2s.setStyleSheet("border: 10px solid #aaaa00;")
        self.line2s.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line2s.setLineWidth(20)
        self.line2s.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2s.setObjectName("line2s")

        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 480, 1881, 160))
        self.groupBox_3.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32; ")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton31 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go1())
        self.pushButton31.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton31.setFont(font)
        self.pushButton31.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton31.setFlat(False)
        self.pushButton31.setObjectName("pushButton31")
        self.pushButton32 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go2())
        self.pushButton32.setGeometry(QtCore.QRect(160, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton32.setFont(font)
        self.pushButton32.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton32.setFlat(False)
        self.pushButton32.setObjectName("pushButton32")
        self.pushButton33 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go3())
        self.pushButton33.setGeometry(QtCore.QRect(300, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton33.setFont(font)
        self.pushButton33.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton33.setFlat(False)
        self.pushButton33.setObjectName("pushButton33")
        self.pushButton34 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go4())
        self.pushButton34.setGeometry(QtCore.QRect(440, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton34.setFont(font)
        self.pushButton34.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton34.setFlat(False)
        self.pushButton34.setObjectName("pushButton34")
        self.pushButton35 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go5())
        self.pushButton35.setGeometry(QtCore.QRect(580, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton35.setFont(font)
        self.pushButton35.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton35.setFlat(False)
        self.pushButton35.setObjectName("pushButton35")
        self.pushButton36 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go6())
        self.pushButton36.setGeometry(QtCore.QRect(720, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton36.setFont(font)
        self.pushButton36.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton36.setFlat(False)
        self.pushButton36.setObjectName("pushButton36")
        self.pushButton37 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go7())
        self.pushButton37.setGeometry(QtCore.QRect(860, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton37.setFont(font)
        self.pushButton37.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton37.setFlat(False)
        self.pushButton37.setObjectName("pushButton37")
        self.pushButton38 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go8())
        self.pushButton38.setGeometry(QtCore.QRect(1000, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton38.setFont(font)
        self.pushButton38.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton38.setFlat(False)
        self.pushButton38.setObjectName("pushButton38")
        self.pushButton39 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go9())
        self.pushButton39.setGeometry(QtCore.QRect(1140, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton39.setFont(font)
        self.pushButton39.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton39.setFlat(False)
        self.pushButton39.setObjectName("pushButton39")
        self.pushButton30 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go10())
        self.pushButton30.setGeometry(QtCore.QRect(1280, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton30.setFont(font)
        self.pushButton30.setStyleSheet("border: 10px solid grey; background-color: #807100; border-radius: 40px;")
        self.pushButton30.setFlat(False)
        self.pushButton30.setObjectName("pushButton30")
        self.dial3p = QtWidgets.QDial(self.groupBox_3, sliderPressed= lambda: self.setDials(3, 1, self.dial3p.value()))
        self.dial3p.setGeometry(QtCore.QRect(1500, 10, 140, 140))
        self.dial3p.setStyleSheet("background: black;")
        self.dial3p.setMinimum(1)
        self.dial3p.setMaximum(4)
        self.dial3p.setInvertedAppearance(False)
        self.dial3p.setInvertedControls(False)
        self.dial3p.setWrapping(False)
        self.dial3p.setNotchTarget(11.7)
        self.dial3p.setNotchesVisible(True)
        self.dial3p.setObjectName("dial3p")
        self.dial3s = QtWidgets.QDial(self.groupBox_3, sliderPressed= lambda: self.setDials(3, 2, self.dial3s.value()))
        self.dial3s.setGeometry(QtCore.QRect(1670, 10, 140, 140))
        self.dial3s.setStyleSheet("background: black;")
        self.dial3s.setMinimum(1)
        self.dial3s.setMaximum(4)
        self.dial3s.setNotchTarget(11.7)
        self.dial3s.setNotchesVisible(True)
        self.dial3s.setObjectName("dial3s")
        self.line3p = QtWidgets.QFrame(self.groupBox_3)
        self.line3p.setGeometry(QtCore.QRect(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        self.line3p.setStyleSheet("border: 10px solid #aaaa00;")
        self.line3p.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line3p.setLineWidth(20)
        self.line3p.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3p.setObjectName("line3p")
        self.line3s = QtWidgets.QFrame(self.groupBox_3)
        self.line3s.setGeometry(QtCore.QRect(1820, 115, 20, 36))
        self.line3s.setStyleSheet("border: 10px solid #aaaa00;")
        self.line3s.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line3s.setLineWidth(20)
        self.line3s.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3s.setObjectName("line3s")

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 650, 1881, 160))
        self.groupBox_4.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32; ")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton41 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go1())
        self.pushButton41.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton41.setFont(font)
        self.pushButton41.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton41.setFlat(False)
        self.pushButton41.setObjectName("pushButton41")
        self.pushButton42 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go2())
        self.pushButton42.setGeometry(QtCore.QRect(160, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton42.setFont(font)
        self.pushButton42.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton42.setFlat(False)
        self.pushButton42.setObjectName("pushButton42")
        self.pushButton43 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go3())
        self.pushButton43.setGeometry(QtCore.QRect(300, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton43.setFont(font)
        self.pushButton43.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton43.setFlat(False)
        self.pushButton43.setObjectName("pushButton43")
        self.pushButton44 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go4())
        self.pushButton44.setGeometry(QtCore.QRect(440, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton44.setFont(font)
        self.pushButton44.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton44.setFlat(False)
        self.pushButton44.setObjectName("pushButton44")
        self.pushButton45 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go5())
        self.pushButton45.setGeometry(QtCore.QRect(580, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton45.setFont(font)
        self.pushButton45.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton45.setFlat(False)
        self.pushButton45.setObjectName("pushButton45")
        self.pushButton46 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go6())
        self.pushButton46.setGeometry(QtCore.QRect(720, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton46.setFont(font)
        self.pushButton46.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton46.setFlat(False)
        self.pushButton46.setObjectName("pushButton46")
        self.pushButton47 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go7())
        self.pushButton47.setGeometry(QtCore.QRect(860, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton47.setFont(font)
        self.pushButton47.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton47.setFlat(False)
        self.pushButton47.setObjectName("pushButton47")
        self.pushButton48 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go8())
        self.pushButton48.setGeometry(QtCore.QRect(1000, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton48.setFont(font)
        self.pushButton48.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton48.setFlat(False)
        self.pushButton48.setObjectName("pushButton48")
        self.pushButton49 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go9())
        self.pushButton49.setGeometry(QtCore.QRect(1140, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton49.setFont(font)
        self.pushButton49.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton49.setFlat(False)
        self.pushButton49.setObjectName("pushButton49")
        self.pushButton40 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go10())
        self.pushButton40.setGeometry(QtCore.QRect(1280, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton40.setFont(font)
        self.pushButton40.setStyleSheet("border: 10px solid grey; background-color: #008071; border-radius: 40px;")
        self.pushButton40.setFlat(False)
        self.pushButton40.setObjectName("pushButton40")
        self.dial4p = QtWidgets.QDial(self.groupBox_4, sliderPressed= lambda: self.setDials(4, 1, self.dial4p.value()))
        self.dial4p.setGeometry(QtCore.QRect(1500, 10, 140, 140))
        self.dial4p.setStyleSheet("background: black;")
        self.dial4p.setMinimum(1)
        self.dial4p.setMaximum(4)
        self.dial4p.setInvertedAppearance(False)
        self.dial4p.setInvertedControls(False)
        self.dial4p.setWrapping(False)
        self.dial4p.setNotchTarget(11.7)
        self.dial4p.setNotchesVisible(True)
        self.dial4p.setObjectName("dial4p")
        self.dial4s = QtWidgets.QDial(self.groupBox_4, sliderPressed= lambda: self.setDials(4, 2, self.dial4s.value()))
        self.dial4s.setGeometry(QtCore.QRect(1670, 10, 140, 140))
        self.dial4s.setStyleSheet("background: black;")
        self.dial4s.setMinimum(1)
        self.dial4s.setMaximum(4)
        self.dial4s.setNotchTarget(11.7)
        self.dial4s.setNotchesVisible(True)
        self.dial4s.setObjectName("dial4s")
        self.line4p = QtWidgets.QFrame(self.groupBox_4)
        self.line4p.setGeometry(QtCore.QRect(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        self.line4p.setStyleSheet("border: 10px solid #aaaa00;")
        self.line4p.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line4p.setLineWidth(20)
        self.line4p.setFrameShape(QtWidgets.QFrame.VLine)
        self.line4p.setObjectName("line4p")
        self.line4s = QtWidgets.QFrame(self.groupBox_4)
        self.line4s.setGeometry(QtCore.QRect(1820, 115, 20, 36))
        self.line4s.setStyleSheet("border: 10px solid #aaaa00;")
        self.line4s.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line4s.setLineWidth(20)
        self.line4s.setFrameShape(QtWidgets.QFrame.VLine)
        self.line4s.setObjectName("line4s")

        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 820, 1881, 160))
        self.groupBox_5.setStyleSheet("background-color: #1e252a; border: 4px solid #262d32;")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setFlat(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.pushButton51 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go1())
        self.pushButton51.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton51.setFont(font)
        self.pushButton51.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton51.setFlat(False)
        self.pushButton51.setObjectName("pushButton51")
        self.pushButton52 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go2())
        self.pushButton52.setGeometry(QtCore.QRect(160, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton52.setFont(font)
        self.pushButton52.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton52.setFlat(False)
        self.pushButton52.setObjectName("pushButton52")
        self.pushButton53 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go3())
        self.pushButton53.setGeometry(QtCore.QRect(300, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton53.setFont(font)
        self.pushButton53.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton53.setFlat(False)
        self.pushButton53.setObjectName("pushButton53")
        self.pushButton54 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go4())
        self.pushButton54.setGeometry(QtCore.QRect(440, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton54.setFont(font)
        self.pushButton54.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton54.setFlat(False)
        self.pushButton54.setObjectName("pushButton54")
        self.pushButton55 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go5())
        self.pushButton55.setGeometry(QtCore.QRect(580, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton55.setFont(font)
        self.pushButton55.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton55.setFlat(False)
        self.pushButton55.setObjectName("pushButton55")
        self.pushButton56 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go6())
        self.pushButton56.setGeometry(QtCore.QRect(720, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton56.setFont(font)
        self.pushButton56.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton56.setFlat(False)
        self.pushButton56.setObjectName("pushButton56")
        self.pushButton57 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go7())
        self.pushButton57.setGeometry(QtCore.QRect(860, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton57.setFont(font)
        self.pushButton57.setAutoFillBackground(False)
        self.pushButton57.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton57.setFlat(False)
        self.pushButton57.setObjectName("pushButton57")
        self.pushButton58 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go8())
        self.pushButton58.setGeometry(QtCore.QRect(1000, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton58.setFont(font)
        self.pushButton58.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton58.setFlat(False)
        self.pushButton58.setObjectName("pushButton58")
        self.pushButton59 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go9())
        self.pushButton59.setGeometry(QtCore.QRect(1140, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton59.setFont(font)
        self.pushButton59.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton59.setFlat(False)
        self.pushButton59.setObjectName("pushButton59")
        self.pushButton50 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go10())
        self.pushButton50.setGeometry(QtCore.QRect(1280, 20, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(32)
        self.pushButton50.setFont(font)
        self.pushButton50.setStyleSheet("border: 10px solid grey; background-color: #8D5395; border-radius: 40px;")
        self.pushButton50.setFlat(False)
        self.pushButton50.setObjectName("pushButton50")
        self.dial5p = QtWidgets.QDial(self.groupBox_5, sliderPressed= lambda: self.setDials(5, 1, self.dial5p.value()))
        self.dial5p.setGeometry(QtCore.QRect(1500, 10, 140, 140))
        self.dial5p.setStyleSheet("background: black;")
        self.dial5p.setMinimum(1)
        self.dial5p.setMaximum(4)
        self.dial5p.setInvertedAppearance(False)
        self.dial5p.setInvertedControls(False)
        self.dial5p.setWrapping(False)
        self.dial5p.setNotchTarget(11.7)
        self.dial5p.setNotchesVisible(True)
        self.dial5p.setObjectName("dial5p")
        self.dial5s = QtWidgets.QDial(self.groupBox_5, sliderPressed= lambda: self.setDials(5, 2, self.dial5s.value()))
        self.dial5s.setGeometry(QtCore.QRect(1670, 10, 140, 140))
        self.dial5s.setStyleSheet("background: black;")
        self.dial5s.setMinimum(1)
        self.dial5s.setMaximum(4)
        self.dial5s.setNotchTarget(11.7)
        self.dial5s.setNotchesVisible(True)
        self.dial5s.setObjectName("dial5s")
        self.line5p = QtWidgets.QFrame(self.groupBox_5)
        self.line5p.setGeometry(QtCore.QRect(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        self.line5p.setStyleSheet("border: 10px solid #aaaa00;")
        self.line5p.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line5p.setLineWidth(20)
        self.line5p.setFrameShape(QtWidgets.QFrame.VLine)
        self.line5p.setObjectName("line5p")
        self.line5s = QtWidgets.QFrame(self.groupBox_5)
        self.line5s.setGeometry(QtCore.QRect(1820, 115, 20, 36))
        self.line5s.setStyleSheet("border: 10px solid #aaaa00;")
        self.line5s.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line5s.setLineWidth(20)
        self.line5s.setFrameShape(QtWidgets.QFrame.VLine)
        self.line5s.setObjectName("line5s")

        self.pushButtonCam1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial1())
        self.pushButtonCam1.setGeometry(QtCore.QRect(570, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonCam1.setFont(font)
        self.pushButtonCam1.setStyleSheet("border: 4px solid red; background-color: #4C8A4C; border-radius: 10px;")
        self.pushButtonCam1.setFlat(False)
        self.pushButtonCam1.setObjectName("pushButtonCam1")
        self.pushButtonCam2 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial2())
        self.pushButtonCam2.setGeometry(QtCore.QRect(730, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonCam2.setFont(font)
        self.pushButtonCam2.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonCam2.setFlat(False)
        self.pushButtonCam2.setObjectName("pushButtonCam2")
        self.pushButtonCam3 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial3())
        self.pushButtonCam3.setGeometry(QtCore.QRect(890, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonCam3.setFont(font)
        self.pushButtonCam3.setStyleSheet("border: 4px solid grey; background-color: #807100; border-radius: 10px;")
        self.pushButtonCam3.setFlat(False)
        self.pushButtonCam3.setObjectName("pushButtonCam3")
        self.pushButtonCam4 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial4())
        self.pushButtonCam4.setGeometry(QtCore.QRect(1050, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonCam4.setFont(font)
        self.pushButtonCam4.setStyleSheet("border: 4px solid grey; background-color: #008071; border-radius: 10px;")
        self.pushButtonCam4.setFlat(False)
        self.pushButtonCam4.setObjectName("pushButtonCam4")
        self.pushButtonCam5 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial5())
        self.pushButtonCam5.setGeometry(QtCore.QRect(1210, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonCam5.setFont(font)
        self.pushButtonCam5.setStyleSheet("border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")
        self.pushButtonCam5.setFlat(False)
        self.pushButtonCam5.setObjectName("pushButtonCam5")

        self.labelCam1AF = QtWidgets.QLabel(self.centralwidget)
        self.labelCam1AF.setGeometry(QtCore.QRect(620, 110, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelCam1AF.setFont(font)
        self.labelCam1AF.setStyleSheet("color:red;")
        self.labelCam1AF.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCam1AF.setObjectName("labelCam1AF")
        self.labelCam1AF.hide()
        self.labelCam2AF = QtWidgets.QLabel(self.centralwidget)
        self.labelCam2AF.setGeometry(QtCore.QRect(780, 110, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelCam2AF.setFont(font)
        self.labelCam2AF.setStyleSheet("color:red;")
        self.labelCam2AF.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCam2AF.setObjectName("labelCam2AF")
        self.labelCam2AF.hide()
        self.labelCam3AF = QtWidgets.QLabel(self.centralwidget)
        self.labelCam3AF.setGeometry(QtCore.QRect(940, 110, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelCam3AF.setFont(font)
        self.labelCam3AF.setStyleSheet("color:red;")
        self.labelCam3AF.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCam3AF.setObjectName("labelCam3AF")
        self.labelCam3AF.hide()
        self.labelCam4AF = QtWidgets.QLabel(self.centralwidget)
        self.labelCam4AF.setGeometry(QtCore.QRect(1100, 110, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelCam4AF.setFont(font)
        self.labelCam4AF.setStyleSheet("color:red;")
        self.labelCam4AF.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCam4AF.setObjectName("labelCam4AF")
        self.labelCam4AF.hide()
        self.labelCam5AF = QtWidgets.QLabel(self.centralwidget)
        self.labelCam5AF.setGeometry(QtCore.QRect(1260, 110, 16, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelCam5AF.setFont(font)
        self.labelCam5AF.setStyleSheet("color:red;")
        self.labelCam5AF.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCam5AF.setObjectName("labelCam5AF")
        self.labelCam5AF.hide()


        self.labelDialPT = QtWidgets.QLabel(self.centralwidget)
        self.labelDialPT.setGeometry(QtCore.QRect(1540, 120, 100, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelDialPT.setFont(font)
        self.labelDialPT.setStyleSheet("color:grey;")
        self.labelDialPT.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDialPT.setObjectName("labelDialPT")

        self.labelDialSL = QtWidgets.QLabel(self.centralwidget)
        self.labelDialSL.setGeometry(QtCore.QRect(1710, 120, 100, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        self.labelDialSL.setFont(font)
        self.labelDialSL.setStyleSheet("color:grey;")
        self.labelDialSL.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDialSL.setObjectName("labelDialSL")

        self.pushButtonSet = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.setPos(3))
        self.pushButtonSet.setGeometry(QtCore.QRect(1760, 30, 120, 71))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.pushButtonSet.setFont(font)
        self.pushButtonSet.setStyleSheet("border: 4px solid grey; background-color: #bbbbbb; border-radius: 10px;")
        self.pushButtonSet.setFlat(False)
        self.pushButtonSet.setObjectName("pushButtonSet")
        self.pushButtonEdit = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.setEditToggle())
        self.pushButtonEdit.setGeometry(QtCore.QRect(40, 30, 120, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonEdit.setFont(font)
        self.pushButtonEdit.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonEdit.setFlat(False)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.pushButtonSLonly = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.slideOnlyToggle())
        self.pushButtonSLonly.setGeometry(QtCore.QRect(1740, 990, 120, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonSLonly.setFont(font)
        self.pushButtonSLonly.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        self.pushButtonSLonly.setFlat(False)
        self.pushButtonSLonly.setObjectName("pushButtonSLonly")
        self.pushButtonFileLoad = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.fileLoad())
        self.pushButtonFileLoad.setGeometry(QtCore.QRect(40, 990, 120, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonFileLoad.setFont(font)
        self.pushButtonFileLoad.setStyleSheet("border: 4px solid #FFFC67; background-color: #44d700; border-radius: 10px;")
        self.pushButtonFileLoad.setFlat(False)
        self.pushButtonFileLoad.setObjectName("pushButtonFileLoad")
        self.pushButtonFileLoad.hide()
        self.pushButtonFileSave = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.fileSave())
        self.pushButtonFileSave.setGeometry(QtCore.QRect(320, 990, 120, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonFileSave.setFont(font)
        self.pushButtonFileSave.setStyleSheet("border: 4px solid #d74444; background-color: #F76666; border-radius: 10px;")
        self.pushButtonFileSave.setFlat(False)
        self.pushButtonFileSave.setObjectName("pushButtonFileSave")
        self.pushButtonFileSave.hide()
        self.pushButtonSettings = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.openSettingsWindow())
        self.pushButtonSettings.setGeometry(QtCore.QRect(1020, 990, 260, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonSettings.setFont(font)
        self.pushButtonSettings.setStyleSheet("border: 4px solid #44a744; background-color: #66F766; border-radius: 10px;")
        self.pushButtonSettings.setFlat(False)
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.pushButtonSettings.hide()
        self.pushButtonLED = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.resetButtonColours())
        self.pushButtonLED.setGeometry(QtCore.QRect(1490, 990, 120, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonLED.setFont(font)
        self.pushButtonLED.setStyleSheet("border: 4px solid #FFFC67; background-color: #F7BA00; border-radius: 10px;")
        self.pushButtonLED.setFlat(False)
        self.pushButtonLED.setObjectName("pushButtonLED")
        self.pushButtonLED.hide()
        self.pushButtonExit = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.pushToClose())
        self.pushButtonExit.setGeometry(QtCore.QRect(1740, 990, 120, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(23)
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setStyleSheet("border: 4px solid #ff0000; background-color: #CC5050; border-radius: 10px;")
        self.pushButtonExit.setFlat(False)
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonExit.hide()
        self.labelFilename = QtWidgets.QLabel(self.centralwidget)
        self.labelFilename.setGeometry(QtCore.QRect(460, 990, 400, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelFilename.setFont(font)
        self.labelFilename.setStyleSheet("color: white; border: 4px solid grey; background-color: #333333; border-radius: 10px;")
        self.labelFilename.setText("")
        self.labelFilename.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFilename.setObjectName("labelFilename")
        self.labelFilename.setHidden(True)
        self.labelInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo.setGeometry(QtCore.QRect(1360, 50, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelInfo.setFont(font)
        self.labelInfo.setStyleSheet("color: white; border: 4px solid grey; background-color: #333333; border-radius: 10px;")
        self.labelInfo.setText("")
        self.labelInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelInfo.setObjectName("labelInfo")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(190, 50, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("color: white; border: 4px solid grey; background-color: #333333; border-radius: 10px;")
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated.connect(self.autoSerial)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuControl = QtWidgets.QMenu(self.menubar)
        self.menuControl.setObjectName("menuControl")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.device_name_list = []
        usb_device_list = list_ports.comports()
        self.device_name_list = [port.device for port in usb_device_list]
        self.device_name_list.insert(0, '-')

        self.buttonConnect(self.device_name_list)

        self.comboBox.addItems(self.device_name_list)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "PTSapp"))
        self.pushButton11.setText(_translate("MainWindow", "1"))
        self.pushButton12.setText(_translate("MainWindow", "2"))
        self.pushButton13.setText(_translate("MainWindow", "3"))
        self.pushButton14.setText(_translate("MainWindow", "4"))
        self.pushButton15.setText(_translate("MainWindow", "5"))
        self.pushButton16.setText(_translate("MainWindow", "6"))
        self.pushButton17.setText(_translate("MainWindow", "7"))
        self.pushButton18.setText(_translate("MainWindow", "8"))
        self.pushButton19.setText(_translate("MainWindow", "9"))
        self.pushButton10.setText(_translate("MainWindow", "10"))
        self.pushButton21.setText(_translate("MainWindow", "1"))
        self.pushButton22.setText(_translate("MainWindow", "2"))
        self.pushButton23.setText(_translate("MainWindow", "3"))
        self.pushButton24.setText(_translate("MainWindow", "4"))
        self.pushButton25.setText(_translate("MainWindow", "5"))
        self.pushButton26.setText(_translate("MainWindow", "6"))
        self.pushButton27.setText(_translate("MainWindow", "7"))
        self.pushButton28.setText(_translate("MainWindow", "8"))
        self.pushButton29.setText(_translate("MainWindow", "9"))
        self.pushButton20.setText(_translate("MainWindow", "10"))
        self.pushButton31.setText(_translate("MainWindow", "1"))
        self.pushButton32.setText(_translate("MainWindow", "2"))
        self.pushButton33.setText(_translate("MainWindow", "3"))
        self.pushButton34.setText(_translate("MainWindow", "4"))
        self.pushButton35.setText(_translate("MainWindow", "5"))
        self.pushButton36.setText(_translate("MainWindow", "6"))
        self.pushButton37.setText(_translate("MainWindow", "7"))
        self.pushButton38.setText(_translate("MainWindow", "8"))
        self.pushButton39.setText(_translate("MainWindow", "9"))
        self.pushButton30.setText(_translate("MainWindow", "10"))
        self.pushButton41.setText(_translate("MainWindow", "1"))
        self.pushButton42.setText(_translate("MainWindow", "2"))
        self.pushButton43.setText(_translate("MainWindow", "3"))
        self.pushButton44.setText(_translate("MainWindow", "4"))
        self.pushButton45.setText(_translate("MainWindow", "5"))
        self.pushButton46.setText(_translate("MainWindow", "6"))
        self.pushButton47.setText(_translate("MainWindow", "7"))
        self.pushButton48.setText(_translate("MainWindow", "8"))
        self.pushButton49.setText(_translate("MainWindow", "9"))
        self.pushButton40.setText(_translate("MainWindow", "10"))
        self.pushButton51.setText(_translate("MainWindow", "1"))
        self.pushButton52.setText(_translate("MainWindow", "2"))
        self.pushButton53.setText(_translate("MainWindow", "3"))
        self.pushButton54.setText(_translate("MainWindow", "4"))
        self.pushButton55.setText(_translate("MainWindow", "5"))
        self.pushButton56.setText(_translate("MainWindow", "6"))
        self.pushButton57.setText(_translate("MainWindow", "7"))
        self.pushButton58.setText(_translate("MainWindow", "8"))
        self.pushButton59.setText(_translate("MainWindow", "9"))
        self.pushButton50.setText(_translate("MainWindow", "10"))
        self.pushButtonCam1.setText(_translate("MainWindow", cam1Label))
        self.pushButtonCam2.setText(_translate("MainWindow", cam2Label))
        self.pushButtonCam3.setText(_translate("MainWindow", cam3Label))
        self.pushButtonCam4.setText(_translate("MainWindow", cam4Label))
        self.pushButtonCam5.setText(_translate("MainWindow", cam5Label))
        self.labelCam1AF.setText(_translate("MainWindow", "AF"))
        self.labelCam2AF.setText(_translate("MainWindow", "AF"))
        self.labelCam3AF.setText(_translate("MainWindow", "AF"))
        self.labelCam4AF.setText(_translate("MainWindow", "AF"))
        self.labelCam5AF.setText(_translate("MainWindow", "AF"))
        self.labelDialPT.setText(_translate("MainWindow", "Pan/Tilt Speed"))
        self.labelDialSL.setText(_translate("MainWindow", "Slide Speed"))
        self.pushButtonSet.setText(_translate("MainWindow", "SET"))
        self.pushButtonEdit.setText(_translate("MainWindow", "Edit"))
        self.pushButtonSLonly.setText(_translate("MainWindow", "SL"))
        self.pushButtonFileLoad.setText(_translate("MainWindow", "Load"))
        self.pushButtonFileSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonSettings.setText(_translate("MainWindow", "Settings"))
        self.pushButtonLED.setText(_translate("MainWindow", "Reset"))
        self.pushButtonExit.setText(_translate("MainWindow", "Exit"))

        self.initFlashTimer()

        #self.show()
        #self.showMaximized()
        self.showFullScreen()
        
        self.autoFileLoad()

    def pushToClose(self):
        self.close()

    def initFlashTimer(self):
        global whichCamSerial
        global SetPosToggle
        # self.timer.singleShot(2000,self.update_function)  # for one time call only (once)

        self.timer = QTimer()
        self.timer.timeout.connect(self.flash)
        self.timer.start(500)

        self.messageTimer = QTimer()
        self.messageTimer.timeout.connect(self.setMessage)
        self.messageTimer.start(10)


    def setDials(self, cam, ps, value):
        if cam == 1:
            if ps == 1:
                if value == 1: self.sendSerial('&1s1')
                elif value == 2: self.sendSerial('&1s2')
                elif value == 3: self.sendSerial('&1s3')
                elif value == 4: self.sendSerial('&1s4')
            else:
                if value == 1: self.sendSerial('&1W1')
                elif value == 2: self.sendSerial('&1W2')
                elif value == 3: self.sendSerial('&1W3')
                elif value == 4: self.sendSerial('&1W4')

        elif cam == 2:
            if ps == 1:
                if value == 1: self.sendSerial('&2s1')
                elif value == 2: self.sendSerial('&2s2')
                elif value == 3: self.sendSerial('&2s3')
                elif value == 4: self.sendSerial('&2s4')
            else:
                if value == 1: self.sendSerial('&2W1')
                elif value == 2: self.sendSerial('&2W2')
                elif value == 3: self.sendSerial('&2W3')
                elif value == 4: self.sendSerial('&2W4')

        elif cam == 3:
            if ps == 1:
                if value == 1: self.sendSerial('&3s1')
                elif value == 2: self.sendSerial('&3s2')
                elif value == 3: self.sendSerial('&3s3')
                elif value == 4: self.sendSerial('&3s4')
            else:
                if value == 1: self.sendSerial('&3W1')
                elif value == 2: self.sendSerial('&3W2')
                elif value == 3: self.sendSerial('&3W3')
                elif value == 4: self.sendSerial('&3W4')

        elif cam == 4:
            if ps == 1:
                if value == 1: self.sendSerial('&4s1')
                elif value == 2: self.sendSerial('&4s2')
                elif value == 3: self.sendSerial('&4s3')
                elif value == 4: self.sendSerial('&4s4')
            else:
                if value == 1: self.sendSerial('&4W1')
                elif value == 2: self.sendSerial('&4W2')
                elif value == 3: self.sendSerial('&4W3')
                elif value == 4: self.sendSerial('&4W4')

        elif cam == 5:
            if ps == 1:
                if value == 1: self.sendSerial('&5s1')
                elif value == 2: self.sendSerial('&5s2')
                elif value == 3: self.sendSerial('&5s3')
                elif value == 4: self.sendSerial('&5s4')
            else:
                if value == 1: self.sendSerial('&5W1')
                elif value == 2: self.sendSerial('&5W2')
                elif value == 3: self.sendSerial('&5W3')
                elif value == 4: self.sendSerial('&5W4')
    
    def setEditToggle(self):
        global editToggle
        global SetPosToggle

        if SetPosToggle:
            self.openMoverWindow()

        elif editToggle:
            editToggle = False
            self.pushButtonEdit.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
        
        else:
            editToggle = True
            self.pushButtonEdit.setStyleSheet("border: 4px solid grey; background-color: #CC5050; border-radius: 10px;")

    def slideOnlyToggle(self):
        global slideToggle
        global cam4Pos1Set
        global cam4Pos1Run
        global cam4AtPos1
        global cam4Pos10Set
        global cam4Pos10Run
        global cam4AtPos10
        global cam5Pos1Set
        global cam5Pos1Run
        global cam5AtPos1
        global cam5Pos10Set
        global cam5Pos10Run
        global cam5AtPos10

        buttonColourSet = "#ff0000"
        buttonColourAt = "#00ff00"

        if (slideToggle):
            slideToggle = False

            self.pushButtonSLonly.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")

            if cam4Pos1Set and not cam4Pos1Run and not cam4AtPos1:                                  # Set , not Run or At
                self.pushButton41.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos1Set and not cam4Pos1Run and cam4AtPos1:                                    # Set & At, not Run
                self.pushButton41.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos1Set:
                self.pushButton41.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

            if cam4Pos10Set and not cam4Pos10Run and not cam4AtPos10:                                  # Position LEDs cam4
                self.pushButton40.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos10Set and not cam4Pos10Run and cam4AtPos10:
                self.pushButton40.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos10Set:
                self.pushButton40.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')


            
            if cam5Pos1Set and not cam5Pos1Run and not cam5AtPos1:                                  # Set , not Run or At
                self.pushButton51.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos1Set and not cam5Pos1Run and cam5AtPos1:                                    # Set & At, not Run
                self.pushButton51.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos1Set:
                self.pushButton51.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

            if cam5Pos10Set and not cam5Pos10Run and not cam5AtPos10:                                  # Position LEDs cam5
                self.pushButton50.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos10Set and not cam5Pos10Run and cam5AtPos10:
                self.pushButton50.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos10Set:
                self.pushButton50.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        else:
            slideToggle = True

            self.pushButtonSLonly.setStyleSheet("border: 4px solid grey; background-color: #01E6CC; border-radius: 10px;")

            if cam4Pos1Set and not cam4Pos1Run and not cam4AtPos1:                                  # Set , not Run or At
                self.pushButton41.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')
            elif cam4Pos1Set and not cam4Pos1Run and cam4AtPos1:                                    # Set & At, not Run
                self.pushButton41.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')
            elif not cam4Pos1Set:
                self.pushButton41.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')

            if cam4Pos10Set and not cam4Pos10Run and not cam4AtPos10:                                  # Position LEDs cam4
                self.pushButton40.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')
            elif cam4Pos10Set and not cam4Pos10Run and cam4AtPos10:
                self.pushButton40.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')
            elif not cam4Pos10Set:
                self.pushButton40.setStyleSheet(f'border: 2px solid grey; background-color: #01E6CC; border-radius: 40px;')


            
            if cam5Pos1Set and not cam5Pos1Run and not cam5AtPos1:                                  # Set , not Run or At
                self.pushButton51.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')
            elif cam5Pos1Set and not cam5Pos1Run and cam5AtPos1:                                    # Set & At, not Run
                self.pushButton51.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')
            elif not cam5Pos1Set:
                self.pushButton51.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')

            if cam5Pos10Set and not cam5Pos10Run and not cam5AtPos10:                                  # Position LEDs cam5
                self.pushButton50.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')
            elif cam5Pos10Set and not cam5Pos10Run and cam5AtPos10:
                self.pushButton50.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')
            elif not cam5Pos10Set:
                self.pushButton50.setStyleSheet(f'border: 2px solid grey; background-color: #E97CF9; border-radius: 40px;')
    
    def fileLoad(self):
        global config
        global message
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label

        fname = QFileDialog.getOpenFileName(self, "Open Config", "C:\\Users\\Music\\Documents", "JSON (*.json)")
    
        if fname:
            self.labelFilename.setText(Path(fname[0]).stem)
            filename = fname[0]
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)

                self.pushButton11.setText(config['11'])
                self.pushButton12.setText(config['12'])
                self.pushButton13.setText(config['13'])
                self.pushButton14.setText(config['14'])
                self.pushButton15.setText(config['15'])
                self.pushButton16.setText(config['16'])
                self.pushButton17.setText(config['17'])
                self.pushButton18.setText(config['18'])
                self.pushButton19.setText(config['19'])
                self.pushButton10.setText(config['10'])
                self.pushButton21.setText(config['21'])
                self.pushButton22.setText(config['22'])
                self.pushButton23.setText(config['23'])
                self.pushButton24.setText(config['24'])
                self.pushButton25.setText(config['25'])
                self.pushButton26.setText(config['26'])
                self.pushButton27.setText(config['27'])
                self.pushButton28.setText(config['28'])
                self.pushButton29.setText(config['29'])
                self.pushButton20.setText(config['20'])
                self.pushButton31.setText(config['31'])
                self.pushButton32.setText(config['32'])
                self.pushButton33.setText(config['33'])
                self.pushButton34.setText(config['34'])
                self.pushButton35.setText(config['35'])
                self.pushButton36.setText(config['36'])
                self.pushButton37.setText(config['37'])
                self.pushButton38.setText(config['38'])
                self.pushButton39.setText(config['39'])
                self.pushButton30.setText(config['30'])
                self.pushButton41.setText(config['41'])
                self.pushButton42.setText(config['42'])
                self.pushButton43.setText(config['43'])
                self.pushButton44.setText(config['44'])
                self.pushButton45.setText(config['45'])
                self.pushButton46.setText(config['46'])
                self.pushButton47.setText(config['47'])
                self.pushButton48.setText(config['48'])
                self.pushButton49.setText(config['49'])
                self.pushButton40.setText(config['40'])
                self.pushButton51.setText(config['51'])
                self.pushButton52.setText(config['52'])
                self.pushButton53.setText(config['53'])
                self.pushButton54.setText(config['54'])
                self.pushButton55.setText(config['55'])
                self.pushButton56.setText(config['56'])
                self.pushButton57.setText(config['57'])
                self.pushButton58.setText(config['58'])
                self.pushButton59.setText(config['59'])
                self.pushButton50.setText(config['50'])

                cam1Label = config['Cam1']
                cam2Label = config['Cam2']
                cam3Label = config['Cam3']
                cam4Label = config['Cam4']
                cam5Label = config['Cam5']
        
            except:
                message = "Couldn't Load File"


    def fileSave(self):
        global config
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label

        config['11'] = self.pushButton11.text()
        config['12'] = self.pushButton12.text()
        config['13'] = self.pushButton13.text()
        config['14'] = self.pushButton14.text()
        config['15'] = self.pushButton15.text()
        config['16'] = self.pushButton16.text()
        config['17'] = self.pushButton17.text()
        config['18'] = self.pushButton18.text()
        config['19'] = self.pushButton19.text()
        config['10'] = self.pushButton10.text()
        config['21'] = self.pushButton21.text()
        config['22'] = self.pushButton22.text()
        config['23'] = self.pushButton23.text()
        config['24'] = self.pushButton24.text()
        config['25'] = self.pushButton25.text()
        config['26'] = self.pushButton26.text()
        config['27'] = self.pushButton27.text()
        config['28'] = self.pushButton28.text()
        config['29'] = self.pushButton29.text()
        config['20'] = self.pushButton20.text()
        config['31'] = self.pushButton31.text()
        config['32'] = self.pushButton32.text()
        config['33'] = self.pushButton33.text()
        config['34'] = self.pushButton34.text()
        config['35'] = self.pushButton35.text()
        config['36'] = self.pushButton36.text()
        config['37'] = self.pushButton37.text()
        config['38'] = self.pushButton38.text()
        config['39'] = self.pushButton39.text()
        config['30'] = self.pushButton30.text()
        config['41'] = self.pushButton41.text()
        config['42'] = self.pushButton42.text()
        config['43'] = self.pushButton43.text()
        config['44'] = self.pushButton44.text()
        config['45'] = self.pushButton45.text()
        config['46'] = self.pushButton46.text()
        config['47'] = self.pushButton47.text()
        config['48'] = self.pushButton48.text()
        config['49'] = self.pushButton49.text()
        config['40'] = self.pushButton40.text()
        config['51'] = self.pushButton51.text()
        config['52'] = self.pushButton52.text()
        config['53'] = self.pushButton53.text()
        config['54'] = self.pushButton54.text()
        config['55'] = self.pushButton55.text()
        config['56'] = self.pushButton56.text()
        config['57'] = self.pushButton57.text()
        config['58'] = self.pushButton58.text()
        config['59'] = self.pushButton59.text()
        config['50'] = self.pushButton50.text()
        config['Cam1'] = cam1Label
        config['Cam2'] = cam2Label
        config['Cam3'] = cam3Label
        config['Cam4'] = cam4Label
        config['Cam5'] = cam5Label

        fname, _ = QFileDialog.getSaveFileName(self, "Save Config", "C:\\Users\\Music\\Documents", "JSON (*.json)")
        
        if fname:
            self.labelFilename.setText(Path(fname).stem)
            with open(fname, 'w') as f:
                json.dump(config, f)


    def autoFileLoad(self):
        global config
        global message
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label

        if sys.platform == "win32":
            filename = 'C:\\Users\\Music\\Documents\\default.json'
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)

                self.pushButton11.setText(config['11'])
                self.pushButton12.setText(config['12'])
                self.pushButton13.setText(config['13'])
                self.pushButton14.setText(config['14'])
                self.pushButton15.setText(config['15'])
                self.pushButton16.setText(config['16'])
                self.pushButton17.setText(config['17'])
                self.pushButton18.setText(config['18'])
                self.pushButton19.setText(config['19'])
                self.pushButton10.setText(config['10'])
                self.pushButton21.setText(config['21'])
                self.pushButton22.setText(config['22'])
                self.pushButton23.setText(config['23'])
                self.pushButton24.setText(config['24'])
                self.pushButton25.setText(config['25'])
                self.pushButton26.setText(config['26'])
                self.pushButton27.setText(config['27'])
                self.pushButton28.setText(config['28'])
                self.pushButton29.setText(config['29'])
                self.pushButton20.setText(config['20'])
                self.pushButton31.setText(config['31'])
                self.pushButton32.setText(config['32'])
                self.pushButton33.setText(config['33'])
                self.pushButton34.setText(config['34'])
                self.pushButton35.setText(config['35'])
                self.pushButton36.setText(config['36'])
                self.pushButton37.setText(config['37'])
                self.pushButton38.setText(config['38'])
                self.pushButton39.setText(config['39'])
                self.pushButton30.setText(config['30'])
                self.pushButton41.setText(config['41'])
                self.pushButton42.setText(config['42'])
                self.pushButton43.setText(config['43'])
                self.pushButton44.setText(config['44'])
                self.pushButton45.setText(config['45'])
                self.pushButton46.setText(config['46'])
                self.pushButton47.setText(config['47'])
                self.pushButton48.setText(config['48'])
                self.pushButton49.setText(config['49'])
                self.pushButton40.setText(config['40'])
                self.pushButton51.setText(config['51'])
                self.pushButton52.setText(config['52'])
                self.pushButton53.setText(config['53'])
                self.pushButton54.setText(config['54'])
                self.pushButton55.setText(config['55'])
                self.pushButton56.setText(config['56'])
                self.pushButton57.setText(config['57'])
                self.pushButton58.setText(config['58'])
                self.pushButton59.setText(config['59'])
                self.pushButton50.setText(config['50'])

                cam1Label = config['Cam1']
                cam2Label = config['Cam2']
                cam3Label = config['Cam3']
                cam4Label = config['Cam4']
                cam5Label = config['Cam5']
            
                self.pushButtonCam1.setText(cam1Label)
                self.pushButtonCam2.setText(cam2Label)
                self.pushButtonCam3.setText(cam3Label)
                self.pushButtonCam4.setText(cam4Label)
                self.pushButtonCam5.setText(cam5Label)
        
            except:
                message = "Couldn't Load File"


    def doJoyMoves(self, dt):
        global axisX
        global axisY
        global axisZ
        global axisW
        global oldAxisX
        global oldAxisY
        global oldAxisZ
        global oldAxisW
        global arr
        global currentMillisMoveCheck
        global previousMillisMoveCheck
        global previousTime
        global moveCheckInterval
        global whichCamSerial

        if (axisX == oldAxisX) and (axisY == oldAxisY) and (axisZ == oldAxisZ) and ((abs(axisX) + abs(axisY) + abs(axisZ)) != 0):
            currentMillisMoveCheck = time.time()
            if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval):
                previousMillisMoveCheck = currentMillisMoveCheck
                #arr = [4, axisZh, axisXh, axisYh]                                          # for debugging
                self.sendJoystick(arr)
        if ((axisX != oldAxisX) or (axisY != oldAxisY) or (axisZ != oldAxisZ)): # or doKeyControlA or doKeyControlD or doKeyControlW or doKeyControlS or doKeyControlSL or doKeyControlSR) and ((time.time() - previousTime) > 0.03) :
            previousTime = time.time()
            oldAxisX = axisX
            oldAxisY = axisY
            oldAxisZ = axisZ
            axisXh = self.toHex(axisX, 16)
            axisYh = self.toHex(axisY, 16)
            axisZh = self.toHex(axisZ, 16)

            arr = [4, axisZh, axisXh, axisYh]
            self.sendJoystick(arr)
            previousMillisMoveCheck = time.time()

        if (axisW != oldAxisW):                                     # ZOOM
            oldAxisW = axisW
            zoomSerial = "&"
            if whichCamSerial == 1: zoomSerial = zoomSerial + "1"
            elif whichCamSerial == 2: zoomSerial = zoomSerial + "2"
            elif whichCamSerial == 3: zoomSerial = zoomSerial + "3"
            elif whichCamSerial == 4: zoomSerial = zoomSerial + "4"
            elif whichCamSerial == 5: zoomSerial = zoomSerial + "5"

            if axisW == -8: self.sendSerial(zoomSerial + 'a8')
            elif axisW == -7: self.sendSerial(zoomSerial + 'a7')
            elif axisW == -6: self.sendSerial(zoomSerial + 'a6')
            elif axisW == -5: self.sendSerial(zoomSerial + 'a5')
            elif axisW == -4: self.sendSerial(zoomSerial + 'a4')
            elif axisW == -3: self.sendSerial(zoomSerial + 'a3')
            elif axisW == -2: self.sendSerial(zoomSerial + 'a2')
            elif axisW == -1: self.sendSerial(zoomSerial + 'a1')
            elif axisW == 1: self.sendSerial(zoomSerial + 'A1')
            elif axisW == 2: self.sendSerial(zoomSerial + 'A2')
            elif axisW == 3: self.sendSerial(zoomSerial + 'A3')
            elif axisW == 4: self.sendSerial(zoomSerial + 'A4')
            elif axisW == 5: self.sendSerial(zoomSerial + 'A5')
            elif axisW == 6: self.sendSerial(zoomSerial + 'A6')
            elif axisW == 7: self.sendSerial(zoomSerial + 'A7')
            elif axisW == 8: self.sendSerial(zoomSerial + 'A8')
            else: 
                self.sendSerial(zoomSerial + 'q')
                self.sendSerial(zoomSerial + 'q')
                self.sendSerial(zoomSerial + 'q')
                self.sendSerial(zoomSerial + 'q')

    def sendJoystick(self, arr):
        global data
        global whichCamSerial
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1AtPos7
        global cam1AtPos8
        global cam1AtPos9
        global cam1AtPos10
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2AtPos7
        global cam2AtPos8
        global cam2AtPos9
        global cam2AtPos10
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3AtPos7
        global cam3AtPos8
        global cam3AtPos9
        global cam3AtPos10
        global cam4AtPos1
        global cam4AtPos2
        global cam4AtPos3
        global cam4AtPos4
        global cam4AtPos5
        global cam4AtPos6
        global cam4AtPos7
        global cam4AtPos8
        global cam4AtPos9
        global cam4AtPos10
        global cam5AtPos1
        global cam5AtPos2
        global cam5AtPos3
        global cam5AtPos4
        global cam5AtPos5
        global cam5AtPos6
        global cam5AtPos7
        global cam5AtPos8
        global cam5AtPos9
        global cam5AtPos10
        
        sliderInt = int(arr[1], 16)
        panInt = int(arr[2], 16)
        tiltInt = int(arr[3], 16)

        #print(sliderInt)

        data[0] = 4
        
        if ((sliderInt > 0) and (sliderInt < 256)):
            data[1] = 0
            data[2] = sliderInt
        elif sliderInt > 256:
            data[1] = 255
            data[2] = (sliderInt-65281)
        else:
            data[1] = 0
            data[2] = 0

        if ((panInt > 0) and (panInt < 256)):
            data[3] = 0
            data[4] = panInt
        elif panInt > 256:
            data[3] = 255
            data[4] = (panInt-65281)
        else:
            data[3] = 0
            data[4] = 0

        if ((tiltInt > 0) and (tiltInt < 256)):
            data[5] = 0
            data[6] = tiltInt
        elif tiltInt > 256:
            data[5] = 255
            data[6] = (tiltInt-65281)
        else:
            data[5] = 0
            data[6] = 0
        
        data[7] = whichCamSerial
        #print(data[2])
        self.sendSerial(data)

        #print(data)                   

        #if not self.serial_port:
        #    pass
        #else:
            #self.serial_port.write(data)
        #   print(data)                                    # for debugging
        
        if whichCamSerial == 1 and (cam1AtPos1 or cam1AtPos2 or cam1AtPos3 or cam1AtPos4 or cam1AtPos5 or cam1AtPos6 or cam1AtPos7 or cam1AtPos8 or cam1AtPos9 or cam1AtPos10):
            cam1AtPos1 = False
            cam1AtPos2 = False
            cam1AtPos3 = False
            cam1AtPos4 = False
            cam1AtPos5 = False
            cam1AtPos6 = False
            cam1AtPos7 = False
            cam1AtPos8 = False
            cam1AtPos9 = False
            cam1AtPos10 = False
            self.doButtonColours()
        elif whichCamSerial == 2 and (cam2AtPos1 or cam2AtPos2 or cam2AtPos3 or cam2AtPos4 or cam2AtPos5 or cam2AtPos6 or cam2AtPos7 or cam2AtPos8 or cam2AtPos9 or cam2AtPos10):
            cam2AtPos1 = False
            cam2AtPos2 = False
            cam2AtPos3 = False
            cam2AtPos4 = False
            cam2AtPos5 = False
            cam2AtPos6 = False
            cam2AtPos7 = False
            cam2AtPos8 = False
            cam2AtPos9 = False
            cam2AtPos10 = False
            self.doButtonColours()
        elif whichCamSerial == 3 and (cam3AtPos1 or cam3AtPos2 or cam3AtPos3 or cam3AtPos4 or cam3AtPos5 or cam3AtPos6 or cam3AtPos7 or cam3AtPos8 or cam3AtPos9 or cam3AtPos10):
            cam3AtPos1 = False
            cam3AtPos2 = False
            cam3AtPos3 = False
            cam3AtPos4 = False
            cam3AtPos5 = False
            cam3AtPos6 = False
            cam3AtPos7 = False
            cam3AtPos8 = False
            cam3AtPos9 = False
            cam3AtPos10 = False
            self.doButtonColours()
        elif whichCamSerial == 4 and (cam4AtPos1 or cam4AtPos2 or cam4AtPos3 or cam4AtPos4 or cam4AtPos5 or cam4AtPos6 or cam4AtPos7 or cam4AtPos8 or cam4AtPos9 or cam4AtPos10):
            cam4AtPos1 = False
            cam4AtPos2 = False
            cam4AtPos3 = False
            cam4AtPos4 = False
            cam4AtPos5 = False
            cam4AtPos6 = False
            cam4AtPos7 = False
            cam4AtPos8 = False
            cam4AtPos9 = False
            cam4AtPos10 = False
            self.doButtonColours()
        elif whichCamSerial == 5 and (cam5AtPos1 or cam5AtPos2 or cam5AtPos3 or cam5AtPos4 or cam5AtPos5 or cam5AtPos6 or cam5AtPos7 or cam5AtPos8 or cam5AtPos9 or cam5AtPos10):
            cam5AtPos1 = False
            cam5AtPos2 = False
            cam5AtPos3 = False
            cam5AtPos4 = False
            cam5AtPos5 = False
            cam5AtPos6 = False
            cam5AtPos7 = False
            cam5AtPos8 = False
            cam5AtPos9 = False
            cam5AtPos10 = False
            self.doButtonColours()


    def scale(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    def toHex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))


    def buttonConnect(self, device_list):
        global btn_scan_show
        global whichCamSerial
        global isConnected
        global message
        global device_name

        serialPortSelect = ""

        if not isConnected:
            device_name_list = device_list
            #print(device_name_list)

            usb_port = 'usbmodem'
            usb_port2 = 'usb/00'
            usb_port3 = 'COM8'
            usb_port4 = 'COM3'
            
            if (usb_port in '\t'.join(device_name_list)):
                serialPortSelect = [string for string in device_name_list if usb_port in string]
            elif (usb_port2 in '\t'.join(device_name_list)):
                serialPortSelect = [string for string in device_name_list if usb_port2 in string]
            elif (usb_port3 in '\t'.join(device_name_list)):
                serialPortSelect = [string for string in device_name_list if usb_port3 in string]
            elif (usb_port4 in '\t'.join(device_name_list)):
                serialPortSelect = [string for string in device_name_list if usb_port4 in string]
            else:
                message = ("No USB Serial Found")

            if serialPortSelect != "":
                message = ("Auto Connecting")
                device_name = serialPortSelect
                
                self.autoPortTimer = QTimer()
                self.autoPortTimer.singleShot(2000,self.autoSerial)

        #else:
        #    self.resetButtonColours()

    def autoSerial(self):
        global btn_scan_show
        global device_name
        global serialLoop

        if device_name == "":
            device_name = self.comboBox.currentText()
        else:
            device_name = device_name[0]
            self.comboBox.setCurrentText(device_name)
        
        #print(device_name)
        #print("Connecting")
        self.thread = ThreadClass(parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(self.readSerial)
        #self.pushButtonConnect.setEnabled(False)

    def stopping(self, dt):
        global whileLoopRun
        global device_name

        whileLoopRun = False
        if device_name is not None:
            Serial.close(device_name)

    def sendSerial(self, toSendData):
        global sendData
        sendData = toSendData

    def readSerial(self, msg):
        global debug
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1AtPos7
        global cam1AtPos8
        global cam1AtPos9
        global cam1AtPos10
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos7Set
        global cam1Pos8Set
        global cam1Pos9Set
        global cam1Pos10Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1Pos7Run
        global cam1Pos8Run
        global cam1Pos9Run
        global cam1Pos10Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2AtPos7
        global cam2AtPos8
        global cam2AtPos9
        global cam2AtPos10
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos7Set
        global cam2Pos8Set
        global cam2Pos9Set
        global cam2Pos10Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2Pos7Run
        global cam2Pos8Run
        global cam2Pos9Run
        global cam2Pos10Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3AtPos7
        global cam3AtPos8
        global cam3AtPos9
        global cam3AtPos10
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos7Set
        global cam3Pos8Set
        global cam3Pos9Set
        global cam3Pos10Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3Pos7Run
        global cam3Pos8Run
        global cam3Pos9Run
        global cam3Pos10Run
        global cam3isRecording
        global cam3isZooming

        global cam4AtPos1
        global cam4AtPos2
        global cam4AtPos3
        global cam4AtPos4
        global cam4AtPos5
        global cam4AtPos6
        global cam4AtPos7
        global cam4AtPos8
        global cam4AtPos9
        global cam4AtPos10
        global cam4Pos1Set
        global cam4Pos2Set
        global cam4Pos3Set
        global cam4Pos4Set
        global cam4Pos5Set
        global cam4Pos6Set
        global cam4Pos7Set
        global cam4Pos8Set
        global cam4Pos9Set
        global cam4Pos10Set
        global cam4Pos1Run
        global cam4Pos2Run
        global cam4Pos3Run
        global cam4Pos4Run
        global cam4Pos5Run
        global cam4Pos6Run
        global cam4Pos7Run
        global cam4Pos8Run
        global cam4Pos9Run
        global cam4Pos10Run
        global cam4isRecording
        global cam4isZooming

        global cam5AtPos1
        global cam5AtPos2
        global cam5AtPos3
        global cam5AtPos4
        global cam5AtPos5
        global cam5AtPos6
        global cam5AtPos7
        global cam5AtPos8
        global cam5AtPos9
        global cam5AtPos10
        global cam5Pos1Set
        global cam5Pos2Set
        global cam5Pos3Set
        global cam5Pos4Set
        global cam5Pos5Set
        global cam5Pos6Set
        global cam5Pos7Set
        global cam5Pos8Set
        global cam5Pos9Set
        global cam5Pos10Set
        global cam5Pos1Run
        global cam5Pos2Run
        global cam5Pos3Run
        global cam5Pos4Run
        global cam5Pos5Run
        global cam5Pos6Run
        global cam5Pos7Run
        global cam5Pos8Run
        global cam5Pos9Run
        global cam5Pos10Run
        global cam5isRecording
        global cam5isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global cam4SliderSpeed
        global cam5SliderSpeed
        global oldcam1Speed
        global oldcam2Speed
        global oldcam3Speed
        global oldcam4Speed
        global oldcam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldcam1PTSpeed
        global oldcam2PTSpeed
        global oldcam3PTSpeed
        global oldcam4PTSpeed
        global oldcam5PTSpeed

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        global Cam4TextColour
        global Cam5TextColour

        global cam1ptAccel
        global cam1slAccel
        global cam1ptSpeed1
        global cam1ptSpeed2
        global cam1ptSpeed3
        global cam1ptSpeed4
        global cam1slSpeed1
        global cam1slSpeed2
        global cam1slSpeed3
        global cam1slSpeed4
        global cam1ZoomLimit

        global cam2ptAccel
        global cam2slAccel
        global cam2ptSpeed1
        global cam2ptSpeed2
        global cam2ptSpeed3
        global cam2ptSpeed4
        global cam2slSpeed1
        global cam2slSpeed2
        global cam2slSpeed3
        global cam2slSpeed4
        global cam2ZoomLimit

        global cam3ptAccel
        global cam3slAccel
        global cam3ptSpeed1
        global cam3ptSpeed2
        global cam3ptSpeed3
        global cam3ptSpeed4
        global cam3slSpeed1
        global cam3slSpeed2
        global cam3slSpeed3
        global cam3slSpeed4
        global cam3ZoomLimit

        global cam4ptAccel
        global cam4slAccel
        global cam4ptSpeed1
        global cam4ptSpeed2
        global cam4ptSpeed3
        global cam4ptSpeed4
        global cam4slSpeed1
        global cam4slSpeed2
        global cam4slSpeed3
        global cam4slSpeed4
        global cam4ZoomLimit

        global cam5ptAccel
        global cam5slAccel
        global cam5ptSpeed1
        global cam5ptSpeed2
        global cam5ptSpeed3
        global cam5ptSpeed4
        global cam5slSpeed1
        global cam5slSpeed2
        global cam5slSpeed3
        global cam5slSpeed4
        global cam5ZoomLimit

        global cam1AF
        global cam2AF
        global cam3AF
        global cam4AF
        global cam5AF

        global whichCamRead

        if debug:
            print(msg)

        #textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
        #if textLength > 8000:
            #self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]

        if msg == '':
            return
        if msg[0] == "":
            msg = ''
            return
        elif msg[0] == "?":
            msg = ''
            return
        elif msg[0] == "~":
            if len(msg) == 1:
                msg = ''
                return
            elif msg[1] == "0":
                msg = ''
                return
            elif msg[1:4] == "111":              # Cam 1 Set Pos 1
                cam1Pos1Set = True
            elif msg[1:4] == "121":
                cam1Pos2Set = True
            elif msg[1:4] == "131":
                cam1Pos3Set = True
            elif msg[1:4] == "141":
                cam1Pos4Set = True
            elif msg[1:4] == "151":
                cam1Pos5Set = True
            elif msg[1:4] == "161":
                cam1Pos6Set = True
            elif msg[1:4] == "171":
                cam1Pos7Set = True
            elif msg[1:4] == "181":
                cam1Pos8Set = True
            elif msg[1:4] == "191":
                cam1Pos9Set = True
            elif msg[1:4] == "101":
                cam1Pos10Set = True
            elif msg[1:4] == "112":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos1Run = True
            elif msg[1:4] == "122":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos2Run = True
            elif msg[1:4] == "132":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos3Run = True
            elif msg[1:4] == "142":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos4Run = True
            elif msg[1:4] == "152":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos5Run = True
            elif msg[1:4] == "162":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos6Run = True
            elif msg[1:4] == "172":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos7Run = True
            elif msg[1:4] == "182":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos8Run = True
            elif msg[1:4] == "192":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos9Run = True
            elif msg[1:4] == "102":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
                cam1Pos10Run = True
            elif msg[1:4] == "113":
                cam1Pos1Run = False
                cam1AtPos1 = True
            elif msg[1:4] == "123":
                cam1Pos2Run = False
                cam1AtPos2 = True
            elif msg[1:4] == "133":
                cam1Pos3Run = False
                cam1AtPos3 = True
            elif msg[1:4] == "143":
                cam1Pos4Run = False
                cam1AtPos4 = True
            elif msg[1:4] == "153":
                cam1Pos5Run = False
                cam1AtPos5 = True
            elif msg[1:4] == "163":
                cam1Pos6Run = False
                cam1AtPos6 = True
            elif msg[1:4] == "173":
                cam1Pos7Run = False
                cam1AtPos7 = True
            elif msg[1:4] == "183":
                cam1Pos8Run = False
                cam1AtPos8 = True
            elif msg[1:4] == "193":
                cam1Pos9Run = False
                cam1AtPos9 = True
            elif msg[1:4] == "103":
                cam1Pos10Run = False
                cam1AtPos10 = True
            elif msg[1:4] == "114":
                cam1isRecording = False
                #self.root.get_screen('main').ids.cam1Record.background_color = get_color_from_hex("#666666")
                #self.root.get_screen('main').ids.cam1Record.text = "Record"
                #client.send_message("/style/bgcolor/4/16", [50, 50, 50])
            elif msg[1:4] == "124":
                cam1isRecording = True
                #self.root.get_screen('main').ids.cam1Record.background_color = get_color_from_hex("#7D0000")
                #self.root.get_screen('main').ids.cam1Record.text = "Recording"
                #client.send_message("/style/bgcolor/4/16", [225, 0, 0])
            elif msg[1:4] == "115":
                cam1AF = True
            elif msg[1:4] == "105":
                cam1AF = False
            elif msg[1:4] == "100":
                cam1Pos1Run = False
                cam1Pos1Set = False
                cam1AtPos1 = False
                cam1Pos2Run = False
                cam1Pos2Set = False
                cam1AtPos2 = False
                cam1Pos3Run = False
                cam1Pos3Set = False
                cam1AtPos3 = False
                cam1Pos4Run = False
                cam1Pos4Set = False
                cam1AtPos4 = False
                cam1Pos5Run = False
                cam1Pos5Set = False
                cam1AtPos5 = False
                cam1Pos6Run = False
                cam1Pos6Set = False
                cam1AtPos6 = False
                cam1Pos7Run = False
                cam1Pos7Set = False
                cam1AtPos7 = False
                cam1Pos8Run = False
                cam1Pos8Set = False
                cam1AtPos8 = False
                cam1Pos9Run = False
                cam1Pos9Set = False
                cam1AtPos9 = False
                cam1Pos10Run = False
                cam1Pos10Set = False
                cam1AtPos10 = False
            elif msg[1:4] == "211":              # Cam 2 Set Pos 1
                cam2Pos1Set = True
            elif msg[1:4] == "221":
                cam2Pos2Set = True
            elif msg[1:4] == "231":
                cam2Pos3Set = True
            elif msg[1:4] == "241":
                cam2Pos4Set = True
            elif msg[1:4] == "251":
                cam2Pos5Set = True
            elif msg[1:4] == "261":
                cam2Pos6Set = True
            elif msg[1:4] == "271":
                cam2Pos7Set = True
            elif msg[1:4] == "281":
                cam2Pos8Set = True
            elif msg[1:4] == "291":
                cam2Pos9Set = True
            elif msg[1:4] == "201":
                cam2Pos10Set = True
            elif msg[1:4] == "212":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos1Run = True
            elif msg[1:4] == "222":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos2Run = True
            elif msg[1:4] == "232":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos3Run = True
            elif msg[1:4] == "242":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos4Run = True
            elif msg[1:4] == "252":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos5Run = True
            elif msg[1:4] == "262":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos6Run = True
            elif msg[1:4] == "272":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos7Run = True
            elif msg[1:4] == "282":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos8Run = True
            elif msg[1:4] == "292":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos9Run = True
            elif msg[1:4] == "202":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
                cam2Pos10Run = True
            elif msg[1:4] == "213":
                cam2Pos1Run = False
                cam2AtPos1 = True
            elif msg[1:4] == "223":
                cam2Pos2Run = False
                cam2AtPos2 = True
            elif msg[1:4] == "233":
                cam2Pos3Run = False
                cam2AtPos3 = True
            elif msg[1:4] == "243":
                cam2Pos4Run = False
                cam2AtPos4 = True
            elif msg[1:4] == "253":
                cam2Pos5Run = False
                cam2AtPos5 = True
            elif msg[1:4] == "263":
                cam2Pos6Run = False
                cam2AtPos6 = True
            elif msg[1:4] == "273":
                cam2Pos7Run = False
                cam2AtPos7 = True
            elif msg[1:4] == "283":
                cam2Pos8Run = False
                cam2AtPos8 = True
            elif msg[1:4] == "293":
                cam2Pos9Run = False
                cam2AtPos9 = True
            elif msg[1:4] == "203":
                cam2Pos10Run = False
                cam2AtPos10 = True
            elif msg[1:4] == "214":
                cam2isRecording = False
                #self.root.get_screen('main').ids.cam2Record.background_color = get_color_from_hex("#666666")
                #self.root.get_screen('main').ids.cam2Record.text = "Record"
                #client.send_message("/style/bgcolor/5/16", [50, 50, 50])
            elif msg[1:4] == "224":
                cam2isRecording = True
                #self.root.get_screen('main').ids.cam2Record.background_color = get_color_from_hex("#7D0000")
                #self.root.get_screen('main').ids.cam2Record.text = "Recording"
                #client.send_message("/style/bgcolor/5/16", [225, 0, 0])
            elif msg[1:4] == "215":
                cam2AF = True
            elif msg[1:4] == "205":
                cam2AF = False
            elif msg[1:4] == "200":
                cam2Pos1Run = False
                cam2Pos1Set = False
                cam2AtPos1 = False
                cam2Pos2Run = False
                cam2Pos2Set = False
                cam2AtPos2 = False
                cam2Pos3Run = False
                cam2Pos3Set = False
                cam2AtPos3 = False
                cam2Pos4Run = False
                cam2Pos4Set = False
                cam2AtPos4 = False
                cam2Pos5Run = False
                cam2Pos5Set = False
                cam2AtPos5 = False
                cam2Pos6Run = False
                cam2Pos6Set = False
                cam2AtPos6 = False
                cam2Pos7Run = False
                cam2Pos7Set = False
                cam2AtPos7 = False
                cam2Pos8Run = False
                cam2Pos8Set = False
                cam2AtPos8 = False
                cam2Pos9Run = False
                cam2Pos9Set = False
                cam2AtPos9 = False
                cam2Pos10Run = False
                cam2Pos10Set = False
                cam2AtPos10 = False
            elif msg[1:4] == "311":              # Cam 3 Set Pos 1
                cam3Pos1Set = True
            elif msg[1:4] == "321":
                cam3Pos2Set = True
            elif msg[1:4] == "331":
                cam3Pos3Set = True
            elif msg[1:4] == "341":
                cam3Pos4Set = True
            elif msg[1:4] == "351":
                cam3Pos5Set = True
            elif msg[1:4] == "361":
                cam3Pos6Set = True
            elif msg[1:4] == "371":
                cam3Pos7Set = True
            elif msg[1:4] == "381":
                cam3Pos8Set = True
            elif msg[1:4] == "391":
                cam3Pos9Set = True
            elif msg[1:4] == "301":
                cam3Pos10Set = True
            elif msg[1:4] == "312":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos1Run = True
            elif msg[1:4] == "322":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos2Run = True
            elif msg[1:4] == "332":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos3Run = True
            elif msg[1:4] == "342":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos4Run = True
            elif msg[1:4] == "352":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos5Run = True
            elif msg[1:4] == "362":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos6Run = True
            elif msg[1:4] == "372":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos7Run = True
            elif msg[1:4] == "382":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos8Run = True
            elif msg[1:4] == "392":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos9Run = True
            elif msg[1:4] == "302":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
                cam3Pos10Run = True
            elif msg[1:4] == "313":
                cam3Pos1Run = False
                cam3AtPos1 = True
            elif msg[1:4] == "323":
                cam3Pos2Run = False
                cam3AtPos2 = True
            elif msg[1:4] == "333":
                cam3Pos3Run = False
                cam3AtPos3 = True
            elif msg[1:4] == "343":
                cam3Pos4Run = False
                cam3AtPos4 = True
            elif msg[1:4] == "353":
                cam3Pos5Run = False
                cam3AtPos5 = True
            elif msg[1:4] == "363":
                cam3Pos6Run = False
                cam3AtPos6 = True
            elif msg[1:4] == "373":
                cam3Pos7Run = False
                cam3AtPos7 = True
            elif msg[1:4] == "383":
                cam3Pos8Run = False
                cam3AtPos8 = True
            elif msg[1:4] == "393":
                cam3Pos9Run = False
                cam3AtPos9 = True
            elif msg[1:4] == "303":
                cam3Pos10Run = False
                cam3AtPos10 = True
            elif msg[1:4] == "314":
                cam3isRecording = False
                #self.root.get_screen('main').ids.cam3Record.background_color = get_color_from_hex("#666666")
                #self.root.get_screen('main').ids.cam3Record.text = "Record"
                #client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "324":
                cam3isRecording = True
                #self.root.get_screen('main').ids.cam3Record.background_color = get_color_from_hex("#7D0000")
                #self.root.get_screen('main').ids.cam3Record.text = "Recording"
                #client.send_message("/style/bgcolor/6/16", [225, 0, 0])
            elif msg[1:4] == "315":
                cam3AF = True
            elif msg[1:4] == "305":
                cam3AF = False
            elif msg[1:4] == "300":
                cam3Pos1Run = False
                cam3Pos1Set = False
                cam3AtPos1 = False
                cam3Pos2Run = False
                cam3Pos2Set = False
                cam3AtPos2 = False
                cam3Pos3Run = False
                cam3Pos3Set = False
                cam3AtPos3 = False
                cam3Pos4Run = False
                cam3Pos4Set = False
                cam3AtPos4 = False
                cam3Pos5Run = False
                cam3Pos5Set = False
                cam3AtPos5 = False
                cam3Pos6Run = False
                cam3Pos6Set = False
                cam3AtPos6 = False
                cam3Pos7Run = False
                cam3Pos7Set = False
                cam3AtPos7 = False
                cam3Pos8Run = False
                cam3Pos8Set = False
                cam3AtPos8 = False
                cam3Pos9Run = False
                cam3Pos9Set = False
                cam3AtPos9 = False
                cam3Pos10Run = False
                cam3Pos10Set = False
                cam3AtPos10 = False
            elif msg[1:4] == "411":              # Cam 4 Set Pos 1
                cam4Pos1Set = True
            elif msg[1:4] == "421":
                cam4Pos2Set = True
            elif msg[1:4] == "431":
                cam4Pos3Set = True
            elif msg[1:4] == "441":
                cam4Pos4Set = True
            elif msg[1:4] == "451":
                cam4Pos5Set = True
            elif msg[1:4] == "461":
                cam4Pos6Set = True
            elif msg[1:4] == "471":
                cam4Pos7Set = True
            elif msg[1:4] == "481":
                cam4Pos8Set = True
            elif msg[1:4] == "491":
                cam4Pos9Set = True
            elif msg[1:4] == "401":
                cam4Pos10Set = True
            elif msg[1:4] == "412":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos1Run = True
            elif msg[1:4] == "422":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos2Run = True
            elif msg[1:4] == "432":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos3Run = True
            elif msg[1:4] == "442":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos4Run = True
            elif msg[1:4] == "452":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos5Run = True
            elif msg[1:4] == "462":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos6Run = True
            elif msg[1:4] == "472":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos7Run = True
            elif msg[1:4] == "482":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos8Run = True
            elif msg[1:4] == "492":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos9Run = True
            elif msg[1:4] == "402":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
                cam4Pos10Run = True
            elif msg[1:4] == "413":
                cam4Pos1Run = False
                cam4AtPos1 = True
            elif msg[1:4] == "423":
                cam4Pos2Run = False
                cam4AtPos2 = True
            elif msg[1:4] == "433":
                cam4Pos3Run = False
                cam4AtPos3 = True
            elif msg[1:4] == "443":
                cam4Pos4Run = False
                cam4AtPos4 = True
            elif msg[1:4] == "453":
                cam4Pos5Run = False
                cam4AtPos5 = True
            elif msg[1:4] == "463":
                cam4Pos6Run = False
                cam4AtPos6 = True
            elif msg[1:4] == "473":
                cam4Pos7Run = False
                cam4AtPos7 = True
            elif msg[1:4] == "483":
                cam4Pos8Run = False
                cam4AtPos8 = True
            elif msg[1:4] == "493":
                cam4Pos9Run = False
                cam4AtPos9 = True
            elif msg[1:4] == "403":
                cam4Pos10Run = False
                cam4AtPos10 = True
            elif msg[1:4] == "414":
                cam4isRecording = False
                #self.root.get_screen('main').ids.cam4Record.background_color = get_color_from_hex("#666666")
                #self.root.get_screen('main').ids.cam4Record.text = "Record"
                #client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "424":
                cam4isRecording = True
                #self.root.get_screen('main').ids.cam4Record.background_color = get_color_from_hex("#7D0000")
                #self.root.get_screen('main').ids.cam4Record.text = "Recording"
                #client.send_message("/style/bgcolor/6/16", [225, 0, 0])
            elif msg[1:4] == "415":
                cam4AF = True
            elif msg[1:4] == "405":
                cam4AF = False
            elif msg[1:4] == "400":
                cam4Pos1Run = False
                cam4Pos1Set = False
                cam4AtPos1 = False
                cam4Pos2Run = False
                cam4Pos2Set = False
                cam4AtPos2 = False
                cam4Pos3Run = False
                cam4Pos3Set = False
                cam4AtPos3 = False
                cam4Pos4Run = False
                cam4Pos4Set = False
                cam4AtPos4 = False
                cam4Pos5Run = False
                cam4Pos5Set = False
                cam4AtPos5 = False
                cam4Pos6Run = False
                cam4Pos6Set = False
                cam4AtPos6 = False
                cam4Pos7Run = False
                cam4Pos7Set = False
                cam4AtPos7 = False
                cam4Pos8Run = False
                cam4Pos8Set = False
                cam4AtPos8 = False
                cam4Pos9Run = False
                cam4Pos9Set = False
                cam4AtPos9 = False
                cam4Pos10Run = False
                cam4Pos10Set = False
                cam4AtPos10 = False
            elif msg[1:4] == "511":              # Cam 5 Set Pos 1
                cam5Pos1Set = True
            elif msg[1:4] == "521":
                cam5Pos2Set = True
            elif msg[1:4] == "531":
                cam5Pos3Set = True
            elif msg[1:4] == "541":
                cam5Pos4Set = True
            elif msg[1:4] == "551":
                cam5Pos5Set = True
            elif msg[1:4] == "561":
                cam5Pos6Set = True
            elif msg[1:4] == "571":
                cam5Pos7Set = True
            elif msg[1:4] == "581":
                cam5Pos8Set = True
            elif msg[1:4] == "591":
                cam5Pos9Set = True
            elif msg[1:4] == "501":
                cam5Pos10Set = True
            elif msg[1:4] == "512":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos1Run = True
            elif msg[1:4] == "522":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos2Run = True
            elif msg[1:4] == "532":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos3Run = True
            elif msg[1:4] == "542":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos4Run = True
            elif msg[1:4] == "552":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos5Run = True
            elif msg[1:4] == "562":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos6Run = True
            elif msg[1:4] == "572":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos7Run = True
            elif msg[1:4] == "582":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos8Run = True
            elif msg[1:4] == "592":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos9Run = True
            elif msg[1:4] == "502":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
                cam5Pos10Run = True
            elif msg[1:4] == "513":
                cam5Pos1Run = False
                cam5AtPos1 = True
            elif msg[1:4] == "523":
                cam5Pos2Run = False
                cam5AtPos2 = True
            elif msg[1:4] == "533":
                cam5Pos3Run = False
                cam5AtPos3 = True
            elif msg[1:4] == "543":
                cam5Pos4Run = False
                cam5AtPos4 = True
            elif msg[1:4] == "553":
                cam5Pos5Run = False
                cam5AtPos5 = True
            elif msg[1:4] == "563":
                cam5Pos6Run = False
                cam5AtPos6 = True
            elif msg[1:4] == "573":
                cam5Pos7Run = False
                cam5AtPos7 = True
            elif msg[1:4] == "583":
                cam5Pos8Run = False
                cam5AtPos8 = True
            elif msg[1:4] == "593":
                cam5Pos9Run = False
                cam5AtPos9 = True
            elif msg[1:4] == "503":
                cam5Pos10Run = False
                cam5AtPos10 = True
            elif msg[1:4] == "514":
                cam5isRecording = False
                #self.root.get_screen('main').ids.cam5Record.background_color = get_color_from_hex("#666666")
                #self.root.get_screen('main').ids.cam5Record.text = "Record"
                #client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "524":
                cam5isRecording = True
                #self.root.get_screen('main').ids.cam5Record.background_color = get_color_from_hex("#7D0000")
                #self.root.get_screen('main').ids.cam5Record.text = "Recording"
                #client.send_message("/style/bgcolor/6/16", [225, 0, 0])
            elif msg[1:4] == "515":
                cam5AF = True
            elif msg[1:4] == "505":
                cam5AF = False
            elif msg[1:4] == "500":
                cam5Pos1Run = False
                cam5Pos1Set = False
                cam5AtPos1 = False
                cam5Pos2Run = False
                cam5Pos2Set = False
                cam5AtPos2 = False
                cam5Pos3Run = False
                cam5Pos3Set = False
                cam5AtPos3 = False
                cam5Pos4Run = False
                cam5Pos4Set = False
                cam5AtPos4 = False
                cam5Pos5Run = False
                cam5Pos5Set = False
                cam5AtPos5 = False
                cam5Pos6Run = False
                cam5Pos6Set = False
                cam5AtPos6 = False
                cam5Pos7Run = False
                cam5Pos7Set = False
                cam5AtPos7 = False
                cam5Pos8Run = False
                cam5Pos8Set = False
                cam5AtPos8 = False
                cam5Pos9Run = False
                cam5Pos9Set = False
                cam5AtPos9 = False
                cam5Pos10Run = False
                cam5Pos10Set = False
                cam5AtPos10 = False
            elif msg[1] == "?":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1AtPos7 = False
                cam1AtPos8 = False
                cam1AtPos9 = False
                cam1AtPos10 = False
            elif msg[1] == "!":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2AtPos7 = False
                cam2AtPos8 = False
                cam2AtPos9 = False
                cam2AtPos10 = False
            elif msg[1] == "@":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3AtPos7 = False
                cam3AtPos8 = False
                cam3AtPos9 = False
                cam3AtPos10 = False
            elif msg[1] == "&":
                cam4AtPos1 = False
                cam4AtPos2 = False
                cam4AtPos3 = False
                cam4AtPos4 = False
                cam4AtPos5 = False
                cam4AtPos6 = False
                cam4AtPos7 = False
                cam4AtPos8 = False
                cam4AtPos9 = False
                cam4AtPos10 = False
            elif msg[1] == "*":
                cam5AtPos1 = False
                cam5AtPos2 = False
                cam5AtPos3 = False
                cam5AtPos4 = False
                cam5AtPos5 = False
                cam5AtPos6 = False
                cam5AtPos7 = False
                cam5AtPos8 = False
                cam5AtPos9 = False
                cam5AtPos10 = False
        elif msg[0:2] == "=1":
            cam1SliderSpeed = int(msg[2])
        elif msg[0:2] == "=2":
            cam2SliderSpeed = int(msg[2])
        elif msg[0:2] == "=3":
            cam3SliderSpeed = int(msg[2])
        elif msg[0:2] == "=4":
            cam4SliderSpeed = int(msg[2])
        elif msg[0:2] == "=5":
            cam5SliderSpeed = int(msg[2])
        elif msg[0:3] == "=@1":
            cam1PTSpeed = int(msg[3])
        elif msg[0:3] == "=@2":
            cam2PTSpeed = int(msg[3])
        elif msg[0:3] == "=@3":
            cam3PTSpeed = int(msg[3])
        elif msg[0:3] == "=@4":
            cam4PTSpeed = int(msg[3])
        elif msg[0:3] == "=@5":
            cam5PTSpeed = int(msg[3])

        elif msg[0:3] == "=a0":
            cam1ptAccel = int(msg[3:])
        elif msg[0:3] == "=a1":
            cam1ptSpeed1 = int(msg[3:])
        elif msg[0:3] == "=a2":
            cam1ptSpeed2 = int(msg[3:])
        elif msg[0:3] == "=a3":
            cam1ptSpeed3 = int(msg[3:])
        elif msg[0:3] == "=a4":
            cam1ptSpeed4 = int(msg[3:])
        elif msg[0:3] == "=A0":
            cam1slAccel = int(msg[3:])
        elif msg[0:3] == "=A1":
            cam1slSpeed1 = int(msg[3:])
        elif msg[0:3] == "=A2":
            cam1slSpeed2 = int(msg[3:])
        elif msg[0:3] == "=A3":
            cam1slSpeed3 = int(msg[3:])
        elif msg[0:3] == "=A4":
            cam1slSpeed4 = int(msg[3:])
        elif msg[0:3] == "=A5":
            cam1ZoomLimit = int(msg[3:])

        elif msg[0:3] == "=s0":
            cam2ptAccel = int(msg[3:])
        elif msg[0:3] == "=s1":
            cam2ptSpeed1 = int(msg[3:])
        elif msg[0:3] == "=s2":
            cam2ptSpeed2 = int(msg[3:])
        elif msg[0:3] == "=s3":
            cam2ptSpeed3 = int(msg[3:])
        elif msg[0:3] == "=s4":
            cam2ptSpeed4 = int(msg[3:])
        elif msg[0:3] == "=S0":
            cam2slAccel = int(msg[3:])
        elif msg[0:3] == "=S1":
            cam2slSpeed1 = int(msg[3:])
        elif msg[0:3] == "=S2":
            cam2slSpeed2 = int(msg[3:])
        elif msg[0:3] == "=S3":
            cam2slSpeed3 = int(msg[3:])
        elif msg[0:3] == "=S4":
            cam2slSpeed4 = int(msg[3:])
        elif msg[0:3] == "=S5":
            cam2ZoomLimit = int(msg[3:])

        elif msg[0:3] == "=d0":
            cam3ptAccel = int(msg[3:])
        elif msg[0:3] == "=d1":
            cam3ptSpeed1 = int(msg[3:])
        elif msg[0:3] == "=d2":
            cam3ptSpeed2 = int(msg[3:])
        elif msg[0:3] == "=d3":
            cam3ptSpeed3 = int(msg[3:])
        elif msg[0:3] == "=d4":
            cam3ptSpeed4 = int(msg[3:])
        elif msg[0:3] == "=D0":
            cam3slAccel = int(msg[3:])
        elif msg[0:3] == "=D1":
            cam3slSpeed1 = int(msg[3:])
        elif msg[0:3] == "=D2":
            cam3slSpeed2 = int(msg[3:])
        elif msg[0:3] == "=D3":
            cam3slSpeed3 = int(msg[3:])
        elif msg[0:3] == "=D4":
            cam3slSpeed4 = int(msg[3:])
        elif msg[0:3] == "=D5":
            cam3ZoomLimit = int(msg[3:])

        elif msg[0:3] == "=f0":
            cam4ptAccel = int(msg[3:])
        elif msg[0:3] == "=f1":
            cam4ptSpeed1 = int(msg[3:])
        elif msg[0:3] == "=f2":
            cam4ptSpeed2 = int(msg[3:])
        elif msg[0:3] == "=f3":
            cam4ptSpeed3 = int(msg[3:])
        elif msg[0:3] == "=f4":
            cam4ptSpeed4 = int(msg[3:])
        elif msg[0:3] == "=F0":
            cam4slAccel = int(msg[3:])
        elif msg[0:3] == "=F1":
            cam4slSpeed1 = int(msg[3:])
        elif msg[0:3] == "=F2":
            cam4slSpeed2 = int(msg[3:])
        elif msg[0:3] == "=F3":
            cam4slSpeed3 = int(msg[3:])
        elif msg[0:3] == "=F4":
            cam4slSpeed4 = int(msg[3:])
        elif msg[0:3] == "=F5":
            cam4ZoomLimit = int(msg[3:])

        elif msg[0:3] == "=g0":
            cam5ptAccel = int(msg[3:])
        elif msg[0:3] == "=g1":
            cam5ptSpeed1 = int(msg[3:])
        elif msg[0:3] == "=g2":
            cam5ptSpeed2 = int(msg[3:])
        elif msg[0:3] == "=g3":
            cam5ptSpeed3 = int(msg[3:])
        elif msg[0:3] == "=g4":
            cam5ptSpeed4 = int(msg[3:])
        elif msg[0:3] == "=G0":
            cam5slAccel = int(msg[3:])
        elif msg[0:3] == "=G1":
            cam5slSpeed1 = int(msg[3:])
        elif msg[0:3] == "=G2":
            cam5slSpeed2 = int(msg[3:])
        elif msg[0:3] == "=G3":
            cam5slSpeed3 = int(msg[3:])
        elif msg[0:3] == "=G4":
            cam5slSpeed4 = int(msg[3:])
        elif msg[0:3] == "=G5":
            cam5ZoomLimit = int(msg[3:])

        elif msg[0:2] == "#$":
            return
        elif msg[0:4] == "Cam1":
            whichCamRead = 1
            #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
            #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam2":
            whichCamRead = 2
            #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
            #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam3":
            whichCamRead = 3
            #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
            #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam4":
            whichCamRead = 4
            #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam4TextColour + "]" + msg + "[/color]")
            #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam5":
            whichCamRead = 5
            #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam5TextColour + "]" + msg + "[/color]")
            #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        else:
            if whichCamRead == 1:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
            elif whichCamRead == 2:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
            elif whichCamRead == 3:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
            elif whichCamRead == 4:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam4TextColour + "]" + msg + "[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
            elif whichCamRead == 5:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam5TextColour + "]" + msg + "[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
            else:
                #self.root.get_screen('main').ids.txtInput_read.text += ("[color=ffffff]") + msg + ("[/color]")
                #self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                pass
        msg = ''

        self.doButtonColours()

    def flash(self):
        global whichCamSerial
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1Pos7Run
        global cam1Pos8Run
        global cam1Pos9Run
        global cam1Pos10Run
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2Pos7Run
        global cam2Pos8Run
        global cam2Pos9Run
        global cam2Pos10Run
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3Pos7Run
        global cam3Pos8Run
        global cam3Pos9Run
        global cam3Pos10Run
        global cam4Pos1Run
        global cam4Pos2Run
        global cam4Pos3Run
        global cam4Pos4Run
        global cam4Pos5Run
        global cam4Pos6Run
        global cam4Pos7Run
        global cam4Pos8Run
        global cam4Pos9Run
        global cam4Pos10Run
        global cam5Pos1Run
        global cam5Pos2Run
        global cam5Pos3Run
        global cam5Pos4Run
        global cam5Pos5Run
        global cam5Pos6Run
        global cam5Pos7Run
        global cam5Pos8Run
        global cam5Pos9Run
        global cam5Pos10Run
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1AtPos7
        global cam1AtPos8
        global cam1AtPos9
        global cam1AtPos10
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2AtPos7
        global cam2AtPos8
        global cam2AtPos9
        global cam2AtPos10
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3AtPos7
        global cam3AtPos8
        global cam3AtPos9
        global cam3AtPos10
        global cam4AtPos1
        global cam4AtPos2
        global cam4AtPos3
        global cam4AtPos4
        global cam4AtPos5
        global cam4AtPos6
        global cam4AtPos7
        global cam4AtPos8
        global cam4AtPos9
        global cam4AtPos10
        global cam5AtPos1
        global cam5AtPos2
        global cam5AtPos3
        global cam5AtPos4
        global cam5AtPos5
        global cam5AtPos6
        global cam5AtPos7
        global cam5AtPos8
        global cam5AtPos9
        global cam5AtPos10

        global flashTick

        if flashTick:
            flashTick = False
            buttonColourFlash = "#ffff00"
        else:
            flashTick = True
            buttonColourFlash = "#000000"

        if cam1Pos1Run and not cam1AtPos1:
            self.pushButton11.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos2Run and not cam1AtPos2:
            self.pushButton12.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos3Run and not cam1AtPos3:
            self.pushButton13.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos4Run and not cam1AtPos4:
            self.pushButton14.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos5Run and not cam1AtPos5:
            self.pushButton15.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos6Run and not cam1AtPos6:
            self.pushButton16.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos7Run and not cam1AtPos7:
            self.pushButton17.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos8Run and not cam1AtPos8:
            self.pushButton18.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos9Run and not cam1AtPos9:
            self.pushButton19.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')
        if cam1Pos10Run and not cam1AtPos10:
            self.pushButton10.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: 40px;')

        
        if cam2Pos1Run and not cam2AtPos1:
            self.pushButton21.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos2Run and not cam2AtPos2:
            self.pushButton22.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos3Run and not cam2AtPos3:
            self.pushButton23.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos4Run and not cam2AtPos4:
            self.pushButton24.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos5Run and not cam2AtPos5:
            self.pushButton25.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos6Run and not cam2AtPos6:
            self.pushButton26.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos7Run and not cam2AtPos7:
            self.pushButton27.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos8Run and not cam2AtPos8:
            self.pushButton28.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos9Run and not cam2AtPos9:
            self.pushButton29.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')
        if cam2Pos10Run and not cam2AtPos10:
            self.pushButton20.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #405C80; border-radius: 40px;')

        
        if cam3Pos1Run and not cam3AtPos1:
            self.pushButton31.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos2Run and not cam3AtPos2:
            self.pushButton32.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos3Run and not cam3AtPos3:
            self.pushButton33.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos4Run and not cam3AtPos4:
            self.pushButton34.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos5Run and not cam3AtPos5:
            self.pushButton35.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos6Run and not cam3AtPos6:
            self.pushButton36.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos7Run and not cam3AtPos7:
            self.pushButton37.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos8Run and not cam3AtPos8:
            self.pushButton38.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos9Run and not cam3AtPos9:
            self.pushButton39.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')
        if cam3Pos10Run and not cam3AtPos10:
            self.pushButton30.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #807100; border-radius: 40px;')

        
        if cam4Pos1Run and not cam4AtPos1:
            self.pushButton41.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos2Run and not cam4AtPos2:
            self.pushButton42.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos3Run and not cam4AtPos3:
            self.pushButton43.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos4Run and not cam4AtPos4:
            self.pushButton44.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos5Run and not cam4AtPos5:
            self.pushButton45.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos6Run and not cam4AtPos6:
            self.pushButton46.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos7Run and not cam4AtPos7:
            self.pushButton47.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos8Run and not cam4AtPos8:
            self.pushButton48.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos9Run and not cam4AtPos9:
            self.pushButton49.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')
        if cam4Pos10Run and not cam4AtPos10:
            self.pushButton40.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #008071; border-radius: 40px;')

        
        if cam5Pos1Run and not cam5AtPos1:
            self.pushButton51.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos2Run and not cam5AtPos2:
            self.pushButton52.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos3Run and not cam5AtPos3:
            self.pushButton53.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos4Run and not cam5AtPos4:
            self.pushButton54.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos5Run and not cam5AtPos5:
            self.pushButton55.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos6Run and not cam5AtPos6:
            self.pushButton56.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos7Run and not cam5AtPos7:
            self.pushButton57.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos8Run and not cam5AtPos8:
            self.pushButton58.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos9Run and not cam5AtPos9:
            self.pushButton59.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')
        if cam5Pos10Run and not cam5AtPos10:
            self.pushButton50.setStyleSheet(f'border: 10px solid {buttonColourFlash}; background-color: #8D5395; border-radius: 40px;')

        

    def doButtonColours(self):
        #print("Button Colours")
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1AtPos7
        global cam1AtPos8
        global cam1AtPos9
        global cam1AtPos10
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos7Set
        global cam1Pos8Set
        global cam1Pos9Set
        global cam1Pos10Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1Pos7Run
        global cam1Pos8Run
        global cam1Pos9Run
        global cam1Pos10Run
        global OLDcam1AtPos1
        global OLDcam1AtPos2
        global OLDcam1AtPos3
        global OLDcam1AtPos4
        global OLDcam1AtPos5
        global OLDcam1AtPos6
        global OLDcam1AtPos7
        global OLDcam1AtPos8
        global OLDcam1AtPos9
        global OLDcam1AtPos10
        global OLDcam1Pos1Set
        global OLDcam1Pos2Set
        global OLDcam1Pos3Set
        global OLDcam1Pos4Set
        global OLDcam1Pos5Set
        global OLDcam1Pos6Set
        global OLDcam1Pos7Set
        global OLDcam1Pos8Set
        global OLDcam1Pos9Set
        global OLDcam1Pos10Set
        global OLDcam1Pos1Run
        global OLDcam1Pos2Run
        global OLDcam1Pos3Run
        global OLDcam1Pos4Run
        global OLDcam1Pos5Run
        global OLDcam1Pos6Run
        global OLDcam1Pos7Run
        global OLDcam1Pos8Run
        global OLDcam1Pos9Run
        global OLDcam1Pos10Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2AtPos7
        global cam2AtPos8
        global cam2AtPos9
        global cam2AtPos10
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos7Set
        global cam2Pos8Set
        global cam2Pos9Set
        global cam2Pos10Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2Pos7Run
        global cam2Pos8Run
        global cam2Pos9Run
        global cam2Pos10Run
        global OLDcam2AtPos1
        global OLDcam2AtPos2
        global OLDcam2AtPos3
        global OLDcam2AtPos4
        global OLDcam2AtPos5
        global OLDcam2AtPos6
        global OLDcam2AtPos7
        global OLDcam2AtPos8
        global OLDcam2AtPos9
        global OLDcam2AtPos10
        global OLDcam2Pos1Set
        global OLDcam2Pos2Set
        global OLDcam2Pos3Set
        global OLDcam2Pos4Set
        global OLDcam2Pos5Set
        global OLDcam2Pos6Set
        global OLDcam2Pos7Set
        global OLDcam2Pos8Set
        global OLDcam2Pos9Set
        global OLDcam2Pos10Set
        global OLDcam2Pos1Run
        global OLDcam2Pos2Run
        global OLDcam2Pos3Run
        global OLDcam2Pos4Run
        global OLDcam2Pos5Run
        global OLDcam2Pos6Run
        global OLDcam2Pos7Run
        global OLDcam2Pos8Run
        global OLDcam2Pos9Run
        global OLDcam2Pos10Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3AtPos7
        global cam3AtPos8
        global cam3AtPos9
        global cam3AtPos10
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos7Set
        global cam3Pos8Set
        global cam3Pos9Set
        global cam3Pos10Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3Pos7Run
        global cam3Pos8Run
        global cam3Pos9Run
        global cam3Pos10Run

        global OLDcam3AtPos1
        global OLDcam3AtPos2
        global OLDcam3AtPos3
        global OLDcam3AtPos4
        global OLDcam3AtPos5
        global OLDcam3AtPos6
        global OLDcam3AtPos7
        global OLDcam3AtPos8
        global OLDcam3AtPos9
        global OLDcam3AtPos10
        global OLDcam3Pos1Set
        global OLDcam3Pos2Set
        global OLDcam3Pos3Set
        global OLDcam3Pos4Set
        global OLDcam3Pos5Set
        global OLDcam3Pos6Set
        global OLDcam3Pos7Set
        global OLDcam3Pos8Set
        global OLDcam3Pos9Set
        global OLDcam3Pos10Set
        global OLDcam3Pos1Run
        global OLDcam3Pos2Run
        global OLDcam3Pos3Run
        global OLDcam3Pos4Run
        global OLDcam3Pos5Run
        global OLDcam3Pos6Run
        global OLDcam3Pos7Run
        global OLDcam3Pos8Run
        global OLDcam3Pos9Run
        global OLDcam3Pos10Run
        global cam3isRecording
        global cam3isZooming

        global OLDcam4AtPos1
        global OLDcam4AtPos2
        global OLDcam4AtPos3
        global OLDcam4AtPos4
        global OLDcam4AtPos5
        global OLDcam4AtPos6
        global OLDcam4AtPos7
        global OLDcam4AtPos8
        global OLDcam4AtPos9
        global OLDcam4AtPos10
        global OLDcam4Pos1Set
        global OLDcam4Pos2Set
        global OLDcam4Pos3Set
        global OLDcam4Pos4Set
        global OLDcam4Pos5Set
        global OLDcam4Pos6Set
        global OLDcam4Pos7Set
        global OLDcam4Pos8Set
        global OLDcam4Pos9Set
        global OLDcam4Pos10Set
        global OLDcam4Pos1Run
        global OLDcam4Pos2Run
        global OLDcam4Pos3Run
        global OLDcam4Pos4Run
        global OLDcam4Pos5Run
        global OLDcam4Pos6Run
        global OLDcam4Pos7Run
        global OLDcam4Pos8Run
        global OLDcam4Pos9Run
        global OLDcam4Pos10Run
        global cam4isRecording
        global cam4isZooming

        global OLDcam5AtPos1
        global OLDcam5AtPos2
        global OLDcam5AtPos3
        global OLDcam5AtPos4
        global OLDcam5AtPos5
        global OLDcam5AtPos6
        global OLDcam5AtPos7
        global OLDcam5AtPos8
        global OLDcam5AtPos9
        global OLDcam5AtPos10
        global OLDcam5Pos1Set
        global OLDcam5Pos2Set
        global OLDcam5Pos3Set
        global OLDcam5Pos4Set
        global OLDcam5Pos5Set
        global OLDcam5Pos6Set
        global OLDcam5Pos7Set
        global OLDcam5Pos8Set
        global OLDcam5Pos9Set
        global OLDcam5Pos10Set
        global OLDcam5Pos1Run
        global OLDcam5Pos2Run
        global OLDcam5Pos3Run
        global OLDcam5Pos4Run
        global OLDcam5Pos5Run
        global OLDcam5Pos6Run
        global OLDcam5Pos7Run
        global OLDcam5Pos8Run
        global OLDcam5Pos9Run
        global OLDcam5Pos10Run
        global cam5isRecording
        global cam5isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global cam4SliderSpeed
        global cam5SliderSpeed
        global oldcam1Speed
        global oldcam2Speed
        global oldcam3Speed
        global oldcam4Speed
        global oldcam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldcam1PTSpeed
        global oldcam2PTSpeed
        global oldcam3PTSpeed
        global oldcam4PTSpeed
        global oldcam5PTSpeed

        global cam1AF
        global cam2AF
        global cam3AF
        global cam4AF
        global cam5AF

        global oldcam1AF
        global oldcam2AF
        global oldcam3AF
        global oldcam4AF
        global oldcam5AF

        global resetButtons

        buttonColourSet = "#ff0000"
        buttonColourAt = "#00ff00"

        if cam1Pos1Set != OLDcam1Pos1Set or cam1Pos1Run != OLDcam1Pos1Run or cam1AtPos1 != OLDcam1AtPos1 or resetButtons:
            OLDcam1Pos1Set = cam1Pos1Set
            OLDcam1Pos1Run = cam1Pos1Run
            OLDcam1AtPos1 = cam1AtPos1
            if cam1Pos1Set and not cam1Pos1Run and not cam1AtPos1:                                  # Set , not Run or At
                self.pushButton11.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos1Set and not cam1Pos1Run and cam1AtPos1:                                    # Set & At, not Run
                self.pushButton11.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos1Set:
                self.pushButton11.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos2Set != OLDcam1Pos2Set or cam1Pos2Run != OLDcam1Pos2Run or cam1AtPos2 != OLDcam1AtPos2 or resetButtons:
            OLDcam1Pos2Set = cam1Pos2Set
            OLDcam1Pos2Run = cam1Pos2Run
            OLDcam1AtPos2 = cam1AtPos2
            if cam1Pos2Set and not cam1Pos2Run and not cam1AtPos2:                                  # Position LEDs Cam1
                self.pushButton12.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos2Set and not cam1Pos2Run and cam1AtPos2:
                self.pushButton12.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos2Set:
                self.pushButton12.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos3Set != OLDcam1Pos3Set or cam1Pos3Run != OLDcam1Pos3Run or cam1AtPos3 != OLDcam1AtPos3 or resetButtons:
            OLDcam1Pos3Set = cam1Pos3Set
            OLDcam1Pos3Run = cam1Pos3Run
            OLDcam1AtPos3 = cam1AtPos3
            if cam1Pos3Set and not cam1Pos3Run and not cam1AtPos3:                                  # Position LEDs Cam1
                self.pushButton13.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos3Set and not cam1Pos3Run and cam1AtPos3:
                self.pushButton13.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos3Set:
                self.pushButton13.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos4Set != OLDcam1Pos4Set or cam1Pos4Run != OLDcam1Pos4Run or cam1AtPos4 != OLDcam1AtPos4 or resetButtons:
            OLDcam1Pos4Set = cam1Pos4Set
            OLDcam1Pos4Run = cam1Pos4Run
            OLDcam1AtPos4 = cam1AtPos4
            if cam1Pos4Set and not cam1Pos4Run and not cam1AtPos4:                                  # Position LEDs Cam1
                self.pushButton14.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos4Set and not cam1Pos4Run and cam1AtPos4:
                self.pushButton14.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos4Set:
                self.pushButton14.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos5Set != OLDcam1Pos5Set or cam1Pos5Run != OLDcam1Pos5Run or cam1AtPos5 != OLDcam1AtPos5 or resetButtons:
            OLDcam1Pos5Set = cam1Pos5Set
            OLDcam1Pos5Run = cam1Pos5Run
            OLDcam1AtPos5 = cam1AtPos5
            if cam1Pos5Set and not cam1Pos5Run and not cam1AtPos5:                                  # Position LEDs Cam1
                self.pushButton15.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos5Set and not cam1Pos5Run and cam1AtPos5:
                self.pushButton15.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos5Set:
                self.pushButton15.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos6Set != OLDcam1Pos6Set or cam1Pos6Run != OLDcam1Pos6Run or cam1AtPos6 != OLDcam1AtPos6 or resetButtons:
            OLDcam1Pos6Set = cam1Pos6Set
            OLDcam1Pos6Run = cam1Pos6Run
            OLDcam1AtPos6 = cam1AtPos6
            if cam1Pos6Set and not cam1Pos6Run and not cam1AtPos6:                                  # Position LEDs Cam1
                self.pushButton16.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos6Set and not cam1Pos6Run and cam1AtPos6:
                self.pushButton16.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos6Set:
                self.pushButton16.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos7Set != OLDcam1Pos7Set or cam1Pos7Run != OLDcam1Pos7Run or cam1AtPos7 != OLDcam1AtPos7 or resetButtons:
            OLDcam1Pos7Set = cam1Pos7Set
            OLDcam1Pos7Run = cam1Pos7Run
            OLDcam1AtPos7 = cam1AtPos7
            if cam1Pos7Set and not cam1Pos7Run and not cam1AtPos7:                                  # Position LEDs Cam1
                self.pushButton17.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos7Set and not cam1Pos7Run and cam1AtPos7:
                self.pushButton17.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos7Set:
                self.pushButton17.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos8Set != OLDcam1Pos8Set or cam1Pos8Run != OLDcam1Pos8Run or cam1AtPos8 != OLDcam1AtPos8 or resetButtons:
            OLDcam1Pos8Set = cam1Pos8Set
            OLDcam1Pos8Run = cam1Pos8Run
            OLDcam1AtPos8 = cam1AtPos8
            if cam1Pos8Set and not cam1Pos8Run and not cam1AtPos8:                                  # Position LEDs Cam1
                self.pushButton18.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos8Set and not cam1Pos8Run and cam1AtPos8:
                self.pushButton18.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos8Set:
                self.pushButton18.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos9Set != OLDcam1Pos9Set or cam1Pos9Run != OLDcam1Pos9Run or cam1AtPos9 != OLDcam1AtPos9 or resetButtons:
            OLDcam1Pos9Set = cam1Pos9Set
            OLDcam1Pos9Run = cam1Pos9Run
            OLDcam1AtPos9 = cam1AtPos9
            if cam1Pos9Set and not cam1Pos9Run and not cam1AtPos9:                                  # Position LEDs Cam1
                self.pushButton19.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos9Set and not cam1Pos9Run and cam1AtPos9:
                self.pushButton19.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos9Set:
                self.pushButton19.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')

        if cam1Pos10Set != OLDcam1Pos10Set or cam1Pos10Run != OLDcam1Pos10Run or cam1AtPos10 != OLDcam1AtPos10 or resetButtons:
            OLDcam1Pos10Set = cam1Pos10Set
            OLDcam1Pos10Run = cam1Pos10Run
            OLDcam1AtPos10 = cam1AtPos10
            if cam1Pos10Set and not cam1Pos10Run and not cam1AtPos10:                                  # Position LEDs Cam1
                self.pushButton10.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: 40px;')
            elif cam1Pos10Set and not cam1Pos10Run and cam1AtPos10:
                self.pushButton10.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: 40px;')
            elif not cam1Pos10Set:
                self.pushButton10.setStyleSheet(f'border: 10px solid grey; background-color: #4C8A4C; border-radius: 40px;')






        if cam2Pos1Set != OLDcam2Pos1Set or cam2Pos1Run != OLDcam2Pos1Run or cam2AtPos1 != OLDcam2AtPos1 or resetButtons:
            OLDcam2Pos1Set = cam2Pos1Set
            OLDcam2Pos1Run = cam2Pos1Run
            OLDcam2AtPos1 = cam2AtPos1
            if cam2Pos1Set and not cam2Pos1Run and not cam2AtPos1:                                  # Set , not Run or At
                self.pushButton21.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos1Set and not cam2Pos1Run and cam2AtPos1:                                    # Set & At, not Run
                self.pushButton21.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos1Set:
                self.pushButton21.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos2Set != OLDcam2Pos2Set or cam2Pos2Run != OLDcam2Pos2Run or cam2AtPos2 != OLDcam2AtPos2 or resetButtons:
            OLDcam2Pos2Set = cam2Pos2Set
            OLDcam2Pos2Run = cam2Pos2Run
            OLDcam2AtPos2 = cam2AtPos2
            if cam2Pos2Set and not cam2Pos2Run and not cam2AtPos2:                                  # Position LEDs cam2
                self.pushButton22.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos2Set and not cam2Pos2Run and cam2AtPos2:
                self.pushButton22.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos2Set:
                self.pushButton22.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos3Set != OLDcam2Pos3Set or cam2Pos3Run != OLDcam2Pos3Run or cam2AtPos3 != OLDcam2AtPos3 or resetButtons:
            OLDcam2Pos3Set = cam2Pos3Set
            OLDcam2Pos3Run = cam2Pos3Run
            OLDcam2AtPos3 = cam2AtPos3
            if cam2Pos3Set and not cam2Pos3Run and not cam2AtPos3:                                  # Position LEDs cam2
                self.pushButton23.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos3Set and not cam2Pos3Run and cam2AtPos3:
                self.pushButton23.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos3Set:
                self.pushButton23.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos4Set != OLDcam2Pos4Set or cam2Pos4Run != OLDcam2Pos4Run or cam2AtPos4 != OLDcam2AtPos4 or resetButtons:
            OLDcam2Pos4Set = cam2Pos4Set
            OLDcam2Pos4Run = cam2Pos4Run
            OLDcam2AtPos4 = cam2AtPos4
            if cam2Pos4Set and not cam2Pos4Run and not cam2AtPos4:                                  # Position LEDs cam2
                self.pushButton24.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos4Set and not cam2Pos4Run and cam2AtPos4:
                self.pushButton24.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos4Set:
                self.pushButton24.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos5Set != OLDcam2Pos5Set or cam2Pos5Run != OLDcam2Pos5Run or cam2AtPos5 != OLDcam2AtPos5 or resetButtons:
            OLDcam2Pos5Set = cam2Pos5Set
            OLDcam2Pos5Run = cam2Pos5Run
            OLDcam2AtPos5 = cam2AtPos5
            if cam2Pos5Set and not cam2Pos5Run and not cam2AtPos5:                                  # Position LEDs cam2
                self.pushButton25.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos5Set and not cam2Pos5Run and cam2AtPos5:
                self.pushButton25.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos5Set:
                self.pushButton25.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos6Set != OLDcam2Pos6Set or cam2Pos6Run != OLDcam2Pos6Run or cam2AtPos6 != OLDcam2AtPos6 or resetButtons:
            OLDcam2Pos6Set = cam2Pos6Set
            OLDcam2Pos6Run = cam2Pos6Run
            OLDcam2AtPos6 = cam2AtPos6
            if cam2Pos6Set and not cam2Pos6Run and not cam2AtPos6:                                  # Position LEDs cam2
                self.pushButton26.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos6Set and not cam2Pos6Run and cam2AtPos6:
                self.pushButton26.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos6Set:
                self.pushButton26.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos7Set != OLDcam2Pos7Set or cam2Pos7Run != OLDcam2Pos7Run or cam2AtPos7 != OLDcam2AtPos7 or resetButtons:
            OLDcam2Pos7Set = cam2Pos7Set
            OLDcam2Pos7Run = cam2Pos7Run
            OLDcam2AtPos7 = cam2AtPos7
            if cam2Pos7Set and not cam2Pos7Run and not cam2AtPos7:                                  # Position LEDs cam2
                self.pushButton27.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos7Set and not cam2Pos7Run and cam2AtPos7:
                self.pushButton27.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos7Set:
                self.pushButton27.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos8Set != OLDcam2Pos8Set or cam2Pos8Run != OLDcam2Pos8Run or cam2AtPos8 != OLDcam2AtPos8 or resetButtons:
            OLDcam2Pos8Set = cam2Pos8Set
            OLDcam2Pos8Run = cam2Pos8Run
            OLDcam2AtPos8 = cam2AtPos8
            if cam2Pos8Set and not cam2Pos8Run and not cam2AtPos8:                                  # Position LEDs cam2
                self.pushButton28.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos8Set and not cam2Pos8Run and cam2AtPos8:
                self.pushButton28.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos8Set:
                self.pushButton28.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos9Set != OLDcam2Pos9Set or cam2Pos9Run != OLDcam2Pos9Run or cam2AtPos9 != OLDcam2AtPos9 or resetButtons:
            OLDcam2Pos9Set = cam2Pos9Set
            OLDcam2Pos9Run = cam2Pos9Run
            OLDcam2AtPos9 = cam2AtPos9
            if cam2Pos9Set and not cam2Pos9Run and not cam2AtPos9:                                  # Position LEDs cam2
                self.pushButton29.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos9Set and not cam2Pos9Run and cam2AtPos9:
                self.pushButton29.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos9Set:
                self.pushButton29.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')

        if cam2Pos10Set != OLDcam2Pos10Set or cam2Pos10Run != OLDcam2Pos10Run or cam2AtPos10 != OLDcam2AtPos10 or resetButtons:
            OLDcam2Pos10Set = cam2Pos10Set
            OLDcam2Pos10Run = cam2Pos10Run
            OLDcam2AtPos10 = cam2AtPos10
            if cam2Pos10Set and not cam2Pos10Run and not cam2AtPos10:                                  # Position LEDs cam2
                self.pushButton20.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #405C80; border-radius: 40px;')
            elif cam2Pos10Set and not cam2Pos10Run and cam2AtPos10:
                self.pushButton20.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #405C80; border-radius: 40px;')
            elif not cam2Pos10Set:
                self.pushButton20.setStyleSheet(f'border: 10px solid grey; background-color: #405C80; border-radius: 40px;')




        if cam3Pos1Set != OLDcam3Pos1Set or cam3Pos1Run != OLDcam3Pos1Run or cam3AtPos1 != OLDcam3AtPos1 or resetButtons:
            OLDcam3Pos1Set = cam3Pos1Set
            OLDcam3Pos1Run = cam3Pos1Run
            OLDcam3AtPos1 = cam3AtPos1
            if cam3Pos1Set and not cam3Pos1Run and not cam3AtPos1:                                  # Set , not Run or At
                self.pushButton31.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos1Set and not cam3Pos1Run and cam3AtPos1:                                    # Set & At, not Run
                self.pushButton31.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos1Set:
                self.pushButton31.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos2Set != OLDcam3Pos2Set or cam3Pos2Run != OLDcam3Pos2Run or cam3AtPos2 != OLDcam3AtPos2 or resetButtons:
            OLDcam3Pos2Set = cam3Pos2Set
            OLDcam3Pos2Run = cam3Pos2Run
            OLDcam3AtPos2 = cam3AtPos2
            if cam3Pos2Set and not cam3Pos2Run and not cam3AtPos2:                                  # Position LEDs cam3
                self.pushButton32.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos2Set and not cam3Pos2Run and cam3AtPos2:
                self.pushButton32.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos2Set:
                self.pushButton32.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos3Set != OLDcam3Pos3Set or cam3Pos3Run != OLDcam3Pos3Run or cam3AtPos3 != OLDcam3AtPos3 or resetButtons:
            OLDcam3Pos3Set = cam3Pos3Set
            OLDcam3Pos3Run = cam3Pos3Run
            OLDcam3AtPos3 = cam3AtPos3
            if cam3Pos3Set and not cam3Pos3Run and not cam3AtPos3:                                  # Position LEDs cam3
                self.pushButton33.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos3Set and not cam3Pos3Run and cam3AtPos3:
                self.pushButton33.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos3Set:
                self.pushButton33.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos4Set != OLDcam3Pos4Set or cam3Pos4Run != OLDcam3Pos4Run or cam3AtPos4 != OLDcam3AtPos4 or resetButtons:
            OLDcam3Pos4Set = cam3Pos4Set
            OLDcam3Pos4Run = cam3Pos4Run
            OLDcam3AtPos4 = cam3AtPos4
            if cam3Pos4Set and not cam3Pos4Run and not cam3AtPos4:                                  # Position LEDs cam3
                self.pushButton34.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos4Set and not cam3Pos4Run and cam3AtPos4:
                self.pushButton34.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos4Set:
                self.pushButton34.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos5Set != OLDcam3Pos5Set or cam3Pos5Run != OLDcam3Pos5Run or cam3AtPos5 != OLDcam3AtPos5 or resetButtons:
            OLDcam3Pos5Set = cam3Pos5Set
            OLDcam3Pos5Run = cam3Pos5Run
            OLDcam3AtPos5 = cam3AtPos5
            if cam3Pos5Set and not cam3Pos5Run and not cam3AtPos5:                                  # Position LEDs cam3
                self.pushButton35.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos5Set and not cam3Pos5Run and cam3AtPos5:
                self.pushButton35.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos5Set:
                self.pushButton35.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos6Set != OLDcam3Pos6Set or cam3Pos6Run != OLDcam3Pos6Run or cam3AtPos6 != OLDcam3AtPos6 or resetButtons:
            OLDcam3Pos6Set = cam3Pos6Set
            OLDcam3Pos6Run = cam3Pos6Run
            OLDcam3AtPos6 = cam3AtPos6
            if cam3Pos6Set and not cam3Pos6Run and not cam3AtPos6:                                  # Position LEDs cam3
                self.pushButton36.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos6Set and not cam3Pos6Run and cam3AtPos6:
                self.pushButton36.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos6Set:
                self.pushButton36.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos7Set != OLDcam3Pos7Set or cam3Pos7Run != OLDcam3Pos7Run or cam3AtPos7 != OLDcam3AtPos7 or resetButtons:
            OLDcam3Pos7Set = cam3Pos7Set
            OLDcam3Pos7Run = cam3Pos7Run
            OLDcam3AtPos7 = cam3AtPos7
            if cam3Pos7Set and not cam3Pos7Run and not cam3AtPos7:                                  # Position LEDs cam3
                self.pushButton37.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos7Set and not cam3Pos7Run and cam3AtPos7:
                self.pushButton37.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos7Set:
                self.pushButton37.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos8Set != OLDcam3Pos8Set or cam3Pos8Run != OLDcam3Pos8Run or cam3AtPos8 != OLDcam3AtPos8 or resetButtons:
            OLDcam3Pos8Set = cam3Pos8Set
            OLDcam3Pos8Run = cam3Pos8Run
            OLDcam3AtPos8 = cam3AtPos8
            if cam3Pos8Set and not cam3Pos8Run and not cam3AtPos8:                                  # Position LEDs cam3
                self.pushButton38.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos8Set and not cam3Pos8Run and cam3AtPos8:
                self.pushButton38.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos8Set:
                self.pushButton38.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos9Set != OLDcam3Pos9Set or cam3Pos9Run != OLDcam3Pos9Run or cam3AtPos9 != OLDcam3AtPos9 or resetButtons:
            OLDcam3Pos9Set = cam3Pos9Set
            OLDcam3Pos9Run = cam3Pos9Run
            OLDcam3AtPos9 = cam3AtPos9
            if cam3Pos9Set and not cam3Pos9Run and not cam3AtPos9:                                  # Position LEDs cam3
                self.pushButton39.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos9Set and not cam3Pos9Run and cam3AtPos9:
                self.pushButton39.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos9Set:
                self.pushButton39.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')

        if cam3Pos10Set != OLDcam3Pos10Set or cam3Pos10Run != OLDcam3Pos10Run or cam3AtPos10 != OLDcam3AtPos10 or resetButtons:
            OLDcam3Pos10Set = cam3Pos10Set
            OLDcam3Pos10Run = cam3Pos10Run
            OLDcam3AtPos10 = cam3AtPos10
            if cam3Pos10Set and not cam3Pos10Run and not cam3AtPos10:                                  # Position LEDs cam3
                self.pushButton30.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #807100; border-radius: 40px;')
            elif cam3Pos10Set and not cam3Pos10Run and cam3AtPos10:
                self.pushButton30.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #807100; border-radius: 40px;')
            elif not cam3Pos10Set:
                self.pushButton30.setStyleSheet(f'border: 10px solid grey; background-color: #807100; border-radius: 40px;')




        if cam4Pos1Set != OLDcam4Pos1Set or cam4Pos1Run != OLDcam4Pos1Run or cam4AtPos1 != OLDcam4AtPos1 or resetButtons:
            OLDcam4Pos1Set = cam4Pos1Set
            OLDcam4Pos1Run = cam4Pos1Run
            OLDcam4AtPos1 = cam4AtPos1
            if cam4Pos1Set and not cam4Pos1Run and not cam4AtPos1:                                  # Set , not Run or At
                self.pushButton41.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos1Set and not cam4Pos1Run and cam4AtPos1:                                    # Set & At, not Run
                self.pushButton41.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos1Set:
                self.pushButton41.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos2Set != OLDcam4Pos2Set or cam4Pos2Run != OLDcam4Pos2Run or cam4AtPos2 != OLDcam4AtPos2 or resetButtons:
            OLDcam4Pos2Set = cam4Pos2Set
            OLDcam4Pos2Run = cam4Pos2Run
            OLDcam4AtPos2 = cam4AtPos2
            if cam4Pos2Set and not cam4Pos2Run and not cam4AtPos2:                                  # Position LEDs cam4
                self.pushButton42.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos2Set and not cam4Pos2Run and cam4AtPos2:
                self.pushButton42.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos2Set:
                self.pushButton42.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos3Set != OLDcam4Pos3Set or cam4Pos3Run != OLDcam4Pos3Run or cam4AtPos3 != OLDcam4AtPos3 or resetButtons:
            OLDcam4Pos3Set = cam4Pos3Set
            OLDcam4Pos3Run = cam4Pos3Run
            OLDcam4AtPos3 = cam4AtPos3
            if cam4Pos3Set and not cam4Pos3Run and not cam4AtPos3:                                  # Position LEDs cam4
                self.pushButton43.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos3Set and not cam4Pos3Run and cam4AtPos3:
                self.pushButton43.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos3Set:
                self.pushButton43.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos4Set != OLDcam4Pos4Set or cam4Pos4Run != OLDcam4Pos4Run or cam4AtPos4 != OLDcam4AtPos4 or resetButtons:
            OLDcam4Pos4Set = cam4Pos4Set
            OLDcam4Pos4Run = cam4Pos4Run
            OLDcam4AtPos4 = cam4AtPos4
            if cam4Pos4Set and not cam4Pos4Run and not cam4AtPos4:                                  # Position LEDs cam4
                self.pushButton44.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos4Set and not cam4Pos4Run and cam4AtPos4:
                self.pushButton44.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos4Set:
                self.pushButton44.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos5Set != OLDcam4Pos5Set or cam4Pos5Run != OLDcam4Pos5Run or cam4AtPos5 != OLDcam4AtPos5 or resetButtons:
            OLDcam4Pos5Set = cam4Pos5Set
            OLDcam4Pos5Run = cam4Pos5Run
            OLDcam4AtPos5 = cam4AtPos5
            if cam4Pos5Set and not cam4Pos5Run and not cam4AtPos5:                                  # Position LEDs cam4
                self.pushButton45.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos5Set and not cam4Pos5Run and cam4AtPos5:
                self.pushButton45.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos5Set:
                self.pushButton45.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos6Set != OLDcam4Pos6Set or cam4Pos6Run != OLDcam4Pos6Run or cam4AtPos6 != OLDcam4AtPos6 or resetButtons:
            OLDcam4Pos6Set = cam4Pos6Set
            OLDcam4Pos6Run = cam4Pos6Run
            OLDcam4AtPos6 = cam4AtPos6
            if cam4Pos6Set and not cam4Pos6Run and not cam4AtPos6:                                  # Position LEDs cam4
                self.pushButton46.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos6Set and not cam4Pos6Run and cam4AtPos6:
                self.pushButton46.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos6Set:
                self.pushButton46.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos7Set != OLDcam4Pos7Set or cam4Pos7Run != OLDcam4Pos7Run or cam4AtPos7 != OLDcam4AtPos7 or resetButtons:
            OLDcam4Pos7Set = cam4Pos7Set
            OLDcam4Pos7Run = cam4Pos7Run
            OLDcam4AtPos7 = cam4AtPos7
            if cam4Pos7Set and not cam4Pos7Run and not cam4AtPos7:                                  # Position LEDs cam4
                self.pushButton47.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos7Set and not cam4Pos7Run and cam4AtPos7:
                self.pushButton47.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos7Set:
                self.pushButton47.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos8Set != OLDcam4Pos8Set or cam4Pos8Run != OLDcam4Pos8Run or cam4AtPos8 != OLDcam4AtPos8 or resetButtons:
            OLDcam4Pos8Set = cam4Pos8Set
            OLDcam4Pos8Run = cam4Pos8Run
            OLDcam4AtPos8 = cam4AtPos8
            if cam4Pos8Set and not cam4Pos8Run and not cam4AtPos8:                                  # Position LEDs cam4
                self.pushButton48.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos8Set and not cam4Pos8Run and cam4AtPos8:
                self.pushButton48.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos8Set:
                self.pushButton48.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos9Set != OLDcam4Pos9Set or cam4Pos9Run != OLDcam4Pos9Run or cam4AtPos9 != OLDcam4AtPos9 or resetButtons:
            OLDcam4Pos9Set = cam4Pos9Set
            OLDcam4Pos9Run = cam4Pos9Run
            OLDcam4AtPos9 = cam4AtPos9
            if cam4Pos9Set and not cam4Pos9Run and not cam4AtPos9:                                  # Position LEDs cam4
                self.pushButton49.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos9Set and not cam4Pos9Run and cam4AtPos9:
                self.pushButton49.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos9Set:
                self.pushButton49.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')

        if cam4Pos10Set != OLDcam4Pos10Set or cam4Pos10Run != OLDcam4Pos10Run or cam4AtPos10 != OLDcam4AtPos10 or resetButtons:
            OLDcam4Pos10Set = cam4Pos10Set
            OLDcam4Pos10Run = cam4Pos10Run
            OLDcam4AtPos10 = cam4AtPos10
            if cam4Pos10Set and not cam4Pos10Run and not cam4AtPos10:                                  # Position LEDs cam4
                self.pushButton40.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #008071; border-radius: 40px;')
            elif cam4Pos10Set and not cam4Pos10Run and cam4AtPos10:
                self.pushButton40.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #008071; border-radius: 40px;')
            elif not cam4Pos10Set:
                self.pushButton40.setStyleSheet(f'border: 10px solid grey; background-color: #008071; border-radius: 40px;')






        if cam5Pos1Set != OLDcam5Pos1Set or cam5Pos1Run != OLDcam5Pos1Run or cam5AtPos1 != OLDcam5AtPos1 or resetButtons:
            OLDcam5Pos1Set = cam5Pos1Set
            OLDcam5Pos1Run = cam5Pos1Run
            OLDcam5AtPos1 = cam5AtPos1
            if cam5Pos1Set and not cam5Pos1Run and not cam5AtPos1:                                  # Set , not Run or At
                self.pushButton51.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos1Set and not cam5Pos1Run and cam5AtPos1:                                    # Set & At, not Run
                self.pushButton51.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos1Set:
                self.pushButton51.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos2Set != OLDcam5Pos2Set or cam5Pos2Run != OLDcam5Pos2Run or cam5AtPos2 != OLDcam5AtPos2 or resetButtons:
            OLDcam5Pos2Set = cam5Pos2Set
            OLDcam5Pos2Run = cam5Pos2Run
            OLDcam5AtPos2 = cam5AtPos2
            if cam5Pos2Set and not cam5Pos2Run and not cam5AtPos2:                                  # Position LEDs cam5
                self.pushButton52.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos2Set and not cam5Pos2Run and cam5AtPos2:
                self.pushButton52.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos2Set:
                self.pushButton52.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos3Set != OLDcam5Pos3Set or cam5Pos3Run != OLDcam5Pos3Run or cam5AtPos3 != OLDcam5AtPos3 or resetButtons:
            OLDcam5Pos3Set = cam5Pos3Set
            OLDcam5Pos3Run = cam5Pos3Run
            OLDcam5AtPos3 = cam5AtPos3
            if cam5Pos3Set and not cam5Pos3Run and not cam5AtPos3:                                  # Position LEDs cam5
                self.pushButton53.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos3Set and not cam5Pos3Run and cam5AtPos3:
                self.pushButton53.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos3Set:
                self.pushButton53.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos4Set != OLDcam5Pos4Set or cam5Pos4Run != OLDcam5Pos4Run or cam5AtPos4 != OLDcam5AtPos4 or resetButtons:
            OLDcam5Pos4Set = cam5Pos4Set
            OLDcam5Pos4Run = cam5Pos4Run
            OLDcam5AtPos4 = cam5AtPos4
            if cam5Pos4Set and not cam5Pos4Run and not cam5AtPos4:                                  # Position LEDs cam5
                self.pushButton54.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos4Set and not cam5Pos4Run and cam5AtPos4:
                self.pushButton54.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos4Set:
                self.pushButton54.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos5Set != OLDcam5Pos5Set or cam5Pos5Run != OLDcam5Pos5Run or cam5AtPos5 != OLDcam5AtPos5 or resetButtons:
            OLDcam5Pos5Set = cam5Pos5Set
            OLDcam5Pos5Run = cam5Pos5Run
            OLDcam5AtPos5 = cam5AtPos5
            if cam5Pos5Set and not cam5Pos5Run and not cam5AtPos5:                                  # Position LEDs cam5
                self.pushButton55.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos5Set and not cam5Pos5Run and cam5AtPos5:
                self.pushButton55.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos5Set:
                self.pushButton55.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos6Set != OLDcam5Pos6Set or cam5Pos6Run != OLDcam5Pos6Run or cam5AtPos6 != OLDcam5AtPos6 or resetButtons:
            OLDcam5Pos6Set = cam5Pos6Set
            OLDcam5Pos6Run = cam5Pos6Run
            OLDcam5AtPos6 = cam5AtPos6
            if cam5Pos6Set and not cam5Pos6Run and not cam5AtPos6:                                  # Position LEDs cam5
                self.pushButton56.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos6Set and not cam5Pos6Run and cam5AtPos6:
                self.pushButton56.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos6Set:
                self.pushButton56.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos7Set != OLDcam5Pos7Set or cam5Pos7Run != OLDcam5Pos7Run or cam5AtPos7 != OLDcam5AtPos7 or resetButtons:
            OLDcam5Pos7Set = cam5Pos7Set
            OLDcam5Pos7Run = cam5Pos7Run
            OLDcam5AtPos7 = cam5AtPos7
            if cam5Pos7Set and not cam5Pos7Run and not cam5AtPos7:                                  # Position LEDs cam5
                self.pushButton57.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos7Set and not cam5Pos7Run and cam5AtPos7:
                self.pushButton57.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos7Set:
                self.pushButton57.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos8Set != OLDcam5Pos8Set or cam5Pos8Run != OLDcam5Pos8Run or cam5AtPos8 != OLDcam5AtPos8 or resetButtons:
            OLDcam5Pos8Set = cam5Pos8Set
            OLDcam5Pos8Run = cam5Pos8Run
            OLDcam5AtPos8 = cam5AtPos8
            if cam5Pos8Set and not cam5Pos8Run and not cam5AtPos8:                                  # Position LEDs cam5
                self.pushButton58.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos8Set and not cam5Pos8Run and cam5AtPos8:
                self.pushButton58.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos8Set:
                self.pushButton58.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos9Set != OLDcam5Pos9Set or cam5Pos9Run != OLDcam5Pos9Run or cam5AtPos9 != OLDcam5AtPos9 or resetButtons:
            OLDcam5Pos9Set = cam5Pos9Set
            OLDcam5Pos9Run = cam5Pos9Run
            OLDcam5AtPos9 = cam5AtPos9
            if cam5Pos9Set and not cam5Pos9Run and not cam5AtPos9:                                  # Position LEDs cam5
                self.pushButton59.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos9Set and not cam5Pos9Run and cam5AtPos9:
                self.pushButton59.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos9Set:
                self.pushButton59.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')

        if cam5Pos10Set != OLDcam5Pos10Set or cam5Pos10Run != OLDcam5Pos10Run or cam5AtPos10 != OLDcam5AtPos10 or resetButtons:
            OLDcam5Pos10Set = cam5Pos10Set
            OLDcam5Pos10Run = cam5Pos10Run
            OLDcam5AtPos10 = cam5AtPos10
            if cam5Pos10Set and not cam5Pos10Run and not cam5AtPos10:                                  # Position LEDs cam5
                self.pushButton50.setStyleSheet(f'border: 10px solid {buttonColourSet}; background-color: #8D5395; border-radius: 40px;')
            elif cam5Pos10Set and not cam5Pos10Run and cam5AtPos10:
                self.pushButton50.setStyleSheet(f'border: 10px solid {buttonColourAt}; background-color: #8D5395; border-radius: 40px;')
            elif not cam5Pos10Set:
                self.pushButton50.setStyleSheet(f'border: 10px solid grey; background-color: #8D5395; border-radius: 40px;')







        
        if oldcam1PTSpeed != cam1PTSpeed:
            oldcam1PTSpeed = cam1PTSpeed
            if cam1PTSpeed == 1:
                self.dial1p.setValue(1)
                self.line1p.setGeometry(1470, 115, 20, 36)            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
            elif cam1PTSpeed == 3:
                self.dial1p.setValue(2)
                self.line1p.setGeometry(1470, 80, 20, 71)
            elif cam1PTSpeed == 5:
                self.dial1p.setValue(3)
                self.line1p.setGeometry(1470, 45, 20, 106)
            elif cam1PTSpeed == 7:
                self.dial1p.setValue(4)
                self.line1p.setGeometry(1470, 10, 20, 141)

        if oldcam2PTSpeed != cam2PTSpeed:
            oldcam2PTSpeed = cam2PTSpeed
            if cam2PTSpeed == 1:
                self.dial2p.setValue(1)
                self.line2p.setGeometry(1470, 115, 20, 36)
            elif cam2PTSpeed == 3:
                self.dial2p.setValue(2)
                self.line2p.setGeometry(1470, 80, 20, 71)
            elif cam2PTSpeed == 5:
                self.dial2p.setValue(3)
                self.line2p.setGeometry(1470, 45, 20, 106)
            elif cam2PTSpeed == 7:
                self.dial2p.setValue(4)
                self.line2p.setGeometry(1470, 10, 20, 141)

        if oldcam3PTSpeed != cam3PTSpeed:
            oldcam3PTSpeed = cam3PTSpeed
            if cam3PTSpeed == 1:
                self.dial3p.setValue(1)
                self.line3p.setGeometry(1470, 115, 20, 36)
            elif cam3PTSpeed == 3:
                self.dial3p.setValue(2)
                self.line3p.setGeometry(1470, 80, 20, 71)
            elif cam3PTSpeed == 5:
                self.dial3p.setValue(3)
                self.line3p.setGeometry(1470, 45, 20, 106)
            elif cam3PTSpeed == 7:
                self.dial3p.setValue(4)
                self.line3p.setGeometry(1470, 10, 20, 141)

        if oldcam4PTSpeed != cam4PTSpeed:
            oldcam4PTSpeed = cam4PTSpeed
            if cam4PTSpeed == 1:
                self.dial4p.setValue(1)
                self.line4p.setGeometry(1470, 115, 20, 36)
            elif cam4PTSpeed == 3:
                self.dial4p.setValue(2)
                self.line4p.setGeometry(1470, 80, 20, 71)
            elif cam4PTSpeed == 5:
                self.dial4p.setValue(3)
                self.line4p.setGeometry(1470, 45, 20, 106)
            elif cam4PTSpeed == 7:
                self.dial4p.setValue(4)
                self.line4p.setGeometry(1470, 10, 20, 141)

        if oldcam5PTSpeed != cam5PTSpeed:
            oldcam5PTSpeed = cam5PTSpeed
            if cam5PTSpeed == 1:
                self.dial5p.setValue(1)
                self.line5p.setGeometry(1470, 115, 20, 36)
            elif cam5PTSpeed == 3:
                self.dial5p.setValue(2)
                self.line5p.setGeometry(1470, 80, 20, 71)
            elif cam5PTSpeed == 5:
                self.dial5p.setValue(3)
                self.line5p.setGeometry(1470, 45, 20, 106)
            elif cam5PTSpeed == 7:
                self.dial5p.setValue(4)
                self.line5p.setGeometry(1470, 10, 20, 141)

        if oldcam1Speed != cam1SliderSpeed:
            oldcam1Speed = cam1SliderSpeed
            if cam1SliderSpeed == 1:
                self.dial1s.setValue(1)
                self.line1s.setGeometry(1820, 115, 20, 36)            #    10, 141      30, 121     50, 101     70, 81      90, 61      110, 41     130, 21
            elif cam1SliderSpeed == 3:
                self.dial1s.setValue(2)
                self.line1s.setGeometry(1820, 80, 20, 71)
            elif cam1SliderSpeed == 5:
                self.dial1s.setValue(3)
                self.line1s.setGeometry(1820, 45, 20, 106)
            elif cam1SliderSpeed >= 7:
                self.dial1s.setValue(4)
                self.line1s.setGeometry(1820, 10, 20, 141)

        if oldcam2Speed != cam2SliderSpeed:
            oldcam2Speed = cam2SliderSpeed
            if cam2SliderSpeed == 1:
                self.dial2s.setValue(1)
                self.line2s.setGeometry(1820, 115, 20, 36)
            elif cam2SliderSpeed == 3:
                self.dial2s.setValue(2)
                self.line2s.setGeometry(1820, 80, 20, 71)
            elif cam2SliderSpeed == 5:
                self.dial2s.setValue(3)
                self.line2s.setGeometry(1820, 45, 20, 106)
            elif cam2SliderSpeed >= 7:
                self.dial2s.setValue(4)
                self.line2s.setGeometry(1820, 10, 20, 141)

        if oldcam3Speed != cam3SliderSpeed:
            oldcam3Speed = cam3SliderSpeed
            if cam3SliderSpeed == 1:
                self.dial3s.setValue(1)
                self.line3s.setGeometry(1820, 115, 20, 36)
            elif cam3SliderSpeed == 3:
                self.dial3s.setValue(2)
                self.line3s.setGeometry(1820, 80, 20, 71)
            elif cam3SliderSpeed == 5:
                self.dial3s.setValue(3)
                self.line3s.setGeometry(1820, 45, 20, 106)
            elif cam3SliderSpeed >= 7:
                self.dial3s.setValue(4)
                self.line3s.setGeometry(1820, 10, 20, 141)

        if oldcam4Speed != cam4SliderSpeed:
            oldcam4Speed = cam4SliderSpeed
            if cam4SliderSpeed == 1:
                self.dial4s.setValue(1)
                self.line4s.setGeometry(1820, 115, 20, 36)
            elif cam4SliderSpeed == 3:
                self.dial4s.setValue(2)
                self.line4s.setGeometry(1820, 80, 20, 71)
            elif cam4SliderSpeed == 5:
                self.dial4s.setValue(3)
                self.line4s.setGeometry(1820, 45, 20, 106)
            elif cam4SliderSpeed >= 7:
                self.dial4s.setValue(4)
                self.line4s.setGeometry(1820, 10, 20, 141)

        if oldcam5Speed != cam5SliderSpeed:
            oldcam5Speed = cam5SliderSpeed
            if cam5SliderSpeed == 1:
                self.dial5s.setValue(1)
                self.line5s.setGeometry(1820, 115, 20, 36)
            elif cam5SliderSpeed == 3:
                self.dial5s.setValue(2)
                self.line5s.setGeometry(1820, 80, 20, 71)
            elif cam5SliderSpeed == 5:
                self.dial5s.setValue(3)
                self.line5s.setGeometry(1820, 45, 20, 106)
            elif cam5SliderSpeed >= 7:
                self.dial5s.setValue(4)
                self.line5s.setGeometry(1820, 10, 20, 141)

        if oldcam1AF != cam1AF:
            oldcam1AF = cam1AF
            if cam1AF:
                self.labelCam1AF.show()
            else :
                self.labelCam1AF.hide()

        if oldcam2AF != cam2AF:
            oldcam2AF = cam2AF
            if cam2AF:
                self.labelCam2AF.show()
            else :
                self.labelCam2AF.hide()

        if oldcam3AF != cam3AF:
            oldcam3AF = cam3AF
            if cam3AF:
                self.labelCam3AF.show()
            else :
                self.labelCam3AF.hide()

        if oldcam4AF != cam4AF:
            oldcam4AF = cam4AF
            if cam4AF:
                self.labelCam4AF.show()
            else :
                self.labelCam4AF.hide()

        if oldcam5AF != cam5AF:
            oldcam5AF = cam5AF
            if cam5AF:
                self.labelCam5AF.show()
            else :
                self.labelCam5AF.hide()


        resetButtons = False

    def resetButtonColours(self):
        global resetButtons
        resetButtons = True

        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1AtPos7
        global cam1AtPos8
        global cam1AtPos9
        global cam1AtPos10
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos7Set
        global cam1Pos8Set
        global cam1Pos9Set
        global cam1Pos10Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1Pos7Run
        global cam1Pos8Run
        global cam1Pos9Run
        global cam1Pos10Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2AtPos7
        global cam2AtPos8
        global cam2AtPos9
        global cam2AtPos10
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos7Set
        global cam2Pos8Set
        global cam2Pos9Set
        global cam2Pos10Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2Pos7Run
        global cam2Pos8Run
        global cam2Pos9Run
        global cam2Pos10Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3AtPos7
        global cam3AtPos8
        global cam3AtPos9
        global cam3AtPos10
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos7Set
        global cam3Pos8Set
        global cam3Pos9Set
        global cam3Pos10Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3Pos7Run
        global cam3Pos8Run
        global cam3Pos9Run
        global cam3Pos10Run
        global cam3isRecording
        global cam3isZooming

        global cam4AtPos1
        global cam4AtPos2
        global cam4AtPos3
        global cam4AtPos4
        global cam4AtPos5
        global cam4AtPos6
        global cam4AtPos7
        global cam4AtPos8
        global cam4AtPos9
        global cam4AtPos10
        global cam4Pos1Set
        global cam4Pos2Set
        global cam4Pos3Set
        global cam4Pos4Set
        global cam4Pos5Set
        global cam4Pos6Set
        global cam4Pos7Set
        global cam4Pos8Set
        global cam4Pos9Set
        global cam4Pos10Set
        global cam4Pos1Run
        global cam4Pos2Run
        global cam4Pos3Run
        global cam4Pos4Run
        global cam4Pos5Run
        global cam4Pos6Run
        global cam4Pos7Run
        global cam4Pos8Run
        global cam4Pos9Run
        global cam4Pos10Run
        global cam4isRecording
        global cam4isZooming

        global cam5AtPos1
        global cam5AtPos2
        global cam5AtPos3
        global cam5AtPos4
        global cam5AtPos5
        global cam5AtPos6
        global cam5AtPos7
        global cam5AtPos8
        global cam5AtPos9
        global cam5AtPos10
        global cam5Pos1Set
        global cam5Pos2Set
        global cam5Pos3Set
        global cam5Pos4Set
        global cam5Pos5Set
        global cam5Pos6Set
        global cam5Pos7Set
        global cam5Pos8Set
        global cam5Pos9Set
        global cam5Pos10Set
        global cam5Pos1Run
        global cam5Pos2Run
        global cam5Pos3Run
        global cam5Pos4Run
        global cam5Pos5Run
        global cam5Pos6Run
        global cam5Pos7Run
        global cam5Pos8Run
        global cam5Pos9Run
        global cam5Pos10Run
        global cam5isRecording
        global cam5isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global cam4SliderSpeed
        global cam5SliderSpeed
        global oldcam1Speed
        global oldcam2Speed
        global oldcam3Speed
        global oldcam4Speed
        global oldcam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldcam1PTSpeed
        global oldcam2PTSpeed
        global oldcam3PTSpeed
        global oldcam4PTSpeed
        global oldcam5PTSpeed

        cam1Pos1Set = False
        cam1Pos2Set = False
        cam1Pos3Set = False
        cam1Pos4Set = False
        cam1Pos5Set = False
        cam1Pos6Set = False
        cam1Pos7Set = False
        cam1Pos8Set = False
        cam1Pos9Set = False
        cam1Pos10Set = False
        cam1Pos1Run = False
        cam1Pos2Run = False
        cam1Pos3Run = False
        cam1Pos4Run = False
        cam1Pos5Run = False
        cam1Pos6Run = False
        cam1Pos7Run = False
        cam1Pos8Run = False
        cam1Pos9Run = False
        cam1Pos10Run = False
        cam1AtPos1 = False
        cam1AtPos2 = False
        cam1AtPos3 = False
        cam1AtPos4 = False
        cam1AtPos5 = False
        cam1AtPos6 = False
        cam1AtPos7 = False
        cam1AtPos8 = False
        cam1AtPos9 = False
        cam1AtPos10 = False

        cam2Pos1Set = False
        cam2Pos2Set = False
        cam2Pos3Set = False
        cam2Pos4Set = False
        cam2Pos5Set = False
        cam2Pos6Set = False
        cam2Pos7Set = False
        cam2Pos8Set = False
        cam2Pos9Set = False
        cam2Pos10Set = False
        cam2Pos1Run = False
        cam2Pos2Run = False
        cam2Pos3Run = False
        cam2Pos4Run = False
        cam2Pos5Run = False
        cam2Pos6Run = False
        cam2Pos7Run = False
        cam2Pos8Run = False
        cam2Pos9Run = False
        cam2Pos10Run = False
        cam2AtPos1 = False
        cam2AtPos2 = False
        cam2AtPos3 = False
        cam2AtPos4 = False
        cam2AtPos5 = False
        cam2AtPos6 = False
        cam2AtPos7 = False
        cam2AtPos8 = False
        cam2AtPos9 = False
        cam2AtPos10 = False

        cam3Pos1Set = False
        cam3Pos2Set = False
        cam3Pos3Set = False
        cam3Pos4Set = False
        cam3Pos5Set = False
        cam3Pos6Set = False
        cam3Pos7Set = False
        cam3Pos8Set = False
        cam3Pos9Set = False
        cam3Pos10Set = False
        cam3Pos1Run = False
        cam3Pos2Run = False
        cam3Pos3Run = False
        cam3Pos4Run = False
        cam3Pos5Run = False
        cam3Pos6Run = False
        cam3Pos7Run = False
        cam3Pos8Run = False
        cam3Pos9Run = False
        cam3Pos10Run = False
        cam3AtPos1 = False
        cam3AtPos2 = False
        cam3AtPos3 = False
        cam3AtPos4 = False
        cam3AtPos5 = False
        cam3AtPos6 = False
        cam3AtPos7 = False
        cam3AtPos8 = False
        cam3AtPos9 = False
        cam3AtPos10 = False

        cam4Pos1Set = False
        cam4Pos2Set = False
        cam4Pos3Set = False
        cam4Pos4Set = False
        cam4Pos5Set = False
        cam4Pos6Set = False
        cam4Pos7Set = False
        cam4Pos8Set = False
        cam4Pos9Set = False
        cam4Pos10Set = False
        cam4Pos1Run = False
        cam4Pos2Run = False
        cam4Pos3Run = False
        cam4Pos4Run = False
        cam4Pos5Run = False
        cam4Pos6Run = False
        cam4Pos7Run = False
        cam4Pos8Run = False
        cam4Pos9Run = False
        cam4Pos10Run = False
        cam4AtPos1 = False
        cam4AtPos2 = False
        cam4AtPos3 = False
        cam4AtPos4 = False
        cam4AtPos5 = False
        cam4AtPos6 = False
        cam4AtPos7 = False
        cam4AtPos8 = False
        cam4AtPos9 = False
        cam4AtPos10 = False

        cam5Pos1Set = False
        cam5Pos2Set = False
        cam5Pos3Set = False
        cam5Pos4Set = False
        cam5Pos5Set = False
        cam5Pos6Set = False
        cam5Pos7Set = False
        cam5Pos8Set = False
        cam5Pos9Set = False
        cam5Pos10Set = False
        cam5Pos1Run = False
        cam5Pos2Run = False
        cam5Pos3Run = False
        cam5Pos4Run = False
        cam5Pos5Run = False
        cam5Pos6Run = False
        cam5Pos7Run = False
        cam5Pos8Run = False
        cam5Pos9Run = False
        cam5Pos10Run = False
        cam5AtPos1 = False
        cam5AtPos2 = False
        cam5AtPos3 = False
        cam5AtPos4 = False
        cam5AtPos5 = False
        cam5AtPos6 = False
        cam5AtPos7 = False
        cam5AtPos8 = False
        cam5AtPos9 = False
        cam5AtPos10 = False

        cam1SliderSpeed = 0
        cam2SliderSpeed = 0
        cam3SliderSpeed = 0
        cam4SliderSpeed = 0
        cam5SliderSpeed = 0

        oldcam1Speed = 9
        oldcam2Speed = 9
        oldcam3Speed = 9
        oldcam4Speed = 9
        oldcam5Speed = 9

        cam1PTSpeed = 0
        cam2PTSpeed = 0
        cam3PTSpeed = 0
        cam4PTSpeed = 0
        cam5PTSpeed = 0

        oldcam1PTSpeed = 9
        oldcam2PTSpeed = 9
        oldcam3PTSpeed = 9
        oldcam4PTSpeed = 9
        oldcam5PTSpeed = 9

        self.dial1p.setValue(1)
        self.line1p.setGeometry(1470, 115, 20, 36)
        self.dial2p.setValue(1)
        self.line2p.setGeometry(1470, 115, 20, 36)
        self.dial3p.setValue(1)
        self.line3p.setGeometry(1470, 115, 20, 36)
        self.dial4p.setValue(1)
        self.line4p.setGeometry(1470, 115, 20, 36)
        self.dial5p.setValue(1)
        self.line5p.setGeometry(1470, 115, 20, 36)
        
        self.dial1s.setValue(1)
        self.line1s.setGeometry(1820, 115, 20, 36)
        self.dial2s.setValue(1)
        self.line2s.setGeometry(1820, 115, 20, 36)
        self.dial3s.setValue(1)
        self.line3s.setGeometry(1820, 115, 20, 36)
        self.dial4s.setValue(1)
        self.line4s.setGeometry(1820, 115, 20, 36)
        self.dial5s.setValue(1)
        self.line5s.setGeometry(1820, 115, 20, 36)

        self.setPos(3)
        self.doButtonColours()
        self.sendSerial("&-")

    def setMessage(self):
        global message
        global serialLoop
        global isConnected
        global newText
        global editButton
        global editToggle
        global manualMove
        global whichCamSerial
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label

        if serialLoop and not isConnected:
            self.comboBox.setStyleSheet("color: white; border: 4px solid grey; background-color: #229922; border-radius: 10px;")
            isConnected = True

        if isConnected:
            #print("joy")
            self.doJoyMoves(1)
            self.labelInfo.setText(message)
            self.messageTimerReset = QTimer()
            self.messageTimerReset.singleShot(2000,self.resetMessage)  # for one time call only. (once)
            message = ""

        if manualMove != "":
            if manualMove == "u10":
                if whichCamSerial == 1:
                    self.sendSerial('&??T10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?T10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?T10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?T10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?T10')
            elif manualMove == "u1":
                if whichCamSerial == 1:
                    self.sendSerial('&??T0.5')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?T0.5')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?T0.5')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?T0.5')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?T0.5')
            elif manualMove == "d1":
                if whichCamSerial == 1:
                    self.sendSerial('&??T-0.5')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?T-0.5')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?T-0.5')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?T-0.5')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?T-0.5')
            elif manualMove == "d10":
                if whichCamSerial == 1:
                    self.sendSerial('&??T-10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?T-10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?T-10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?T-10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?T-10')
            elif manualMove == "l10":
                if whichCamSerial == 1:
                    self.sendSerial('&??P-10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?P-10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?P-10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?P-10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?P-10')
            elif manualMove == "l1":
                if whichCamSerial == 1:
                    self.sendSerial('&??P-0.5')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?P-0.5')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?P-0.5')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?P-0.5')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?P-0.5')
            elif manualMove == "r1":
                if whichCamSerial == 1:
                    self.sendSerial('&??P0.5')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?P0.5')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?P0.5')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?P0.5')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?P0.5')
            elif manualMove == "r10":
                if whichCamSerial == 1:
                    self.sendSerial('&??P10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?P10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?P10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?P10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?P10')
            elif manualMove == "sl100":
                if whichCamSerial == 1:
                    self.sendSerial('&??X-100')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?X-100')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?X-100')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?X-100')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?X-100')
            elif manualMove == "sl10":
                if whichCamSerial == 1:
                    self.sendSerial('&??X-10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?X-10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?X-10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?X-10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?X-10')
            elif manualMove == "sr10":
                if whichCamSerial == 1:
                    self.sendSerial('&??X10')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?X10')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?X10')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?X10')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?X10')
            elif manualMove == "sr100":
                if whichCamSerial == 1:
                    self.sendSerial('&??X100')
                elif whichCamSerial == 2:
                    self.sendSerial('&!?X100')
                elif whichCamSerial == 3:
                    self.sendSerial('&@?X100')
                elif whichCamSerial == 4:
                    self.sendSerial('&&?X100')
                elif whichCamSerial == 5:
                    self.sendSerial('&*?X100')
                    
            manualMove = ""

        if newText != "":
            if editButton == 11: self.pushButton11.setText(newText)
            if editButton == 12: self.pushButton12.setText(newText)
            if editButton == 13: self.pushButton13.setText(newText)
            if editButton == 14: self.pushButton14.setText(newText)
            if editButton == 15: self.pushButton15.setText(newText)
            if editButton == 16: self.pushButton16.setText(newText)
            if editButton == 17: self.pushButton17.setText(newText)
            if editButton == 18: self.pushButton18.setText(newText)
            if editButton == 19: self.pushButton19.setText(newText)
            if editButton == 10: self.pushButton10.setText(newText)

            if editButton == 21: self.pushButton21.setText(newText)
            if editButton == 22: self.pushButton22.setText(newText)
            if editButton == 23: self.pushButton23.setText(newText)
            if editButton == 24: self.pushButton24.setText(newText)
            if editButton == 25: self.pushButton25.setText(newText)
            if editButton == 26: self.pushButton26.setText(newText)
            if editButton == 27: self.pushButton27.setText(newText)
            if editButton == 28: self.pushButton28.setText(newText)
            if editButton == 29: self.pushButton29.setText(newText)
            if editButton == 20: self.pushButton20.setText(newText)

            if editButton == 31: self.pushButton31.setText(newText)
            if editButton == 32: self.pushButton32.setText(newText)
            if editButton == 33: self.pushButton33.setText(newText)
            if editButton == 34: self.pushButton34.setText(newText)
            if editButton == 35: self.pushButton35.setText(newText)
            if editButton == 36: self.pushButton36.setText(newText)
            if editButton == 37: self.pushButton37.setText(newText)
            if editButton == 38: self.pushButton38.setText(newText)
            if editButton == 39: self.pushButton39.setText(newText)
            if editButton == 30: self.pushButton30.setText(newText)

            if editButton == 41: self.pushButton41.setText(newText)
            if editButton == 42: self.pushButton42.setText(newText)
            if editButton == 43: self.pushButton43.setText(newText)
            if editButton == 44: self.pushButton44.setText(newText)
            if editButton == 45: self.pushButton45.setText(newText)
            if editButton == 46: self.pushButton46.setText(newText)
            if editButton == 47: self.pushButton47.setText(newText)
            if editButton == 48: self.pushButton48.setText(newText)
            if editButton == 49: self.pushButton49.setText(newText)
            if editButton == 40: self.pushButton40.setText(newText)

            if editButton == 51: self.pushButton51.setText(newText)
            if editButton == 52: self.pushButton52.setText(newText)
            if editButton == 53: self.pushButton53.setText(newText)
            if editButton == 54: self.pushButton54.setText(newText)
            if editButton == 55: self.pushButton55.setText(newText)
            if editButton == 56: self.pushButton56.setText(newText)
            if editButton == 57: self.pushButton57.setText(newText)
            if editButton == 58: self.pushButton58.setText(newText)
            if editButton == 59: self.pushButton59.setText(newText)
            if editButton == 50: self.pushButton50.setText(newText)

            if editButton == 61: 
                cam1Label = newText
                self.pushButtonCam1.setText(cam1Label)
            if editButton == 62: 
                cam2Label = newText
                self.pushButtonCam2.setText(cam2Label)
            if editButton == 63: 
                cam3Label = newText
                self.pushButtonCam3.setText(cam3Label)
            if editButton == 64: 
                cam4Label = newText
                self.pushButtonCam4.setText(cam4Label)
            if editButton == 65: 
                cam5Label = newText
                self.pushButtonCam5.setText(cam5Label)

            newText = ""
            
    def resetMessage(self):
        self.labelInfo.setText("")

    def setPos(self, state):
        global SetPosToggle
        global editToggle
        global cam1Label
        global cam2Label
        global cam3Label
        global cam4Label
        global cam5Label
        
        if (SetPosToggle == True and state == 3) or state == 0:
            SetPosToggle = False
            editToggle = False
            self.pushButtonSet.setStyleSheet("border: 4px solid grey; background-color: #bbbbbb; border-radius: 10px;")
            self.pushButtonCam1.setText(cam1Label)
            self.pushButtonCam2.setText(cam2Label)
            self.pushButtonCam3.setText(cam3Label)
            self.pushButtonCam4.setText(cam4Label)
            self.pushButtonCam5.setText(cam5Label)
            self.pushButtonEdit.setText("Edit")
            self.pushButtonEdit.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
            self.pushButtonExit.hide()
            self.pushButtonLED.hide()
            self.pushButtonFileLoad.hide()
            self.pushButtonFileSave.hide()
            self.pushButtonSettings.hide()
            self.pushButtonSLonly.show()
            self.labelFilename.setHidden(True)
        elif (SetPosToggle == False and state == 3) or state == 1:
            SetPosToggle = True
            editToggle = False
            self.pushButtonSet.setStyleSheet("border: 4px solid #ff0000; background-color: #CC5050; border-radius: 10px;")
            self.pushButtonCam1.setText("Clear")
            self.pushButtonCam2.setText("Clear")
            self.pushButtonCam3.setText("Clear")
            self.pushButtonCam4.setText("Clear")
            self.pushButtonCam5.setText("Clear")
            self.pushButtonEdit.setText("Move")
            self.pushButtonEdit.setStyleSheet("border: 4px solid #FFFC67; background-color: #F7BA00; border-radius: 10px;")
            self.pushButtonExit.show()
            self.pushButtonLED.show()
            self.pushButtonFileLoad.show()
            self.pushButtonFileSave.show()
            self.pushButtonSettings.show()
            self.pushButtonSLonly.hide()
            self.labelFilename.setHidden(False)


    def whichCamSerial1(self):
        global whichCamSerial
        global SetPosToggle
        global editToggle
        global editButton

        if editToggle:
            editButton = 61
            currentText = self.pushButtonCam1.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1D')
        else:
            whichCamSerial = 1
            self.pushButtonCam1.setStyleSheet("border: 4px solid red; background-color: #4C8A4C; border-radius: 10px;")
            self.pushButtonCam2.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
            self.pushButtonCam3.setStyleSheet("border: 4px solid grey; background-color: #807100; border-radius: 10px;")
            self.pushButtonCam4.setStyleSheet("border: 4px solid grey; background-color: #008071; border-radius: 10px;")
            self.pushButtonCam5.setStyleSheet("border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def whichCamSerial2(self):
        global whichCamSerial
        global SetPosToggle
        global editToggle
        global editButton

        if editToggle:
            editButton = 62
            currentText = self.pushButtonCam2.text()
            self.openEditWindow(currentText)
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2D')
        else:
            whichCamSerial = 2
            self.pushButtonCam1.setStyleSheet("border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
            self.pushButtonCam2.setStyleSheet("border: 4px solid red; background-color: #405C80; border-radius: 10px;")
            self.pushButtonCam3.setStyleSheet("border: 4px solid grey; background-color: #807100; border-radius: 10px;")
            self.pushButtonCam4.setStyleSheet("border: 4px solid grey; background-color: #008071; border-radius: 10px;")
            self.pushButtonCam5.setStyleSheet("border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def whichCamSerial3(self):
        global whichCamSerial
        global SetPosToggle
        global editToggle
        global editButton

        if editToggle:
            editButton = 63
            currentText = self.pushButtonCam3.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3D')
        else:
            whichCamSerial = 3
            self.pushButtonCam1.setStyleSheet("border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
            self.pushButtonCam2.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
            self.pushButtonCam3.setStyleSheet("border: 4px solid red; background-color: #807100; border-radius: 10px;")
            self.pushButtonCam4.setStyleSheet("border: 4px solid grey; background-color: #008071; border-radius: 10px;")
            self.pushButtonCam5.setStyleSheet("border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def whichCamSerial4(self):
        global whichCamSerial
        global SetPosToggle
        global editToggle
        global editButton

        if editToggle:
            editButton = 64
            currentText = self.pushButtonCam4.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4D')
        else:
            whichCamSerial = 4
            self.pushButtonCam1.setStyleSheet("border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
            self.pushButtonCam2.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
            self.pushButtonCam3.setStyleSheet("border: 4px solid grey; background-color: #807100; border-radius: 10px;")
            self.pushButtonCam4.setStyleSheet("border: 4px solid red; background-color: #008071; border-radius: 10px;")
            self.pushButtonCam5.setStyleSheet("border: 4px solid grey; background-color: #8D5395; border-radius: 10px;")

    def whichCamSerial5(self):
        global whichCamSerial
        global SetPosToggle
        global editToggle
        global editButton

        if editToggle:
            editButton = 65
            currentText = self.pushButtonCam5.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5D')
        else:
            whichCamSerial = 5
            self.pushButtonCam1.setStyleSheet("border: 4px solid grey; background-color: #4C8A4C; border-radius: 10px;")
            self.pushButtonCam2.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px;")
            self.pushButtonCam3.setStyleSheet("border: 4px solid grey; background-color: #807100; border-radius: 10px;")
            self.pushButtonCam4.setStyleSheet("border: 4px solid grey; background-color: #008071; border-radius: 10px;")
            self.pushButtonCam5.setStyleSheet("border: 4px solid red; background-color: #8D5395; border-radius: 10px;")


    def Cam1Go1(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos1Set
        global cam1AtPos1

        if editToggle:
            editButton = 11
            currentText = self.pushButton11.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1Z')
            return
        elif cam1Pos1Set and not cam1AtPos1:
            self.sendSerial('&1z')

    def Cam1Go2(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos2Set
        global cam1AtPos2

        if editToggle:
            editButton = 12
            currentText = self.pushButton12.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1X')
            return
        elif cam1Pos2Set and not cam1AtPos2:
            self.sendSerial('&1x')

    def Cam1Go3(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos3Set
        global cam1AtPos3

        if editToggle:
            editButton = 13
            currentText = self.pushButton13.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1C')
            return
        elif cam1Pos3Set and not cam1AtPos3:
            self.sendSerial('&1c')

    def Cam1Go4(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos4Set
        global cam1AtPos4

        if editToggle:
            editButton = 14
            currentText = self.pushButton14.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1V')
            return
        elif cam1Pos4Set and not cam1AtPos4:
            self.sendSerial('&1v')

    def Cam1Go5(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos5Set
        global cam1AtPos5

        if editToggle:
            editButton = 15
            currentText = self.pushButton15.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1B')
            return
        elif cam1Pos5Set and not cam1AtPos5:
            self.sendSerial('&1b')

    def Cam1Go6(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos6Set
        global cam1AtPos6

        if editToggle:
            editButton = 16
            currentText = self.pushButton16.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1N')
            return
        elif cam1Pos6Set and not cam1AtPos6:
            self.sendSerial('&1n')

    def Cam1Go7(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos7Set
        global cam1AtPos7

        if editToggle:
            editButton = 17
            currentText = self.pushButton17.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1M')
            return
        elif cam1Pos7Set and not cam1AtPos7:
            self.sendSerial('&1m')

    def Cam1Go8(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos8Set
        global cam1AtPos8

        if editToggle:
            editButton = 18
            currentText = self.pushButton18.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1<')
            return
        elif cam1Pos8Set and not cam1AtPos8:
            self.sendSerial('&1,')

    def Cam1Go9(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos9Set
        global cam1AtPos9

        if editToggle:
            editButton = 19
            currentText = self.pushButton19.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1>')
            return
        elif cam1Pos9Set and not cam1AtPos9:
            self.sendSerial('&1.')

    def Cam1Go10(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam1Pos10Set
        global cam1AtPos10

        if editToggle:
            editButton = 10
            currentText = self.pushButton10.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1?')
            return
        elif cam1Pos10Set and not cam1AtPos10:
            self.sendSerial('&1/')

    def Cam2Go1(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos1Set
        global cam2AtPos1

        if editToggle:
            editButton = 21
            currentText = self.pushButton21.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2Z')
            return
        elif cam2Pos1Set and not cam2AtPos1:
            self.sendSerial('&2z')

    def Cam2Go2(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos2Set
        global cam2AtPos2

        if editToggle:
            editButton = 22
            currentText = self.pushButton22.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2X')
            return
        elif cam2Pos2Set and not cam2AtPos2:
            self.sendSerial('&2x')

    def Cam2Go3(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos3Set
        global cam2AtPos3

        if editToggle:
            editButton = 23
            currentText = self.pushButton23.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2C')
            return
        elif cam2Pos3Set and not cam2AtPos3:
            self.sendSerial('&2c')

    def Cam2Go4(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos4Set
        global cam2AtPos4

        if editToggle:
            editButton = 24
            currentText = self.pushButton24.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2V')
            return
        elif cam2Pos4Set and not cam2AtPos4:
            self.sendSerial('&2v')

    def Cam2Go5(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos5Set
        global cam2AtPos5

        if editToggle:
            editButton = 25
            currentText = self.pushButton25.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2B')
            return
        elif cam2Pos5Set and not cam2AtPos5:
            self.sendSerial('&2b')

    def Cam2Go6(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos6Set
        global cam2AtPos6

        if editToggle:
            editButton = 26
            currentText = self.pushButton26.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2N')
            return
        elif cam2Pos6Set and not cam2AtPos6:
            self.sendSerial('&2n')

    def Cam2Go7(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos7Set
        global cam2AtPos7

        if editToggle:
            editButton = 27
            currentText = self.pushButton27.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2M')
            return
        elif cam2Pos7Set and not cam2AtPos7:
            self.sendSerial('&2m')

    def Cam2Go8(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos8Set
        global cam2AtPos8

        if editToggle:
            editButton = 28
            currentText = self.pushButton28.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2<')
            return
        elif cam2Pos8Set and not cam2AtPos8:
            self.sendSerial('&2,')

    def Cam2Go9(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos9Set
        global cam2AtPos9

        if editToggle:
            editButton = 29
            currentText = self.pushButton29.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2>')
            return
        elif cam2Pos9Set and not cam2AtPos9:
            self.sendSerial('&2.')

    def Cam2Go10(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam2Pos10Set
        global cam2AtPos10

        if editToggle:
            editButton = 20
            currentText = self.pushButton20.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2?')
            return
        elif cam2Pos10Set and not cam2AtPos10:
            self.sendSerial('&2/')

    def Cam3Go1(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos1Set
        global cam3AtPos1

        if editToggle:
            editButton = 31
            currentText = self.pushButton31.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3Z')
            return
        elif cam3Pos1Set and not cam3AtPos1:
            self.sendSerial('&3z')

    def Cam3Go2(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos2Set
        global cam3AtPos2

        if editToggle:
            editButton = 32
            currentText = self.pushButton32.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3X')
            return
        elif cam3Pos2Set and not cam3AtPos2:
            self.sendSerial('&3x')

    def Cam3Go3(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos3Set
        global cam3AtPos3

        if editToggle:
            editButton = 33
            currentText = self.pushButton33.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3C')
            return
        elif cam3Pos3Set and not cam3AtPos3:
            self.sendSerial('&3c')

    def Cam3Go4(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos4Set
        global cam3AtPos4

        if editToggle:
            editButton = 34
            currentText = self.pushButton34.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3V')
            return
        elif cam3Pos4Set and not cam3AtPos4:
            self.sendSerial('&3v')

    def Cam3Go5(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos5Set
        global cam3AtPos5

        if editToggle:
            editButton = 35
            currentText = self.pushButton35.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3B')
            return
        elif cam3Pos5Set and not cam3AtPos5:
            self.sendSerial('&3b')

    def Cam3Go6(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos6Set
        global cam3AtPos6

        if editToggle:
            editButton = 36
            currentText = self.pushButton36.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3N')
            return
        elif cam3Pos6Set and not cam3AtPos6:
            self.sendSerial('&3n')

    def Cam3Go7(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos7Set
        global cam3AtPos7

        if editToggle:
            editButton = 37
            currentText = self.pushButton37.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3M')
            return
        elif cam3Pos7Set and not cam3AtPos7:
            self.sendSerial('&3m')

    def Cam3Go8(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos8Set
        global cam3AtPos8

        if editToggle:
            editButton = 38
            currentText = self.pushButton38.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3<')
            return
        elif cam3Pos8Set and not cam3AtPos8:
            self.sendSerial('&3,')

    def Cam3Go9(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos9Set
        global cam3AtPos9

        if editToggle:
            editButton = 39
            currentText = self.pushButton39.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3>')
            return
        elif cam3Pos9Set and not cam3AtPos9:
            self.sendSerial('&3.')

    def Cam3Go10(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam3Pos10Set
        global cam3AtPos10

        if editToggle:
            editButton = 30
            currentText = self.pushButton30.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3?')
            return
        elif cam3Pos10Set and not cam3AtPos10:
            self.sendSerial('&3/')

    def Cam4Go1(self):
        global SetPosToggle
        global editToggle
        global editButton
        global slideToggle
        global cam4Pos1Set
        global cam4AtPos1

        if editToggle:
            editButton = 41
            currentText = self.pushButton41.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4Z')
            return
        elif cam4Pos1Set and not cam4AtPos1 and not slideToggle:
            self.sendSerial('&4z')
        elif cam4Pos1Set and not cam4AtPos1 and slideToggle:
            self.sendSerial('&4y')

    def Cam4Go2(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos2Set
        global cam4AtPos2

        if editToggle:
            editButton = 42
            currentText = self.pushButton42.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4X')
            return
        elif cam4Pos2Set and not cam4AtPos2:
            self.sendSerial('&4x')

    def Cam4Go3(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos3Set
        global cam4AtPos3

        if editToggle:
            editButton = 43
            currentText = self.pushButton43.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4C')
            return
        elif cam4Pos3Set and not cam4AtPos3:
            self.sendSerial('&4c')

    def Cam4Go4(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos4Set
        global cam4AtPos4

        if editToggle:
            editButton = 44
            currentText = self.pushButton44.text()
            self.openEditWindow(currentText)
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4V')
            return
        elif cam4Pos4Set and not cam4AtPos4:
            self.sendSerial('&4v')

    def Cam4Go5(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos5Set
        global cam4AtPos5

        if editToggle:
            editButton = 45
            currentText = self.pushButton45.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4B')
            return
        elif cam4Pos5Set and not cam4AtPos5:
            self.sendSerial('&4b')

    def Cam4Go6(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos6Set
        global cam4AtPos6

        if editToggle:
            editButton = 46
            currentText = self.pushButton46.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4N')
            return
        elif cam4Pos6Set and not cam4AtPos6:
            self.sendSerial('&4n')

    def Cam4Go7(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos7Set
        global cam4AtPos7

        if editToggle:
            editButton = 47
            currentText = self.pushButton47.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4M')
            return
        elif cam4Pos7Set and not cam4AtPos7:
            self.sendSerial('&4m')

    def Cam4Go8(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos8Set
        global cam4AtPos8

        if editToggle:
            editButton = 48
            currentText = self.pushButton48.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4<')
            return
        elif cam4Pos8Set and not cam4AtPos8:
            self.sendSerial('&4,')

    def Cam4Go9(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos9Set
        global cam4AtPos9

        if editToggle:
            editButton = 49
            currentText = self.pushButton49.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4>')
            return
        elif cam4Pos9Set and not cam4AtPos9:
            self.sendSerial('&4.')

    def Cam4Go10(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam4Pos10Set
        global cam4AtPos10

        if editToggle:
            editButton = 40
            currentText = self.pushButton40.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4?')
            return
        elif cam4Pos10Set and not cam4AtPos10 and not slideToggle:
            self.sendSerial('&4/')
        elif cam4Pos10Set and not cam4AtPos10 and slideToggle:
            self.sendSerial('&4Y')

    def Cam5Go1(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos1Set
        global cam5AtPos1

        if editToggle:
            editButton = 51
            currentText = self.pushButton51.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5Z')
            return
        elif cam5Pos1Set and not cam5AtPos1 and not slideToggle:
            self.sendSerial('&5z')
        elif cam5Pos1Set and not cam5AtPos1 and slideToggle:
            self.sendSerial('&5y')

    def Cam5Go2(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos2Set
        global cam5AtPos2

        if editToggle:
            editButton = 52
            currentText = self.pushButton52.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5X')
            return
        elif cam5Pos2Set and not cam5AtPos2:
            self.sendSerial('&5x')

    def Cam5Go3(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos3Set
        global cam5AtPos3

        if editToggle:
            editButton = 53
            currentText = self.pushButton53.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5C')
            return
        elif cam5Pos3Set and not cam5AtPos3:
            self.sendSerial('&5c')

    def Cam5Go4(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos4Set
        global cam5AtPos4

        if editToggle:
            editButton = 54
            currentText = self.pushButton54.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5V')
            return
        elif cam5Pos4Set and not cam5AtPos4:
            self.sendSerial('&5v')

    def Cam5Go5(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos5Set
        global cam5AtPos5

        if editToggle:
            editButton = 55
            currentText = self.pushButton55.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5B')
            return
        elif cam5Pos5Set and not cam5AtPos5:
            self.sendSerial('&5b')

    def Cam5Go6(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos6Set
        global cam5AtPos6

        if editToggle:
            editButton = 56
            currentText = self.pushButton56.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5N')
            return
        elif cam5Pos6Set and not cam5AtPos6:
            self.sendSerial('&5n')

    def Cam5Go7(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos7Set
        global cam5AtPos7

        if editToggle:
            editButton = 57
            currentText = self.pushButton57.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5M')
            return
        elif cam5Pos7Set and not cam5AtPos7:
            self.sendSerial('&5m')

    def Cam5Go8(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos8Set
        global cam5AtPos8

        if editToggle:
            editButton = 58
            currentText = self.pushButton58.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5<')
            return
        elif cam5Pos8Set and not cam5AtPos8:
            self.sendSerial('&5,')

    def Cam5Go9(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos9Set
        global cam5AtPos9

        if editToggle:
            editButton = 59
            currentText = self.pushButton59.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5>')
            return
        elif cam5Pos9Set and not cam5AtPos9:
            self.sendSerial('&5.')

    def Cam5Go10(self):
        global SetPosToggle
        global editToggle
        global editButton
        global cam5Pos10Set
        global cam5AtPos10

        if editToggle:
            editButton = 50
            currentText = self.pushButton50.text()
            self.openEditWindow(currentText)
        elif SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5?')
            return
        elif cam5Pos10Set and not cam5AtPos10 and not slideToggle:
            self.sendSerial('&5/')
        elif cam5Pos10Set and not cam5AtPos10 and slideToggle:
            self.sendSerial('&5Y')

class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True

    def run(self):
        global debug
        global msg
        global serialLoop
        global sendData
        global moveCheckInterval
        global axisX
        global axisY
        global axisZ
        global axisW
        global oldAxisX
        global oldAxisY
        global oldAxisZ
        global oldAxisW
        global previousMillisMoveCheck
        global message

        try:
            self.serial_port = Serial(device_name, 38400, 8, 'N', 1, timeout=1)
            serialLoop = True
            message = (f"Connected to {device_name}")
        except:
            message = ("Couldn't connect")
            self.stop()

        sendData = ""
        sendData = '&-'
        while serialLoop:
            if not self.serial_port.is_open:
                serialLoop = False
            else:
                while (self.serial_port.in_waiting > 0):
                    received_msg = self.serial_port.readline()
                    msg = bytes(received_msg).decode('utf8', "ignore")
                    self.any_signal.emit(msg)
                    msg=''

                if sendData != "":
                    if debug:
                        print(sendData)

                    if type(sendData) is str:
                        data = bytes((sendData + '\n'), 'utf8')
                        try:
                            self.serial_port.write(data)
                        except Exception as error:
                            print("Didn't send button :(")
                            print(error)
                            self.stop()

                    elif type(sendData) is bytearray:
                        joyData = sendData
                        oldAxisX = axisX
                        oldAxisY = axisY
                        oldAxisZ = axisZ
                        try:
                            self.serial_port.write(sendData)
                            previousMillisMoveCheck = time.time()
                        except:
                            print("Didn't send joystick :(")
                            self.stop()

                    sendData = ""

                if (axisX == oldAxisX) and (axisY == oldAxisY) and (axisZ == oldAxisZ) and ((abs(axisX) + abs(axisY) + abs(axisZ)) != 0):
                    currentMillisMoveCheck = time.time()
                    if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval):
                        previousMillisMoveCheck = currentMillisMoveCheck
                        try:
                            self.serial_port.write(joyData)
                            previousMillisMoveCheck = time.time()
                            #print("Re-sending Joystick for keep-alive")    # debugging
                        except:
                            print("Didn't RE-send joystick :(")
                            self.stop()
                            
    def stop(self):
        self.is_running = False
        print("Stopping thread", self.index)
        self.terminate()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = PTSapp("")
    sys.exit(app.exec_())