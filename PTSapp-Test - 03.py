from operator import index
from PySide6.QtCore import Qt, QTimer, Signal, QThread, QObject
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QMainWindow, QFileDialog, QApplication #, QDesktopWidget
from PySide6.QtGui import *
from serial.tools import list_ports
from serial import Serial
import sys, time, os, subprocess, re, json, pkg_resources, pyjoystick
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from sys import platform
from pathlib import Path

class camera:
    active = False
    name = ""

    pos1Set = False
    pos2Set = False
    pos3Set = False
    pos4Set = False
    pos5Set = False
    pos6Set = False
    pos7Set = False
    pos8Set = False
    pos9Set = False
    pos10Set = False
    pos1Run = False
    pos2Run = False
    pos3Run = False
    pos4Run = False
    pos5Run = False
    pos6Run = False
    pos7Run = False
    pos8Run = False
    pos9Run = False
    pos10Run = False
    pos1At = False
    pos2At = False
    pos3At = False
    pos4At = False
    pos5At = False
    pos6At = False
    pos7At = False
    pos8At = False
    pos9At = False
    pos10At = False
    pos1OldSet = False
    pos2OldSet = False
    pos3OldSet = False
    pos4OldSet = False
    pos5OldSet = False
    pos6OldSet = False
    pos7OldSet = False
    pos8OldSet = False
    pos9OldSet = False
    pos10OldSet = False
    pos1OldRun = False
    pos2OldRun = False
    pos3OldRun = False
    pos4OldRun = False
    pos5OldRun = False
    pos6OldRun = False
    pos7OldRun = False
    pos8OldRun = False
    pos9OldRun = False
    pos10OldRun = False
    pos1OldAt = False
    pos2OldAt = False
    pos3OldAt = False
    pos4OldAt = False
    pos5OldAt = False
    pos6OldAt = False
    pos7OldAt = False
    pos8OldAt = False
    pos9OldAt = False
    pos10OldAt = False

    pos1Name = ""
    pos2Name = ""
    pos3Name = ""
    pos4Name = ""
    pos5Name = ""
    pos6Name = ""
    pos7Name = ""
    pos8Name = ""
    pos9Name = ""
    pos10Name = ""
    
    panTiltAccel = 0
    sliderAccel = 0
    panTiltSpeed = 0
    sliderSpeed = 0
    slideLimit = 0
    zoomLimit = 0

    panTiltSpeed1 = 0
    panTiltSpeed2 = 0
    panTiltSpeed3 = 0
    panTiltSpeed4 = 0
    sliderSpeed1 = 0
    sliderSpeed2 = 0
    sliderSpeed3 = 0
    sliderSpeed4 = 0

    panTiltSpeedOld = 0
    sliderSpeedOld = 0

    panTiltSpeed = 0
    sliderSpeed = 0

    hasSlider = False
    slideToggle = False

    running = False
    useSetSpeed = False

    revAxisX = False
    revAxisY = False
    revAxisZ = False
    revAxisW = False

camera1 = camera()
camera2 = camera()
camera3 = camera()
camera4 = camera()
camera5 = camera()

camera1.name = "Balcony"
camera2.name = "Left"
camera3.name = "Centre"
camera4.name = "Right"
camera5.name = "Slider"
winSize = 1

arr = []

class serialDeviceList():
    device_name_list = []
    usb_device_list = list_ports.comports()
    device_name_list = [port.device for port in usb_device_list]
    device_name_list.insert(0, '-')

    serialDevice = ""

serialPortList = serialDeviceList()
#print(serialPortList.device_name_list)

class serialConnect():
    def __init__(self, parent=None,index=0):
        super(serialConnect, self).__init__(parent)

    def __new__(self):
        serialDeviceList.serialDevice = serialDeviceList.serialDevice[0]

        if appSettings.debug:
            print("Selected device: ", serialDeviceList.serialDevice)
            print(serialPortList)

        self.startThread(self)

    def startThread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.serialMsg.connect(repceiveMsg)
        self.thread.start()

    def quitThread(self):
        #print("thread")
        appSettings.running = False

class joystickMoves():
    def doJoyMoves(self, dt):
        if ((appSettings.axisX != appSettings.oldAxisX) or (appSettings.axisY != appSettings.oldAxisY) or (appSettings.axisZ != appSettings.oldAxisZ) or (appSettings.axisW != appSettings.oldAxisW)): # or doKeyControlA or doKeyControlD or doKeyControlW or doKeyControlS or doKeyControlSL or doKeyControlSR) 
            appSettings.previousTime = time.time()
            appSettings.axisXh = joystickMoves.toHex(self, appSettings.axisX, 16)
            appSettings.axisYh = joystickMoves.toHex(self, appSettings.axisY, 16)
            appSettings.axisZh = joystickMoves.toHex(self, appSettings.axisZ, 16)
            appSettings.axisWh = joystickMoves.toHex(self, appSettings.axisW, 16)

            arr = [4, appSettings.axisZh, appSettings.axisXh, appSettings.axisYh, appSettings.axisWh]
            joystickMoves.sendJoystick(self, arr)
            appSettings.previousMillisMoveCheck = time.time()

    def sendJoystick(self, arr):
        sliderInt = int(arr[1], 16)
        panInt = int(arr[2], 16)
        tiltInt = int(arr[3], 16)
        zoomInt = int(arr[4], 16)

        appSettings.data[0] = 4
        
        if ((appSettings.whichCamSerial==1 and camera1.revAxisX) or (appSettings.whichCamSerial==2 and camera2.revAxisX) or (appSettings.whichCamSerial==3 and camera3.revAxisX) or (appSettings.whichCamSerial==4 and camera4.revAxisX) or (appSettings.whichCamSerial==5 and camera5.revAxisX)):
            panInt = -panInt
        if ((appSettings.whichCamSerial==1 and camera1.revAxisY) or (appSettings.whichCamSerial==2 and camera2.revAxisY) or (appSettings.whichCamSerial==3 and camera3.revAxisY) or (appSettings.whichCamSerial==4 and camera4.revAxisY) or (appSettings.whichCamSerial==5 and camera5.revAxisY)):
            tiltInt = -tiltInt
        if ((appSettings.whichCamSerial==1 and camera1.revAxisZ) or (appSettings.whichCamSerial==2 and camera2.revAxisZ) or (appSettings.whichCamSerial==3 and camera3.revAxisZ) or (appSettings.whichCamSerial==4 and camera4.revAxisZ) or (appSettings.whichCamSerial==5 and camera5.revAxisZ)):
            sliderInt = -sliderInt
        if ((appSettings.whichCamSerial==1 and camera1.revAxisW) or (appSettings.whichCamSerial==2 and camera2.revAxisW) or (appSettings.whichCamSerial==3 and camera3.revAxisW) or (appSettings.whichCamSerial==4 and camera4.revAxisW) or (appSettings.whichCamSerial==5 and camera5.revAxisW)):
            zoomInt = -zoomInt
        

        if ((sliderInt > 0) and (sliderInt < 256)):
            appSettings.data[1] = 0
            appSettings.data[2] = sliderInt
        elif sliderInt > 256:
            appSettings.data[1] = 255
            appSettings.data[2] = (sliderInt-65281)
        else:
            appSettings.data[1] = 0
            appSettings.data[2] = 0

        if ((panInt > 0) and (panInt < 256)):
            appSettings.data[3] = 0
            appSettings.data[4] = panInt
        elif panInt > 256:
            appSettings.data[3] = 255
            appSettings.data[4] = (panInt-65281)
        else:
            appSettings.data[3] = 0
            appSettings.data[4] = 0

        if ((tiltInt > 0) and (tiltInt < 256)):
            appSettings.data[5] = 0
            appSettings.data[6] = tiltInt
        elif tiltInt > 256:
            appSettings.data[5] = 255
            appSettings.data[6] = (tiltInt-65281)
        else:
            appSettings.data[5] = 0
            appSettings.data[6] = 0

        if ((zoomInt > 0) and (zoomInt < 256)):
            appSettings.data[7] = 0
            appSettings.data[8] = zoomInt
        elif zoomInt > 256:
            appSettings.data[7] = 255
            appSettings.data[8] = (zoomInt-65281)
        else:
            appSettings.data[7] = 0
            appSettings.data[8] = 0
        
        appSettings.data[9] = appSettings.whichCamSerial
        Worker.sendSerial(self, appSettings.data)
        
        if appSettings.whichCamSerial == 1 and (camera1.pos1At or camera1.pos2At or camera1.pos3At or camera1.pos4At or camera1.pos5At or camera1.pos6At or camera1.pos7At or camera1.pos8At or camera1.pos9At or camera1.pos10At):
            camera1.pos1At = False
            camera1.pos2At = False
            camera1.pos3At = False
            camera1.pos4At = False
            camera1.pos5At = False
            camera1.pos6At = False
            camera1.pos7At = False
            camera1.pos8At = False
            camera1.pos9At = False
            camera1.pos10At = False
            doButtonColours()
        elif appSettings.whichCamSerial == 1 and (camera2.pos1At or camera2.pos2At or camera2.pos3At or camera2.pos4At or camera2.pos5At or camera2.pos6At or camera2.pos7At or camera2.pos8At or camera2.pos9At or camera2.pos10At):
            camera2.pos1At = False
            camera2.pos2At = False
            camera2.pos3At = False
            camera2.pos4At = False
            camera2.pos5At = False
            camera2.pos6At = False
            camera2.pos7At = False
            camera2.pos8At = False
            camera2.pos9At = False
            camera2.pos10At = False
            doButtonColours()
        elif appSettings.whichCamSerial == 1 and (camera3.pos1At or camera3.pos2At or camera3.pos3At or camera3.pos4At or camera3.pos5At or camera3.pos6At or camera3.pos7At or camera3.pos8At or camera3.pos9At or camera3.pos10At):
            camera3.pos1At = False
            camera3.pos2At = False
            camera3.pos3At = False
            camera3.pos4At = False
            camera3.pos5At = False
            camera3.pos6At = False
            camera3.pos7At = False
            camera3.pos8At = False
            camera3.pos9At = False
            camera3.pos10At = False
            doButtonColours()
        elif appSettings.whichCamSerial == 1 and (camera4.pos1At or camera4.pos2At or camera4.pos3At or camera4.pos4At or camera4.pos5At or camera4.pos6At or camera4.pos7At or camera4.pos8At or camera4.pos9At or camera4.pos10At):
            camera4.pos1At = False
            camera4.pos2At = False
            camera4.pos3At = False
            camera4.pos4At = False
            camera4.pos5At = False
            camera4.pos6At = False
            camera4.pos7At = False
            camera4.pos8At = False
            camera4.pos9At = False
            camera4.pos10At = False
            doButtonColours()
        elif appSettings.whichCamSerial == 1 and (camera5.pos1At or camera5.pos2At or camera5.pos3At or camera5.pos4At or camera5.pos5At or camera5.pos6At or camera5.pos7At or camera5.pos8At or camera5.pos9At or camera5.pos10At):
            camera5.pos1At = False
            camera5.pos2At = False
            camera5.pos3At = False
            camera5.pos4At = False
            camera5.pos5At = False
            camera5.pos6At = False
            camera5.pos7At = False
            camera5.pos8At = False
            camera5.pos9At = False
            camera5.pos10At = False
            doButtonColours()


    def scale(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    def toHex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

class Worker(QtCore.QThread): #QObject):
    finished = Signal()
    serialMsg = Signal(bytes)

    def __init__(self, parent=None,index=0):
        super(Worker, self).__init__(parent)
        self.index=index
        self.is_running = True
        self.serial_port = None  # Persistent connection


    def sendSerial(self, command):
        # Use the persistent connection instead of opening a new one
        if self.serial_port is None or not self.serial_port.is_open:
            if appSettings.debug:
                print("Warning: Serial port not available for sendSerial()")
            return
            
        if type(command) is str:
            data = bytes((command + '\n'), 'utf8')
            try:
                self.serial_port.write(data)
                #if appSettings.debug:
                #    print("Serial Sent: ", data)
            except PermissionError as error:
                appSettings.message = ("COM port in use by another application")
                print(f"Permission Error: {error} - Try closing other serial applications or run as Administrator")
                if appSettings.running:
                    self.finished.emit()
                appSettings.running = False
            except Exception as error:
                appSettings.message = ("Couldn't connect")
                print(error)
                if appSettings.running:
                    self.finished.emit()
                appSettings.running = False
            finally:
                if serial_port is not None and serial_port.is_open:
                    serial_port.close()

        elif type(command) is bytearray:
            appSettings.joyData = command
            appSettings.oldAxisX = appSettings.axisX
            appSettings.oldAxisY = appSettings.axisY
            appSettings.oldAxisZ = appSettings.axisZ
            appSettings.oldAxisW = appSettings.axisW
            try:
                self.serial_port.write(command)
                appSettings.previousMillisMoveCheck = time.time()
                if appSettings.debug:
                    print("Serial Sent: ", command)
            except Exception as error:
                appSettings.message = ("Couldn't connect")
                if appSettings.running:
                    self.finished.emit()
                print("Didn't send joystick :(")
                appSettings.running = False

        command = ""

    def run(self):
        try:
            self.serial_port = Serial(serialDeviceList.serialDevice, 38400, 8, 'N', 1, timeout=1)
            time.sleep(0.1)  # Small delay to ensure port is ready
            appSettings.message = (f"Connected to {serialDeviceList.serialDevice}")
            index = PTSapp.comboBox.findText(serialDeviceList.serialDevice)
            PTSapp.comboBox.setCurrentIndex(index)
            appSettings.running = True
        except PermissionError as error:
            appSettings.message = ("COM port in use - Run as Administrator or close other applications")
            print(f"Permission Error: {error}")
            self.finished.emit()
            appSettings.running = False
            return
        except Exception as error:
            appSettings.message = ("Couldn't connect")
            print(f"Connection Error: {error}")
            self.finished.emit()
            appSettings.running = False
            return
        
        try:
            self.sendSerial('&-')
        except:
            pass

        while appSettings.running and self.serial_port is not None and self.serial_port.is_open:
            if self.serial_port.in_waiting > 0:
                received_msg = self.serial_port.readline()
                msg = bytes(received_msg).decode('utf8', "ignore")
                self.serialMsg.emit(msg)
                msg=''

            if (appSettings.axisX == appSettings.oldAxisX) and (appSettings.axisY == appSettings.oldAxisY) and (appSettings.axisZ == appSettings.oldAxisZ) and (appSettings.axisW == appSettings.oldAxisW) and ((abs(appSettings.axisX) + abs(appSettings.axisY) + abs(appSettings.axisZ) + abs(appSettings.axisW)) != 0):
                appSettings.currentMillisMoveCheck = time.time()
            if (appSettings.currentMillisMoveCheck - appSettings.previousMillisMoveCheck > appSettings.moveCheckInterval):
                appSettings.previousMillisMoveCheck = appSettings.currentMillisMoveCheck
                try:
                    self.serial_port.write(appSettings.joyData)
                    appSettings.previousMillisMoveCheck = time.time()
                    if appSettings.debug:
                        print("Re-sending Joystick for keep-alive")    # debugging
                except:
                    print("Didn't RE-send joystick :(")
                    #self.stop()

        # Cleanup: close the port when loop exits
        if self.serial_port is not None and self.serial_port.is_open:
            try:
                self.serial_port.close()
            except:
                pass

        self.finished.emit()
        
        self.stop()

    def stop(self):
        self.is_running = False
        Worker.exit
        QThread.exit
        
class PTSapp(QMainWindow):
    global agX
    global agY

    global butttonLayoutX
    global butttonLayoutY
    global buttonGoX
    global buttonGoY
    global buttonCamY
    global winSize

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
        self.setPos(3)
        self.ui3 = Ui_MoverWindow()
        self.ui3.setupUi()
    
    def openSettingsWindow(self):
        if appSettings.running:
            Worker.sendSerial(self, '&1K')
            Worker.sendSerial(self, '&2K')
            time.sleep(0.1)
            Worker.sendSerial(self, '&3K')
            time.sleep(0.1)
            Worker.sendSerial(self, '&4K')
            time.sleep(0.1)
            Worker.sendSerial(self, '&5K')

        self.setPos(3)
        self.ui4 = Ui_SettingsWindow()
        self.ui4.setupUi()

    def closeEvent(self, event):
        appSettings.running = False
        
    def setupUi(self):
        global butttonLayoutX
        global butttonLayoutY
        global buttonGoX
        global buttonGoY
        global borderSize
        global borderSize2
        global borderRadius
        global borderRadius2
        global buttonCamY
        global agX
        global agY
        global winSize

        self.setObjectName("PTSapp")

        ag = QtGui.QGuiApplication.primaryScreen().size()
        agX = ag.width()
        agY = ag.height()

        if appSettings.debug:
            agX = agX / 1.4
            agY = agY / 1.6

            print(agX)
            print(agY)

            self.resize(agX, agY)
        
        agY = agY * 0.97

        if sys.platform == "win32":
            #agY = agY * 0.96
            winSize = 0.75
        
        buttonGoX = agX * 0.0625        # 120,  120/1920
        buttonGoY = agY * 0.1111        # 120,  120/1080

        buttonCamY = agY * 0.06574       # 71,   71/1080

        butttonLayoutX = agX * 0.01042      # 20 / 1920
        butttonLayoutY = agY * 0.01852      # 20 / 1080

        borderSize = butttonLayoutX / 2
        borderSize2 = borderSize / 2
        borderRadius = butttonLayoutX * 1.8
        borderRadius2 = borderRadius * 0.5

        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 7, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        self.groupBox.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32; ")
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")

        self.serial_port = None
        self.thread = None

        def handle_key_event(key):
            #print(key, '-', key.keytype, '-', key.number, '-', key.value, '-', key.joystick)
            #keytest = key[1]
            #print(key.number)
            
            #print(key)

            joyName = str(key.joystick)
            joyName = joyName.lower()
            #print(joyName)

            joyType = str(key)

            deadRange = 0.15

            if re.search('xbox', joyName):
                #print(key.number)
                if joyType[-6:] == "Axis 3":
                    if (key.value < -deadRange):
                        appSettings.axisX = int(joystickMoves.scale(self, key.value, (-1, deadRange), (-255, 0)))
                    elif (key.value > deadRange):
                        appSettings.axisX = int(joystickMoves.scale(self, key.value, (1, -deadRange), (255, 0)))
                    else:
                        appSettings.axisX = 0
                    
                    #appSettings.axisX = int(self.scale(self, key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 4":
                    if (key.value < -deadRange):
                        appSettings.axisY = int(joystickMoves.scale(self, key.value, (-1, deadRange), (255, 0)))
                    elif (key.value > deadRange):
                        appSettings.axisY = int(joystickMoves.scale(self, key.value, (1, -deadRange), (-255, 0)))
                    else:
                        appSettings.axisY = 0

                    #appSettings.axisY = int(self.scale(self, key.value, (-1, 1), (255,-255)))
                elif joyType[-6:] == "Axis 0":
                    if (key.value < -deadRange):
                        appSettings.axisZ = int(joystickMoves.scale(self, key.value, (-1, deadRange), (-255, 0)))
                    elif (key.value > deadRange):
                        appSettings.axisZ = int(joystickMoves.scale(self, key.value, (1, -deadRange), (255, 0)))
                    else:
                        appSettings.axisZ = 0

                    #appSettings.axisZ = int(self.scale(self, key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 1":
                    if (key.value < -deadRange):
                        appSettings.axisW = int(joystickMoves.scale(self, key.value, (-1, (deadRange*2)), (255, 0)))
                    elif (key.value > deadRange):
                        appSettings.axisW = int(joystickMoves.scale(self, key.value, (1, -(deadRange*2)), (-255, 0)))
                    else:
                        appSettings.axisW = 0

                    #appSettings.axisW = int(self.scale(self, key.value, (-1, 1), (8,-8)))            
            else:
                if joyType[-6:] == "Axis 2":
                    if (key.value < -deadRange):
                        appSettings.axisX = int(joystickMoves.scale(self, key.value, (-1, deadRange), (-255, 0)))
                        if appSettings.axisX < -254:
                            appSettings.axisX = -254
                    elif (key.value > deadRange):
                        appSettings.axisX = int(joystickMoves.scale(self, key.value, (1, -deadRange), (255, 0)))
                        if appSettings.axisX > 254:
                            appSettings.axisX = 254
                    else:
                        appSettings.axisX = 0
                    
                    #appSettings.axisX = int(self.scale(self, key.value, (-1, 1), (-255,255)))
                elif joyType[-6:] == "Axis 3":
                    if (key.value < -deadRange):
                        appSettings.axisY = int(joystickMoves.scale(self, key.value, (-1, deadRange), (255, 0)))
                        if appSettings.axisY < -254:
                            appSettings.axisY = -254
                    elif (key.value > deadRange):
                        appSettings.axisY = int(joystickMoves.scale(self, key.value, (1, -deadRange), (-255, 0)))
                        if appSettings.axisY > 254:
                            appSettings.axisY = 254
                    else:
                        appSettings.axisY = 0

                    #appSettings.axisY = int(self.scale(self, key.value, (-1, 1), (255,-255)))
                elif joyType[-6:] == "Axis 0":
                    if (key.value < -deadRange):
                        appSettings.axisZ = int(joystickMoves.scale(self, key.value, (-1, deadRange), (-255, 0)))
                        if appSettings.axisZ < -254:
                            appSettings.axisZ = -254
                    elif (key.value > deadRange):
                        appSettings.axisZ = int(joystickMoves.scale(self, key.value, (1, -deadRange), (255, 0)))
                        if appSettings.axisZ > 254:
                            appSettings.axisZ= 254
                    else:
                        appSettings.axisZ = 0
                    #print(appSettings.axisZ)

                elif joyType[-6:] == "Axis 1":
                    if (key.value < -deadRange):
                        appSettings.axisW = int(joystickMoves.scale(self, key.value, (-1, (deadRange*2)), (255, 0)))
                    elif (key.value > deadRange):
                        appSettings.axisW = int(joystickMoves.scale(self, key.value, (1, -(deadRange*2)), (-255, 0)))
                    else:
                        appSettings.axisW = 0

            joystickMoves.doJoyMoves(self, 1)


        mngr = pyjoystick.ThreadEventManager(event_loop=run_event_loop, handle_key_event=handle_key_event)
        mngr.start()

        borderSize = butttonLayoutX / 2
        borderRadius = butttonLayoutX * 1.8

        PTSapp.pushButton11 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go1())
        PTSapp.pushButton11.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton11.setFont(font)
        PTSapp.pushButton11.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton11.setFlat(False)
        PTSapp.pushButton11.setObjectName("pushButton11")
        PTSapp.pushButton12 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go2())
        PTSapp.pushButton12.setGeometry(QtCore.QRect(butttonLayoutX * 8, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton12.setFont(font)
        PTSapp.pushButton12.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton12.setFlat(False)
        PTSapp.pushButton12.setObjectName("pushButton12")
        PTSapp.pushButton13 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go3())
        PTSapp.pushButton13.setGeometry(QtCore.QRect(buttonGoX * 2.5, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton13.setFont(font)
        PTSapp.pushButton13.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton13.setFlat(False)
        PTSapp.pushButton13.setObjectName("pushButton13")
        PTSapp.pushButton14 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go4())
        PTSapp.pushButton14.setGeometry(QtCore.QRect(butttonLayoutX * 22, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton14.setFont(font)
        PTSapp.pushButton14.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton14.setFlat(False)
        PTSapp.pushButton14.setObjectName("pushButton14")
        PTSapp.pushButton15 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go5())
        PTSapp.pushButton15.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton15.setFont(font)
        PTSapp.pushButton15.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton15.setFlat(False)
        PTSapp.pushButton15.setObjectName("pushButton15")
        PTSapp.pushButton16 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go6())
        PTSapp.pushButton16.setGeometry(QtCore.QRect(butttonLayoutX * 36, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton16.setFont(font)
        PTSapp.pushButton16.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton16.setFlat(False)
        PTSapp.pushButton16.setObjectName("pushButton16")
        PTSapp.pushButton17 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go7())
        PTSapp.pushButton17.setGeometry(QtCore.QRect(butttonLayoutX * 43, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton17.setFont(font)
        PTSapp.pushButton17.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton17.setFlat(False)
        PTSapp.pushButton17.setObjectName("pushButton17")
        PTSapp.pushButton18 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go8())
        PTSapp.pushButton18.setGeometry(QtCore.QRect(butttonLayoutX * 50, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton18.setFont(font)
        PTSapp.pushButton18.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton18.setFlat(False)
        PTSapp.pushButton18.setObjectName("pushButton18")
        PTSapp.pushButton19 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go9())
        PTSapp.pushButton19.setGeometry(QtCore.QRect(butttonLayoutX * 57, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton19.setFont(font)
        PTSapp.pushButton19.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton19.setFlat(False)
        PTSapp.pushButton19.setObjectName("pushButton19")
        PTSapp.pushButton10 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1Go10())
        PTSapp.pushButton10.setGeometry(QtCore.QRect(butttonLayoutX * 64, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton10.setFont(font)
        PTSapp.pushButton10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;")
        PTSapp.pushButton10.setFlat(False)
        PTSapp.pushButton10.setObjectName("pushButton10")
        PTSapp.dial1p = QtWidgets.QDial(self.groupBox, sliderPressed= lambda: self.setDials(1, 1, PTSapp.dial1p.value()))
        PTSapp.dial1p.setGeometry(QtCore.QRect(butttonLayoutX * 75, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))
        PTSapp.dial1p.setStyleSheet("background: black;")
        PTSapp.dial1p.setMinimum(1)
        PTSapp.dial1p.setMaximum(4)
        #self.dial1p.setInvertedAppearance(False)
        #self.dial1p.setInvertedControls(False)
        PTSapp.dial1p.setWrapping(False)
        PTSapp.dial1p.setNotchTarget(11.7)
        PTSapp.dial1p.setNotchesVisible(True)
        PTSapp.dial1p.setObjectName("dial1p")
        PTSapp.dial1s = QtWidgets.QDial(self.groupBox, sliderPressed= lambda: self.setDials(1, 2, PTSapp.dial1s.value()))
        PTSapp.dial1s.setGeometry(QtCore.QRect(butttonLayoutX * 83.5, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))
        PTSapp.dial1s.setStyleSheet("background: black;")
        PTSapp.dial1s.setMinimum(1)
        PTSapp.dial1s.setMaximum(4)
        PTSapp.dial1s.setNotchTarget(11.7)
        PTSapp.dial1s.setNotchesVisible(True)
        PTSapp.dial1s.setObjectName("dial1s")
        PTSapp.line1p = QtWidgets.QFrame(self.groupBox)
        PTSapp.line1p.setGeometry(QtCore.QRect(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        PTSapp.line1p.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line1p.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line1p.setLineWidth(20)
        PTSapp.line1p.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line1p.setObjectName("line1p")
        PTSapp.line1s = QtWidgets.QFrame(self.groupBox)
        PTSapp.line1s.setGeometry(QtCore.QRect(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0))
        PTSapp.line1s.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line1s.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line1s.setLineWidth(20)
        PTSapp.line1s.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line1s.setObjectName("line1s")
        PTSapp.pushButtonSetSpeedCam1 = QtWidgets.QPushButton(self.groupBox, clicked= lambda: self.Cam1SetSpeed())
        PTSapp.pushButtonSetSpeedCam1.setGeometry(QtCore.QRect(butttonLayoutX * 81.65, butttonLayoutY * 5.5, buttonGoX * 0.36, buttonGoY * 0.36))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1)
        PTSapp.pushButtonSetSpeedCam1.setFont(font)
        PTSapp.pushButtonSetSpeedCam1.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius*0.3}px;")
        PTSapp.pushButtonSetSpeedCam1.setFlat(False)
        PTSapp.pushButtonSetSpeedCam1.setObjectName("pushButtonSetSpeedCam1")

        PTSapp.groupBox11 = QtWidgets.QGroupBox(self.centralwidget)
        PTSapp.groupBox11.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 7, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        PTSapp.groupBox11.setStyleSheet(f"background-color: rgba(12, 12, 12, 120); border: {borderSize2}px solid #262d32;")
        PTSapp.groupBox11.setTitle("")
        PTSapp.groupBox11.setObjectName("groupBox11")

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 15.5, (butttonLayoutX * 94) +1, butttonLayoutY * 8))#(20, 310, 1881, 160))
        self.groupBox_2.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        PTSapp.pushButton21 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go1())
        PTSapp.pushButton21.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton21.setFont(font)
        PTSapp.pushButton21.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton21.setFlat(False)
        PTSapp.pushButton21.setObjectName("pushButton21")
        PTSapp.pushButton22 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go2())
        PTSapp.pushButton22.setGeometry(QtCore.QRect(butttonLayoutX * 8, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton22.setFont(font)
        PTSapp.pushButton22.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton22.setFlat(False)
        PTSapp.pushButton22.setObjectName("pushButton22")
        PTSapp.pushButton23 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go3())
        PTSapp.pushButton23.setGeometry(QtCore.QRect(buttonGoX * 2.5, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton23.setFont(font)
        PTSapp.pushButton23.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton23.setFlat(False)
        PTSapp.pushButton23.setObjectName("pushButton23")
        PTSapp.pushButton24 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go4())
        PTSapp.pushButton24.setGeometry(QtCore.QRect(butttonLayoutX * 22, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton24.setFont(font)
        PTSapp.pushButton24.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton24.setFlat(False)
        PTSapp.pushButton24.setObjectName("pushButton24")
        PTSapp.pushButton25 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go5())
        PTSapp.pushButton25.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton25.setFont(font)
        PTSapp.pushButton25.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton25.setFlat(False)
        PTSapp.pushButton25.setObjectName("pushButton25")
        PTSapp.pushButton26 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go6())
        PTSapp.pushButton26.setGeometry(QtCore.QRect(butttonLayoutX * 36, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton26.setFont(font)
        PTSapp.pushButton26.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton26.setFlat(False)
        PTSapp.pushButton26.setObjectName("pushButton26")
        PTSapp.pushButton27 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go7())
        PTSapp.pushButton27.setGeometry(QtCore.QRect(butttonLayoutX * 43, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton27.setFont(font)
        PTSapp.pushButton27.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton27.setFlat(False)
        PTSapp.pushButton27.setObjectName("pushButton27")
        PTSapp.pushButton28 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go8())
        PTSapp.pushButton28.setGeometry(QtCore.QRect(butttonLayoutX * 50, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton28.setFont(font)
        PTSapp.pushButton28.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton28.setFlat(False)
        PTSapp.pushButton28.setObjectName("pushButton28")
        PTSapp.pushButton29 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go9())
        PTSapp.pushButton29.setGeometry(QtCore.QRect(butttonLayoutX * 57, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton29.setFont(font)
        PTSapp.pushButton29.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton29.setFlat(False)
        PTSapp.pushButton29.setObjectName("pushButton29")
        PTSapp.pushButton20 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2Go10())
        PTSapp.pushButton20.setGeometry(QtCore.QRect(butttonLayoutX * 64, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton20.setFont(font)
        PTSapp.pushButton20.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        PTSapp.pushButton20.setFlat(False)
        PTSapp.pushButton20.setObjectName("pushButton20")
        PTSapp.dial2p = QtWidgets.QDial(self.groupBox_2, sliderPressed= lambda: self.setDials(2, 1, PTSapp.dial2p.value()))
        PTSapp.dial2p.setGeometry(QtCore.QRect(butttonLayoutX * 75, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))  #(1500, 10, 140, 140))
        PTSapp.dial2p.setStyleSheet("background: black;")
        PTSapp.dial2p.setMinimum(1)
        PTSapp.dial2p.setMaximum(4)
        PTSapp.dial2p.setTracking(True)
        PTSapp.dial2p.setInvertedAppearance(False)
        PTSapp.dial2p.setInvertedControls(False)
        PTSapp.dial2p.setWrapping(False)
        PTSapp.dial2p.setNotchTarget(11.7)
        PTSapp.dial2p.setNotchesVisible(True)
        PTSapp.dial2p.setObjectName("dial2p")
        PTSapp.dial2s = QtWidgets.QDial(self.groupBox_2, sliderPressed= lambda: self.setDials(2, 2, PTSapp.dial2s.value()))
        PTSapp.dial2s.setGeometry(QtCore.QRect(butttonLayoutX * 83.5, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))    #(1670, 10, 140, 140))
        PTSapp.dial2s.setStyleSheet("background: black;")
        PTSapp.dial2s.setMinimum(1)
        PTSapp.dial2s.setMaximum(4)
        PTSapp.dial2s.setNotchTarget(11.7)
        PTSapp.dial2s.setNotchesVisible(True)
        PTSapp.dial2s.setObjectName("dial2s")
        PTSapp.line2p = QtWidgets.QFrame(self.groupBox_2)
        PTSapp.line2p.setGeometry(QtCore.QRect(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0))   #(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        PTSapp.line2p.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line2p.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line2p.setLineWidth(20)
        PTSapp.line2p.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line2p.setObjectName("line2p")
        PTSapp.line2s = QtWidgets.QFrame(self.groupBox_2)
        PTSapp.line2s.setGeometry(QtCore.QRect(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)) #(1820, 115, 20, 36))
        PTSapp.line2s.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line2s.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line2s.setLineWidth(20)
        PTSapp.line2s.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line2s.setObjectName("line2s")
        PTSapp.pushButtonSetSpeedCam2 = QtWidgets.QPushButton(self.groupBox_2, clicked= lambda: self.Cam2SetSpeed())
        PTSapp.pushButtonSetSpeedCam2.setGeometry(QtCore.QRect(butttonLayoutX * 81.65, butttonLayoutY * 5.5, buttonGoX * 0.36, buttonGoY * 0.36))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1)
        PTSapp.pushButtonSetSpeedCam2.setFont(font)
        PTSapp.pushButtonSetSpeedCam2.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #405C80; border-radius: {borderRadius*0.3}px;")
        PTSapp.pushButtonSetSpeedCam2.setFlat(False)
        PTSapp.pushButtonSetSpeedCam2.setObjectName("pushButtonSetSpeedCam2")

        self.groupBox21 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox21.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 15.5, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        self.groupBox21.setStyleSheet(f"background-color: rgba(12, 12, 12, 120); border: {borderSize2}px solid #262d32;")
        self.groupBox21.setTitle("")
        self.groupBox21.setObjectName("groupBox21")

        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 24, (butttonLayoutX * 94) +1, butttonLayoutY * 8))#(20, 480, 1881, 160))
        self.groupBox_3.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32; ")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")
        PTSapp.pushButton31 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go1())
        PTSapp.pushButton31.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton31.setFont(font)
        PTSapp.pushButton31.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton31.setFlat(False)
        PTSapp.pushButton31.setObjectName("pushButton31")
        PTSapp.pushButton32 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go2())
        PTSapp.pushButton32.setGeometry(QtCore.QRect(butttonLayoutX * 8, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton32.setFont(font)
        PTSapp.pushButton32.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton32.setFlat(False)
        PTSapp.pushButton32.setObjectName("pushButton32")
        PTSapp.pushButton33 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go3())
        PTSapp.pushButton33.setGeometry(QtCore.QRect(buttonGoX * 2.5, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton33.setFont(font)
        PTSapp.pushButton33.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton33.setFlat(False)
        PTSapp.pushButton33.setObjectName("pushButton33")
        PTSapp.pushButton34 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go4())
        PTSapp.pushButton34.setGeometry(QtCore.QRect(butttonLayoutX * 22, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton34.setFont(font)
        PTSapp.pushButton34.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton34.setFlat(False)
        PTSapp.pushButton34.setObjectName("pushButton34")
        PTSapp.pushButton35 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go5())
        PTSapp.pushButton35.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton35.setFont(font)
        PTSapp.pushButton35.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton35.setFlat(False)
        PTSapp.pushButton35.setObjectName("pushButton35")
        PTSapp.pushButton36 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go6())
        PTSapp.pushButton36.setGeometry(QtCore.QRect(butttonLayoutX * 36, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton36.setFont(font)
        PTSapp.pushButton36.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton36.setFlat(False)
        PTSapp.pushButton36.setObjectName("pushButton36")
        PTSapp.pushButton37 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go7())
        PTSapp.pushButton37.setGeometry(QtCore.QRect(butttonLayoutX * 43, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton37.setFont(font)
        PTSapp.pushButton37.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton37.setFlat(False)
        PTSapp.pushButton37.setObjectName("pushButton37")
        PTSapp.pushButton38 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go8())
        PTSapp.pushButton38.setGeometry(QtCore.QRect(butttonLayoutX * 50, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton38.setFont(font)
        PTSapp.pushButton38.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton38.setFlat(False)
        PTSapp.pushButton38.setObjectName("pushButton38")
        PTSapp.pushButton39 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go9())
        PTSapp.pushButton39.setGeometry(QtCore.QRect(butttonLayoutX * 57, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton39.setFont(font)
        PTSapp.pushButton39.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton39.setFlat(False)
        PTSapp.pushButton39.setObjectName("pushButton39")
        PTSapp.pushButton30 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3Go10())
        PTSapp.pushButton30.setGeometry(QtCore.QRect(butttonLayoutX * 64, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton30.setFont(font)
        PTSapp.pushButton30.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        PTSapp.pushButton30.setFlat(False)
        PTSapp.pushButton30.setObjectName("pushButton30")
        PTSapp.dial3p = QtWidgets.QDial(self.groupBox_3, sliderPressed= lambda: self.setDials(3, 1, PTSapp.dial3p.value()))
        PTSapp.dial3p.setGeometry(QtCore.QRect(butttonLayoutX * 75, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))  #(1500, butttonLayoutY/2, 140, 140))
        PTSapp.dial3p.setStyleSheet("background: black;")
        PTSapp.dial3p.setMinimum(1)
        PTSapp.dial3p.setMaximum(4)
        PTSapp.dial3p.setInvertedAppearance(False)
        PTSapp.dial3p.setInvertedControls(False)
        PTSapp.dial3p.setWrapping(False)
        PTSapp.dial3p.setNotchTarget(11.7)
        PTSapp.dial3p.setNotchesVisible(True)
        PTSapp.dial3p.setObjectName("dial3p")
        PTSapp.dial3s = QtWidgets.QDial(self.groupBox_3, sliderPressed= lambda: self.setDials(3, 2, PTSapp.dial3s.value()))
        PTSapp.dial3s.setGeometry(QtCore.QRect(butttonLayoutX * 83.5, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))    #(1670, butttonLayoutY/2, 140, 140))
        PTSapp.dial3s.setStyleSheet("background: black;")
        PTSapp.dial3s.setMinimum(1)
        PTSapp.dial3s.setMaximum(4)
        PTSapp.dial3s.setNotchTarget(11.7)
        PTSapp.dial3s.setNotchesVisible(True)
        PTSapp.dial3s.setObjectName("dial3s")
        PTSapp.line3p = QtWidgets.QFrame(self.groupBox_3)
        PTSapp.line3p.setGeometry(QtCore.QRect(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0))   #(1470, 115, buttonGoX, buttonGoY * 1.8))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        PTSapp.line3p.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line3p.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line3p.setLineWidth(20)
        PTSapp.line3p.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line3p.setObjectName("line3p")
        PTSapp.line3s = QtWidgets.QFrame(self.groupBox_3)
        PTSapp.line3s.setGeometry(QtCore.QRect(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)) #(1820, 115, buttonGoX, buttonGoY * 1.8))
        PTSapp.line3s.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line3s.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line3s.setLineWidth(20)
        PTSapp.line3s.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line3s.setObjectName("line3s")
        PTSapp.pushButtonSetSpeedCam3 = QtWidgets.QPushButton(self.groupBox_3, clicked= lambda: self.Cam3SetSpeed())
        PTSapp.pushButtonSetSpeedCam3.setGeometry(QtCore.QRect(butttonLayoutX * 81.65, butttonLayoutY * 5.5, buttonGoX * 0.36, buttonGoY * 0.36))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1)
        PTSapp.pushButtonSetSpeedCam3.setFont(font)
        PTSapp.pushButtonSetSpeedCam3.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #807100; border-radius: {borderRadius*0.3}px;")
        PTSapp.pushButtonSetSpeedCam3.setFlat(False)
        PTSapp.pushButtonSetSpeedCam3.setObjectName("pushButtonSetSpeedCam3")

        self.groupBox31 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox31.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 24, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        self.groupBox31.setStyleSheet(f"background-color: rgba(12, 12, 12, 120); border: {borderSize2}px solid #262d32;")
        self.groupBox31.setTitle("")
        self.groupBox31.setObjectName("groupBox31")

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 32.5, (butttonLayoutX * 94) +1, butttonLayoutY * 8))#(20, 650, 1881, 160))
        self.groupBox_4.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32; ")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setObjectName("groupBox_4")
        PTSapp.pushButton41 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go1())
        PTSapp.pushButton41.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton41.setFont(font)
        PTSapp.pushButton41.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton41.setFlat(False)
        PTSapp.pushButton41.setObjectName("pushButton41")
        PTSapp.pushButton42 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go2())
        PTSapp.pushButton42.setGeometry(QtCore.QRect(butttonLayoutX * 8, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton42.setFont(font)
        PTSapp.pushButton42.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton42.setFlat(False)
        PTSapp.pushButton42.setObjectName("pushButton42")
        PTSapp.pushButton43 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go3())
        PTSapp.pushButton43.setGeometry(QtCore.QRect(buttonGoX * 2.5, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton43.setFont(font)
        PTSapp.pushButton43.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton43.setFlat(False)
        PTSapp.pushButton43.setObjectName("pushButton43")
        PTSapp.pushButton44 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go4())
        PTSapp.pushButton44.setGeometry(QtCore.QRect(butttonLayoutX * 22, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton44.setFont(font)
        PTSapp.pushButton44.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton44.setFlat(False)
        PTSapp.pushButton44.setObjectName("pushButton44")
        PTSapp.pushButton45 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go5())
        PTSapp.pushButton45.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton45.setFont(font)
        PTSapp.pushButton45.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton45.setFlat(False)
        PTSapp.pushButton45.setObjectName("pushButton45")
        PTSapp.pushButton46 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go6())
        PTSapp.pushButton46.setGeometry(QtCore.QRect(butttonLayoutX * 36, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton46.setFont(font)
        PTSapp.pushButton46.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton46.setFlat(False)
        PTSapp.pushButton46.setObjectName("pushButton46")
        PTSapp.pushButton47 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go7())
        PTSapp.pushButton47.setGeometry(QtCore.QRect(butttonLayoutX * 43, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton47.setFont(font)
        PTSapp.pushButton47.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton47.setFlat(False)
        PTSapp.pushButton47.setObjectName("pushButton47")
        PTSapp.pushButton48 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go8())
        PTSapp.pushButton48.setGeometry(QtCore.QRect(butttonLayoutX * 50, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton48.setFont(font)
        PTSapp.pushButton48.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton48.setFlat(False)
        PTSapp.pushButton48.setObjectName("pushButton48")
        PTSapp.pushButton49 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go9())
        PTSapp.pushButton49.setGeometry(QtCore.QRect(butttonLayoutX * 57, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton49.setFont(font)
        PTSapp.pushButton49.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton49.setFlat(False)
        PTSapp.pushButton49.setObjectName("pushButton49")
        PTSapp.pushButton40 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4Go10())
        PTSapp.pushButton40.setGeometry(QtCore.QRect(butttonLayoutX * 64, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton40.setFont(font)
        PTSapp.pushButton40.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;")
        PTSapp.pushButton40.setFlat(False)
        PTSapp.pushButton40.setObjectName("pushButton40")
        PTSapp.dial4p = QtWidgets.QDial(self.groupBox_4, sliderPressed= lambda: self.setDials(4, 1, PTSapp.dial4p.value()))
        PTSapp.dial4p.setGeometry(QtCore.QRect(butttonLayoutX * 75, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))  #(1500, 10, 140, 140))
        PTSapp.dial4p.setStyleSheet("background: black;")
        PTSapp.dial4p.setMinimum(1)
        PTSapp.dial4p.setMaximum(4)
        PTSapp.dial4p.setInvertedAppearance(False)
        PTSapp.dial4p.setInvertedControls(False)
        PTSapp.dial4p.setWrapping(False)
        PTSapp.dial4p.setNotchTarget(11.7)
        PTSapp.dial4p.setNotchesVisible(True)
        PTSapp.dial4p.setObjectName("dial4p")
        PTSapp.dial4s = QtWidgets.QDial(self.groupBox_4, sliderPressed= lambda: self.setDials(4, 2, PTSapp.dial4s.value()))
        PTSapp.dial4s.setGeometry(QtCore.QRect(butttonLayoutX * 83.5, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))    #(1670, 10, 140, 140))
        PTSapp.dial4s.setStyleSheet("background: black;")
        PTSapp.dial4s.setMinimum(1)
        PTSapp.dial4s.setMaximum(4)
        PTSapp.dial4s.setNotchTarget(11.7)
        PTSapp.dial4s.setNotchesVisible(True)
        PTSapp.dial4s.setObjectName("dial4s")
        PTSapp.line4p = QtWidgets.QFrame(self.groupBox_4)
        PTSapp.line4p.setGeometry(QtCore.QRect(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0))   #(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        PTSapp.line4p.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line4p.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line4p.setLineWidth(20)
        PTSapp.line4p.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line4p.setObjectName("line4p")
        PTSapp.line4s = QtWidgets.QFrame(self.groupBox_4)
        PTSapp.line4s.setGeometry(QtCore.QRect(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)) #(1820, 115, 20, 36))
        PTSapp.line4s.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line4s.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line4s.setLineWidth(20)
        PTSapp.line4s.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line4s.setObjectName("line4s")
        PTSapp.pushButtonSetSpeedCam4 = QtWidgets.QPushButton(self.groupBox_4, clicked= lambda: self.Cam4SetSpeed())
        PTSapp.pushButtonSetSpeedCam4.setGeometry(QtCore.QRect(butttonLayoutX * 81.65, butttonLayoutY * 5.5, buttonGoX * 0.36, buttonGoY * 0.36))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1)
        PTSapp.pushButtonSetSpeedCam4.setFont(font)
        PTSapp.pushButtonSetSpeedCam4.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #008071; border-radius: {borderRadius*0.3}px;")
        PTSapp.pushButtonSetSpeedCam4.setFlat(False)
        PTSapp.pushButtonSetSpeedCam4.setObjectName("pushButtonSetSpeedCam4")

        self.groupBox41 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox41.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 32.5, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        self.groupBox41.setStyleSheet(f"background-color: rgba(12, 12, 12, 120); border: {borderSize2}px solid #262d32;")
        self.groupBox41.setTitle("")
        self.groupBox41.setObjectName("groupBox41")

        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 41, (butttonLayoutX * 94) +1, butttonLayoutY * 8))#(20, 820, 1881, 160))
        self.groupBox_5.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32;")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setFlat(False)
        self.groupBox_5.setObjectName("groupBox_5")
        PTSapp.pushButton51 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go1())
        PTSapp.pushButton51.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton51.setFont(font)
        PTSapp.pushButton51.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton51.setFlat(False)
        PTSapp.pushButton51.setObjectName("pushButton51")
        PTSapp.pushButton52 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go2())
        PTSapp.pushButton52.setGeometry(QtCore.QRect(butttonLayoutX * 8, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton52.setFont(font)
        PTSapp.pushButton52.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton52.setFlat(False)
        PTSapp.pushButton52.setObjectName("pushButton52")
        PTSapp.pushButton53 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go3())
        PTSapp.pushButton53.setGeometry(QtCore.QRect(buttonGoX * 2.5, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton53.setFont(font)
        PTSapp.pushButton53.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton53.setFlat(False)
        PTSapp.pushButton53.setObjectName("pushButton53")
        PTSapp.pushButton54 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go4())
        PTSapp.pushButton54.setGeometry(QtCore.QRect(butttonLayoutX * 22, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton54.setFont(font)
        PTSapp.pushButton54.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton54.setFlat(False)
        PTSapp.pushButton54.setObjectName("pushButton54")
        PTSapp.pushButton55 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go5())
        PTSapp.pushButton55.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton55.setFont(font)
        PTSapp.pushButton55.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton55.setFlat(False)
        PTSapp.pushButton55.setObjectName("pushButton55")
        PTSapp.pushButton56 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go6())
        PTSapp.pushButton56.setGeometry(QtCore.QRect(butttonLayoutX * 36, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton56.setFont(font)
        PTSapp.pushButton56.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton56.setFlat(False)
        PTSapp.pushButton56.setObjectName("pushButton56")
        PTSapp.pushButton57 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go7())
        PTSapp.pushButton57.setGeometry(QtCore.QRect(butttonLayoutX * 43, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton57.setFont(font)
        PTSapp.pushButton57.setAutoFillBackground(False)
        PTSapp.pushButton57.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton57.setFlat(False)
        PTSapp.pushButton57.setObjectName("pushButton57")
        PTSapp.pushButton58 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go8())
        PTSapp.pushButton58.setGeometry(QtCore.QRect(butttonLayoutX * 50, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton58.setFont(font)
        PTSapp.pushButton58.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton58.setFlat(False)
        PTSapp.pushButton58.setObjectName("pushButton58")
        PTSapp.pushButton59 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go9())
        PTSapp.pushButton59.setGeometry(QtCore.QRect(butttonLayoutX * 57, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton59.setFont(font)
        PTSapp.pushButton59.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton59.setFlat(False)
        PTSapp.pushButton59.setObjectName("pushButton59")
        PTSapp.pushButton50 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5Go10())
        PTSapp.pushButton50.setGeometry(QtCore.QRect(butttonLayoutX * 64, butttonLayoutY, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButton50.setFont(font)
        PTSapp.pushButton50.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;")
        PTSapp.pushButton50.setFlat(False)
        PTSapp.pushButton50.setObjectName("pushButton50")
        PTSapp.dial5p = QtWidgets.QDial(self.groupBox_5, sliderPressed= lambda: self.setDials(5, 1, PTSapp.dial5p.value()))
        PTSapp.dial5p.setGeometry(QtCore.QRect(butttonLayoutX * 75, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))  #(1500, 10, 140, 140))
        PTSapp.dial5p.setStyleSheet("background: black;")
        PTSapp.dial5p.setMinimum(1)
        PTSapp.dial5p.setMaximum(4)
        PTSapp.dial5p.setInvertedAppearance(False)
        PTSapp.dial5p.setInvertedControls(False)
        PTSapp.dial5p.setWrapping(False)
        PTSapp.dial5p.setNotchTarget(11.7)
        PTSapp.dial5p.setNotchesVisible(True)
        PTSapp.dial5p.setObjectName("dial5p")
        PTSapp.dial5s = QtWidgets.QDial(self.groupBox_5, sliderPressed= lambda: self.setDials(5, 2, PTSapp.dial5s.value()))
        PTSapp.dial5s.setGeometry(QtCore.QRect(butttonLayoutX * 83.5, butttonLayoutY / 2, butttonLayoutX * 7, butttonLayoutY * 7))    #(1670, 10, 140, 140))
        PTSapp.dial5s.setStyleSheet("background: black;")
        PTSapp.dial5s.setMinimum(1)
        PTSapp.dial5s.setMaximum(4)
        PTSapp.dial5s.setNotchTarget(11.7)
        PTSapp.dial5s.setNotchesVisible(True)
        PTSapp.dial5s.setObjectName("dial5s")
        PTSapp.line5p = QtWidgets.QFrame(self.groupBox_5)
        PTSapp.line5p.setGeometry(QtCore.QRect(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0))   #(1470, 115, 20, 36))            #    1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
        PTSapp.line5p.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line5p.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line5p.setLineWidth(20)
        PTSapp.line5p.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line5p.setObjectName("line5p")
        PTSapp.line5s = QtWidgets.QFrame(self.groupBox_5)
        PTSapp.line5s.setGeometry(QtCore.QRect(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)) #(1820, 115, 20, 36))
        PTSapp.line5s.setStyleSheet(f"border: {borderSize}px solid #aaaa00;")
        PTSapp.line5s.setFrameShadow(QtWidgets.QFrame.Plain)
        PTSapp.line5s.setLineWidth(20)
        PTSapp.line5s.setFrameShape(QtWidgets.QFrame.VLine)
        PTSapp.line5s.setObjectName("line5s")
        PTSapp.pushButtonSetSpeedCam5 = QtWidgets.QPushButton(self.groupBox_5, clicked= lambda: self.Cam5SetSpeed())
        PTSapp.pushButtonSetSpeedCam5.setGeometry(QtCore.QRect(butttonLayoutX * 81.65, butttonLayoutY * 5.5, buttonGoX * 0.36, buttonGoY * 0.36))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1)
        PTSapp.pushButtonSetSpeedCam5.setFont(font)
        PTSapp.pushButtonSetSpeedCam5.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #8D5395; border-radius: {borderRadius*0.3}px;")
        PTSapp.pushButtonSetSpeedCam5.setFlat(False)
        PTSapp.pushButtonSetSpeedCam5.setObjectName("pushButtonSetSpeedCam5")

        self.groupBox51 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox51.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 41, (butttonLayoutX * 94) +1, butttonLayoutY * 8))
        self.groupBox51.setStyleSheet(f"background-color: rgba(12, 12, 12, 120); border: {borderSize2}px solid #262d32;")
        self.groupBox51.setTitle("")
        self.groupBox51.setObjectName("groupBox51")

        PTSapp.pushButtonCam1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial1())
        PTSapp.pushButtonCam1.setGeometry(QtCore.QRect(butttonLayoutX * 29, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        PTSapp.pushButtonCam1.setFont(font)
        PTSapp.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonCam1.setFlat(False)
        PTSapp.pushButtonCam1.setObjectName("pushButtonCam1")
        PTSapp.pushButtonCam2 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial2())
        PTSapp.pushButtonCam2.setGeometry(QtCore.QRect(butttonLayoutX * 37, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        PTSapp.pushButtonCam2.setFont(font)
        PTSapp.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonCam2.setFlat(False)
        PTSapp.pushButtonCam2.setObjectName("pushButtonCam2")
        PTSapp.pushButtonCam3 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial3())
        PTSapp.pushButtonCam3.setGeometry(QtCore.QRect(butttonLayoutX * 45, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        PTSapp.pushButtonCam3.setFont(font)
        PTSapp.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonCam3.setFlat(False)
        PTSapp.pushButtonCam3.setObjectName("pushButtonCam3")
        PTSapp.pushButtonCam4 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial4())
        PTSapp.pushButtonCam4.setGeometry(QtCore.QRect(butttonLayoutX * 53, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        PTSapp.pushButtonCam4.setFont(font)
        PTSapp.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonCam4.setFlat(False)
        PTSapp.pushButtonCam4.setObjectName("pushButtonCam4")
        PTSapp.pushButtonCam5 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.whichCamSerial5())
        PTSapp.pushButtonCam5.setGeometry(QtCore.QRect(butttonLayoutX * 61, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        PTSapp.pushButtonCam5.setFont(font)
        PTSapp.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonCam5.setFlat(False)
        PTSapp.pushButtonCam5.setObjectName("pushButtonCam5")



        self.labelDialPT = QtWidgets.QLabel(self.centralwidget)
        self.labelDialPT.setGeometry(QtCore.QRect(butttonLayoutX * 76.5, butttonLayoutY * 6, buttonGoX, butttonLayoutY * 0.8))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.8)
        self.labelDialPT.setFont(font)
        self.labelDialPT.setStyleSheet("color:grey;")
        self.labelDialPT.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDialPT.setObjectName("labelDialPT")

        self.labelDialSL = QtWidgets.QLabel(self.centralwidget)
        self.labelDialSL.setGeometry(QtCore.QRect(butttonLayoutX * 85.5, butttonLayoutY * 6, buttonGoX / 1.2, butttonLayoutY * 0.8))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.8)
        self.labelDialSL.setFont(font)
        self.labelDialSL.setStyleSheet("color:grey;")
        self.labelDialSL.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDialSL.setObjectName("labelDialSL")

        PTSapp.pushButtonSet = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.setPos(3))
        PTSapp.pushButtonSet.setGeometry(QtCore.QRect(butttonLayoutX * 88, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButtonSet.setFont(font)
        PTSapp.pushButtonSet.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #bbbbbb; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonSet.setFlat(False)
        PTSapp.pushButtonSet.setObjectName("pushButtonSet")
        PTSapp.pushButtonEdit = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.setEditToggle())
        PTSapp.pushButtonEdit.setGeometry(QtCore.QRect(butttonLayoutX * 2, butttonLayoutY * 1.5, buttonGoX, buttonCamY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButtonEdit.setFont(font)
        PTSapp.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonEdit.setFlat(False)
        PTSapp.pushButtonEdit.setObjectName("pushButtonEdit")
        PTSapp.pushButtonRun = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.runToggle())
        PTSapp.pushButtonRun.setGeometry(QtCore.QRect(butttonLayoutX * 74.5, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButtonRun.setFont(font)
        PTSapp.pushButtonRun.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonRun.setFlat(False)
        PTSapp.pushButtonRun.setObjectName("pushButtonRun")
        PTSapp.pushButtonSLonly = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.slideOnlyToggle())
        PTSapp.pushButtonSLonly.setGeometry(QtCore.QRect(butttonLayoutX * 87, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButtonSLonly.setFont(font)
        PTSapp.pushButtonSLonly.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonSLonly.setFlat(False)
        PTSapp.pushButtonSLonly.setObjectName("pushButtonSLonly")
        PTSapp.pushButtonFileLoad = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.fileLoad())
        PTSapp.pushButtonFileLoad.setGeometry(QtCore.QRect(butttonLayoutX * 2, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        self.pushButtonFileLoad.setFont(font)
        self.pushButtonFileLoad.setStyleSheet(f"border: {borderSize2}px solid #FFFC67; background-color: #33A000; border-radius: {borderRadius2}px;")
        self.pushButtonFileLoad.setFlat(False)
        self.pushButtonFileLoad.setObjectName("pushButtonFileLoad")
        self.pushButtonFileLoad.hide()
        self.pushButtonFileSave = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.fileSave())
        self.pushButtonFileSave.setGeometry(QtCore.QRect(butttonLayoutX * 16, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        self.pushButtonFileSave.setFont(font)
        self.pushButtonFileSave.setStyleSheet(f"border: {borderSize2}px solid #d74444; background-color: #F76666; border-radius: {borderRadius2}px;")
        self.pushButtonFileSave.setFlat(False)
        self.pushButtonFileSave.setObjectName("pushButtonFileSave")
        self.pushButtonFileSave.hide()
        PTSapp.pushButtonSettings = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.openSettingsWindow())
        PTSapp.pushButtonSettings.setGeometry(QtCore.QRect(butttonLayoutX * 51, butttonLayoutY * 49.5, buttonGoX * 2.17, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        PTSapp.pushButtonSettings.setFont(font)
        PTSapp.pushButtonSettings.setStyleSheet(f"border: {borderSize2}px solid #FFFC67; background-color: #33A000; border-radius: {borderRadius2}px;")
        PTSapp.pushButtonSettings.setFlat(False)
        PTSapp.pushButtonSettings.setObjectName("pushButtonSettings")
        PTSapp.pushButtonSettings.hide()
        self.pushButtonLED = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.resetButtonColours())
        self.pushButtonLED.setGeometry(QtCore.QRect(butttonLayoutX * 74.5, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        self.pushButtonLED.setFont(font)
        self.pushButtonLED.setStyleSheet(f"border: {borderSize2}px solid #FFFC67; background-color: #C39300; border-radius: {borderRadius2}px;")
        self.pushButtonLED.setFlat(False)
        self.pushButtonLED.setObjectName("pushButtonLED")
        self.pushButtonLED.hide()
        self.pushButtonExit = QtWidgets.QPushButton(self.centralwidget,  clicked= lambda: self.pushToClose())
        self.pushButtonExit.setGeometry(QtCore.QRect(butttonLayoutX * 87, butttonLayoutY * 49.5, buttonGoX, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2)
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setStyleSheet(f"border: {borderSize2}px solid #ff0000; background-color: #CC5050; border-radius: {borderRadius2}px;")
        self.pushButtonExit.setFlat(False)
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonExit.hide()
        self.labelFilename = QtWidgets.QLabel(self.centralwidget)
        self.labelFilename.setGeometry(QtCore.QRect(butttonLayoutX * 23, butttonLayoutY * 49.5, buttonGoX * 3.33333, buttonCamY * 0.7183))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.1)
        self.labelFilename.setFont(font)
        self.labelFilename.setStyleSheet(f"color: white; border: {borderSize2}px solid grey; background-color: #333333; border-radius: {borderRadius2}px;")
        self.labelFilename.setText("")
        self.labelFilename.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFilename.setObjectName("labelFilename")
        self.labelFilename.setHidden(True)
        PTSapp.labelInfo = QtWidgets.QLabel(self.centralwidget)
        PTSapp.labelInfo.setGeometry(QtCore.QRect(butttonLayoutX * 68, butttonLayoutY * 2.5, buttonGoX * 3.0917, buttonCamY * 0.6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.8)
        PTSapp.labelInfo.setFont(font)
        PTSapp.labelInfo.setStyleSheet(f"color: white; border: {borderSize2}px solid grey; background-color: #333333; border-radius: {borderRadius2}px;")
        PTSapp.labelInfo.setText("")
        PTSapp.labelInfo.setAlignment(QtCore.Qt.AlignCenter)
        PTSapp.labelInfo.setObjectName("labelInfo")
        PTSapp.comboBox = QtWidgets.QComboBox(self.centralwidget)
        PTSapp.comboBox.setGeometry(QtCore.QRect(butttonLayoutX * 9.5, butttonLayoutY * 2.5, buttonGoX * 3.0917, buttonCamY * 0.6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.1)
        PTSapp.comboBox.setFont(font)
        PTSapp.comboBox.setStyleSheet(f"color: white; border: {borderSize2}px solid grey; background-color: #333333; border-radius: {borderRadius2}px;")
        PTSapp.comboBox.setCurrentText("")
        PTSapp.comboBox.setObjectName("comboBox")
        PTSapp.comboBox.activated.connect(self.activated)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, agX, buttonCamY * 0.2))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuControl = QtWidgets.QMenu(self.menubar)
        self.menuControl.setObjectName("menuControl")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.buttonConnect(serialPortList.device_name_list)

        PTSapp.comboBox.addItems(serialPortList.device_name_list)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        #Timers()
        self.initFlashTimer()

    def activated(self):
        serialDeviceList.serialDevice= PTSapp.comboBox.currentText()
        serialPort = serialConnect()

    def retranslateUi(self):
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
        self.pushButtonCam1.setText(_translate("MainWindow", camera1.name))
        self.pushButtonCam2.setText(_translate("MainWindow", camera2.name))
        self.pushButtonCam3.setText(_translate("MainWindow", camera3.name))
        self.pushButtonCam4.setText(_translate("MainWindow", camera4.name))
        self.pushButtonCam5.setText(_translate("MainWindow", camera5.name))
        self.pushButtonSetSpeedCam1.setText(_translate("MainWindow", "SS"))
        self.pushButtonSetSpeedCam2.setText(_translate("MainWindow", "SS"))
        self.pushButtonSetSpeedCam3.setText(_translate("MainWindow", "SS"))
        self.pushButtonSetSpeedCam4.setText(_translate("MainWindow", "SS"))
        self.pushButtonSetSpeedCam5.setText(_translate("MainWindow", "SS"))
        self.labelDialPT.setText(_translate("MainWindow", "Pan/Tilt Speed"))
        self.labelDialSL.setText(_translate("MainWindow", "Slide Speed"))
        self.pushButtonSet.setText(_translate("MainWindow", "SET"))
        self.pushButtonEdit.setText(_translate("MainWindow", "Edit"))
        self.pushButtonRun.setText(_translate("MainWindow", "Run"))
        self.pushButtonSLonly.setText(_translate("MainWindow", "SL"))
        self.pushButtonFileLoad.setText(_translate("MainWindow", "Load"))
        self.pushButtonFileSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonSettings.setText(_translate("MainWindow", "Settings"))
        self.pushButtonLED.setText(_translate("MainWindow", "Reset"))
        self.pushButtonExit.setText(_translate("MainWindow", "Exit"))

        #self.initFlashTimer()

        #rt = Timers(10, flash)
        #QtCore.QTimer.singleShot(500,flash.run(self))
        #flash.run(self)

        #flashInit()

        if appSettings.debug:
            self.show()
        else:
            if sys.platform == "win32" or sys.platform == "linux":
                self.showFullScreen()
            else:
                self.showMaximized()

    def setDials(self, cam, ps, value):
        if cam == 1:
            if ps == 1:
                if value == 1: Worker.sendSerial(self, '&1s1')
                elif value == 2: Worker.sendSerial(self, '&1s2')
                elif value == 3: Worker.sendSerial(self, '&1s3')
                elif value == 4: Worker.sendSerial(self, '&1s4')
            else:
                if value == 1: Worker.sendSerial(self, '&1W1')
                elif value == 2: Worker.sendSerial(self, '&1W2')
                elif value == 3: Worker.sendSerial(self, '&1W3')
                elif value == 4: Worker.sendSerial(self, '&1W4')

        elif cam == 2:
            if ps == 1:
                if value == 1: Worker.sendSerial(self, '&2s1')
                elif value == 2: Worker.sendSerial(self, '&2s2')
                elif value == 3: Worker.sendSerial(self, '&2s3')
                elif value == 4: Worker.sendSerial(self, '&2s4')
            else:
                if value == 1: Worker.sendSerial(self, '&2W1')
                elif value == 2: Worker.sendSerial(self, '&2W2')
                elif value == 3: Worker.sendSerial(self, '&2W3')
                elif value == 4: Worker.sendSerial(self, '&2W4')

        elif cam == 3:
            if ps == 1:
                if value == 1: Worker.sendSerial(self, '&3s1')
                elif value == 2: Worker.sendSerial(self, '&3s2')
                elif value == 3: Worker.sendSerial(self, '&3s3')
                elif value == 4: Worker.sendSerial(self, '&3s4')
            else:
                if value == 1: Worker.sendSerial(self, '&3W1')
                elif value == 2: Worker.sendSerial(self, '&3W2')
                elif value == 3: Worker.sendSerial(self, '&3W3')
                elif value == 4: Worker.sendSerial(self, '&3W4')

        elif cam == 4:
            if ps == 1:
                if value == 1: Worker.sendSerial(self, '&4s1')
                elif value == 2: Worker.sendSerial(self, '&4s2')
                elif value == 3: Worker.sendSerial(self, '&4s3')
                elif value == 4: Worker.sendSerial(self, '&4s4')
            else:
                if value == 1: Worker.sendSerial(self, '&4W1')
                elif value == 2: Worker.sendSerial(self, '&4W2')
                elif value == 3: Worker.sendSerial(self, '&4W3')
                elif value == 4: Worker.sendSerial(self, '&4W4')

        elif cam == 5:
            if ps == 1:
                if value == 1: Worker.sendSerial(self, '&5s1')
                elif value == 2: Worker.sendSerial(self, '&5s2')
                elif value == 3: Worker.sendSerial(self, '&5s3')
                elif value == 4: Worker.sendSerial(self, '&5s4')
            else:
                if value == 1: Worker.sendSerial(self, '&5W1')
                elif value == 2: Worker.sendSerial(self, '&5W2')
                elif value == 3: Worker.sendSerial(self, '&5W3')
                elif value == 4: Worker.sendSerial(self, '&5W4')

    def setPos(self, state):
        appSettings.setState = state
        if (appSettings.setPosToggle == True and appSettings.setState == 3) or appSettings.setState == 0:
            appSettings.setPosToggle = False
            appSettings.editToggle = False
            self.pushButtonSet.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #bbbbbb; border-radius: {borderRadius2}px;")
            self.pushButtonCam1.setText(camera1.name)
            self.pushButtonCam2.setText(camera2.name)
            self.pushButtonCam3.setText(camera3.name)
            self.pushButtonCam4.setText(camera4.name)
            self.pushButtonCam5.setText(camera5.name)
            self.pushButtonEdit.setText("Edit")
            self.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonExit.hide()
            self.pushButtonLED.hide()
            self.pushButtonFileLoad.hide()
            self.pushButtonFileSave.hide()
            self.pushButtonSettings.hide()
            self.pushButtonRun.show()
            self.pushButtonSLonly.show()
            self.labelFilename.setHidden(True)
        elif (appSettings.setPosToggle == False and appSettings.setState == 3) or appSettings.setState == 1:
            appSettings.setPosToggle = True
            appSettings.editToggle = False
            self.pushButtonSet.setStyleSheet(f"border: {borderSize2}px solid #ff0000; background-color: #CC5050; border-radius: {borderRadius2}px;")
            self.pushButtonCam1.setText("Clear")
            self.pushButtonCam2.setText("Clear")
            self.pushButtonCam3.setText("Clear")
            self.pushButtonCam4.setText("Clear")
            self.pushButtonCam5.setText("Clear")
            PTSapp.pushButtonEdit.setText("Move")
            PTSapp.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid #FFFC67; background-color: #F7BA00; border-radius: {borderRadius2}px;")
            self.pushButtonExit.show()
            self.pushButtonLED.show()
            self.pushButtonFileLoad.show()
            self.pushButtonFileSave.show()
            self.pushButtonSettings.show()
            self.pushButtonRun.hide()
            self.pushButtonSLonly.hide()
            self.labelFilename.setHidden(False)

    def setEditToggle(self):
        if appSettings.setPosToggle:
            self.openMoverWindow()

        elif appSettings.editToggle == True:
            appSettings.editToggle = False
            self.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        else:
            appSettings.editToggle = True
            self.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #CC5050; border-radius: {borderRadius2}px;")

    def runToggle(self):
        if appSettings.runToggle == False:
            appSettings.runToggle = True
            self.pushButtonRun.setStyleSheet(f"border: {borderSize2}px solid #ff0000; background-color: #CC5050; border-radius: {borderRadius2}px;")
            
            self.pushButtonCam1.setText("Run")
            self.pushButtonCam2.setText("Run")
            self.pushButtonCam3.setText("Run")
            self.pushButtonCam4.setText("Run")
            self.pushButtonCam5.setText("Run")
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

        else:
            appSettings.runToggle = False
            self.pushButtonRun.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")

            self.pushButtonCam1.setText("Cam1")
            self.pushButtonCam2.setText("Cam2")
            self.pushButtonCam3.setText("Cam3")
            self.pushButtonCam4.setText("Cam4")
            self.pushButtonCam5.setText("Cam5")

            if appSettings.whichCamSerial == 1 and camera1.running == False:
                self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
                
            if appSettings.whichCamSerial == 2 and camera2.running == False:
                self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #405C80; border-radius: {borderRadius2}px;")
                
            if appSettings.whichCamSerial == 3 and camera3.running == False:
                self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #807100; border-radius: {borderRadius2}px;")
                
            if appSettings.whichCamSerial == 4 and camera4.running == False:
                self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #008071; border-radius: {borderRadius2}px;")
                
            if appSettings.whichCamSerial == 5 and camera5.running == False:
                self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #8D5395; border-radius: {borderRadius2}px;")
    
    def whichCamSerial1(self):
        cam1test = 0
        if appSettings.editToggle:
            appSettings.editButton = 61
            currentText = self.pushButtonCam1.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1D')
            appSettings.message = ("Clear Camera 1")
            PTSapp.setMessage(self)
        elif appSettings.runToggle:
            if camera1.pos1Set: cam1test += 1
            if camera1.pos2Set: cam1test += 1
            if camera1.pos3Set: cam1test += 1
            if camera1.pos4Set: cam1test += 1
            if camera1.pos5Set: cam1test += 1
            if camera1.pos6Set: cam1test += 1
            if camera1.pos7Set: cam1test += 1
            if camera1.pos8Set: cam1test += 1
            if camera1.pos9Set: cam1test += 1
            if camera1.pos10Set: cam1test += 1

            if cam1test > 1:
                if camera1.running:
                    camera1.running = False
                    self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
                else:
                    camera1.running = True
                    self.runCam1()
                return
            else:
                appSettings.message = ("Not pos set")
                PTSapp.setMessage(self)
                return
        else:
            appSettings.whichCamSerial = 1
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

    def whichCamSerial2(self):
        cam2test = 0

        if appSettings.editToggle:
            appSettings.editButton = 62
            currentText = self.pushButtonCam2.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2D')
            appSettings.message = ("Clear Camera 2")
            PTSapp.setMessage(self)
        elif appSettings.runToggle:
            if camera2.pos1Set: cam2test += 1
            if camera2.pos2Set: cam2test += 1
            if camera2.pos3Set: cam2test += 1
            if camera2.pos4Set: cam2test += 1
            if camera2.pos5Set: cam2test += 1
            if camera2.pos6Set: cam2test += 1
            if camera2.pos7Set: cam2test += 1
            if camera2.pos8Set: cam2test += 1
            if camera2.pos9Set: cam2test += 1
            if camera2.pos10Set: cam2test += 1

            if cam2test > 1:
                if camera2.running:
                    camera2.running = False
                    self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
                else:
                    camera2.running = True
                    self.runCam2()
                return
            else:
                appSettings.message = ("Not pos set")
                PTSapp.setMessage(self)
                return
        else:
            appSettings.whichCamSerial = 2
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

    def whichCamSerial3(self):
        cam3test = 0

        if appSettings.editToggle:
            appSettings.editButton = 63
            currentText = self.pushButtonCam3.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3D')
            appSettings.message = ("Clear Camera 3")
            PTSapp.setMessage(self)
        elif appSettings.runToggle:
            if camera3.pos1Set: cam3test += 1
            if camera3.pos2Set: cam3test += 1
            if camera3.pos3Set: cam3test += 1
            if camera3.pos4Set: cam3test += 1
            if camera3.pos5Set: cam3test += 1
            if camera3.pos6Set: cam3test += 1
            if camera3.pos7Set: cam3test += 1
            if camera3.pos8Set: cam3test += 1
            if camera3.pos9Set: cam3test += 1
            if camera3.pos10Set: cam3test += 1

            if cam3test > 1:
                if camera3.running:
                    camera3.running = False
                    self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
                else:
                    camera3.running = True
                    self.runCam3()
                return
            else:
                appSettings.message = ("Not pos set")
                PTSapp.setMessage(self)
                return
        else:
            appSettings.whichCamSerial = 3
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

    def whichCamSerial4(self):
        cam4test = 0

        if appSettings.editToggle:
            appSettings.editButton = 64
            currentText = self.pushButtonCam4.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4D')
            appSettings.message = ("Clear Camera 4")
            PTSapp.setMessage(self)
        elif appSettings.runToggle:
            if camera4.pos1Set: cam4test += 1
            if camera4.pos2Set: cam4test += 1
            if camera4.pos3Set: cam4test += 1
            if camera4.pos4Set: cam4test += 1
            if camera4.pos5Set: cam4test += 1
            if camera4.pos6Set: cam4test += 1
            if camera4.pos7Set: cam4test += 1
            if camera4.pos8Set: cam4test += 1
            if camera4.pos9Set: cam4test += 1
            if camera4.pos10Set: cam4test += 1

            if cam4test > 1:
                if camera4.running:
                    camera4.running = False
                    self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
                else:
                    camera4.running = True
                    self.runCam4()
                return
            else:
                appSettings.message = ("Not pos set")
                PTSapp.setMessage(self)
                return
        else:
            appSettings.whichCamSerial = 4
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

    def whichCamSerial5(self):
        cam5test = 0

        if appSettings.editToggle:
            appSettings.editButton = 65
            currentText = self.pushButtonCam5.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5D')
            appSettings.message = ("Clear Camera 5")
            PTSapp.setMessage(self)
        elif appSettings.runToggle:
            if camera5.pos1Set: cam5test += 1
            if camera5.pos2Set: cam5test += 1
            if camera5.pos3Set: cam5test += 1
            if camera5.pos4Set: cam5test += 1
            if camera5.pos5Set: cam5test += 1
            if camera5.pos6Set: cam5test += 1
            if camera5.pos7Set: cam5test += 1
            if camera5.pos8Set: cam5test += 1
            if camera5.pos9Set: cam5test += 1
            if camera5.pos10Set: cam5test += 1

            if cam5test > 1:
                if camera5.running:
                    camera5.running = False
                    self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")
                else:
                    camera5.running = True
                    self.runCam5()
                return
            else:
                appSettings.message = ("Not pos set")
                PTSapp.setMessage(self)
                return
        else:
            appSettings.whichCamSerial = 5
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #8D5395; border-radius: {borderRadius2}px;")

    def runCam1(self):
        if camera1.pos1At:
            if camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
        elif camera1.pos2At:
            if camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
        elif camera1.pos3At:
            if camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
        elif camera1.pos4At:
            if camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
        elif camera1.pos5At:
            if camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
        elif camera1.pos6At:
            if camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
        elif camera1.pos7At:
            if camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
        elif camera1.pos8At:
            if camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
            elif camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
        elif camera1.pos9At:
            if camera1.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
        elif camera1.pos10At:
            if camera1.pos1Set:
                Worker.sendSerial(self, '&1z')
            elif camera1.pos2Set:
                Worker.sendSerial(self, '&1x')
            elif camera1.pos3Set:
                Worker.sendSerial(self, '&1c')
            elif camera1.pos4Set:
                Worker.sendSerial(self, '&1v')
            elif camera1.pos5Set:
                Worker.sendSerial(self, '&1b')
            elif camera1.pos6Set:
                Worker.sendSerial(self, '&1n')
            elif camera1.pos7Set:
                Worker.sendSerial(self, '&1m')
            elif camera1.pos8Set:
                Worker.sendSerial(self, '&1,')
            elif camera1.pos9Set:
                Worker.sendSerial(self, '&1.')
    
    def runCam2(self):
        if camera2.pos1At:
            if camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
        elif camera2.pos2At:
            if camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
        elif camera2.pos3At:
            if camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
        elif camera2.pos4At:
            if camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
        elif camera2.pos5At:
            if camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
        elif camera2.pos6At:
            if camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
        elif camera2.pos7At:
            if camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
        elif camera2.pos8At:
            if camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
            elif camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
        elif camera2.pos9At:
            if camera2.pos10Set:
                Worker.sendSerial(self, '&2/')
            elif camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
        elif camera2.pos10At:
            if camera2.pos1Set:
                Worker.sendSerial(self, '&2z')
            elif camera2.pos2Set:
                Worker.sendSerial(self, '&2x')
            elif camera2.pos3Set:
                Worker.sendSerial(self, '&2c')
            elif camera2.pos4Set:
                Worker.sendSerial(self, '&2v')
            elif camera2.pos5Set:
                Worker.sendSerial(self, '&2b')
            elif camera2.pos6Set:
                Worker.sendSerial(self, '&2n')
            elif camera2.pos7Set:
                Worker.sendSerial(self, '&2m')
            elif camera2.pos8Set:
                Worker.sendSerial(self, '&2,')
            elif camera2.pos9Set:
                Worker.sendSerial(self, '&2.')
    
    def runCam3(self):
        if camera3.pos1At:
            if camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
        elif camera3.pos2At:
            if camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
        elif camera3.pos3At:
            if camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
        elif camera3.pos4At:
            if camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
        elif camera3.pos5At:
            if camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
        elif camera3.pos6At:
            if camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
        elif camera3.pos7At:
            if camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
        elif camera3.pos8At:
            if camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
            elif camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
        elif camera3.pos9At:
            if camera3.pos10Set:
                Worker.sendSerial(self, '&3/')
            elif camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
        elif camera3.pos10At:
            if camera3.pos1Set:
                Worker.sendSerial(self, '&3z')
            elif camera3.pos2Set:
                Worker.sendSerial(self, '&3x')
            elif camera3.pos3Set:
                Worker.sendSerial(self, '&3c')
            elif camera3.pos4Set:
                Worker.sendSerial(self, '&3v')
            elif camera3.pos5Set:
                Worker.sendSerial(self, '&3b')
            elif camera3.pos6Set:
                Worker.sendSerial(self, '&3n')
            elif camera3.pos7Set:
                Worker.sendSerial(self, '&3m')
            elif camera3.pos8Set:
                Worker.sendSerial(self, '&3,')
            elif camera3.pos9Set:
                Worker.sendSerial(self, '&3.')
    
    def runCam4(self):
        if camera4.pos1At:
            if camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
        elif camera4.pos2At:
            if camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
        elif camera4.pos3At:
            if camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
        elif camera4.pos4At:
            if camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
        elif camera4.pos5At:
            if camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&1/')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
        elif camera4.pos6At:
            if camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
        elif camera4.pos7At:
            if camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
        elif camera4.pos8At:
            if camera4.pos9Set:
                Worker.sendSerial(self, '&4.')
            elif camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
        elif camera4.pos9At:
            if camera4.pos10Set:
                Worker.sendSerial(self, '&4/')
            elif camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
        elif camera4.pos10At:
            if camera4.pos1Set:
                Worker.sendSerial(self, '&4z')
            elif camera4.pos2Set:
                Worker.sendSerial(self, '&4x')
            elif camera4.pos3Set:
                Worker.sendSerial(self, '&4c')
            elif camera4.pos4Set:
                Worker.sendSerial(self, '&4v')
            elif camera4.pos5Set:
                Worker.sendSerial(self, '&4b')
            elif camera4.pos6Set:
                Worker.sendSerial(self, '&4n')
            elif camera4.pos7Set:
                Worker.sendSerial(self, '&4m')
            elif camera4.pos8Set:
                Worker.sendSerial(self, '&4,')
            elif camera4.pos9Set:
                Worker.sendSerial(self, '&4.')

    def runCam5(self):
        if camera5.pos1At:
            if camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
        elif camera5.pos2At:
            if camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
        elif camera5.pos3At:
            if camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
        elif camera5.pos4At:
            if camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
        elif camera5.pos5At:
            if camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
        elif camera5.pos6At:
            if camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
        elif camera5.pos7At:
            if camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
        elif camera5.pos8At:
            if camera5.pos9Set:
                Worker.sendSerial(self, '&5.')
            elif camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
        elif camera5.pos9At:
            if camera5.pos10Set:
                Worker.sendSerial(self, '&5/')
            elif camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
        elif camera5.pos10At:
            if camera5.pos1Set:
                Worker.sendSerial(self, '&5z')
            elif camera5.pos2Set:
                Worker.sendSerial(self, '&5x')
            elif camera5.pos3Set:
                Worker.sendSerial(self, '&5c')
            elif camera5.pos4Set:
                Worker.sendSerial(self, '&5v')
            elif camera5.pos5Set:
                Worker.sendSerial(self, '&5b')
            elif camera5.pos6Set:
                Worker.sendSerial(self, '&5n')
            elif camera5.pos7Set:
                Worker.sendSerial(self, '&5m')
            elif camera5.pos8Set:
                Worker.sendSerial(self, '&5,')
            elif camera5.pos9Set:
                Worker.sendSerial(self, '&5.')

    def flash(self):
        if appSettings.flashTick:
            appSettings.flashTick = False
            buttonColourFlash = "#ffff00"
        else:
            appSettings.flashTick = True
            buttonColourFlash = "#000000"

        if camera1.pos1Run and not camera1.pos1At:
            if camera1.slideToggle and camera1.hasSlider:
                PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #40D140; border-radius: {borderRadius}px;')
            elif not camera1.slideToggle:
                PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos2Run and not camera1.pos2At:
            PTSapp.pushButton12.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos3Run and not camera1.pos3At:
            PTSapp.pushButton13.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos4Run and not camera1.pos4At:
            PTSapp.pushButton14.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos5Run and not camera1.pos5At:
            PTSapp.pushButton15.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos6Run and not camera1.pos6At:
            PTSapp.pushButton16.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos7Run and not camera1.pos7At:
            PTSapp.pushButton17.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos8Run and not camera1.pos8At:
            PTSapp.pushButton18.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos9Run and not camera1.pos9At:
            PTSapp.pushButton19.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
        if camera1.pos10Run and not camera1.pos10At:
            if camera1.slideToggle and camera1.hasSlider:
                PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #40D140; border-radius: {borderRadius}px;')
            elif not camera1.slideToggle:
                PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        
        if camera2.pos1Run and not camera2.pos1At:
            if camera2.slideToggle and camera2.hasSlider:
                PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
            elif not camera2.slideToggle:
                PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos2Run and not camera2.pos2At:
            PTSapp.pushButton22.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos3Run and not camera2.pos3At:
            PTSapp.pushButton23.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos4Run and not camera2.pos4At:
            PTSapp.pushButton24.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos5Run and not camera2.pos5At:
            PTSapp.pushButton25.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos6Run and not camera2.pos6At:
            PTSapp.pushButton26.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos7Run and not camera2.pos7At:
            PTSapp.pushButton27.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos8Run and not camera2.pos8At:
            PTSapp.pushButton28.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos9Run and not camera2.pos9At:
            PTSapp.pushButton29.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')
        if camera2.pos10Run and not camera2.pos10At:
            if camera2.slideToggle and camera2.hasSlider:
                PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
            elif not camera2.slideToggle:
                PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius}px;')

        
        if camera3.pos1Run and not camera3.pos1At:
            if camera3.slideToggle and camera3.hasSlider:
                PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #B4A21C; border-radius: {borderRadius}px;')
            elif not camera3.slideToggle:
                PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos2Run and not camera3.pos2At:
            PTSapp.pushButton32.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos3Run and not camera3.pos3At:
            PTSapp.pushButton33.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos4Run and not camera3.pos4At:
            PTSapp.pushButton34.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos5Run and not camera3.pos5At:
            PTSapp.pushButton35.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos6Run and not camera3.pos6At:
            PTSapp.pushButton36.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos7Run and not camera3.pos7At:
            PTSapp.pushButton37.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos8Run and not camera3.pos8At:
            PTSapp.pushButton38.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos9Run and not camera3.pos9At:
            PTSapp.pushButton39.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')
        if camera3.pos10Run and not camera3.pos10At:
            if camera3.slideToggle and camera3.hasSlider:
                PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #B4A21C; border-radius: {borderRadius}px;')
            elif not camera3.slideToggle:
                PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius}px;')

        
        if camera4.pos1Run and not camera4.pos1At:
            if camera4.slideToggle and camera4.hasSlider:
                PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #01E6CC; border-radius: {borderRadius}px;')
            elif not camera4.slideToggle:
                PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos2Run and not camera4.pos2At:
            PTSapp.pushButton42.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos3Run and not camera4.pos3At:
            PTSapp.pushButton43.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos4Run and not camera4.pos4At:
            PTSapp.pushButton44.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos5Run and not camera4.pos5At:
            PTSapp.pushButton45.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos6Run and not camera4.pos6At:
            PTSapp.pushButton46.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos7Run and not camera4.pos7At:
            PTSapp.pushButton47.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos8Run and not camera4.pos8At:
            PTSapp.pushButton48.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos9Run and not camera4.pos9At:
            PTSapp.pushButton49.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')
        if camera4.pos10Run and not camera4.pos10At:
            if camera4.slideToggle and camera4.hasSlider:
                PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #01E6CC; border-radius: {borderRadius}px;')
            elif not camera4.slideToggle:
                PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius}px;')

        
        if camera5.pos1Run and not camera5.pos1At:
            if camera5.slideToggle and camera5.hasSlider:
                PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #E97CF9; border-radius: {borderRadius}px;')
            elif not camera5.slideToggle:
                PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos2Run and not camera5.pos2At:
            PTSapp.pushButton52.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos3Run and not camera5.pos3At:
            PTSapp.pushButton53.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos4Run and not camera5.pos4At:
            PTSapp.pushButton54.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos5Run and not camera5.pos5At:
            PTSapp.pushButton55.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos6Run and not camera5.pos6At:
            PTSapp.pushButton56.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos7Run and not camera5.pos7At:
            PTSapp.pushButton57.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos8Run and not camera5.pos8At:
            PTSapp.pushButton58.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos9Run and not camera5.pos9At:
            PTSapp.pushButton59.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')
        if camera5.pos10Run and not camera5.pos10At:
            if camera5.slideToggle and camera5.hasSlider:
                PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #E97CF9; border-radius: {borderRadius}px;')
            elif not camera5.slideToggle:
                PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera1.running:
            PTSapp.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        if camera2.running:
            PTSapp.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius2}px;")
        if camera3.running:
            PTSapp.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius2}px;")
        if camera4.running:
            PTSapp.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius2}px;")
        if camera5.running:
            PTSapp.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius2}px;")



        if camera1.running:
            self.pushButtonCam1.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        if camera2.running:
            self.pushButtonCam2.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #405C80; border-radius: {borderRadius2}px;")
        if camera3.running:
            self.pushButtonCam3.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #807100; border-radius: {borderRadius2}px;")
        if camera4.running:
            self.pushButtonCam4.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #008071; border-radius: {borderRadius2}px;")
        if camera5.running:
            self.pushButtonCam5.setStyleSheet(f"border: {borderSize2}px solid {buttonColourFlash}; background-color: #8D5395; border-radius: {borderRadius2}px;")

        if camera1.useSetSpeed:
            self.pushButtonSetSpeedCam1.setStyleSheet(f"border: {(borderSize* 0.4)}px solid red; background-color: #40D140; border-radius: {borderRadius*0.3}px;")
        elif not camera1.useSetSpeed:
            self.pushButtonSetSpeedCam1.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius*0.3}px;")

        if camera2.useSetSpeed:
            self.pushButtonSetSpeedCam2.setStyleSheet(f"border: {(borderSize* 0.4)}px solid red; background-color: #5C8BC9; border-radius: {borderRadius*0.3}px;")
        elif not camera2.useSetSpeed:
            self.pushButtonSetSpeedCam2.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #405C80; border-radius: {borderRadius*0.3}px;")
        
        if camera3.useSetSpeed:
            self.pushButtonSetSpeedCam3.setStyleSheet(f"border: {(borderSize* 0.4)}px solid red; background-color: #B4A21C; border-radius: {borderRadius*0.3}px;")
        elif not camera3.useSetSpeed:
            self.pushButtonSetSpeedCam3.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #807100; border-radius: {borderRadius*0.3}px;")

        if camera4.useSetSpeed:
            self.pushButtonSetSpeedCam4.setStyleSheet(f"border: {(borderSize* 0.4)}px solid red; background-color: #01E6CC; border-radius: {borderRadius*0.3}px;")
        elif not camera4.useSetSpeed:
            self.pushButtonSetSpeedCam4.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #008071; border-radius: {borderRadius*0.3}px;")
        
        if camera5.useSetSpeed:
            self.pushButtonSetSpeedCam5.setStyleSheet(f"border: {(borderSize* 0.4)}px solid red; background-color: #E97CF9; border-radius: {borderRadius*0.3}px;")
        elif not camera5.useSetSpeed:
            self.pushButtonSetSpeedCam5.setStyleSheet(f"border: {(borderSize* 0.4)}px solid grey; background-color: #8D5395; border-radius: {borderRadius*0.3}px;")
    
    def initFlashTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.flash)
        self.timer.start(500)

        self.messageTimer = QTimer()
        self.messageTimer.timeout.connect(self.setMessage)
        self.messageTimer.start(100)

    def fileLoad(self):
        config = {}

        if sys.platform == "win32":
            fname = QFileDialog.getOpenFileName(self, "Open Config", "C:\\Users\\Music\\Documents", "JSON (*.json)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Open Config", "~/Documents", "JSON (*.json)")
    
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

                camera1.name = config['Cam1']
                camera2.name = config['Cam2']
                camera3.name = config['Cam3']
                camera4.name = config['Cam4']
                camera5.name = config['Cam5']
        
            except:
                appSettings.message = ("Couldn't Load File")
                PTSapp.setMessage(self)

    def fileSave(self):
        config = {}

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
        config['Cam1'] = camera1.name
        config['Cam2'] = camera2.name
        config['Cam3'] = camera3.name
        config['Cam4'] = camera4.name
        config['Cam5'] = camera5.name

        if sys.platform == "win32":
            fname, _ = QFileDialog.getSaveFileName(self, "Save Config", "C:\\Users\\Music\\Documents", "JSON (*.json)")
        else:
            fname, _ = QFileDialog.getSaveFileName(self, "Save Config", "~/Documents", "JSON (*.json)")
        
        if fname:
            self.labelFilename.setText(Path(fname).stem)
            with open(fname, 'w') as f:
                json.dump(config, f)

    def autoFileLoad(self):
        config = {}
        if sys.platform == "win32":
            filename = 'C:\\Users\\Music\\Documents\\default.json'
        else:
            filename = '~/Documents/default.json'

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

            camera1.name = config['Cam1']
            camera2.name = config['Cam2']
            camera3.name = config['Cam3']
            camera4.name = config['Cam4']
            camera5.name = config['Cam5']
        
            self.pushButtonCam1.setText(camera1.name)
            self.pushButtonCam2.setText(camera2.name)
            self.pushButtonCam3.setText(camera3.name)
            self.pushButtonCam4.setText(camera4.name)
            self.pushButtonCam5.setText(camera5.name)
    
        except:
            appSettings.message = ("Couldn't Load File")
            PTSapp.setMessage(self)

    def buttonConnect(self, device_list):
        serialPortSelect = ""
        device_name_list = device_list

        usb_port = 'usbmodem'
        usb_port2 = 'usb/00'
        usb_port3 = 'COM8'
        usb_port4 = 'COM3'
        usb_port5 = 'ACM0'
        
        if (usb_port in '\t'.join(device_name_list)):
            serialDeviceList.serialDevice = list(([string for string in device_name_list if usb_port in string]))
        elif (usb_port2 in '\t'.join(device_name_list)):
            serialDeviceList.serialDevice = list(([string for string in device_name_list if usb_port2 in string]))
        elif (usb_port3 in '\t'.join(device_name_list)):
            serialDeviceList.serialDevice = list(([string for string in device_name_list if usb_port3 in string]))
        elif (usb_port4 in '\t'.join(device_name_list)):
            serialDeviceList.serialDevice = list(([string for string in device_name_list if usb_port4 in string]))
        elif (usb_port5 in '\t'.join(device_name_list)):
            serialDeviceList.serialDevice = list(([string for string in device_name_list if usb_port5 in string]))
        else:
            appSettings.message = ("No USB Serial Found")

        if serialDeviceList.serialDevice != "":
            appSettings.message = ("Auto Connecting")
            serialPort = serialConnect()

    def pushToClose(self):
        #print("pushToClose")
        self.close()

    def Cam1Go1(self):
        if appSettings.editToggle:
            appSettings.editButton = 11
            currentText = self.pushButton11.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1Z')
            return
        elif camera1.pos1Set and not camera1.pos1At:
            Worker.sendSerial(self, '&1z')

    def Cam1Go2(self):
        if appSettings.editToggle:
            appSettings.editButton = 12
            currentText = self.pushButton12.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1X')
            return
        elif camera1.pos2Set and not camera1.pos2At:
            Worker.sendSerial(self, '&1x')

    def Cam1Go3(self):
        if appSettings.editToggle:
            appSettings.editButton = 13
            currentText = self.pushButton13.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1C')
            return
        elif camera1.pos3Set and not camera1.pos3At:
            Worker.sendSerial(self, '&1c')

    def Cam1Go4(self):
        if appSettings.editToggle:
            appSettings.editButton = 14
            currentText = self.pushButton14.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1V')
            return
        elif camera1.pos4Set and not camera1.pos4At:
            Worker.sendSerial(self, '&1v')

    def Cam1Go5(self):
        if appSettings.editToggle:
            appSettings.editButton = 15
            currentText = self.pushButton15.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1B')
            return
        elif camera1.pos5Set and not camera1.pos5At:
            Worker.sendSerial(self, '&1b')

    def Cam1Go6(self):
        if appSettings.editToggle:
            appSettings.editButton = 16
            currentText = self.pushButton16.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1N')
            return
        elif camera1.pos6Set and not camera1.pos6At:
            Worker.sendSerial(self, '&1n')

    def Cam1Go7(self):
        if appSettings.editToggle:
            appSettings.editButton = 17
            currentText = self.pushButton17.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1M')
            return
        elif camera1.pos7Set and not camera1.pos7At:
            Worker.sendSerial(self, '&1m')

    def Cam1Go8(self):
        if appSettings.editToggle:
            appSettings.editButton = 18
            currentText = self.pushButton18.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1<')
            return
        elif camera1.pos8Set and not camera1.pos8At:
            Worker.sendSerial(self, '&1,')

    def Cam1Go9(self):
        if appSettings.editToggle:
            appSettings.editButton = 19
            currentText = self.pushButton19.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1>')
            return
        elif camera1.pos9Set and not camera1.pos9At:
            Worker.sendSerial(self, '&1.')

    def Cam1Go10(self):
        if appSettings.editToggle:
            appSettings.editButton = 10
            currentText = self.pushButton10.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&1?')
            return
        elif camera1.pos10Set and not camera1.pos10At:
            Worker.sendSerial(self, '&1/')

    def Cam2Go1(self):
        if appSettings.editToggle:
            appSettings.editButton = 21
            currentText = self.pushButton21.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2Z')
            return
        elif camera2.pos1Set and not camera2.pos1At:
            Worker.sendSerial(self, '&2z')

    def Cam2Go2(self):
        if appSettings.editToggle:
            appSettings.editButton = 22
            currentText = self.pushButton22.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2X')
            return
        elif camera2.pos2Set and not camera2.pos2At:
            Worker.sendSerial(self, '&2x')

    def Cam2Go3(self):
        if appSettings.editToggle:
            appSettings.editButton = 23
            currentText = self.pushButton23.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2C')
            return
        elif camera2.pos3Set and not camera2.pos3At:
            Worker.sendSerial(self, '&2c')

    def Cam2Go4(self):
        if appSettings.editToggle:
            appSettings.editButton = 24
            currentText = self.pushButton24.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2V')
            return
        elif camera2.pos4Set and not camera2.pos4At:
            Worker.sendSerial(self, '&2v')

    def Cam2Go5(self):
        if appSettings.editToggle:
            appSettings.editButton = 25
            currentText = self.pushButton25.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2B')
            return
        elif camera2.pos5Set and not camera2.pos5At:
            Worker.sendSerial(self, '&2b')

    def Cam2Go6(self):
        if appSettings.editToggle:
            appSettings.editButton = 26
            currentText = self.pushButton26.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2N')
            return
        elif camera2.pos6Set and not camera2.pos6At:
            Worker.sendSerial(self, '&2n')

    def Cam2Go7(self):
        if appSettings.editToggle:
            appSettings.editButton = 27
            currentText = self.pushButton27.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2M')
            return
        elif camera2.pos7Set and not camera2.pos7At:
            Worker.sendSerial(self, '&2m')

    def Cam2Go8(self):
        if appSettings.editToggle:
            appSettings.editButton = 28
            currentText = self.pushButton28.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2<')
            return
        elif camera2.pos8Set and not camera2.pos8At:
            Worker.sendSerial(self, '&2,')

    def Cam2Go9(self):
        if appSettings.editToggle:
            appSettings.editButton = 29
            currentText = self.pushButton29.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2>')
            return
        elif camera2.pos9Set and not camera2.pos9At:
            Worker.sendSerial(self, '&2.')

    def Cam2Go10(self):
        if appSettings.editToggle:
            appSettings.editButton = 20
            currentText = self.pushButton20.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&2?')
            return
        elif camera2.pos10Set and not camera2.pos10At:
            Worker.sendSerial(self, '&2/')

    def Cam3Go1(self):
        if appSettings.editToggle:
            appSettings.editButton = 31
            currentText = self.pushButton31.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3Z')
            return
        elif camera3.pos1Set and not camera3.pos1At:
            Worker.sendSerial(self, '&3z')

    def Cam3Go2(self):
        if appSettings.editToggle:
            appSettings.editButton = 32
            currentText = self.pushButton32.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3X')
            return
        elif camera3.pos2Set and not camera3.pos2At:
            Worker.sendSerial(self, '&3x')

    def Cam3Go3(self):
        if appSettings.editToggle:
            appSettings.editButton = 33
            currentText = self.pushButton33.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3C')
            return
        elif camera3.pos3Set and not camera3.pos3At:
            Worker.sendSerial(self, '&3c')

    def Cam3Go4(self):
        if appSettings.editToggle:
            appSettings.editButton = 34
            currentText = self.pushButton34.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3V')
            return
        elif camera3.pos4Set and not camera3.pos4At:
            Worker.sendSerial(self, '&3v')

    def Cam3Go5(self):
        if appSettings.editToggle:
            appSettings.editButton = 35
            currentText = self.pushButton35.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3B')
            return
        elif camera3.pos5Set and not camera3.pos5At:
            Worker.sendSerial(self, '&3b')

    def Cam3Go6(self):
        if appSettings.editToggle:
            appSettings.editButton = 36
            currentText = self.pushButton36.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3N')
            return
        elif camera3.pos6Set and not camera3.pos6At:
            Worker.sendSerial(self, '&3n')

    def Cam3Go7(self):
        if appSettings.editToggle:
            appSettings.editButton = 37
            currentText = self.pushButton37.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3M')
            return
        elif camera3.pos7Set and not camera3.pos7At:
            Worker.sendSerial(self, '&3m')

    def Cam3Go8(self):
        if appSettings.editToggle:
            appSettings.editButton = 38
            currentText = self.pushButton38.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3<')
            return
        elif camera3.pos8Set and not camera3.pos8At:
            Worker.sendSerial(self, '&3,')

    def Cam3Go9(self):
        if appSettings.editToggle:
            appSettings.editButton = 39
            currentText = self.pushButton39.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3>')
            return
        elif camera3.pos9Set and not camera3.pos9At:
            Worker.sendSerial(self, '&3.')

    def Cam3Go10(self):
        if appSettings.editToggle:
            appSettings.editButton = 30
            currentText = self.pushButton30.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&3?')
            return
        elif camera3.pos10Set and not camera3.pos10At:
            Worker.sendSerial(self, '&3/')

    def Cam4Go1(self):
        if appSettings.editToggle:
            appSettings.editButton = 41
            currentText = self.pushButton41.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4Z')
            return
        elif camera4.pos1Set and not camera4.pos1At and not camera4.slideToggle:
            Worker.sendSerial(self, '&4z')
        elif camera4.pos1Set and not camera4.pos1At and camera4.slideToggle:
            Worker.sendSerial(self, '&4y')

    def Cam4Go2(self):
        if appSettings.editToggle:
            appSettings.editButton = 42
            currentText = self.pushButton42.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4X')
            return
        elif camera4.pos2Set and not camera4.pos2At:
            Worker.sendSerial(self, '&4x')

    def Cam4Go3(self):
        if appSettings.editToggle:
            appSettings.editButton = 43
            currentText = self.pushButton43.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4C')
            return
        elif camera4.pos3Set and not camera4.pos3At:
            Worker.sendSerial(self, '&4c')

    def Cam4Go4(self):
        if appSettings.editToggle:
            appSettings.editButton = 44
            currentText = self.pushButton44.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4V')
            return
        elif camera4.pos4Set and not camera4.pos4At:
            Worker.sendSerial(self, '&4v')

    def Cam4Go5(self):
        if appSettings.editToggle:
            appSettings.editButton = 45
            currentText = self.pushButton45.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4B')
            return
        elif camera4.pos5Set and not camera4.pos5At:
            Worker.sendSerial(self, '&4b')

    def Cam4Go6(self):
        if appSettings.editToggle:
            appSettings.editButton = 46
            currentText = self.pushButton46.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4N')
            return
        elif camera4.pos6Set and not camera4.pos6At:
            Worker.sendSerial(self, '&4n')

    def Cam4Go7(self):
        if appSettings.editToggle:
            appSettings.editButton = 47
            currentText = self.pushButton47.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4M')
            return
        elif camera4.pos7Set and not camera4.pos7At:
            Worker.sendSerial(self, '&4m')

    def Cam4Go8(self):
        if appSettings.editToggle:
            appSettings.editButton = 48
            currentText = self.pushButton48.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4<')
            return
        elif camera4.pos8Set and not camera4.pos8At:
            Worker.sendSerial(self, '&4,')

    def Cam4Go9(self):
        if appSettings.editToggle:
            appSettings.editButton = 49
            currentText = self.pushButton49.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4>')
            return
        elif camera4.pos9Set and not camera4.pos9At:
            Worker.sendSerial(self, '&4.')

    def Cam4Go10(self):
        if appSettings.editToggle:
            appSettings.editButton = 40
            currentText = self.pushButton40.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&4?')
            return
            return
        elif camera4.pos10Set and not camera4.pos10At and not camera4.slideToggle:
            Worker.sendSerial(self, '&4/')
        elif camera4.pos10Set and not camera4.pos10At and camera4.slideToggle:
            Worker.sendSerial(self, '&4Y')

    def Cam5Go1(self):
        if appSettings.editToggle:
            appSettings.editButton = 51
            currentText = self.pushButton51.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5Z')
            return
        elif camera5.pos1Set and not camera5.pos1At and not camera5.slideToggle:
            Worker.sendSerial(self, '&5z')
        elif camera5.pos1Set and not camera5.pos1At and camera5.slideToggle:
            Worker.sendSerial(self, '&5y')

    def Cam5Go2(self):
        if appSettings.editToggle:
            appSettings.editButton = 52
            currentText = self.pushButton52.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5X')
            return
        elif camera5.pos2Set and not camera5.pos2At:
            Worker.sendSerial(self, '&5x')

    def Cam5Go3(self):
        if appSettings.editToggle:
            appSettings.editButton = 53
            currentText = self.pushButton53.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5C')
            return
        elif camera5.pos3Set and not camera5.pos3At:
            Worker.sendSerial(self, '&5c')

    def Cam5Go4(self):
        if appSettings.editToggle:
            appSettings.editButton = 54
            currentText = self.pushButton54.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5V')
            return
        elif camera5.pos4Set and not camera5.pos4At:
            Worker.sendSerial(self, '&5v')

    def Cam5Go5(self):
        if appSettings.editToggle:
            appSettings.editButton = 55
            currentText = self.pushButton55.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5B')
            return
        elif camera5.pos5Set and not camera5.pos5At:
            Worker.sendSerial(self, '&5b')

    def Cam5Go6(self):
        if appSettings.editToggle:
            appSettings.editButton = 56
            currentText = self.pushButton56.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5N')
            return
        elif camera5.pos6Set and not camera5.pos6At:
            Worker.sendSerial(self, '&5n')

    def Cam5Go7(self):
        if appSettings.editToggle:
            appSettings.editButton = 57
            currentText = self.pushButton57.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5M')
            return
        elif camera5.pos7Set and not camera5.pos7At:
            Worker.sendSerial(self, '&5m')

    def Cam5Go8(self):
        if appSettings.editToggle:
            appSettings.editButton = 58
            currentText = self.pushButton58.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5<')
            return
        elif camera5.pos8Set and not camera5.pos8At:
            Worker.sendSerial(self, '&5,')

    def Cam5Go9(self):
        if appSettings.editToggle:
            appSettings.editButton = 59
            currentText = self.pushButton59.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5>')
            return
        elif camera5.pos9Set and not camera5.pos9At:
            Worker.sendSerial(self, '&5.')

    def Cam5Go10(self):
        if appSettings.editToggle:
            appSettings.editButton = 50
            currentText = self.pushButton50.text()
            self.openEditWindow(currentText)
        elif appSettings.setPosToggle:
            self.setPos(3)
            Worker.sendSerial(self, '&5?')
            return
        elif camera5.pos10Set and not camera5.pos10At and not camera5.slideToggle:
            Worker.sendSerial(self, '&5/')
        elif camera5.pos10Set and not camera5.pos10At and camera5.slideToggle:
            Worker.sendSerial(self, '&5Y')

    def Cam1SetSpeed(self):
        Worker.sendSerial(self, '&1i')

    def Cam2SetSpeed(self):
        Worker.sendSerial(self, '&2i')

    def Cam3SetSpeed(self):
        Worker.sendSerial(self, '&3i')

    def Cam4SetSpeed(self):
        Worker.sendSerial(self, '&4i')

    def Cam5SetSpeed(self):
        Worker.sendSerial(self, '&5i')

    def setMessage(self):
        if appSettings.message != "":
            PTSapp.labelInfo.setText(appSettings.message)
            QtCore.QTimer.singleShot(5000,PTSapp.resetMessage)  # for one time call only. (once)
            appSettings.message = ""

    def resetMessage():
        PTSapp.labelInfo.setText("")
        appSettings.message = ""

class Ui_SettingsWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi()
        self.installEventFilter(self) #keyboard control
        #self.valueChanged.connect(self.checkzero)

    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            key = event.key()
            if key == 71:  # g
                #print("KEY TEST")
                self.TLStep()

        return super().eventFilter(obj, event)

    def setupUi(self):
        global whichCamSerial

        global butttonLayoutX
        global butttonLayoutY
        global buttonGoX
        global buttonGoY
        global borderSize
        global borderSize2
        global borderRadius
        global borderRadius2
        global winSize
        global serialText

        self.setObjectName("settingsWindow")

        ag = QtGui.QGuiApplication.primaryScreen().size()
        agX = ag.width()
        agY = ag.height()

        if appSettings.debug:
            agX = agX / 1.4
            agY = agY / 1.6

            self.resize(agX, agY)

        agY = agY * 0.97

        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(butttonLayoutX, butttonLayoutY * 0.5, (buttonGoX * 10.917)+1, (buttonGoY * 8.3333333333)+1))
        self.groupBox.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButtonZoomLimit = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelZoomLimit.setFocus())
        self.pushButtonZoomLimit.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 32.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonZoomLimit.setFont(font)
        self.pushButtonZoomLimit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonZoomLimit.setObjectName("pushButtonZoomLimit")
        self.pushButtonSlideLimit = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelZoomLimit.setFocus())
        self.pushButtonSlideLimit.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 32.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSlideLimit.setFont(font)
        self.pushButtonSlideLimit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonSlideLimit.setObjectName("pushButtonSlideLimit")
        self.pushButtonSlideLocate = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.locateHome())
        self.pushButtonSlideLocate.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 36.5, (buttonGoX * 1)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.9)
        self.pushButtonSlideLocate.setFont(font)
        self.pushButtonSlideLocate.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonSlideLocate.setObjectName("pushButtonSlideLocate")
        self.pushButtonSlideSetHome = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.setHome())
        self.pushButtonSlideSetHome.setGeometry(QtCore.QRect(butttonLayoutX * 44.5, butttonLayoutY * 36.5, (buttonGoX * 1)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.9)
        self.pushButtonSlideSetHome.setFont(font)
        self.pushButtonSlideSetHome.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonSlideSetHome.setObjectName("pushButtonSlideSetHome")
        self.labelCamHasSlider = QtWidgets.QLabel(self.groupBox)
        self.labelCamHasSlider.setGeometry(QtCore.QRect(butttonLayoutX * 35, butttonLayoutY * 30.3, buttonGoX * 1.2, butttonLayoutY * 1.2))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.1)
        self.labelCamHasSlider.setFont(font)
        self.labelCamHasSlider.setStyleSheet("border: 0px; color:grey;")
        self.labelCamHasSlider.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCamHasSlider.setObjectName("labelCamHasSlider")
        self.labelCamHasSlider.setVisible(False)
        self.pushButtonPTS4 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed4.setFocus())
        self.pushButtonPTS4.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 10.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonPTS4.setFont(font)
        self.pushButtonPTS4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonPTS4.setObjectName("pushButtonPTS4")
        self.pushButtonPTS3 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed3.setFocus())
        self.pushButtonPTS3.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 15, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonPTS3.setFont(font)
        self.pushButtonPTS3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonPTS3.setObjectName("pushButtonPTS3")
        self.pushButtonPTS2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed2.setFocus())
        self.pushButtonPTS2.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 19.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonPTS2.setFont(font)
        self.pushButtonPTS2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonPTS2.setObjectName("pushButtonPTS2")
        self.pushButtonPTS1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTspeed1.setFocus())
        self.pushButtonPTS1.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 24, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonPTS1.setFont(font)
        self.pushButtonPTS1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonPTS1.setObjectName("pushButtonPTS1")
        self.pushButtonSS4 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed4.setFocus())
        self.pushButtonSS4.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 10.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSS4.setFont(font)
        self.pushButtonSS4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonSS4.setObjectName("pushButtonSS4")
        self.pushButtonSS3 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed3.setFocus())
        self.pushButtonSS3.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 15, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSS3.setFont(font)
        self.pushButtonSS3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonSS3.setObjectName("pushButtonSS3")
        self.pushButtonSS2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed2.setFocus())
        self.pushButtonSS2.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 19.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSS2.setFont(font)
        self.pushButtonSS2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonSS2.setObjectName("pushButtonSS2")
        self.pushButtonSS1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLspeed1.setFocus())
        self.pushButtonSS1.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 24, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSS1.setFont(font)
        self.pushButtonSS1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonSS1.setObjectName("pushButtonSS1")
        self.pushButtonSA = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelSLaccel.setFocus())
        self.pushButtonSA.setGeometry(QtCore.QRect(butttonLayoutX * 35.5, butttonLayoutY * 3.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonSA.setFont(font)
        self.pushButtonSA.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonSA.setObjectName("pushButtonSA")
        self.pushButtonPTA = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.labelPTaccel.setFocus())
        self.pushButtonPTA.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 3.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonPTA.setFont(font)
        self.pushButtonPTA.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonPTA.setObjectName("pushButtonPTA")
        self.labelPTaccel = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTaccel.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 3.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelPTaccel.setFont(font)
        self.labelPTaccel.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTaccel.setText("")
        self.labelPTaccel.setObjectName("labelPTaccel")
        self.labelZoomLimit = QtWidgets.QLineEdit(self.groupBox)
        self.labelZoomLimit.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 32.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelZoomLimit.setFont(font)
        self.labelZoomLimit.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelZoomLimit.setText("")
        self.labelZoomLimit.setObjectName("labelZoomLimit")
        self.labelTLSteps = QtWidgets.QLineEdit(self.groupBox)
        self.labelTLSteps.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 40.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelTLSteps.setFont(font)
        self.labelTLSteps.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelTLSteps.setText("")
        self.labelTLSteps.setObjectName("labelTLSteps")
        self.pushButtonTLSteps = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.TLSet())
        self.pushButtonTLSteps.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 40.5, (buttonGoX * 2.5)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.3)
        self.pushButtonTLSteps.setFont(font)
        self.pushButtonTLSteps.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonTLSteps.setObjectName("pushButtonTLSteps")
        self.pushButtonTLStart = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.TLStart())
        self.pushButtonTLStart.setGeometry(QtCore.QRect(butttonLayoutX * 1.5, butttonLayoutY * 44.5, (buttonGoX * 1)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        self.pushButtonTLStart.setFont(font)
        self.pushButtonTLStart.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonTLStart.setObjectName("pushButtonTLStart")
        self.pushButtonTLStop = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.TLStop())
        self.pushButtonTLStop.setGeometry(QtCore.QRect(butttonLayoutX * 10.5, butttonLayoutY * 44.5, (buttonGoX * 1)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.5)
        self.pushButtonTLStop.setFont(font)
        self.pushButtonTLStop.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        self.pushButtonTLStop.setObjectName("pushButtonTLStop")
        #self.pushButtonTLStep = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.TLStep())
        #self.pushButtonTLStep.setGeometry(QtCore.QRect(butttonLayoutX * 10.5, butttonLayoutY * 48.5, (buttonGoX * 1)+1, (buttonGoY * 0.5)+1))
        #font = QtGui.QFont()
        #font.setFamily("Helvetica Neue")
        #font.setPointSize(butttonLayoutX * winSize * 1.5)
        #self.pushButtonTLStep.setFont(font)
        #self.pushButtonTLStep.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")
        #self.pushButtonTLStep.setObjectName("pushButtonTLStep")
        self.labelPTspeed4 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed4.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 10.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelPTspeed4.setFont(font)
        self.labelPTspeed4.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed4.setText("")
        self.labelPTspeed4.setObjectName("labelPTspeed4")
        self.labelPTspeed3 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed3.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 15, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelPTspeed3.setFont(font)
        self.labelPTspeed3.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed3.setText("")
        self.labelPTspeed3.setObjectName("labelPTspeed3")
        self.labelPTspeed2 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed2.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 19.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelPTspeed2.setFont(font)
        self.labelPTspeed2.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed2.setText("")
        self.labelPTspeed2.setObjectName("labelPTspeed2")
        self.labelPTspeed1 = QtWidgets.QLineEdit(self.groupBox)
        self.labelPTspeed1.setGeometry(QtCore.QRect(butttonLayoutX * 18, butttonLayoutY * 24, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelPTspeed1.setFont(font)
        self.labelPTspeed1.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelPTspeed1.setText("")
        self.labelPTspeed1.setObjectName("labelPTspeed1")
        self.labelSLaccel = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLaccel.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 3.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSLaccel.setFont(font)
        self.labelSLaccel.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLaccel.setText("")
        self.labelSLaccel.setObjectName("labelSLaccel")
        self.labelSLspeed4 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed4.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 10.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSLspeed4.setFont(font)
        self.labelSLspeed4.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed4.setText("")
        self.labelSLspeed4.setObjectName("labelSLspeed4")
        self.labelSLspeed3 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed3.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 15, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSLspeed3.setFont(font)
        self.labelSLspeed3.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed3.setText("")
        self.labelSLspeed3.setObjectName("labelSLspeed3")
        self.labelSLspeed2 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed2.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 19.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSLspeed2.setFont(font)
        self.labelSLspeed2.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed2.setText("")
        self.labelSLspeed2.setObjectName("labelSLspeed2")
        self.labelSLspeed1 = QtWidgets.QLineEdit(self.groupBox)
        self.labelSLspeed1.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 24, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSLspeed1.setFont(font)
        self.labelSLspeed1.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSLspeed1.setText("")
        self.labelSLspeed1.setObjectName("labelSLspeed1")
        self.labelSlideLimit = QtWidgets.QLineEdit(self.groupBox)
        self.labelSlideLimit.setGeometry(QtCore.QRect(butttonLayoutX * 52, butttonLayoutY * 32.5, (buttonGoX * 1.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3.2)
        self.labelSlideLimit.setFont(font)
        self.labelSlideLimit.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.labelSlideLimit.setText("")
        self.labelSlideLimit.setObjectName("labelSlideLimit")

        self.serialTextWindow = QtWidgets.QTextEdit(self.groupBox)
        self.serialTextWindow.setGeometry(QtCore.QRect(butttonLayoutX * 30, butttonLayoutY * 40.5, (buttonGoX * 5.5)+1, (buttonGoY * 1.4)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 0.8)
        self.serialTextWindow.setFont(font)
        self.serialTextWindow.setStyleSheet("color:#ffffff;border: 2px solid grey;")
        self.serialTextWindow.setHtml(appSettings.serialText)
        self.serialTextWindow.setObjectName("serialTextWindow")
        self.serialTextWindow.verticalScrollBar().setValue(self.serialTextWindow.verticalScrollBar().maximum())

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(butttonLayoutX * 67.5, butttonLayoutY * 33.5, (buttonGoX * 4.5833333333)+1, (buttonGoY * 2.8333333333)+1))
        self.groupBox_2.setStyleSheet(f"background-color: #1e252a; border: {borderSize2}px solid #262d32;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButtonNum1 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('1'))
        self.pushButtonNum1.setGeometry(QtCore.QRect(butttonLayoutX * 0.5, butttonLayoutY, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum1.setFont(font)
        self.pushButtonNum1.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum1.setObjectName("pushButtonNum1")
        self.pushButtonNum1.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum2 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('2'))
        self.pushButtonNum2.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum2.setFont(font)
        self.pushButtonNum2.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum2.setObjectName("pushButtonNum2")
        self.pushButtonNum2.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum3 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('3'))
        self.pushButtonNum3.setGeometry(QtCore.QRect(butttonLayoutX * 12.5, butttonLayoutY, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum3.setFont(font)
        self.pushButtonNum3.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum3.setObjectName("pushButtonNum3")
        self.pushButtonNum3.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum4 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('4'))
        self.pushButtonNum4.setGeometry(QtCore.QRect(butttonLayoutX * 0.5, butttonLayoutY * 5, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum4.setFont(font)
        self.pushButtonNum4.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum4.setObjectName("pushButtonNum4")
        self.pushButtonNum4.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum5 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('5'))
        self.pushButtonNum5.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY * 5, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum5.setFont(font)
        self.pushButtonNum5.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum5.setObjectName("pushButtonNum5")
        self.pushButtonNum5.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum6 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('6'))
        self.pushButtonNum6.setGeometry(QtCore.QRect(butttonLayoutX * 12.5, butttonLayoutY * 5, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum6.setFont(font)
        self.pushButtonNum6.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum6.setObjectName("pushButtonNum6")
        self.pushButtonNum6.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum7 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('7'))
        self.pushButtonNum7.setGeometry(QtCore.QRect(butttonLayoutX * 0.5, butttonLayoutY * 9, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum7.setFont(font)
        self.pushButtonNum7.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum7.setObjectName("pushButtonNum7")
        self.pushButtonNum7.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum8 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('8'))
        self.pushButtonNum8.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY * 9, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum8.setFont(font)
        self.pushButtonNum8.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum8.setObjectName("pushButtonNum8")
        self.pushButtonNum8.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum9 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('9'))
        self.pushButtonNum9.setGeometry(QtCore.QRect(butttonLayoutX * 12.5, butttonLayoutY * 9, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum9.setFont(font)
        self.pushButtonNum9.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum9.setObjectName("pushButtonNum9")
        self.pushButtonNum9.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNum0 = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.emulateKey('0'))
        self.pushButtonNum0.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY * 13, (buttonGoX * 0.833333)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNum0.setFont(font)
        self.pushButtonNum0.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNum0.setObjectName("pushButtonNum0")
        self.pushButtonNum0.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNumBS = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.keyBackSpace())
        self.pushButtonNumBS.setGeometry(QtCore.QRect(butttonLayoutX * 20.5, butttonLayoutY, buttonGoX + 1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.6)
        self.pushButtonNumBS.setFont(font)
        self.pushButtonNumBS.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNumBS.setObjectName("pushButtonNumBS")
        self.pushButtonNumBS.setFocusPolicy(Qt.NoFocus)
        self.pushButtonNumEnt = QtWidgets.QPushButton(self.groupBox_2, clicked = lambda: self.keyEnter())
        self.pushButtonNumEnt.setGeometry(QtCore.QRect(butttonLayoutX * 19.5, butttonLayoutY * 13, (buttonGoX * 1.25)+1, (buttonGoY * 0.5)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonNumEnt.setFont(font)
        self.pushButtonNumEnt.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonNumEnt.setObjectName("pushButtonNumEnt")
        self.pushButtonNumEnt.setFocusPolicy(Qt.NoFocus)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(butttonLayoutX * 69, butttonLayoutY * 0.5, (buttonGoX * 2.417)+1, (buttonGoY * 4.83333)+1))
        self.groupBox_3.setStyleSheet(f"color: #FFFFFF; background-color: #1e252a; border: {borderSize2}px solid #262d32;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButtonCam1 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam1GetSettings())
        self.pushButtonCam1.setGeometry(QtCore.QRect(butttonLayoutX * 3, butttonLayoutY * 1.5, (buttonGoX * 1.417)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonCam1.setFont(font)
        self.pushButtonCam1.setStyleSheet(f"color:black; border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam1.setFlat(False)
        self.pushButtonCam1.setObjectName("pushButtonCam1")
        self.pushButtonCam2 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam2GetSettings())
        self.pushButtonCam2.setGeometry(QtCore.QRect(butttonLayoutX * 3, butttonLayoutY * 7, (buttonGoX * 1.417)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonCam2.setFont(font)
        self.pushButtonCam2.setStyleSheet(f"color:black; border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setFlat(False)
        self.pushButtonCam2.setObjectName("pushButtonCam2")
        self.pushButtonCam3 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam3GetSettings())
        self.pushButtonCam3.setGeometry(QtCore.QRect(butttonLayoutX * 3, butttonLayoutY * 12.5, (buttonGoX * 1.417)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonCam3.setFont(font)
        self.pushButtonCam3.setStyleSheet(f"color:black; border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setFlat(False)
        self.pushButtonCam3.setObjectName("pushButtonCam3")
        self.pushButtonCam4 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam4GetSettings())
        self.pushButtonCam4.setGeometry(QtCore.QRect(butttonLayoutX * 3, butttonLayoutY * 18, (buttonGoX * 1.417)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonCam4.setFont(font)
        self.pushButtonCam4.setStyleSheet(f"color:black; border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setFlat(False)
        self.pushButtonCam4.setObjectName("pushButtonCam4")
        self.pushButtonCam5 = QtWidgets.QPushButton(self.groupBox_3, clicked = lambda: self.cam5GetSettings())
        self.pushButtonCam5.setGeometry(QtCore.QRect(butttonLayoutX * 3, butttonLayoutY * 23.5, (buttonGoX * 1.417)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonCam5.setFont(font)
        self.pushButtonCam5.setStyleSheet(f"color:black; border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setFlat(False)
        self.pushButtonCam5.setObjectName("pushButtonCam5")
        self.pushButtonClose = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.pushToClose())
        self.pushButtonClose.setGeometry(QtCore.QRect(butttonLayoutX * 86, butttonLayoutY * 2, (buttonGoX * 1.5)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #aa4c4C; border-radius: {borderRadius}px;")
        self.pushButtonClose.setFlat(False)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.pushButtonStore = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.sendStoreEEPROM())
        self.pushButtonStore.setGeometry(QtCore.QRect(butttonLayoutX * 86, butttonLayoutY * 23.5, (buttonGoX * 1.5)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushButtonStore.setFont(font)
        self.pushButtonStore.setStyleSheet(f"border: {borderSize2}px solid red; background-color: #4caa4C; border-radius: {borderRadius}px;")
        self.pushButtonStore.setFlat(False)
        self.pushButtonStore.setObjectName("pushButtonStore")
        self.checkBoxRevX = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxRevX.setGeometry(QtCore.QRect(butttonLayoutX * 20, butttonLayoutY * 45, 87, 20))
        self.checkBoxRevX.setObjectName("checkBoxRevX")
        self.checkBoxRevX.stateChanged.connect(self.on_checkboxX_toggled)
        self.checkBoxRevY = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxRevY.setGeometry(QtCore.QRect(butttonLayoutX * 20, butttonLayoutY * 46, 87, 20))
        self.checkBoxRevY.setObjectName("checkBoxRevY")
        self.checkBoxRevY.stateChanged.connect(self.on_checkboxY_toggled)
        self.checkBoxRevZ = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxRevZ.setGeometry(QtCore.QRect(butttonLayoutX * 20, butttonLayoutY * 47, 87, 20))
        self.checkBoxRevZ.setObjectName("checkBoxRevZ")
        self.checkBoxRevZ.stateChanged.connect(self.on_checkboxZ_toggled)
        self.checkBoxRevW = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxRevW.setGeometry(QtCore.QRect(butttonLayoutX * 20, butttonLayoutY * 48, 87, 20))
        self.checkBoxRevW.setObjectName("checkBoxRevW")
        self.checkBoxRevW.stateChanged.connect(self.on_checkboxW_toggled)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, buttonGoX * 16.5, (buttonGoY * 0.2)+1))
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
        self.pushButtonSlideLimit.setText(_translate("settingsWindow", "Slide Limit"))
        self.pushButtonSlideLocate.setText(_translate("settingsWindow", "Locate Home"))
        self.pushButtonSlideSetHome.setText(_translate("settingsWindow", "Set Home"))
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
        self.pushButtonNumEnt.setText(_translate("settingsWindow", "Set"))    #"↩"))
        self.pushButtonCam1.setText(_translate("settingsWindow", "Cam1"))
        self.pushButtonCam2.setText(_translate("settingsWindow", "Cam2"))
        self.pushButtonCam3.setText(_translate("settingsWindow", "Cam3"))
        self.pushButtonCam4.setText(_translate("settingsWindow", "Cam4"))
        self.pushButtonCam5.setText(_translate("settingsWindow", "Cam5"))
        self.pushButtonClose.setText(_translate("settingsWindow", "Close"))
        self.pushButtonStore.setText(_translate("settingsWindow", "Store"))
        self.labelCamHasSlider.setText(_translate("settingsWindow", "Has Slider"))
        self.pushButtonTLSteps.setText(_translate("settingsWindow", "TimeLapse Steps"))
        self.pushButtonTLStart.setText(_translate("settingsWindow", "Start"))
        self.pushButtonTLStop.setText(_translate("settingsWindow", "Stop"))
        self.checkBoxRevX.setText(_translate("settingsWindow", "Reverse X"))
        self.checkBoxRevY.setText(_translate("settingsWindow", "Reverse Y"))
        self.checkBoxRevZ.setText(_translate("settingsWindow", "Reverse Z"))
        self.checkBoxRevW.setText(_translate("settingsWindow", "Reverse W"))
        #self.pushButtonTLStep.setText(_translate("settingsWindow", "Step"))
        
        QtWidgets.QApplication.processEvents()

        if appSettings.debug:
            self.show()
        else:
            if sys.platform == "win32" or sys.platform == "linux":
                self.showFullScreen()
            else:
                self.showMaximized()
        if appSettings.running:
            self.getSettings()

        QtCore.QTimer.singleShot(500,self.scrollText)

    def getSettings(self):
        Worker.sendSerial(self, '&1K')
        Worker.sendSerial(self, '&2K')
        Worker.sendSerial(self, '&3K')
        Worker.sendSerial(self, '&4K')
        Worker.sendSerial(self, '&5K')
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
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'L' + widget.text())
            self.labelPTspeed4.setFocus()
        elif widget.objectName() == "labelSLaccel":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'l' + widget.text())
            self.labelSLspeed4.setFocus()
        elif widget.objectName() == "labelPTspeed1":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'F' + widget.text())
            self.labelZoomLimit.setFocus()
        elif widget.objectName() == "labelPTspeed2":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'f' + widget.text())
            self.labelPTspeed1.setFocus()
        elif widget.objectName() == "labelPTspeed3":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'G' + widget.text())
            self.labelPTspeed2.setFocus()
        elif widget.objectName() == "labelPTspeed4":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'g' + widget.text())
            self.labelPTspeed3.setFocus()
        elif widget.objectName() == "labelSLspeed1":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'H' + widget.text())
            self.labelSlideLimit.setFocus()
        elif widget.objectName() == "labelSLspeed2":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'h' + widget.text())
            self.labelSLspeed1.setFocus()
        elif widget.objectName() == "labelSLspeed3":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'J' + widget.text())
            self.labelSLspeed2.setFocus()
        elif widget.objectName() == "labelSLspeed4":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'j' + widget.text())
            self.labelSLspeed3.setFocus()
        elif widget.objectName() == "labelSlideLimit":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 't' + widget.text())
            self.labelPTaccel.setFocus()
        elif widget.objectName() == "labelZoomLimit":
            Worker.sendSerial(self, '&' + str(whichCamSerial) + 'w' + widget.text())
            self.labelSLaccel.setFocus()
            
        QtCore.QTimer.singleShot(500,self.scrollText)

    def scrollText(self):
        self.serialTextWindow.setHtml(appSettings.serialText)
        self.serialTextWindow.verticalScrollBar().setValue(self.serialTextWindow.verticalScrollBar().maximum())

    def sendStoreEEPROM(self):
        Worker.sendSerial(self, '&' + str(whichCamSerial) + 'U')
        QtCore.QTimer.singleShot(500,self.scrollText)

    def pushToClose(self):
        self.close()

    def on_checkboxX_toggled(self):
        if self.checkBoxRevX.isChecked():
            if appSettings.whichCamSerial == 1:
                camera1.revAxisX = True
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisX = True
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisX = True
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisX = True
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisX = True
        else:
            if appSettings.whichCamSerial == 1:
                camera1.revAxisX = False
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisX = False
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisX = False
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisX = False
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisX = False

    def on_checkboxY_toggled(self):
        if self.checkBoxRevY.isChecked():
            if appSettings.whichCamSerial == 1:
                camera1.revAxisY = True
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisY = True
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisY = True
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisY = True
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisY = True
        else:
            if appSettings.whichCamSerial == 1:
                camera1.revAxisY = False
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisY = False
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisY = False
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisY = False
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisY = False
            
    def on_checkboxZ_toggled(self):
        if self.checkBoxRevZ.isChecked():
            if appSettings.whichCamSerial == 1:
                camera1.revAxisZ = True
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisZ = True
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisZ = True
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisZ = True
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisZ = True
        else:
            if appSettings.whichCamSerial == 1:
                camera1.revAxisZ = False
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisZ = False
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisZ = False
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisZ = False
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisZ = False
            
    def on_checkboxW_toggled(self):
        if self.checkBoxRevW.isChecked():
            if appSettings.whichCamSerial == 1:
                camera1.revAxisW = True
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisW = True
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisW = True
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisW = True
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisW = True
        else:
            if appSettings.whichCamSerial == 1:
                camera1.revAxisW = False
            elif appSettings.whichCamSerial == 2:
                camera2.revAxisW = False
            elif appSettings.whichCamSerial == 3:
                camera3.revAxisW = False
            elif appSettings.whichCamSerial == 4:
                camera4.revAxisW = False
            elif appSettings.whichCamSerial == 5:
                camera5.revAxisW = False

    def cam1GetSettings(self):
        appSettings.whichCamSerial = 1
        Worker.sendSerial(self, '&1K')

        QtCore.QTimer.singleShot(200,self.showCam1Settings)

    def showCam1Settings(self):
        self.labelPTaccel.setText(str(camera1.panTiltAccel))
        self.labelSLaccel.setText(str(camera1.sliderAccel))
        self.labelPTspeed1.setText(str(camera1.panTiltSpeed1))
        self.labelPTspeed2.setText(str(camera1.panTiltSpeed2))
        self.labelPTspeed3.setText(str(camera1.panTiltSpeed3))
        self.labelPTspeed4.setText(str(camera1.panTiltSpeed4))
        self.labelSLspeed1.setText(str(camera1.sliderSpeed1))
        self.labelSLspeed2.setText(str(camera1.sliderSpeed2))
        self.labelSLspeed3.setText(str(camera1.sliderSpeed3))
        self.labelSLspeed4.setText(str(camera1.sliderSpeed4))
        self.labelSlideLimit.setText(str(camera1.slideLimit))
        self.labelZoomLimit.setText(str(camera1.zoomLimit))
        self.checkBoxRevX.setChecked(camera1.revAxisX)
        self.checkBoxRevY.setChecked(camera1.revAxisY)
        self.checkBoxRevZ.setChecked(camera1.revAxisZ)
        self.checkBoxRevW.setChecked(camera1.revAxisW)

        if camera1.hasSlider == True:
            self.labelCamHasSlider.setVisible(True)
        else:
            self.labelCamHasSlider.setVisible(False)

        self.pushButtonCam1.setStyleSheet(f"color: black; border: {borderSize2}px solid red; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

        QtCore.QTimer.singleShot(500,self.scrollText)

    def cam2GetSettings(self):
        appSettings.whichCamSerial = 2
        Worker.sendSerial(self, '&2K')

        QtCore.QTimer.singleShot(200,self.showCam2Settings)

    def showCam2Settings(self):
        self.labelPTaccel.setText(str(camera2.panTiltAccel))
        self.labelSLaccel.setText(str(camera2.sliderAccel))
        self.labelPTspeed1.setText(str(camera2.panTiltSpeed1))
        self.labelPTspeed2.setText(str(camera2.panTiltSpeed2))
        self.labelPTspeed3.setText(str(camera2.panTiltSpeed3))
        self.labelPTspeed4.setText(str(camera2.panTiltSpeed4))
        self.labelSLspeed1.setText(str(camera2.sliderSpeed1))
        self.labelSLspeed2.setText(str(camera2.sliderSpeed2))
        self.labelSLspeed3.setText(str(camera2.sliderSpeed3))
        self.labelSLspeed4.setText(str(camera2.sliderSpeed4))
        self.labelSlideLimit.setText(str(camera2.slideLimit))
        self.labelZoomLimit.setText(str(camera2.zoomLimit))
        self.checkBoxRevX.setChecked(camera2.revAxisX)
        self.checkBoxRevY.setChecked(camera2.revAxisY)
        self.checkBoxRevZ.setChecked(camera2.revAxisZ)
        self.checkBoxRevW.setChecked(camera2.revAxisW)

        if camera2.hasSlider == True:
            self.labelCamHasSlider.setVisible(True)
        else:
            self.labelCamHasSlider.setVisible(False)

        self.pushButtonCam1.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setStyleSheet(f"color: black; border: {borderSize2}px solid red; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

        QtCore.QTimer.singleShot(500,self.scrollText)

    def cam3GetSettings(self):
        appSettings.whichCamSerial = 3
        Worker.sendSerial(self, '&3K')

        QtCore.QTimer.singleShot(200,self.showCam3Settings)

    def showCam3Settings(self):
        self.labelPTaccel.setText(str(camera3.panTiltAccel))
        self.labelSLaccel.setText(str(camera3.sliderAccel))
        self.labelPTspeed1.setText(str(camera3.panTiltSpeed1))
        self.labelPTspeed2.setText(str(camera3.panTiltSpeed2))
        self.labelPTspeed3.setText(str(camera3.panTiltSpeed3))
        self.labelPTspeed4.setText(str(camera3.panTiltSpeed4))
        self.labelSLspeed1.setText(str(camera3.sliderSpeed1))
        self.labelSLspeed2.setText(str(camera3.sliderSpeed2))
        self.labelSLspeed3.setText(str(camera3.sliderSpeed3))
        self.labelSLspeed4.setText(str(camera3.sliderSpeed4))
        self.labelSlideLimit.setText(str(camera3.slideLimit))
        self.labelZoomLimit.setText(str(camera3.zoomLimit))
        self.checkBoxRevX.setChecked(camera3.revAxisX)
        self.checkBoxRevY.setChecked(camera3.revAxisY)
        self.checkBoxRevZ.setChecked(camera3.revAxisZ)
        self.checkBoxRevW.setChecked(camera3.revAxisW)

        if camera3.hasSlider == True:
            self.labelCamHasSlider.setVisible(True)
        else:
            self.labelCamHasSlider.setVisible(False)

        self.pushButtonCam1.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setStyleSheet(f"color: black; border: {borderSize2}px solid red; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

        QtCore.QTimer.singleShot(500,self.scrollText)

    def cam4GetSettings(self):
        appSettings.whichCamSerial = 4
        Worker.sendSerial(self, '&4K')

        QtCore.QTimer.singleShot(200,self.showCam4Settings)

    def showCam4Settings(self):
        self.labelPTaccel.setText(str(camera4.panTiltAccel))
        self.labelSLaccel.setText(str(camera4.sliderAccel))
        self.labelPTspeed1.setText(str(camera4.panTiltSpeed1))
        self.labelPTspeed2.setText(str(camera4.panTiltSpeed2))
        self.labelPTspeed3.setText(str(camera4.panTiltSpeed3))
        self.labelPTspeed4.setText(str(camera4.panTiltSpeed4))
        self.labelSLspeed1.setText(str(camera4.sliderSpeed1))
        self.labelSLspeed2.setText(str(camera4.sliderSpeed2))
        self.labelSLspeed3.setText(str(camera4.sliderSpeed3))
        self.labelSLspeed4.setText(str(camera4.sliderSpeed4))
        self.labelSlideLimit.setText(str(camera4.slideLimit))
        self.labelZoomLimit.setText(str(camera4.zoomLimit))
        self.checkBoxRevX.setChecked(camera4.revAxisX)
        self.checkBoxRevY.setChecked(camera4.revAxisY)
        self.checkBoxRevZ.setChecked(camera4.revAxisZ)
        self.checkBoxRevW.setChecked(camera4.revAxisW)

        if camera4.hasSlider == True:
            self.labelCamHasSlider.setVisible(True)
        else:
            self.labelCamHasSlider.setVisible(False)

        self.pushButtonCam1.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setStyleSheet(f"color: black; border: {borderSize2}px solid red; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #8D5395; border-radius: {borderRadius2}px;")

        QtCore.QTimer.singleShot(500,self.scrollText)

    def cam5GetSettings(self):
        appSettings.whichCamSerial = 5
        Worker.sendSerial(self, '&5K')

        QtCore.QTimer.singleShot(200,self.showCam5Settings)

    def showCam5Settings(self):
        self.labelPTaccel.setText(str(camera5.panTiltAccel))
        self.labelSLaccel.setText(str(camera5.sliderAccel))
        self.labelPTspeed1.setText(str(camera5.panTiltSpeed1))
        self.labelPTspeed2.setText(str(camera5.panTiltSpeed2))
        self.labelPTspeed3.setText(str(camera5.panTiltSpeed3))
        self.labelPTspeed4.setText(str(camera5.panTiltSpeed4))
        self.labelSLspeed1.setText(str(camera5.sliderSpeed1))
        self.labelSLspeed2.setText(str(camera5.sliderSpeed2))
        self.labelSLspeed3.setText(str(camera5.sliderSpeed3))
        self.labelSLspeed4.setText(str(camera5.sliderSpeed4))
        self.labelSlideLimit.setText(str(camera5.slideLimit))
        self.labelZoomLimit.setText(str(camera5.zoomLimit))
        self.checkBoxRevX.setChecked(camera5.revAxisX)
        self.checkBoxRevY.setChecked(camera5.revAxisY)
        self.checkBoxRevZ.setChecked(camera5.revAxisZ)
        self.checkBoxRevW.setChecked(camera5.revAxisW)

        if camera5.hasSlider == True:
            self.labelCamHasSlider.setVisible(True)
        else:
            self.labelCamHasSlider.setVisible(False)

        self.pushButtonCam1.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius2}px;")
        self.pushButtonCam2.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
        self.pushButtonCam3.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #807100; border-radius: {borderRadius2}px;")
        self.pushButtonCam4.setStyleSheet(f"color: black; border: {borderSize2}px solid grey; background-color: #008071; border-radius: {borderRadius2}px;")
        self.pushButtonCam5.setStyleSheet(f"color: black; border: {borderSize2}px solid red; background-color: #8D5395; border-radius: {borderRadius2}px;")

        QtCore.QTimer.singleShot(500,self.scrollText)

    def sendSerial(self, toSendData):
        global sendData
        sendData = toSendData

    def locateHome(self):
        global locateHomeActive
        global whichCamSerial

        if locateHomeActive:
            locateHomeActive = False
            self.pushButtonSlideLocate.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")

            if appSettings.whichCamSerial == 1:
                Worker.sendSerial(self, '&1T')
            elif appSettings.whichCamSerial == 2:
                Worker.sendSerial(self, '&2T')
            elif appSettings.whichCamSerial == 3:
                Worker.sendSerial(self, '&3T')
            elif appSettings.whichCamSerial == 4:
                Worker.sendSerial(self, '&4T')
            elif appSettings.whichCamSerial == 5:
                Worker.sendSerial(self, '&5T')
        else:
            locateHomeActive = True
            self.pushButtonSlideLocate.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #a0405C; border-radius: {borderRadius2}px;")

            if appSettings.whichCamSerial == 1:
                Worker.sendSerial(self, '&1T')
            elif appSettings.whichCamSerial == 2:
                Worker.sendSerial(self, '&2T')
            elif appSettings.whichCamSerial == 3:
                Worker.sendSerial(self, '&3T')
            elif appSettings.whichCamSerial == 4:
                Worker.sendSerial(self, '&4T')
            elif appSettings.whichCamSerial == 5:
                Worker.sendSerial(self, '&5T')

    def setHome(self):
        global locateHomeActive
        global whichCamSerial

        if locateHomeActive:
            locateHomeActive = False
            self.pushButtonSlideLocate.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")

            if appSettings.whichCamSerial == 1:
                Worker.sendSerial(self, '&1u')
            elif appSettings.whichCamSerial == 2:
                Worker.sendSerial(self, '&2u')
            elif appSettings.whichCamSerial == 3:
                Worker.sendSerial(self, '&3u')
            elif appSettings.whichCamSerial == 4:
                Worker.sendSerial(self, '&4u')
            elif appSettings.whichCamSerial == 5:
                Worker.sendSerial(self, '&5u')

        self.pushButtonSlideSetHome.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #40805C; border-radius: {borderRadius2}px;")

    def TLSet(self):
        global whichCamSerial

        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&1o' + self.labelTLSteps.text())
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&2o' + self.labelTLSteps.text())
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&3o' + self.labelTLSteps.text())
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&4o' + self.labelTLSteps.text())
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&5o' + self.labelTLSteps.text())

    def TLStart(self):
        global whichCamSerial

        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&1e')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&2e')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&3e')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&4e')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&5e')

    def TLStop(self):
        global whichCamSerial

        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&1E')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&2E')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&3E')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&4E')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&5E')

    def TLStep(self):
        global whichCamSerial

        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&1O')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&2O')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&3O')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&4O')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&5O')

class Ui_MoverWindow(QMainWindow):
    def __init__(self):
        super(Ui_MoverWindow, self).__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

    def setupUi(self):
        global butttonLayoutX
        global butttonLayoutY
        global buttonGoX
        global buttonGoY
        global borderSize
        global borderSize2
        global borderRadius
        global borderRadius2
        global winSize

        self.setObjectName("MainWindow")
        self.resize((buttonGoX * 7.1666666667)+1 , (buttonGoY * 6.6666666667)+1)
        self.setStyleSheet("background-color: #181e23;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushUP10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.up10())
        self.pushUP10.setGeometry(QtCore.QRect(butttonLayoutX * 12, 0, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushUP10.setFont(font)
        self.pushUP10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #208020; border-radius: {borderRadius}px;")
        self.pushUP10.setObjectName("pushUP10")
        self.pushUP1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.up1())
        self.pushUP1.setGeometry(QtCore.QRect(butttonLayoutX * 12, butttonLayoutY * 6.5, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushUP1.setFont(font)
        self.pushUP1.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #40a040; border-radius: {borderRadius}px;")
        self.pushUP1.setObjectName("pushUP1")
        self.pushDOWN1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.down1())
        self.pushDOWN1.setGeometry(QtCore.QRect(butttonLayoutX * 12, butttonLayoutY * 17.5, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushDOWN1.setFont(font)
        self.pushDOWN1.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #40a040; border-radius: {borderRadius}px;")
        self.pushDOWN1.setObjectName("pushDOWN1")
        self.pushDOWN10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.down10())
        self.pushDOWN10.setGeometry(QtCore.QRect(butttonLayoutX * 12, butttonLayoutY * 24, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushDOWN10.setFont(font)
        self.pushDOWN10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #208020; border-radius: {borderRadius}px;")
        self.pushDOWN10.setObjectName("pushDOWN10")
        self.pushLEFT10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.left10())
        self.pushLEFT10.setGeometry(QtCore.QRect(0, butttonLayoutY * 12, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushLEFT10.setFont(font)
        self.pushLEFT10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        self.pushLEFT10.setObjectName("pushLEFT10")
        self.pushLEFT1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.left1())
        self.pushLEFT1.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY * 12, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushLEFT1.setFont(font)
        self.pushLEFT1.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #a09100; border-radius: {borderRadius}px;")
        self.pushLEFT1.setObjectName("pushLEFT1")
        self.pushRIGHT1 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.right1())
        self.pushRIGHT1.setGeometry(QtCore.QRect(butttonLayoutX * 17.5, butttonLayoutY * 12, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushRIGHT1.setFont(font)
        self.pushRIGHT1.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #a09100; border-radius: {borderRadius}px;")
        self.pushRIGHT1.setObjectName("pushRIGHT1")
        self.pushRIGHT10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.right10())
        self.pushRIGHT10.setGeometry(QtCore.QRect(butttonLayoutX * 24, butttonLayoutY * 12, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushRIGHT10.setFont(font)
        self.pushRIGHT10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;")
        self.pushRIGHT10.setObjectName("pushRIGHT10")
        self.pushSlideLeft100 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideLeft100())
        self.pushSlideLeft100.setGeometry(QtCore.QRect(0, butttonLayoutY * 32, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushSlideLeft100.setFont(font)
        self.pushSlideLeft100.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #710080; border-radius: {borderRadius}px;")
        self.pushSlideLeft100.setObjectName("pushSlideLeft100")
        self.pushSlideLeft10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideLeft10())
        self.pushSlideLeft10.setGeometry(QtCore.QRect(butttonLayoutX * 6.5, butttonLayoutY * 32, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushSlideLeft10.setFont(font)
        self.pushSlideLeft10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #9100a0; border-radius: {borderRadius}px;")
        self.pushSlideLeft10.setObjectName("pushSlideLeft10")
        self.pushSlideRight10 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideRight10())
        self.pushSlideRight10.setGeometry(QtCore.QRect(butttonLayoutX * 17.5, butttonLayoutY * 32, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushSlideRight10.setFont(font)
        self.pushSlideRight10.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #9100a0; border-radius: {borderRadius}px;")
        self.pushSlideRight10.setObjectName("pushSlideRight10")
        self.pushSlideRight100 = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.slideRight100())
        self.pushSlideRight100.setGeometry(QtCore.QRect(butttonLayoutX * 24, butttonLayoutY * 32, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushSlideRight100.setFont(font)
        self.pushSlideRight100.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #710080; border-radius: {borderRadius}px;")
        self.pushSlideRight100.setObjectName("pushSlideRight100")
        self.pushZoomInFast = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(6), released= lambda: self.zoomMove(0))
        self.pushZoomInFast.setGeometry(QtCore.QRect(butttonLayoutX * 37, butttonLayoutY * 2.5, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushZoomInFast.setFont(font)
        self.pushZoomInFast.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        self.pushZoomInFast.setObjectName("pushZoomInFast")
        self.pushZoomInSlow = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(1), released= lambda: self.zoomMove(0))
        self.pushZoomInSlow.setGeometry(QtCore.QRect(butttonLayoutX * 37, butttonLayoutY * 9, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushZoomInSlow.setFont(font)
        self.pushZoomInSlow.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #607Ca0; border-radius: {borderRadius}px;")
        self.pushZoomInSlow.setObjectName("pushZoomInSlow")
        self.pushZoomOutSlow = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(-1), released= lambda: self.zoomMove(0))
        self.pushZoomOutSlow.setGeometry(QtCore.QRect(butttonLayoutX * 37, butttonLayoutY * 20, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushZoomOutSlow.setFont(font)
        self.pushZoomOutSlow.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #607Ca0; border-radius: {borderRadius}px;")
        self.pushZoomOutSlow.setObjectName("pushZoomOutSlow")
        self.pushZoomOutFast = QtWidgets.QPushButton(self.centralwidget, pressed= lambda: self.zoomMove(-6), released= lambda: self.zoomMove(0))
        self.pushZoomOutFast.setGeometry(QtCore.QRect(butttonLayoutX * 37, butttonLayoutY * 26.5, buttonGoX + 1, buttonGoY + 1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 2.2)
        self.pushZoomOutFast.setFont(font)
        self.pushZoomOutFast.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;")
        self.pushZoomOutFast.setObjectName("pushZoomOutFast")
        self.pushClose = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.pushToClose())
        self.pushClose.setGeometry(QtCore.QRect(butttonLayoutX * 0.5, 0, (buttonGoX * 0.8333333333)+1, (buttonGoY * 0.8333333333)+1))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 3)
        self.pushClose.setFont(font)
        self.pushClose.setStyleSheet(f"border: {borderSize}px solid grey; background-color: #cc7777; border-radius: {borderRadius}px;")
        self.pushClose.setObjectName("pushClose")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, (buttonGoX * 5)+3, buttonGoY * 0.2))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.showNormal()
    
        if appSettings.debug:
            ag = self.geometry
        else:
            ag = QtGui.QGuiApplication.primaryScreen().size()

        widget = self.geometry()
        x = (ag.width() / 2) - (widget.width() / 2)
        y = 2 * ag.height() - ag.height() - widget.height() - 50
        if appSettings.debug:
            x = x - 100
            y = y - 100
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
        zoomSerial = "&"
        
        if appSettings.whichCamSerial == 1: zoomSerial = zoomSerial + "1"
        elif appSettings.whichCamSerial == 2: zoomSerial = zoomSerial + "2"
        elif appSettings.whichCamSerial == 3: zoomSerial = zoomSerial + "3"
        elif appSettings.whichCamSerial == 4: zoomSerial = zoomSerial + "4"
        elif appSettings.whichCamSerial == 5: zoomSerial = zoomSerial + "5"

        if speed == -8: Worker.sendSerial(self, zoomSerial + 'a8')
        elif speed == -7: Worker.sendSerial(self, zoomSerial + 'a7')
        elif speed == -6: Worker.sendSerial(self, zoomSerial + 'a6')
        elif speed == -5: Worker.sendSerial(self, zoomSerial + 'a5')
        elif speed == -4: Worker.sendSerial(self, zoomSerial + 'a4')
        elif speed == -3: Worker.sendSerial(self, zoomSerial + 'a3')
        elif speed == -2: Worker.sendSerial(self, zoomSerial + 'a2')
        elif speed == -1: Worker.sendSerial(self, zoomSerial + 'a1')
        elif speed == 1: Worker.sendSerial(self, zoomSerial + 'A1')
        elif speed == 2: Worker.sendSerial(self, zoomSerial + 'A2')
        elif speed == 3: Worker.sendSerial(self, zoomSerial + 'A3')
        elif speed == 4: Worker.sendSerial(self, zoomSerial + 'A4')
        elif speed == 5: Worker.sendSerial(self, zoomSerial + 'A5')
        elif speed == 6: Worker.sendSerial(self, zoomSerial + 'A6')
        elif speed == 7: Worker.sendSerial(self, zoomSerial + 'A7')
        elif speed == 8: Worker.sendSerial(self, zoomSerial + 'A8')
        else: 
            Worker.sendSerial(self, zoomSerial + 'q')
            Worker.sendSerial(self, zoomSerial + 'q')
            Worker.sendSerial(self, zoomSerial + 'q')
            Worker.sendSerial(self, zoomSerial + 'q')
            Worker.sendSerial(self, zoomSerial + 'q')

    
    def up10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??T10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?T10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?T10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?T10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?T10')

    def up1(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??T0.5')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?T0.5')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?T0.5')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?T0.5')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?T0.5')

    def down1(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??T-0.5')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?T-0.5')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?T-0.5')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?T-0.5')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?T-0.5')

    def down10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??T-10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?T-10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?T-10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?T-10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?T-10')

    def left10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??P-10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?P-10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?P-10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?P-10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?P-10')

    def left1(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??P-0.5')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?P-0.5')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?P-0.5')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?P-0.5')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?P-0.5')

    def right1(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??P0.5')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?P0.5')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?P0.5')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?P0.5')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?P0.5')

    def right10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??P10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?P10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?P10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?P10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?P10')



    def slideLeft100(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??X-100')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?X-100')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?X-100')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?X-100')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?X-100')

    def slideLeft10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??X-10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?X-10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?X-10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?X-10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?X-10')

    def slideRight10(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??X10')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?X10')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?X10')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?X10')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?X10')

    def slideRight100(self):
        if appSettings.whichCamSerial == 1:
            Worker.sendSerial(self, '&??X100')
        elif appSettings.whichCamSerial == 2:
            Worker.sendSerial(self, '&!?X100')
        elif appSettings.whichCamSerial == 3:
            Worker.sendSerial(self, '&@?X100')
        elif appSettings.whichCamSerial == 4:
            Worker.sendSerial(self, '&&?X100')
        elif appSettings.whichCamSerial == 5:
            Worker.sendSerial(self, '&*?X100')

class Ui_editWindow(QMainWindow):
    def __init__(self):
        super(Ui_editWindow, self).__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

    def setupUi(self):
        global butttonLayoutX
        global butttonLayoutY
        global buttonGoX
        global buttonGoY
        global buttonCamY
        global borderSize
        global borderSize2
        global borderRadius
        global borderRadius2
        global winSize

        self.setObjectName("editWindow")
        self.resize(buttonGoX * 3, buttonGoY* 1.4)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #7593BC;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(butttonLayoutX * 2, butttonLayoutY * 2.5, buttonGoX, buttonCamY)) #butttonLayoutX * 2, butttonLayoutY * 1.5, buttonGoX, buttonGoY))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(butttonLayoutX * winSize * 1.6)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #cccccc; border-radius: {borderRadius2}px;")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.editSet())
        self.pushButton.setGeometry(QtCore.QRect(butttonLayoutX *10, butttonLayoutY * 2.5, (buttonGoX), buttonCamY)) # * 0.75)+1, (buttonGoY * 0.6666666667)+1))
        font = QtGui.QFont()
        font.setPointSize(butttonLayoutX * winSize * 2.4)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #cccccc;")
        self.pushButton.setObjectName("pushButton")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, buttonGoX * 2.7666666667, buttonGoY * 0.2))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

        ag = QtGui.QGuiApplication.primaryScreen().size()
        widget = self.geometry()

        x = (ag.width() / 2) - (widget.width() / 2)
        y = ag.height() / 4

        x = int(x)
        y = int(y)
        
        self.move(x, y)

        self.lineEdit.setFocus()
        
    def editSet(self):
        newText = self.lineEdit.text()

        if appSettings.editButton == 11: PTSapp.pushButton11.setText(newText)
        if appSettings.editButton == 12: PTSapp.pushButton12.setText(newText)
        if appSettings.editButton == 13: PTSapp.pushButton13.setText(newText)
        if appSettings.editButton == 14: PTSapp.pushButton14.setText(newText)
        if appSettings.editButton == 15: PTSapp.pushButton15.setText(newText)
        if appSettings.editButton == 16: PTSapp.pushButton16.setText(newText)
        if appSettings.editButton == 17: PTSapp.pushButton17.setText(newText)
        if appSettings.editButton == 18: PTSapp.pushButton18.setText(newText)
        if appSettings.editButton == 19: PTSapp.pushButton19.setText(newText)
        if appSettings.editButton == 10: PTSapp.pushButton10.setText(newText)

        if appSettings.editButton == 21: PTSapp.pushButton21.setText(newText)
        if appSettings.editButton == 22: PTSapp.pushButton22.setText(newText)
        if appSettings.editButton == 23: PTSapp.pushButton23.setText(newText)
        if appSettings.editButton == 24: PTSapp.pushButton24.setText(newText)
        if appSettings.editButton == 25: PTSapp.pushButton25.setText(newText)
        if appSettings.editButton == 26: PTSapp.pushButton26.setText(newText)
        if appSettings.editButton == 27: PTSapp.pushButton27.setText(newText)
        if appSettings.editButton == 28: PTSapp.pushButton28.setText(newText)
        if appSettings.editButton == 29: PTSapp.pushButton29.setText(newText)
        if appSettings.editButton == 20: PTSapp.pushButton20.setText(newText)

        if appSettings.editButton == 31: PTSapp.pushButton31.setText(newText)
        if appSettings.editButton == 32: PTSapp.pushButton32.setText(newText)
        if appSettings.editButton == 33: PTSapp.pushButton33.setText(newText)
        if appSettings.editButton == 34: PTSapp.pushButton34.setText(newText)
        if appSettings.editButton == 35: PTSapp.pushButton35.setText(newText)
        if appSettings.editButton == 36: PTSapp.pushButton36.setText(newText)
        if appSettings.editButton == 37: PTSapp.pushButton37.setText(newText)
        if appSettings.editButton == 38: PTSapp.pushButton38.setText(newText)
        if appSettings.editButton == 39: PTSapp.pushButton39.setText(newText)
        if appSettings.editButton == 30: PTSapp.pushButton30.setText(newText)

        if appSettings.editButton == 41: PTSapp.pushButton41.setText(newText)
        if appSettings.editButton == 42: PTSapp.pushButton42.setText(newText)
        if appSettings.editButton == 43: PTSapp.pushButton43.setText(newText)
        if appSettings.editButton == 44: PTSapp.pushButton44.setText(newText)
        if appSettings.editButton == 45: PTSapp.pushButton45.setText(newText)
        if appSettings.editButton == 46: PTSapp.pushButton46.setText(newText)
        if appSettings.editButton == 47: PTSapp.pushButton47.setText(newText)
        if appSettings.editButton == 48: PTSapp.pushButton48.setText(newText)
        if appSettings.editButton == 49: PTSapp.pushButton49.setText(newText)
        if appSettings.editButton == 40: PTSapp.pushButton40.setText(newText)

        if appSettings.editButton == 51: PTSapp.pushButton51.setText(newText)
        if appSettings.editButton == 52: PTSapp.pushButton52.setText(newText)
        if appSettings.editButton == 53: PTSapp.pushButton53.setText(newText)
        if appSettings.editButton == 54: PTSapp.pushButton54.setText(newText)
        if appSettings.editButton == 55: PTSapp.pushButton55.setText(newText)
        if appSettings.editButton == 56: PTSapp.pushButton56.setText(newText)
        if appSettings.editButton == 57: PTSapp.pushButton57.setText(newText)
        if appSettings.editButton == 58: PTSapp.pushButton58.setText(newText)
        if appSettings.editButton == 59: PTSapp.pushButton59.setText(newText)
        if appSettings.editButton == 50: PTSapp.pushButton50.setText(newText)

        if appSettings.editButton == 61: 
            camera1.name = newText
            PTSapp.pushButtonCam1.setText(camera1.name)
        if appSettings.editButton == 62: 
            camera2.name = newText
            PTSapp.pushButtonCam2.setText(camera2.name)
        if appSettings.editButton == 63: 
            camera3.name = newText
            PTSapp.pushButtonCam3.setText(camera3.name)
        if appSettings.editButton == 64: 
            camera4.name = newText
            PTSapp.pushButtonCam4.setText(camera4.name)
        if appSettings.editButton == 65: 
            camera5.name = newText
            PTSapp.pushButtonCam5.setText(camera5.name)

        newText = ""

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

class repceiveMsg():
    def __init__(self, msg):
        super().__init__()
        serialText = msg

        while True:
            if appSettings.debug:
                print("Received msg:", msg)

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
                    camera1.pos1Set = True
                elif msg[1:4] == "121":
                    camera1.pos2Set = True
                elif msg[1:4] == "131":
                    camera1.pos3Set = True
                elif msg[1:4] == "141":
                    camera1.pos4Set = True
                elif msg[1:4] == "151":
                    camera1.pos5Set = True
                elif msg[1:4] == "161":
                    camera1.pos6Set = True
                elif msg[1:4] == "171":
                    camera1.pos7Set = True
                elif msg[1:4] == "181":
                    camera1.pos8Set = True
                elif msg[1:4] == "191":
                    camera1.pos9Set = True
                elif msg[1:4] == "101":
                    camera1.pos10Set = True
                elif msg[1:4] == "112":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos1Run = True
                elif msg[1:4] == "122":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos2Run = True
                elif msg[1:4] == "132":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos3Run = True
                elif msg[1:4] == "142":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos4Run = True
                elif msg[1:4] == "152":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos5Run = True
                elif msg[1:4] == "162":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos6Run = True
                elif msg[1:4] == "172":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos7Run = True
                elif msg[1:4] == "182":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos8Run = True
                elif msg[1:4] == "192":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos9Run = True
                elif msg[1:4] == "102":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                    camera1.pos10Run = True
                elif msg[1:4] == "113":
                    camera1.pos1Run = False
                    camera1.pos1At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "123":
                    camera1.pos2Run = False
                    camera1.pos2At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "133":
                    camera1.pos3Run = False
                    camera1.pos3At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "143":
                    camera1.pos4Run = False
                    camera1.pos4At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "153":
                    camera1.pos5Run = False
                    camera1.pos5At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "163":
                    camera1.pos6Run = False
                    camera1.pos6At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "173":
                    camera1.pos7Run = False
                    camera1.pos7At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "183":
                    camera1.pos8Run = False
                    camera1.pos8At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "193":
                    camera1.pos9Run = False
                    camera1.pos9At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "103":
                    camera1.pos10Run = False
                    camera1.pos10At = True
                    if camera1.running:
                        PTSapp.runCam1(self)
                elif msg[1:4] == "114":
                    pass
                elif msg[1:4] == "124":
                    pass
                elif msg[1:4] == "115":
                    camera1.useSetSpeed = True
                elif msg[1:4] == "105":
                    camera1.useSetSpeed = False
                elif msg[1:4] == "100":
                    camera1.pos1Run = False
                    camera1.pos1Set = False
                    camera1.pos1At = False
                    camera1.pos2Run = False
                    camera1.pos2Set = False
                    camera1.pos2At = False
                    camera1.pos3Run = False 
                    camera1.pos3Set = False
                    camera1.pos3At = False
                    camera1.pos4Run = False
                    camera1.pos4Set = False
                    camera1.pos4At = False
                    camera1.pos5Run = False
                    camera1.pos5Set = False
                    camera1.pos5At = False
                    camera1.pos6Run = False
                    camera1.pos6Set = False
                    camera1.pos6At = False
                    camera1.pos7Run = False
                    camera1.pos7Set = False
                    camera1.pos7At = False
                    camera1.pos8Run = False
                    camera1.pos8Set = False
                    camera1.pos8At = False
                    camera1.pos9Run = False
                    camera1.pos9Set = False
                    camera1.pos9At = False
                    camera1.pos10Run = False
                    camera1.pos10Set = False
                    camera1.pos10At = False
                    
                elif msg[1:4] == "211":              # Cam 2 Set Pos 1
                    camera2.pos1Set = True
                elif msg[1:4] == "221":
                    camera2.pos2Set = True
                elif msg[1:4] == "231":
                    camera2.pos3Set = True
                elif msg[1:4] == "241":
                    camera2.pos4Set = True
                elif msg[1:4] == "251":
                    camera2.pos5Set = True
                elif msg[1:4] == "261":
                    camera2.pos6Set = True
                elif msg[1:4] == "271":
                    camera2.pos7Set = True
                elif msg[1:4] == "281":
                    camera2.pos8Set = True
                elif msg[1:4] == "291":
                    camera2.pos9Set = True
                elif msg[1:4] == "201":
                    camera2.pos10Set = True
                elif msg[1:4] == "212":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos1Run = True
                elif msg[1:4] == "222":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos2Run = True
                elif msg[1:4] == "232":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos3Run = True
                elif msg[1:4] == "242":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos4Run = True
                elif msg[1:4] == "252":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos5Run = True
                elif msg[1:4] == "262":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos6Run = True
                elif msg[1:4] == "272":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos7Run = True
                elif msg[1:4] == "282":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos8Run = True
                elif msg[1:4] == "292":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos9Run = True
                elif msg[1:4] == "202":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                    camera2.pos10Run = True
                elif msg[1:4] == "213":
                    camera2.pos1Run = False
                    camera2.pos1At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "223":
                    camera2.pos2Run = False
                    camera2.pos2At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "233":
                    camera2.pos3Run = False
                    camera2.pos3At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "243":
                    camera2.pos4Run = False
                    camera2.pos4At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "253":
                    camera2.pos5Run = False
                    camera2.pos5At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "263":
                    camera2.pos6Run = False
                    camera2.pos6At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "273":
                    camera2.pos7Run = False
                    camera2.pos7At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "283":
                    camera2.pos8Run = False
                    camera2.pos8At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "293":
                    camera2.pos9Run = False
                    camera2.pos9At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "203":
                    camera2.pos10Run = False
                    camera2.pos10At = True
                    if camera2.running:
                        PTSapp.runCam2(self)
                elif msg[1:4] == "214":
                    pass
                elif msg[1:4] == "224":
                    pass
                elif msg[1:4] == "215":
                    camera2.useSetSpeed = True
                elif msg[1:4] == "205":
                    camera2.useSetSpeed = False
                elif msg[1:4] == "200":
                    camera2.pos1Run = False
                    camera2.pos1Set = False
                    camera2.pos1At = False
                    camera2.pos2Run = False
                    camera2.pos2Set = False
                    camera2.pos2At = False
                    camera2.pos3Run = False 
                    camera2.pos3Set = False
                    camera2.pos3At = False
                    camera2.pos4Run = False
                    camera2.pos4Set = False
                    camera2.pos4At = False
                    camera2.pos5Run = False
                    camera2.pos5Set = False
                    camera2.pos5At = False
                    camera2.pos6Run = False
                    camera2.pos6Set = False
                    camera2.pos6At = False
                    camera2.pos7Run = False
                    camera2.pos7Set = False
                    camera2.pos7At = False
                    camera2.pos8Run = False
                    camera2.pos8Set = False
                    camera2.pos8At = False
                    camera2.pos9Run = False
                    camera2.pos9Set = False
                    camera2.pos9At = False
                    camera2.pos10Run = False
                    camera2.pos10Set = False
                    camera2.pos10At = False
                elif msg[1:4] == "311":              # Cam 3 Set Pos 1
                    camera3.pos1Set = True
                elif msg[1:4] == "321":
                    camera3.pos2Set = True
                elif msg[1:4] == "331":
                    camera3.pos3Set = True
                elif msg[1:4] == "341":
                    camera3.pos4Set = True
                elif msg[1:4] == "351":
                    camera3.pos5Set = True
                elif msg[1:4] == "361":
                    camera3.pos6Set = True
                elif msg[1:4] == "371":
                    camera3.pos7Set = True
                elif msg[1:4] == "381":
                    camera3.pos8Set = True
                elif msg[1:4] == "391":
                    camera3.pos9Set = True
                elif msg[1:4] == "301":
                    camera3.pos10Set = True
                elif msg[1:4] == "312":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos1Run = True
                elif msg[1:4] == "322":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos2Run = True
                elif msg[1:4] == "332":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos3Run = True
                elif msg[1:4] == "342":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos4Run = True
                elif msg[1:4] == "352":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos5Run = True
                elif msg[1:4] == "362":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos6Run = True
                elif msg[1:4] == "372":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos7Run = True
                elif msg[1:4] == "382":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos8Run = True
                elif msg[1:4] == "392":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos9Run = True
                elif msg[1:4] == "302":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                    camera3.pos10Run = True
                elif msg[1:4] == "313":
                    camera3.pos1Run = False
                    camera3.pos1At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "323":
                    camera3.pos2Run = False
                    camera3.pos2At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "333":
                    camera3.pos3Run = False
                    camera3.pos3At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "343":
                    camera3.pos4Run = False
                    camera3.pos4At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "353":
                    camera3.pos5Run = False
                    camera3.pos5At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "363":
                    camera3.pos6Run = False
                    camera3.pos6At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "373":
                    camera3.pos7Run = False
                    camera3.pos7At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "383":
                    camera3.pos8Run = False
                    camera3.pos8At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "393":
                    camera3.pos9Run = False
                    camera3.pos9At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "303":
                    camera3.pos10Run = False
                    camera3.pos10At = True
                    if camera3.running:
                        PTSapp.runCam3(self)
                elif msg[1:4] == "314":
                    pass
                elif msg[1:4] == "324":
                    pass
                elif msg[1:4] == "315":
                    camera3.useSetSpeed = True
                elif msg[1:4] == "305":
                    camera3.useSetSpeed = False
                elif msg[1:4] == "300":
                    camera3.pos1Run = False
                    camera3.pos1Set = False
                    camera3.pos1At = False
                    camera3.pos2Run = False
                    camera3.pos2Set = False
                    camera3.pos2At = False
                    camera3.pos3Run = False 
                    camera3.pos3Set = False
                    camera3.pos3At = False
                    camera3.pos4Run = False
                    camera3.pos4Set = False
                    camera3.pos4At = False
                    camera3.pos5Run = False
                    camera3.pos5Set = False
                    camera3.pos5At = False
                    camera3.pos6Run = False
                    camera3.pos6Set = False
                    camera3.pos6At = False
                    camera3.pos7Run = False
                    camera3.pos7Set = False
                    camera3.pos7At = False
                    camera3.pos8Run = False
                    camera3.pos8Set = False
                    camera3.pos8At = False
                    camera3.pos9Run = False
                    camera3.pos9Set = False
                    camera3.pos9At = False
                    camera3.pos10Run = False
                    camera3.pos10Set = False
                    camera3.pos10At = False
                elif msg[1:4] == "411":              # Cam 4 Set Pos 1
                    camera4.pos1Set = True
                elif msg[1:4] == "421":
                    camera4.pos2Set = True
                elif msg[1:4] == "431":
                    camera4.pos3Set = True
                elif msg[1:4] == "441":
                    camera4.pos4Set = True
                elif msg[1:4] == "451":
                    camera4.pos5Set = True
                elif msg[1:4] == "461":
                    camera4.pos6Set = True
                elif msg[1:4] == "471":
                    camera4.pos7Set = True
                elif msg[1:4] == "481":
                    camera4.pos8Set = True
                elif msg[1:4] == "491":
                    camera4.pos9Set = True
                elif msg[1:4] == "401":
                    camera4.pos10Set = True
                elif msg[1:4] == "412":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos1Run = True
                elif msg[1:4] == "422":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos2Run = True
                elif msg[1:4] == "432":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos3Run = True
                elif msg[1:4] == "442":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos4Run = True
                elif msg[1:4] == "452":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos5Run = True
                elif msg[1:4] == "462":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos6Run = True
                elif msg[1:4] == "472":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos7Run = True
                elif msg[1:4] == "482":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos8Run = True
                elif msg[1:4] == "492":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos9Run = True
                elif msg[1:4] == "402":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                    camera4.pos10Run = True
                elif msg[1:4] == "413":
                    camera4.pos1Run = False
                    camera4.pos1At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "423":
                    camera4.pos2Run = False
                    camera4.pos2At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "433":
                    camera4.pos3Run = False
                    camera4.pos3At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "443":
                    camera4.pos4Run = False
                    camera4.pos4At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "453":
                    camera4.pos5Run = False
                    camera4.pos5At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "463":
                    camera4.pos6Run = False
                    camera4.pos6At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "473":
                    camera4.pos7Run = False
                    camera4.pos7At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "483":
                    camera4.pos8Run = False
                    camera4.pos8At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "493":
                    camera4.pos9Run = False
                    camera4.pos9At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "403":
                    camera4.pos10Run = False
                    camera4.pos10At = True
                    if camera4.running:
                        PTSapp.runCam4(self)
                elif msg[1:4] == "414":
                    pass
                elif msg[1:4] == "424":
                    pass
                elif msg[1:4] == "415":
                    camera4.useSetSpeed = True
                elif msg[1:4] == "405":
                    camera4.useSetSpeed = False
                elif msg[1:4] == "400":
                    camera4.pos1Run = False
                    camera4.pos1Set = False
                    camera4.pos1At = False
                    camera4.pos2Run = False
                    camera4.pos2Set = False
                    camera4.pos2At = False
                    camera4.pos3Run = False 
                    camera4.pos3Set = False
                    camera4.pos3At = False
                    camera4.pos4Run = False
                    camera4.pos4Set = False
                    camera4.pos4At = False
                    camera4.pos5Run = False
                    camera4.pos5Set = False
                    camera4.pos5At = False
                    camera4.pos6Run = False
                    camera4.pos6Set = False
                    camera4.pos6At = False
                    camera4.pos7Run = False
                    camera4.pos7Set = False
                    camera4.pos7At = False
                    camera4.pos8Run = False
                    camera4.pos8Set = False
                    camera4.pos8At = False
                    camera4.pos9Run = False
                    camera4.pos9Set = False
                    camera4.pos9At = False
                    camera4.pos10Run = False
                    camera4.pos10Set = False
                    camera4.pos10At = False
                elif msg[1:4] == "511":              # Cam 5 Set Pos 1
                    camera5.pos1Set = True
                elif msg[1:4] == "521":
                    camera5.pos2Set = True
                elif msg[1:4] == "531":
                    camera5.pos3Set = True
                elif msg[1:4] == "541":
                    camera5.pos4Set = True
                elif msg[1:4] == "551":
                    camera5.pos5Set = True
                elif msg[1:4] == "561":
                    camera5.pos6Set = True
                elif msg[1:4] == "571":
                    camera5.pos7Set = True
                elif msg[1:4] == "581":
                    camera5.pos8Set = True
                elif msg[1:4] == "591":
                    camera5.pos9Set = True
                elif msg[1:4] == "501":
                    camera5.pos10Set = True
                elif msg[1:4] == "512":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos1Run = True
                elif msg[1:4] == "522":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos2Run = True
                elif msg[1:4] == "532":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos3Run = True
                elif msg[1:4] == "542":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos4Run = True
                elif msg[1:4] == "552":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos5Run = True
                elif msg[1:4] == "562":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos6Run = True
                elif msg[1:4] == "572":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos7Run = True
                elif msg[1:4] == "582":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos8Run = True
                elif msg[1:4] == "592":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos9Run = True
                elif msg[1:4] == "502":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
                    camera5.pos10Run = True
                elif msg[1:4] == "513":
                    camera5.pos1Run = False
                    camera5.pos1At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "523":
                    camera5.pos2Run = False
                    camera5.pos2At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "533":
                    camera5.pos3Run = False
                    camera5.pos3At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "543":
                    camera5.pos4Run = False
                    camera5.pos4At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "553":
                    camera5.pos5Run = False
                    camera5.pos5At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "563":
                    camera5.pos6Run = False
                    camera5.pos6At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "573":
                    camera5.pos7Run = False
                    camera5.pos7At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "583":
                    camera5.pos8Run = False
                    camera5.pos8At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "593":
                    camera5.pos9Run = False
                    camera5.pos9At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "503":
                    camera5.pos10Run = False
                    camera5.pos10At = True
                    if camera5.running:
                        PTSapp.runCam5(self)
                elif msg[1:4] == "514":
                    pass
                elif msg[1:4] == "524":
                    pass
                elif msg[1:4] == "515":
                    camera5.useSetSpeed = True
                elif msg[1:4] == "505":
                    camera5.useSetSpeed = False
                elif msg[1:4] == "500":
                    camera5.pos1Run = False
                    camera5.pos1Set = False
                    camera5.pos1At = False
                    camera5.pos2Run = False
                    camera5.pos2Set = False
                    camera5.pos2At = False
                    camera5.pos3Run = False 
                    camera5.pos3Set = False
                    camera5.pos3At = False
                    camera5.pos4Run = False
                    camera5.pos4Set = False
                    camera5.pos4At = False
                    camera5.pos5Run = False
                    camera5.pos5Set = False
                    camera5.pos5At = False
                    camera5.pos6Run = False
                    camera5.pos6Set = False
                    camera5.pos6At = False
                    camera5.pos7Run = False
                    camera5.pos7Set = False
                    camera5.pos7At = False
                    camera5.pos8Run = False
                    camera5.pos8Set = False
                    camera5.pos8At = False
                    camera5.pos9Run = False
                    camera5.pos9Set = False
                    camera5.pos9At = False
                    camera5.pos10Run = False
                    camera5.pos10Set = False
                    camera5.pos10At = False
                elif msg[1] == "?":
                    camera1.pos1At = False
                    camera1.pos2At = False
                    camera1.pos3At = False
                    camera1.pos4At = False
                    camera1.pos5At = False
                    camera1.pos6At = False
                    camera1.pos7At = False
                    camera1.pos8At = False
                    camera1.pos9At = False
                    camera1.pos10At = False
                elif msg[1] == "!":
                    camera2.pos1At = False
                    camera2.pos2At = False
                    camera2.pos3At = False
                    camera2.pos4At = False
                    camera2.pos5At = False
                    camera2.pos6At = False
                    camera2.pos7At = False
                    camera2.pos8At = False
                    camera2.pos9At = False
                    camera2.pos10At = False
                elif msg[1] == "@":
                    camera3.pos1At = False
                    camera3.pos2At = False
                    camera3.pos3At = False
                    camera3.pos4At = False
                    camera3.pos5At = False
                    camera3.pos6At = False
                    camera3.pos7At = False
                    camera3.pos8At = False
                    camera3.pos9At = False
                    camera3.pos10At = False
                elif msg[1] == "&":
                    camera4.pos1At = False
                    camera4.pos2At = False
                    camera4.pos3At = False
                    camera4.pos4At = False
                    camera4.pos5At = False
                    camera4.pos6At = False
                    camera4.pos7At = False
                    camera4.pos8At = False
                    camera4.pos9At = False
                    camera4.pos10At = False
                elif msg[1] == "*":
                    camera5.pos1At = False
                    camera5.pos2At = False
                    camera5.pos3At = False
                    camera5.pos4At = False
                    camera5.pos5At = False
                    camera5.pos6At = False
                    camera5.pos7At = False
                    camera5.pos8At = False
                    camera5.pos9At = False
                    camera5.pos10At = False
            
            elif msg[0:2] == "#+":                  # *********
                self.aliveCam1()
            elif msg[0:2] == "=1":
                camera1.sliderSpeed = int(msg[2])
            elif msg[0:2] == "=2":
                camera2.sliderSpeed = int(msg[2])
            elif msg[0:2] == "=3":
                camera3.sliderSpeed = int(msg[2])
            elif msg[0:2] == "=4":
                camera4.sliderSpeed = int(msg[2])
            elif msg[0:2] == "=5":
                camera5.sliderSpeed = int(msg[2])
            elif msg[0:3] == "=@1":
                camera1.panTiltSpeed = int(msg[3])
            elif msg[0:3] == "=@2":
                camera2.panTiltSpeed = int(msg[3])
            elif msg[0:3] == "=@3":
                camera3.panTiltSpeed = int(msg[3])
            elif msg[0:3] == "=@4":
                camera4.panTiltSpeed = int(msg[3])
            elif msg[0:3] == "=@5":
                camera5.panTiltSpeed = int(msg[3])

            elif msg[0:3] == "=a0":
                camera1.panTiltAccel = int(msg[3:])
            elif msg[0:3] == "=a1":
                camera1.panTiltSpeed1 = int(msg[3:])
            elif msg[0:3] == "=a2":
                camera1.panTiltSpeed2 = int(msg[3:])
            elif msg[0:3] == "=a3":
                camera1.panTiltSpeed3 = int(msg[3:])
            elif msg[0:3] == "=a4":
                camera1.panTiltSpeed4 = int(msg[3:])
            elif msg[0:3] == "=A0":
                camera1.sliderAccel = int(msg[3:])
            elif msg[0:3] == "=A1":
                camera1.sliderSpeed1 = int(msg[3:])
            elif msg[0:3] == "=A2":
                camera1.sliderSpeed2 = int(msg[3:])
            elif msg[0:3] == "=A3":
                camera1.sliderSpeed3 = int(msg[3:])
            elif msg[0:3] == "=A4":
                camera1.sliderSpeed4 = int(msg[3:])
            elif msg[0:3] == "=a5":
                camera1.slideLimit = int(msg[3:])
            elif msg[0:3] == "=A5":
                camera1.zoomLimit = int(msg[3:])

            elif msg[0:3] == "=s0":
                camera2.panTiltAccel = int(msg[3:])
            elif msg[0:3] == "=s1":
                camera2.panTiltSpeed1 = int(msg[3:])
            elif msg[0:3] == "=s2":
                camera2.panTiltSpeed2 = int(msg[3:])
            elif msg[0:3] == "=s3":
                camera2.panTiltSpeed3 = int(msg[3:])
            elif msg[0:3] == "=s4":
                camera2.panTiltSpeed4 = int(msg[3:])
            elif msg[0:3] == "=S0":
                camera2.sliderAccel = int(msg[3:])
            elif msg[0:3] == "=S1":
                camera2.sliderSpeed1 = int(msg[3:])
            elif msg[0:3] == "=S2":
                camera2.sliderSpeed2 = int(msg[3:])
            elif msg[0:3] == "=S3":
                camera2.sliderSpeed3 = int(msg[3:])
            elif msg[0:3] == "=S4":
                camera2.sliderSpeed4 = int(msg[3:])
            elif msg[0:3] == "=s5":
                camera2.slideLimit = int(msg[3:])
            elif msg[0:3] == "=S5":
                camera2.zoomLimit = int(msg[3:])

            elif msg[0:3] == "=d0":
                camera3.panTiltAccel = int(msg[3:])
            elif msg[0:3] == "=d1":
                camera3.panTiltSpeed1 = int(msg[3:])
            elif msg[0:3] == "=d2":
                camera3.panTiltSpeed2 = int(msg[3:])
            elif msg[0:3] == "=d3":
                camera3.panTiltSpeed3 = int(msg[3:])
            elif msg[0:3] == "=d4":
                camera3.panTiltSpeed4 = int(msg[3:])
            elif msg[0:3] == "=D0":
                camera3.sliderAccel = int(msg[3:])
            elif msg[0:3] == "=D1":
                camera3.sliderSpeed1 = int(msg[3:])
            elif msg[0:3] == "=D2":
                camera3.sliderSpeed2 = int(msg[3:])
            elif msg[0:3] == "=D3":
                camera3.sliderSpeed3 = int(msg[3:])
            elif msg[0:3] == "=D4":
                camera3.sliderSpeed4 = int(msg[3:])
            elif msg[0:3] == "=d5":
                camera3.slideLimit = int(msg[3:])
            elif msg[0:3] == "=D5":
                camera3.zoomLimit = int(msg[3:])

            elif msg[0:3] == "=f0":
                camera4.panTiltAccel = int(msg[3:])
            elif msg[0:3] == "=f1":
                camera4.panTiltSpeed1 = int(msg[3:])
            elif msg[0:3] == "=f2":
                camera4.panTiltSpeed2 = int(msg[3:])
            elif msg[0:3] == "=f3":
                camera4.panTiltSpeed3 = int(msg[3:])
            elif msg[0:3] == "=f4":
                camera4.panTiltSpeed4 = int(msg[3:])
            elif msg[0:3] == "=F0":
                camera4.sliderAccel = int(msg[3:])
            elif msg[0:3] == "=F1":
                camera4.sliderSpeed1 = int(msg[3:])
            elif msg[0:3] == "=F2":
                camera4.sliderSpeed2 = int(msg[3:])
            elif msg[0:3] == "=F3":
                camera4.sliderSpeed3 = int(msg[3:])
            elif msg[0:3] == "=F4":
                camera4.sliderSpeed4 = int(msg[3:])
            elif msg[0:3] == "=f5":
                camera4.slideLimit = int(msg[3:])
            elif msg[0:3] == "=F5":
                camera4.zoomLimit = int(msg[3:])

            elif msg[0:3] == "=g0":
                camera5.panTiltAccel = int(msg[3:])
            elif msg[0:3] == "=g1":
                camera5.panTiltSpeed1 = int(msg[3:])
            elif msg[0:3] == "=g2":
                camera5.panTiltSpeed2 = int(msg[3:])
            elif msg[0:3] == "=g3":
                camera5.panTiltSpeed3 = int(msg[3:])
            elif msg[0:3] == "=g4":
                camera5.panTiltSpeed4 = int(msg[3:])
            elif msg[0:3] == "=G0":
                camera5.sliderAccel = int(msg[3:])
            elif msg[0:3] == "=G1":
                camera5.sliderSpeed1 = int(msg[3:])
            elif msg[0:3] == "=G2":
                camera5.sliderSpeed2 = int(msg[3:])
            elif msg[0:3] == "=G3":
                camera5.sliderSpeed3 = int(msg[3:])
            elif msg[0:3] == "=G4":
                camera5.sliderSpeed4 = int(msg[3:])
            elif msg[0:3] == "=g5":
                camera5.slideLimit = int(msg[3:])
            elif msg[0:3] == "=G5":
                camera5.zoomLimit = int(msg[3:])

            elif msg[0:4] == "=-1+":
                self.aliveCam1()
            elif msg[0:4] == "=-2+":
                self.aliveCam2()
            elif msg[0:4] == "=-3+":
                self.aliveCam3()
            elif msg[0:4] == "=-4+":
                self.aliveCam4()
            elif msg[0:4] == "=-5+":
                self.aliveCam5()

            elif msg[0:4] == "=-1-":
                self.deadCam1()
            elif msg[0:4] == "=-2-":
                self.deadCam2()
            elif msg[0:4] == "=-3-":
                self.deadCam3()
            elif msg[0:4] == "=-4-":
                self.deadCam4()
            elif msg[0:4] == "=-5-":
                self.deadCam5()

            elif msg[0:2] == "#$":
                serialText += "</font><br>"
                #QtWidgets.QApplication.processEvents()
                QtCore.QTimer.singleShot(500,self.scrollText())

            elif msg[0:4] == "Cam1":
                whichCamRead = 1
                textLength = len(appSettings.serialText)
                if textLength > 8000:
                    appSettings.serialText = (appSettings.serialText[1000:textLength])
                appSettings.serialText += "<font color=#40D140 size='3'>Cam1:<br>"
            elif msg[0:4] == "Cam2":
                whichCamRead = 2
                textLength = len(appSettings.serialText)
                if textLength > 8000:
                    appSettings.serialText = (appSettings.serialText[1000:textLength])
                appSettings.serialText += "<font color=#5C8BC9 size='3'>Cam2:<br>"
            elif msg[0:4] == "Cam3":
                whichCamRead = 3
                textLength = len(appSettings.serialText)
                if textLength > 8000:
                    appSettings.serialText = (appSettings.serialText[1000:textLength])
                appSettings.serialText += "<font color=#B4A21C size='3'>Cam3:<br>"
            elif msg[0:4] == "Cam4":
                whichCamRead = 4
                textLength = len(appSettings.serialText)
                if textLength > 8000:
                    appSettings.serialText = (appSettings.serialText[1000:textLength])
                appSettings.serialText += "<font color=#01E6CC size='3'>Cam4:<br>"
            elif msg[0:4] == "Cam5":
                whichCamRead = 5
                textLength = len(appSettings.serialText)
                if textLength > 8000:
                    appSettings.serialText = (appSettings.serialText[1000:textLength])
                appSettings.serialText += "<font color=#E97CF9 size='3'>Cam5:<br>"
            else:
                appSettings.serialText += msg + "<br>"
                #QtWidgets.QApplication.processEvents()
                QtCore.QTimer.singleShot(500,self.scrollText)

                #QtCore.QTimer.singleShot(500,Ui_SettingsWindow.scrollText(Ui_SettingsWindow))

            msg = ''
            #QtWidgets.QApplication.processEvents()

            doButtonColours()
    def scrollText(self):

        Ui_SettingsWindow.serialTextWindow.setHtml(appSettings.serialText)
        QtWidgets.QApplication.processEvents()
        Ui_SettingsWindow.serialTextWindow.verticalScrollBar().setValue(Ui_SettingsWindow.serialTextWindow.verticalScrollBar().maximum())
        QtCore.QTimer.singleShot(0, Ui_SettingsWindow.serialTextWindow.show())

    def aliveCam1(self):
        PTSapp.groupBox11.hide()
    
    def aliveCam2(self):
        PTSapp.groupBox21.hide()
    
    def aliveCam3(self):
        PTSapp.groupBox31.hide()

    def aliveCam4(self):
        PTSapp.groupBox41.hide()
    
    def aliveCam5(self):
        PTSapp.groupBox51.hide()

    def deadCam1(self):
        camera1.pos1Set = False
        camera1.pos2Set = False
        camera1.pos3Set = False
        camera1.pos4Set = False
        camera1.pos5Set = False
        camera1.pos6Set = False
        camera1.pos7Set = False
        camera1.pos8Set = False
        camera1.pos9Set = False
        camera1.pos10Set = False
        camera1.pos1Run = False
        camera1.pos2Run = False
        camera1.pos3Run = False
        camera1.pos4Run = False
        camera1.pos5Run = False
        camera1.pos6Run = False
        camera1.pos7Run = False
        camera1.pos8Run = False
        camera1.pos9Run = False
        camera1.pos10Run = False
        camera1.pos1At = False
        camera1.pos2At = False
        camera1.pos3At = False
        camera1.pos4At = False
        camera1.pos5At = False
        camera1.pos6At = False
        camera1.pos7At = False
        camera1.pos8At = False
        camera1.pos9At = False
        camera1.pos10At = False

        camera1.panTiltSpeed = 0
        camera1.sliderSpeed = 0

        doButtonColours()

        PTSapp.setupUi.dial1p.setValue(1)
        PTSapp.setupUi.line1p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0)
        PTSapp.setupUi.dial1s.setValue(1)
        PTSapp.setupUi.line1s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)

        PTSapp.groupBox11.show()

    def deadCam2(self):
        camera2.pos1Set = False
        camera2.pos2Set = False
        camera2.pos3Set = False
        camera2.pos4Set = False
        camera2.pos5Set = False
        camera2.pos6Set = False
        camera2.pos7Set = False
        camera2.pos8Set = False
        camera2.pos9Set = False
        camera2.pos10Set = False
        camera2.pos1Run = False
        camera2.pos2Run = False
        camera2.pos3Run = False
        camera2.pos4Run = False
        camera2.pos5Run = False
        camera2.pos6Run = False
        camera2.pos7Run = False
        camera2.pos8Run = False
        camera2.pos9Run = False
        camera2.pos10Run = False
        camera2.pos1At = False
        camera2.pos2At = False
        camera2.pos3At = False
        camera2.pos4At = False
        camera2.pos5At = False
        camera2.pos6At = False
        camera2.pos7At = False
        camera2.pos8At = False
        camera2.pos9At = False
        camera2.pos10At = False

        camera2.panTiltSpeed = 0
        camera2.sliderSpeed = 0

        doButtonColours()

        PTSapp.setupUi.dial2p.setValue(1)
        PTSapp.setupUi.line2p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0)
        PTSapp.setupUi.dial2s.setValue(1)
        PTSapp.setupUi.line2s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)

        PTSapp.groupBox21.show()

    def deadCam3(self):
        camera3.pos1Set = False
        camera3.pos2Set = False
        camera3.pos3Set = False
        camera3.pos4Set = False
        camera3.pos5Set = False
        camera3.pos6Set = False
        camera3.pos7Set = False
        camera3.pos8Set = False
        camera3.pos9Set = False
        camera3.pos10Set = False
        camera3.pos1Run = False
        camera3.pos2Run = False
        camera3.pos3Run = False
        camera3.pos4Run = False
        camera3.pos5Run = False
        camera3.pos6Run = False
        camera3.pos7Run = False
        camera3.pos8Run = False
        camera3.pos9Run = False
        camera3.pos10Run = False
        camera3.pos1At = False
        camera3.pos2At = False
        camera3.pos3At = False
        camera3.pos4At = False
        camera3.pos5At = False
        camera3.pos6At = False
        camera3.pos7At = False
        camera3.pos8At = False
        camera3.pos9At = False
        camera3.pos10At = False

        camera3.panTiltSpeed = 0
        camera3.sliderSpeed = 0

        doButtonColours()

        PTSapp.setupUi.dial3p.setValue(1)
        PTSapp.setupUi.line3p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0)
        PTSapp.setupUi.dial3s.setValue(1)
        PTSapp.setupUi.line3s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)

        PTSapp.groupBox31.show()

    def deadCam4(self):
        camera4.pos1Set = False
        camera4.pos2Set = False
        camera4.pos3Set = False
        camera4.pos4Set = False
        camera4.pos5Set = False
        camera4.pos6Set = False
        camera4.pos7Set = False
        camera4.pos8Set = False
        camera4.pos9Set = False
        camera4.pos10Set = False
        camera4.pos1Run = False
        camera4.pos2Run = False
        camera4.pos3Run = False
        camera4.pos4Run = False
        camera4.pos5Run = False
        camera4.pos6Run = False
        camera4.pos7Run = False
        camera4.pos8Run = False
        camera4.pos9Run = False
        camera4.pos10Run = False
        camera4.pos1At = False
        camera4.pos2At = False
        camera4.pos3At = False
        camera4.pos4At = False
        camera4.pos5At = False
        camera4.pos6At = False
        camera4.pos7At = False
        camera4.pos8At = False
        camera4.pos9At = False
        camera4.pos10At = False

        camera4.panTiltSpeed = 0
        camera4.sliderSpeed = 0

        doButtonColours()

        PTSapp.setupUi.dial4p.setValue(1)
        PTSapp.setupUi.line4p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0)
        PTSapp.setupUi.dial4s.setValue(1)
        PTSapp.setupUi.line4s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)

        PTSapp.groupBox41.show()

    def deadCam5(self):
        camera5.pos1Set = False
        camera5.pos2Set = False
        camera5.pos3Set = False
        camera5.pos4Set = False
        camera5.pos5Set = False
        camera5.pos6Set = False
        camera5.pos7Set = False
        camera5.pos8Set = False
        camera5.pos9Set = False
        camera5.pos10Set = False
        camera5.pos1Run = False
        camera5.pos2Run = False
        camera5.pos3Run = False
        camera5.pos4Run = False
        camera5.pos5Run = False
        camera5.pos6Run = False
        camera5.pos7Run = False
        camera5.pos8Run = False
        camera5.pos9Run = False
        camera5.pos10Run = False
        camera5.pos1At = False
        camera5.pos2At = False
        camera5.pos3At = False
        camera5.pos4At = False
        camera5.pos5At = False
        camera5.pos6At = False
        camera5.pos7At = False
        camera5.pos8At = False
        camera5.pos9At = False
        camera5.pos10At = False

        camera5.panTiltSpeed = 0
        camera5.sliderSpeed = 0

        doButtonColours()

        PTSapp.setupUi.dial5p.setValue(1)
        PTSapp.setupUi.line5p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, 0)
        PTSapp.setupUi.dial5s.setValue(1)
        PTSapp.setupUi.line5s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, 0)

        PTSapp.groupBox51.show()

class resetButtons():
    resetButtons = False

class doButtonColours():
    def __new__(self):
        buttonColourSet = "#ff0000"
        buttonColourAt = "#00ff00"

        if camera1.pos1Set != camera1.pos1OldSet or camera1.pos1Run != camera1.pos1OldRun or camera1.pos1At != camera1.pos1OldAt or resetButtons.resetButtons:
            camera1.pos1OldSet = camera1.pos1Set
            camera1.pos1OldRun = camera1.pos1Run
            camera1.pos1OldAt = camera1.pos1At
            if camera1.slideToggle and camera1.hasSlider:
                if camera1.pos1Set and not camera1.pos1Run and not camera1.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #40D140; border-radius: {borderRadius}px;')
                elif camera1.pos1Set and not camera1.pos1Run and camera1.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #40D140; border-radius: {borderRadius}px;')
                elif not camera1.pos1Set:
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #40D140; border-radius: {borderRadius}px;')
            else:
                if camera1.pos1Set and not camera1.pos1Run and not camera1.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
                elif camera1.pos1Set and not camera1.pos1Run and camera1.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
                elif not camera1.pos1Set:
                    PTSapp.pushButton11.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos2Set != camera1.pos2OldSet or camera1.pos2Run != camera1.pos2OldRun or camera1.pos2At != camera1.pos2OldAt or resetButtons.resetButtons:
            camera1.pos2OldSet = camera1.pos2Set
            camera1.pos2OldRun = camera1.pos2Run
            camera1.pos2OldAt = camera1.pos2At
            if camera1.pos2Set and not camera1.pos2Run and not camera1.pos2At:                                  # Position LEDs Cam1
                PTSapp.pushButton12.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos2Set and not camera1.pos2Run and camera1.pos2At:
                PTSapp.pushButton12.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos2Set:
                PTSapp.pushButton12.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos3Set != camera1.pos3OldSet or camera1.pos3Run != camera1.pos3OldRun or camera1.pos3At != camera1.pos3OldAt or resetButtons.resetButtons:
            camera1.pos3OldSet = camera1.pos3Set
            camera1.pos3OldRun = camera1.pos3Run
            camera1.pos3OldAt = camera1.pos3At
            if camera1.pos3Set and not camera1.pos3Run and not camera1.pos3At:                                  # Position LEDs Cam1
                PTSapp.pushButton13.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos3Set and not camera1.pos3Run and camera1.pos3At:
                PTSapp.pushButton13.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos3Set:
                PTSapp.pushButton13.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos4Set != camera1.pos4OldSet or camera1.pos4Run != camera1.pos4OldRun or camera1.pos4At != camera1.pos4OldAt or resetButtons.resetButtons:
            camera1.pos4OldSet = camera1.pos4Set
            camera1.pos4OldRun = camera1.pos4Run
            camera1.pos4OldAt = camera1.pos4At
            if camera1.pos4Set and not camera1.pos4Run and not camera1.pos4At:                                  # Position LEDs Cam1
                PTSapp.pushButton14.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos4Set and not camera1.pos4Run and camera1.pos4At:
                PTSapp.pushButton14.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos4Set:
                PTSapp.pushButton14.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos5Set != camera1.pos5OldSet or camera1.pos5Run != camera1.pos5OldRun or camera1.pos5At != camera1.pos5OldAt or resetButtons.resetButtons:
            camera1.pos5OldSet = camera1.pos5Set
            camera1.pos5OldRun = camera1.pos5Run
            camera1.pos5OldAt = camera1.pos5At
            if camera1.pos5Set and not camera1.pos5Run and not camera1.pos5At:                                  # Position LEDs Cam1
                PTSapp.pushButton15.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos5Set and not camera1.pos5Run and camera1.pos5At:
                PTSapp.pushButton15.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos5Set:
                PTSapp.pushButton15.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos6Set != camera1.pos6OldSet or camera1.pos6Run != camera1.pos6OldRun or camera1.pos6At != camera1.pos6OldAt or resetButtons.resetButtons:
            camera1.pos6OldSet = camera1.pos6Set
            camera1.pos6OldRun = camera1.pos6Run
            camera1.pos6OldAt = camera1.pos6At
            if camera1.pos6Set and not camera1.pos6Run and not camera1.pos6At:                                  # Position LEDs Cam1
                PTSapp.pushButton16.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos6Set and not camera1.pos6Run and camera1.pos6At:
                PTSapp.pushButton16.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos6Set:
                PTSapp.pushButton16.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos7Set != camera1.pos7OldSet or camera1.pos7Run != camera1.pos7OldRun or camera1.pos7At != camera1.pos7OldAt or resetButtons.resetButtons:
            camera1.pos7OldSet = camera1.pos7Set
            camera1.pos7OldRun = camera1.pos7Run
            camera1.pos7OldAt = camera1.pos7At
            if camera1.pos7Set and not camera1.pos7Run and not camera1.pos7At:                                  # Position LEDs Cam1
                PTSapp.pushButton17.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos7Set and not camera1.pos7Run and camera1.pos7At:
                PTSapp.pushButton17.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos7Set:
                PTSapp.pushButton17.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')
                
        if camera1.pos8Set != camera1.pos8OldSet or camera1.pos8Run != camera1.pos8OldRun or camera1.pos8At != camera1.pos8OldAt or resetButtons.resetButtons:
            camera1.pos8OldSet = camera1.pos8Set
            camera1.pos8OldRun = camera1.pos8Run
            camera1.pos8OldAt = camera1.pos8At
            if camera1.pos8Set and not camera1.pos8Run and not camera1.pos8At:                                  # Position LEDs Cam1
                PTSapp.pushButton18.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos8Set and not camera1.pos8Run and camera1.pos8At:
                PTSapp.pushButton18.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos8Set:
                PTSapp.pushButton18.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos9Set != camera1.pos9OldSet or camera1.pos9Run != camera1.pos9OldRun or camera1.pos9At != camera1.pos9OldAt or resetButtons.resetButtons:
            camera1.pos9OldSet = camera1.pos9Set
            camera1.pos9OldRun = camera1.pos9Run
            camera1.pos9OldAt = camera1.pos9At
            if camera1.pos9Set and not camera1.pos9Run and not camera1.pos9At:                                  # Position LEDs Cam1
                PTSapp.pushButton19.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif camera1.pos9Set and not camera1.pos9Run and camera1.pos9At:
                PTSapp.pushButton19.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
            elif not camera1.pos9Set:
                PTSapp.pushButton19.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')

        if camera1.pos10Set != camera1.pos10OldSet or camera1.pos10Run != camera1.pos10OldRun or camera1.pos10At != camera1.pos10OldAt or resetButtons.resetButtons:
            camera1.pos10OldSet = camera1.pos10Set
            camera1.pos10OldRun = camera1.pos10Run
            camera1.pos10OldAt = camera1.pos10At
            if camera1.slideToggle and camera1.hasSlider:
                if camera1.pos10Set and not camera1.pos10Run and not camera1.pos10At:                                  # Position LEDs Cam1
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #40D140; border-radius: {borderRadius}px;')
                elif camera1.pos10Set and not camera1.pos10Run and camera1.pos10At:
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #40D140; border-radius: {borderRadius}px;')
                elif not camera1.pos10Set:
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #40D140; border-radius: {borderRadius}px;')
            else:
                if camera1.pos10Set and not camera1.pos10Run and not camera1.pos10At:                                  # Position LEDs Cam1
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
                elif camera1.pos10Set and not camera1.pos10Run and camera1.pos10At:
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #4C8A4C; border-radius: {borderRadius}px;')
                elif not camera1.pos10Set:
                    PTSapp.pushButton10.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #4C8A4C; border-radius: {borderRadius}px;')






        if camera2.pos1Set != camera2.pos1OldSet or camera2.pos1Run != camera2.pos1OldRun or camera2.pos1At != camera2.pos1OldAt or resetButtons.resetButtons:
            camera2.pos1OldSet = camera2.pos1Set
            camera2.pos1OldRun = camera2.pos1Run
            camera2.pos1OldAt = camera2.pos1At
            if camera2.slideToggle and camera2.hasSlider:
                if camera2.pos1Set and not camera2.pos1Run and not camera2.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
                elif camera2.pos1Set and not camera2.pos1Run and camera2.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
                elif not camera2.pos1Set:
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #5C8BC9; border-radius: {borderRadius}px;')
            else:
                if camera2.pos1Set and not camera2.pos1Run and not camera2.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
                elif camera2.pos1Set and not camera2.pos1Run and camera2.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
                elif not camera2.pos1Set:
                    PTSapp.pushButton21.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos2Set != camera2.pos2OldSet or camera2.pos2Run != camera2.pos2OldRun or camera2.pos2At != camera2.pos2OldAt or resetButtons.resetButtons:
            camera2.pos2OldSet = camera2.pos2Set
            camera2.pos2OldRun = camera2.pos2Run
            camera2.pos2OldAt = camera2.pos2At
            if camera2.pos2Set and not camera2.pos2Run and not camera2.pos1At:                                  # Position LEDs cam1
                PTSapp.pushButton22.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos2Set and not camera2.pos2Run and camera2.pos2At:
                PTSapp.pushButton22.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos2Set:
                PTSapp.pushButton22.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos3Set != camera2.pos3OldSet or camera2.pos3Run != camera2.pos3OldRun or camera2.pos3At != camera2.pos3OldAt or resetButtons.resetButtons:
            camera2.pos3OldSet = camera2.pos3Set
            camera2.pos3OldRun = camera2.pos3Run
            camera2.pos3OldAt = camera2.pos3At
            if camera2.pos3Set and not camera2.pos3Run and not camera2.pos3At:                                  # Position LEDs cam2
                PTSapp.pushButton23.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos3Set and not camera2.pos3Run and camera2.pos3At:
                PTSapp.pushButton23.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos3Set:
                PTSapp.pushButton23.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')
                
        if camera2.pos4Set != camera2.pos4OldSet or camera2.pos4Run != camera2.pos4OldRun or camera2.pos4At != camera2.pos4OldAt or resetButtons.resetButtons:
            camera2.pos4OldSet = camera2.pos4Set
            camera2.pos4OldRun = camera2.pos4Run
            camera2.pos4OldAt = camera2.pos4At
            if camera2.pos4Set and not camera2.pos4Run and not camera2.pos4At:                                  # Position LEDs cam2
                PTSapp.pushButton24.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos4Set and not camera2.pos4Run and camera2.pos4At:
                PTSapp.pushButton24.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos4Set:
                PTSapp.pushButton24.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos5Set != camera2.pos5OldSet or camera2.pos5Run != camera2.pos5OldRun or camera2.pos5At != camera2.pos5OldAt or resetButtons.resetButtons:
            camera2.pos5OldSet = camera2.pos5Set
            camera2.pos5OldRun = camera2.pos5Run
            camera2.pos5OldAt = camera2.pos5At
            if camera2.pos5Set and not camera2.pos5Run and not camera2.pos5At:                                  # Position LEDs cam2
                PTSapp.pushButton25.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos5Set and not camera2.pos5Run and camera2.pos5At:
                PTSapp.pushButton25.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos5Set:
                PTSapp.pushButton25.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos6Set != camera2.pos6OldSet or camera2.pos6Run != camera2.pos6OldRun or camera2.pos6At != camera2.pos6OldAt or resetButtons.resetButtons:
            camera2.pos6OldSet = camera2.pos6Set
            camera2.pos6OldRun = camera2.pos6Run
            camera2.pos6OldAt = camera2.pos6At
            if camera2.pos6Set and not camera2.pos6Run and not camera2.pos6At:                                  # Position LEDs cam2
                PTSapp.pushButton26.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos6Set and not camera2.pos6Run and camera2.pos6At:
                PTSapp.pushButton26.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos6Set:
                PTSapp.pushButton26.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos7Set != camera2.pos7OldSet or camera2.pos7Run != camera2.pos7OldRun or camera2.pos7At != camera2.pos7OldAt or resetButtons.resetButtons:
            camera2.pos7OldSet = camera2.pos7Set
            camera2.pos7OldRun = camera2.pos7Run
            camera2.pos7OldAt = camera2.pos7At
            if camera2.pos7Set and not camera2.pos7Run and not camera2.pos7At:                                  # Position LEDs cam2
                PTSapp.pushButton27.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos7Set and not camera2.pos7Run and camera2.pos7At:
                PTSapp.pushButton27.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos7Set:
                PTSapp.pushButton27.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos8Set != camera2.pos8OldSet or camera2.pos8Run != camera2.pos8OldRun or camera2.pos8At != camera2.pos8OldAt or resetButtons.resetButtons:
            camera2.pos8OldSet = camera2.pos8Set
            camera2.pos8OldRun = camera2.pos8Run
            camera2.pos8OldAt = camera2.pos8At
            if camera2.pos8Set and not camera2.pos8Run and not camera2.pos8At:                                  # Position LEDs cam2
                PTSapp.pushButton28.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos8Set and not camera2.pos8Run and camera2.pos8At:
                PTSapp.pushButton28.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos8Set:
                PTSapp.pushButton28.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos9Set != camera2.pos9OldSet or camera2.pos9Run != camera2.pos9OldRun or camera2.pos9At != camera2.pos9OldAt or resetButtons.resetButtons:
            camera2.pos9OldSet = camera2.pos9Set
            camera2.pos9OldRun = camera2.pos9Run
            camera2.pos9OldAt = camera2.pos9At
            if camera2.pos9Set and not camera2.pos9Run and not camera2.pos9At:                                  # Position LEDs cam2
                PTSapp.pushButton29.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif camera2.pos9Set and not camera2.pos9Run and camera2.pos9At:
                PTSapp.pushButton29.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
            elif not camera2.pos9Set:
                PTSapp.pushButton29.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')

        if camera2.pos10Set != camera2.pos10OldSet or camera2.pos10Run != camera2.pos10OldRun or camera2.pos10At != camera2.pos10OldAt or resetButtons.resetButtons:
            camera2.pos10OldSet = camera2.pos10Set
            camera2.pos10OldRun = camera2.pos10Run
            camera2.pos10OldAt = camera2.pos10At
            if camera2.slideToggle and camera2.hasSlider:
                if camera2.pos10Set and not camera2.pos10Run and not camera2.pos10At:                                  # Position LEDs cam2
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
                elif camera2.pos10Set and not camera2.pos10Run and camera2.pos10At:
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #5C8BC9; border-radius: {borderRadius}px;')
                elif not camera2.pos10Set:
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #5C8BC9; border-radius: {borderRadius}px;')
            else:
                if camera2.pos10Set and not camera2.pos10Run and not camera2.pos10At:                                  # Position LEDs cam2
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #405C80; border-radius: {borderRadius}px;')
                elif camera2.pos10Set and not camera2.pos10Run and camera2.pos10At:
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #405C80; border-radius: {borderRadius}px;')
                elif not camera2.pos10Set:
                    PTSapp.pushButton20.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #405C80; border-radius: {borderRadius}px;')


        if camera3.pos1Set != camera3.pos1OldSet or camera3.pos1Run != camera3.pos1OldRun or camera3.pos1At != camera3.pos1OldAt or resetButtons.resetButtons:
            camera3.pos1OldSet = camera3.pos1Set
            camera3.pos1OldRun = camera3.pos1Run
            camera3.pos1OldAt = camera3.pos1At
            if camera3.slideToggle and camera3.hasSlider:
                if camera3.pos1Set and not camera3.pos1Run and not camera3.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #B4A21C; border-radius: {borderRadius}px;')
                elif camera3.pos1Set and not camera3.pos1Run and camera3.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #B4A21C; border-radius: {borderRadius}px;')
                elif not camera3.pos1Set:
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #B4A21C; border-radius: {borderRadius}px;')
            else:
                if camera3.pos1Set and not camera3.pos1Run and not camera3.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
                elif camera3.pos1Set and not camera3.pos1Run and camera3.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
                elif not camera3.pos1Set:
                    PTSapp.pushButton31.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos2Set != camera3.pos2OldSet or camera3.pos2Run != camera3.pos2OldRun or camera3.pos2At != camera3.pos2OldAt or resetButtons.resetButtons:
            camera3.pos2OldSet = camera3.pos2Set
            camera3.pos2OldRun = camera3.pos2Run
            camera3.pos2OldAt = camera3.pos2At
            if camera3.pos2Set and not camera3.pos2Run and not camera3.pos2At:                                  # Position LEDs cam3
                PTSapp.pushButton32.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos2Set and not camera3.pos2Run and camera3.pos2At:
                PTSapp.pushButton32.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos2Set:
                PTSapp.pushButton32.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos3Set != camera3.pos3OldSet or camera3.pos3Run != camera3.pos3OldRun or camera3.pos3At != camera3.pos3OldAt or resetButtons.resetButtons:
            camera3.pos3OldSet = camera3.pos3Set
            camera3.pos3OldRun = camera3.pos3Run
            camera3.pos3OldAt = camera3.pos3At
            if camera3.pos3Set and not camera3.pos3Run and not camera3.pos3At:                                  # Position LEDs cam3
                PTSapp.pushButton33.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos3Set and not camera3.pos3Run and camera3.pos3At:
                PTSapp.pushButton33.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos3Set:
                PTSapp.pushButton33.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos4Set != camera3.pos4OldSet or camera3.pos4Run != camera3.pos4OldRun or camera3.pos4At != camera3.pos4OldAt or resetButtons.resetButtons:
            camera3.pos4OldSet = camera3.pos4Set
            camera3.pos4OldRun = camera3.pos4Run
            camera3.pos4OldAt = camera3.pos4At
            if camera3.pos4Set and not camera3.pos4Run and not camera3.pos4At:                                  # Position LEDs cam3
                PTSapp.pushButton34.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos4Set and not camera3.pos4Run and camera3.pos4At:
                PTSapp.pushButton34.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos4Set:
                PTSapp.pushButton34.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos5Set != camera3.pos5OldSet or camera3.pos5Run != camera3.pos5OldRun or camera3.pos5At != camera3.pos5OldAt or resetButtons.resetButtons:
            camera3.pos5OldSet = camera3.pos5Set
            camera3.pos5OldRun = camera3.pos5Run
            camera3.pos5OldAt = camera3.pos5At
            if camera3.pos5Set and not camera3.pos5Run and not camera3.pos5At:                                  # Position LEDs cam3
                PTSapp.pushButton35.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos5Set and not camera3.pos5Run and camera3.pos5At:
                PTSapp.pushButton35.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos5Set:
                PTSapp.pushButton35.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos6Set != camera3.pos6OldSet or camera3.pos6Run != camera3.pos6OldRun or camera3.pos6At != camera3.pos6OldAt or resetButtons.resetButtons:
            camera3.pos6OldSet = camera3.pos6Set
            camera3.pos6OldRun = camera3.pos6Run
            camera3.pos6OldAt = camera3.pos6At
            if camera3.pos6Set and not camera3.pos6Run and not camera3.pos6At:                                  # Position LEDs cam3
                PTSapp.pushButton36.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos6Set and not camera3.pos6Run and camera3.pos6At:
                PTSapp.pushButton36.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos6Set:
                PTSapp.pushButton36.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')
                
        if camera3.pos7Set != camera3.pos7OldSet or camera3.pos7Run != camera3.pos7OldRun or camera3.pos7At != camera3.pos7OldAt or resetButtons.resetButtons:
            camera3.pos7OldSet = camera3.pos7Set
            camera3.pos7OldRun = camera3.pos7Run
            camera3.pos7OldAt = camera3.pos7At
            if camera3.pos7Set and not camera3.pos7Run and not camera3.pos7At:                                  # Position LEDs cam3
                PTSapp.pushButton37.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos7Set and not camera3.pos7Run and camera3.pos7At:
                PTSapp.pushButton37.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos7Set:
                PTSapp.pushButton37.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos8Set != camera3.pos8OldSet or camera3.pos8Run != camera3.pos8OldRun or camera3.pos8At != camera3.pos8OldAt or resetButtons.resetButtons:
            camera3.pos8OldSet = camera3.pos8Set
            camera3.pos8OldRun = camera3.pos8Run
            camera3.pos8OldAt = camera3.pos8At
            if camera3.pos8Set and not camera3.pos8Run and not camera3.pos8At:                                  # Position LEDs cam3
                PTSapp.pushButton38.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos8Set and not camera3.pos8Run and camera3.pos8At:
                PTSapp.pushButton38.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos8Set:
                PTSapp.pushButton38.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos9Set != camera3.pos9OldSet or camera3.pos9Run != camera3.pos9OldRun or camera3.pos9At != camera3.pos9OldAt or resetButtons.resetButtons:
            camera3.pos9OldSet = camera3.pos9Set
            camera3.pos9OldRun = camera3.pos9Run
            camera3.pos9OldAt = camera3.pos9At
            if camera3.pos9Set and not camera3.pos9Run and not camera3.pos9At:                                  # Position LEDs cam3
                PTSapp.pushButton39.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
            elif camera3.pos9Set and not camera3.pos9Run and camera3.pos9At:
                PTSapp.pushButton39.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
            elif not camera3.pos9Set:
                PTSapp.pushButton39.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')

        if camera3.pos10Set != camera3.pos10OldSet or camera3.pos10Run != camera3.pos10OldRun or camera3.pos10At != camera3.pos10OldAt or resetButtons.resetButtons:
            camera3.pos10OldSet = camera3.pos10Set
            camera3.pos10OldRun = camera3.pos10Run
            camera3.pos10OldAt = camera3.pos10At
            if camera3.slideToggle and camera3.hasSlider:
                if camera3.pos10Set and not camera3.pos10Run and not camera3.pos10At:                                  # Position LEDs cam3
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #B4A21C; border-radius: {borderRadius}px;')
                elif camera3.pos10Set and not camera3.pos10Run and camera3.pos10At:
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #B4A21C; border-radius: {borderRadius}px;')
                elif not camera3.pos10Set:
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #B4A21C; border-radius: {borderRadius}px;')
            else:
                if camera3.pos10Set and not camera3.pos10Run and not camera3.pos10At:                                  # Position LEDs cam3
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #807100; border-radius: {borderRadius}px;')
                elif camera3.pos10Set and not camera3.pos10Run and camera3.pos10At:
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #807100; border-radius: {borderRadius}px;')
                elif not camera3.pos10Set:
                    PTSapp.pushButton30.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #807100; border-radius: {borderRadius}px;')




        if camera4.pos1Set != camera4.pos1OldSet or camera4.pos1Run != camera4.pos1OldRun or camera4.pos1At != camera4.pos1OldAt or resetButtons.resetButtons:
            camera4.pos1OldSet = camera4.pos1Set
            camera4.pos1OldRun = camera4.pos1Run
            camera4.pos1OldAt = camera4.pos1At
            if camera4.slideToggle and camera4.hasSlider:
                if camera4.pos1Set and not camera4.pos1Run and not camera4.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #01E6CC; border-radius: {borderRadius}px;')
                elif camera4.pos1Set and not camera4.pos1Run and camera4.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #01E6CC; border-radius: {borderRadius}px;')
                elif not camera4.pos1Set:
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #01E6CC; border-radius: {borderRadius}px;')
            else:
                if camera4.pos1Set and not camera4.pos1Run and not camera4.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
                elif camera4.pos1Set and not camera4.pos1Run and camera4.pos1At:                                    # Set & At, not Run
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
                elif not camera4.pos1Set:
                    PTSapp.pushButton41.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos2Set != camera4.pos2OldSet or camera4.pos2Run != camera4.pos2OldRun or camera4.pos2At != camera4.pos2OldAt or resetButtons.resetButtons:
            camera4.pos2OldSet = camera4.pos2Set
            camera4.pos2OldRun = camera4.pos2Run
            camera4.pos2OldAt = camera4.pos2At
            if camera4.pos2Set and not camera4.pos2Run and not camera4.pos2At:                                  # Position LEDs cam4
                PTSapp.pushButton42.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos2Set and not camera4.pos2Run and camera4.pos2At:
                PTSapp.pushButton42.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos2Set:
                PTSapp.pushButton42.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos3Set != camera4.pos3OldSet or camera4.pos3Run != camera4.pos3OldRun or camera4.pos3At != camera4.pos3OldAt or resetButtons.resetButtons:
            camera4.pos3OldSet = camera4.pos3Set
            camera4.pos3OldRun = camera4.pos3Run
            camera4.pos3OldAt = camera4.pos3At
            if camera4.pos3Set and not camera4.pos3Run and not camera4.pos3At:                                  # Position LEDs cam4
                PTSapp.pushButton43.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos3Set and not camera4.pos3Run and camera4.pos3At:
                PTSapp.pushButton43.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos3Set:
                PTSapp.pushButton43.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos4Set != camera4.pos4OldSet or camera4.pos4Run != camera4.pos4OldRun or camera4.pos4At != camera4.pos4OldAt or resetButtons.resetButtons:
            camera4.pos4OldSet = camera4.pos4Set
            camera4.pos4OldRun = camera4.pos4Run
            camera4.pos4OldAt = camera4.pos4At
            if camera4.pos4Set and not camera4.pos4Run and not camera4.pos4At:                                  # Position LEDs cam4
                PTSapp.pushButton44.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos4Set and not camera4.pos4Run and camera4.pos4At:
                PTSapp.pushButton44.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos4Set:
                PTSapp.pushButton44.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos5Set != camera4.pos5OldSet or camera4.pos5Run != camera4.pos5OldRun or camera4.pos5At != camera4.pos5OldAt or resetButtons.resetButtons:
            camera4.pos5OldSet = camera4.pos5Set
            camera4.pos5OldRun = camera4.pos5Run
            camera4.pos5OldAt = camera4.pos5At
            if camera4.pos5Set and not camera4.pos5Run and not camera4.pos5At:                                  # Position LEDs cam4
                PTSapp.pushButton45.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos5Set and not camera4.pos5Run and camera4.pos5At:
                PTSapp.pushButton45.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos5Set:
                PTSapp.pushButton45.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos6Set != camera4.pos6OldSet or camera4.pos6Run != camera4.pos6OldRun or camera4.pos6At != camera4.pos6OldAt or resetButtons.resetButtons:
            camera4.pos6OldSet = camera4.pos6Set
            camera4.pos6OldRun = camera4.pos6Run
            camera4.pos6OldAt = camera4.pos6At
            if camera4.pos6Set and not camera4.pos6Run and not camera4.pos6At:                                  # Position LEDs cam4
                PTSapp.pushButton46.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos6Set and not camera4.pos6Run and camera4.pos6At:
                PTSapp.pushButton46.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos6Set:
                PTSapp.pushButton46.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos7Set != camera4.pos7OldSet or camera4.pos7Run != camera4.pos7OldRun or camera4.pos7At != camera4.pos7OldAt or resetButtons.resetButtons:
            camera4.pos7OldSet = camera4.pos7Set
            camera4.pos7OldRun = camera4.pos7Run
            camera4.pos7OldAt = camera4.pos7At
            if camera4.pos7Set and not camera4.pos7Run and not camera4.pos7At:                                  # Position LEDs cam4
                PTSapp.pushButton47.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos7Set and not camera4.pos7Run and camera4.pos7At:
                PTSapp.pushButton47.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos7Set:
                PTSapp.pushButton47.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos8Set != camera4.pos8OldSet or camera4.pos8Run != camera4.pos8OldRun or camera4.pos8At != camera4.pos8OldAt or resetButtons.resetButtons:
            camera4.pos8OldSet = camera4.pos8Set
            camera4.pos8OldRun = camera4.pos8Run
            camera4.pos8OldAt = camera4.pos8At
            if camera4.pos8Set and not camera4.pos8Run and not camera4.pos8At:                                  # Position LEDs cam4
                PTSapp.pushButton48.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos8Set and not camera4.pos8Run and camera4.pos8At:
                PTSapp.pushButton48.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos8Set:
                PTSapp.pushButton48.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos9Set != camera4.pos9OldSet or camera4.pos9Run != camera4.pos9OldRun or camera4.pos9At != camera4.pos9OldAt or resetButtons.resetButtons:
            camera4.pos9OldSet = camera4.pos9Set
            camera4.pos9OldRun = camera4.pos9Run
            camera4.pos9OldAt = camera4.pos9At
            if camera4.pos9Set and not camera4.pos9Run and not camera4.pos9At:                                  # Position LEDs cam4
                PTSapp.pushButton49.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
            elif camera4.pos9Set and not camera4.pos9Run and camera4.pos9At:
                PTSapp.pushButton49.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
            elif not camera4.pos9Set:
                PTSapp.pushButton49.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')

        if camera4.pos10Set != camera4.pos10OldSet or camera4.pos10Run != camera4.pos10OldRun or camera4.pos10At != camera4.pos10OldAt or resetButtons.resetButtons:
            camera4.pos10OldSet = camera4.pos10Set
            camera4.pos10OldRun = camera4.pos10Run
            camera4.pos10OldAt = camera4.pos10At
            if camera4.slideToggle and camera4.hasSlider:
                if camera4.pos10Set and not camera4.pos10Run and not camera4.pos10At:                                  # Position LEDs cam4
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #01E6CC; border-radius: {borderRadius}px;')
                elif camera4.pos10Set and not camera4.pos10Run and camera4.pos10At:
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #01E6CC; border-radius: {borderRadius}px;')
                elif not camera4.pos10Set:
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #01E6CC; border-radius: {borderRadius}px;')
            else:

                if camera4.pos10Set and not camera4.pos10Run and not camera4.pos10At:
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #008071; border-radius: {borderRadius}px;')
                elif camera4.pos10Set and not camera4.pos10Run and camera4.pos10At:
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #008071; border-radius: {borderRadius}px;')
                elif not camera4.pos10Set:
                    PTSapp.pushButton40.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #008071; border-radius: {borderRadius}px;')




        if camera5.pos1Set != camera5.pos1OldSet or camera5.pos1Run != camera5.pos1OldRun or camera5.pos1At != camera5.pos1OldAt or resetButtons.resetButtons:
            camera5.pos1OldSet = camera5.pos1Set
            camera5.pos1OldRun = camera5.pos1Run
            camera5.pos1OldAt = camera5.pos1At
            if camera5.slideToggle and camera5.hasSlider:
                if camera5.pos1Set and not camera5.pos1Run and not camera5.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #E97CF9; border-radius: {borderRadius}px;')
                elif camera5.pos1Set and not camera5.pos1Run and camera5.pos1At:
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #E97CF9; border-radius: {borderRadius}px;')
                elif not camera5.pos1Set:
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #E97CF9; border-radius: {borderRadius}px;')
            else:
                if camera5.pos1Set and not camera5.pos1Run and not camera5.pos1At:                                  # Set , not Run or At
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
                elif camera5.pos1Set and not camera5.pos1Run and camera5.pos1At:
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
                elif not camera5.pos1Set:
                    PTSapp.pushButton51.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos2Set != camera5.pos2OldSet or camera5.pos2Run != camera5.pos2OldRun or camera5.pos2At != camera5.pos2OldAt or resetButtons.resetButtons:
            camera5.pos2OldSet = camera5.pos2Set
            camera5.pos2OldRun = camera5.pos2Run
            camera5.pos2OldAt = camera5.pos2At
            if camera5.pos2Set and not camera5.pos2Run and not camera5.pos2At:                                  # Position LEDs cam5
                PTSapp.pushButton52.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos2Set and not camera5.pos2Run and camera5.pos2At:
                PTSapp.pushButton52.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos2Set:
                PTSapp.pushButton52.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos3Set != camera5.pos3OldSet or camera5.pos3Run != camera5.pos3OldRun or camera5.pos3At != camera5.pos3OldAt or resetButtons.resetButtons:
            camera5.pos3OldSet = camera5.pos3Set
            camera5.pos3OldRun = camera5.pos3Run
            camera5.pos3OldAt = camera5.pos3At
            if camera5.pos3Set and not camera5.pos3Run and not camera5.pos3At:                                  # Position LEDs cam5
                PTSapp.pushButton53.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos3Set and not camera5.pos3Run and camera5.pos3At:
                PTSapp.pushButton53.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos3Set:
                PTSapp.pushButton53.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos4Set != camera5.pos4OldSet or camera5.pos4Run != camera5.pos4OldRun or camera5.pos4At != camera5.pos4OldAt or resetButtons.resetButtons:
            camera5.pos4OldSet = camera5.pos4Set
            camera5.pos4OldRun = camera5.pos4Run
            camera5.pos4OldAt = camera5.pos4At
            if camera5.pos4Set and not camera5.pos4Run and not camera5.pos4At:                                  # Position LEDs cam5
                PTSapp.pushButton54.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos4Set and not camera5.pos4Run and camera5.pos4At:
                PTSapp.pushButton54.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos4Set:
                PTSapp.pushButton54.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos5Set != camera5.pos5OldSet or camera5.pos5Run != camera5.pos5OldRun or camera5.pos5At != camera5.pos5OldAt or resetButtons.resetButtons:
            camera5.pos5OldSet = camera5.pos5Set
            camera5.pos5OldRun = camera5.pos5Run
            camera5.pos5OldAt = camera5.pos5At
            if camera5.pos5Set and not camera5.pos5Run and not camera5.pos5At:                                  # Position LEDs cam5
                PTSapp.pushButton55.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos5Set and not camera5.pos5Run and camera5.pos5At:
                PTSapp.pushButton6.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D7397; border-radius: {borderRadius}px;')
            elif not camera5.pos5Set:
                PTSapp.pushButton55.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos6Set != camera5.pos6OldSet or camera5.pos6Run != camera5.pos6OldRun or camera5.pos6At != camera5.pos6OldAt or resetButtons.resetButtons:
            camera5.pos6OldSet = camera5.pos6Set
            camera5.pos6OldRun = camera5.pos6Run
            camera5.pos6OldAt = camera5.pos6At
            if camera5.pos6Set and not camera5.pos6Run and not camera5.pos6At:                                  # Position LEDs cam5
                PTSapp.pushButton56.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos6Set and not camera5.pos6Run and camera5.pos6At:
                PTSapp.pushButton56.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos6Set:
                PTSapp.pushButton56.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos7Set != camera5.pos7OldSet or camera5.pos7Run != camera5.pos7OldRun or camera5.pos7At != camera5.pos7OldAt or resetButtons.resetButtons:
            camera5.pos7OldSet = camera5.pos7Set
            camera5.pos7OldRun = camera5.pos7Run
            camera5.pos7OldAt = camera5.pos7At
            if camera5.pos7Set and not camera5.pos7Run and not camera5.pos7At:                                  # Position LEDs cam5
                PTSapp.pushButton57.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos7Set and not camera5.pos7Run and camera5.pos7At:
                PTSapp.pushButton57.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos7Set:
                PTSapp.pushButton57.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos8Set != camera5.pos8OldSet or camera5.pos8Run != camera5.pos8OldRun or camera5.pos8At != camera5.pos8OldAt or resetButtons.resetButtons:
            camera5.pos8OldSet = camera5.pos8Set
            camera5.pos8OldRun = camera5.pos8Run
            camera5.pos8OldAt = camera5.pos8At
            if camera5.pos8Set and not camera5.pos8Run and not camera5.pos8At:                                  # Position LEDs cam5
                PTSapp.pushButton58.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos8Set and not camera5.pos8Run and camera5.pos8At:
                PTSapp.pushButton58.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos8Set:
                PTSapp.pushButton58.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos9Set != camera5.pos9OldSet or camera5.pos9Run != camera5.pos9OldRun or camera5.pos9At != camera5.pos9OldAt or resetButtons.resetButtons:
            camera5.pos9OldSet = camera5.pos9Set
            camera5.pos9OldRun = camera5.pos9Run
            camera5.pos9OldAt = camera5.pos9At
            if camera5.pos9Set and not camera5.pos9Run and not camera5.pos9At:                                  # Position LEDs cam5
                PTSapp.pushButton59.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif camera5.pos9Set and not camera5.pos9Run and camera5.pos9At:
                PTSapp.pushButton59.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
            elif not camera5.pos9Set:
                PTSapp.pushButton59.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')

        if camera5.pos10Set != camera5.pos10OldSet or camera5.pos10Run != camera5.pos10OldRun or camera5.pos10At != camera5.pos10OldAt or resetButtons.resetButtons:
            camera5.pos10OldSet = camera5.pos10Set
            camera5.pos10OldRun = camera5.pos10Run
            camera5.pos10OldAt = camera5.pos10At
            if camera5.slideToggle and camera5.hasSlider:
                if camera5.pos10Set and not camera5.pos10Run and not camera5.pos10At:                                  # Position LEDs cam5
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #E97CF9; border-radius: {borderRadius}px;')
                elif camera5.pos10Set and not camera5.pos10Run and camera5.pos10At:
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #E97CF9; border-radius: {borderRadius}px;')
                elif not camera5.pos10Set:
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #E97CF9; border-radius: {borderRadius}px;')
            else:
                if camera5.pos10Set and not camera5.pos10Run and not camera5.pos10At:
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourSet}; background-color: #8D5395; border-radius: {borderRadius}px;')
                elif camera5.pos10Set and not camera5.pos10Run and camera5.pos10At:
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid {buttonColourAt}; background-color: #8D5395; border-radius: {borderRadius}px;')
                elif not camera5.pos10Set:
                    PTSapp.pushButton50.setStyleSheet(f'border: {borderSize}px solid grey; background-color: #8D5395; border-radius: {borderRadius}px;')





        
        if camera1.panTiltSpeedOld != camera1.panTiltSpeed:
            camera1.panTiltSpeedOld = camera1.panTiltSpeed
            if camera1.panTiltSpeed == 1:
                PTSapp.dial1p.setValue(1)
                PTSapp.line1p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8) # 1470, 10, 20, 141           1470, 45, 20, 106           1470, 80, 20, 71           1470, 115, 20, 36
            elif camera1.panTiltSpeed == 3:
                PTSapp.dial1p.setValue(2)
                PTSapp.line1p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
            elif camera1.panTiltSpeed == 5:
                PTSapp.dial1p.setValue(3)
                PTSapp.line1p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
            elif camera1.panTiltSpeed == 7:
                PTSapp.dial1p.setValue(4)
                PTSapp.line1p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)

        if camera2.panTiltSpeedOld != camera2.panTiltSpeed:
            camera2.panTiltSpeedOld = camera2.panTiltSpeed
            if camera2.panTiltSpeed == 1:
                PTSapp.dial2p.setValue(1)
                PTSapp.line2p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
            elif camera2.panTiltSpeed == 3:
                PTSapp.dial2p.setValue(2)
                PTSapp.line2p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
            elif camera2.panTiltSpeed == 5:
                PTSapp.dial2p.setValue(3)
                PTSapp.line2p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
            elif camera2.panTiltSpeed == 7:
                PTSapp.dial2p.setValue(4)
                PTSapp.line2p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)

        if camera3.panTiltSpeedOld != camera3.panTiltSpeed:
            camera3.panTiltSpeedOld = camera3.panTiltSpeed
            if camera3.panTiltSpeed == 1:
                PTSapp.dial3p.setValue(1)
                PTSapp.line3p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
            elif camera3.panTiltSpeed == 3:
                PTSapp.dial3p.setValue(2)
                PTSapp.line3p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
            elif camera3.panTiltSpeed == 5:
                PTSapp.dial3p.setValue(3)
                PTSapp.line3p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
            elif camera3.panTiltSpeed == 7:
                PTSapp.dial3p.setValue(4)
                PTSapp.line3p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)

        if camera4.panTiltSpeedOld != camera4.panTiltSpeed:
            camera4.panTiltSpeedOld = camera4.panTiltSpeed
            if camera4.panTiltSpeed == 1:
                PTSapp.dial4p.setValue(1)
                PTSapp.line4p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
            elif camera4.panTiltSpeed == 3:
                PTSapp.dial4p.setValue(2)
                PTSapp.line4p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
            elif camera4.panTiltSpeed == 5:
                PTSapp.dial4p.setValue(3)
                PTSapp.line4p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
            elif camera4.panTiltSpeed == 7:
                PTSapp.dial4p.setValue(4)
                PTSapp.line4p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)

        if camera5.panTiltSpeedOld != camera5.panTiltSpeed:
            camera5.panTiltSpeedOld = camera5.panTiltSpeed
            if camera5.panTiltSpeed == 1:
                PTSapp.dial5p.setValue(1)
                PTSapp.line5p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
            elif camera5.panTiltSpeed == 3:
                PTSapp.dial5p.setValue(2)
                PTSapp.line5p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
            elif camera5.panTiltSpeed == 5:
                PTSapp.dial5p.setValue(3)
                PTSapp.line5p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
            elif camera5.panTiltSpeed == 7:
                PTSapp.dial5p.setValue(4)
                PTSapp.line5p.setGeometry(butttonLayoutX * 73.5, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)

        if camera1.sliderSpeedOld != camera1.sliderSpeed:
            camera1.sliderSpeedOld = camera1.sliderSpeed
            if camera1.sliderSpeed == 1:
                PTSapp.dial1s.setValue(1)
                PTSapp.line1s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
                camera1.hasSlider = True
            elif camera1.sliderSpeed == 3:
                PTSapp.dial1s.setValue(2)
                PTSapp.line1s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
                camera1.hasSlider = True
            elif camera1.sliderSpeed == 5:
                PTSapp.dial1s.setValue(3)
                PTSapp.line1s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
                camera1.hasSlider = True
            elif camera1.sliderSpeed >= 7:
                PTSapp.dial1s.setValue(4)
                PTSapp.line1s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)
                camera1.hasSlider = True

        if camera2.sliderSpeedOld != camera2.sliderSpeed:
            camera2.sliderSpeedOld = camera2.sliderSpeed
            if camera2.sliderSpeed == 1:
                PTSapp.dial2s.setValue(1)
                PTSapp.line2s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
                camera2.hasSlider = True
            elif camera2.sliderSpeed == 3:
                PTSapp.dial2s.setValue(2)
                PTSapp.line2s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
                camera2.hasSlider = True
            elif camera2.sliderSpeed == 5:
                PTSapp.dial2s.setValue(3)
                PTSapp.line2s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
                camera2.hasSlider = True
            elif camera2.sliderSpeed >= 7:
                PTSapp.dial2s.setValue(4)
                PTSapp.line2s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)
                camera2.hasSlider = True

        if camera3.sliderSpeedOld != camera3.sliderSpeed:
            camera3.sliderSpeedOld = camera3.sliderSpeed
            if camera3.sliderSpeed == 1:
                PTSapp.dial3s.setValue(1)
                PTSapp.line3s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
                camera3.hasSlider = True
            elif camera3.sliderSpeed == 3:
                PTSapp.dial3s.setValue(2)
                PTSapp.line3s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
                camera3.hasSlider = True
            elif camera3.sliderSpeed == 5:
                PTSapp.dial3s.setValue(3)
                PTSapp.line3s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
                camera3.hasSlider = True
            elif camera3.sliderSpeed >= 7:
                PTSapp.dial3s.setValue(4)
                PTSapp.line3s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)
                camera3.hasSlider = True

        if camera4.sliderSpeedOld != camera4.sliderSpeed:
            camera4.sliderSpeedOld = camera4.sliderSpeed
            if camera4.sliderSpeed == 1:
                PTSapp.dial4s.setValue(1)
                PTSapp.line4s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
                camera4.hasSlider = True
            elif camera4.sliderSpeed == 3:
                PTSapp.dial4s.setValue(2)
                PTSapp.line4s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
                camera4.hasSlider = True
            elif camera4.sliderSpeed == 5:
                PTSapp.dial4s.setValue(3)
                PTSapp.line4s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
                camera4.hasSlider = True
            elif camera4.sliderSpeed >= 7:
                PTSapp.dial4s.setValue(4)
                PTSapp.line4s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)
                camera4.hasSlider = True

        if camera5.sliderSpeedOld != camera5.sliderSpeed:
            camera5.sliderSpeedOld = camera5.sliderSpeed
            if camera5.sliderSpeed == 1:
                PTSapp.dial5s.setValue(1)
                PTSapp.line5s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 5.75, butttonLayoutX, butttonLayoutY * 1.8)
                camera5.hasSlider = True
            elif camera5.sliderSpeed == 3:
                PTSapp.dial5s.setValue(2)
                PTSapp.line5s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 4, butttonLayoutX, butttonLayoutY * 3.55)
                camera5.hasSlider = True
            elif camera5.sliderSpeed == 5:
                PTSapp.dial5s.setValue(3)
                PTSapp.line5s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 2.25, butttonLayoutX, butttonLayoutY * 5.3)
                camera5.hasSlider = True
            elif camera5.sliderSpeed >= 7:
                PTSapp.dial5s.setValue(4)
                PTSapp.line5s.setGeometry(butttonLayoutX * 91, butttonLayoutY * 0.5, butttonLayoutX, butttonLayoutY * 7.05)
                camera5.hasSlider = True


            resetButtons.resetButtons = False

class appSettings():
    setState = 0
    setPosToggle = False
    editToggle = False
    editButton = 0
    serialText = ""
    whichCamSerial = 1
    runToggle = False
    flashTick = False
    editNumber = 0
    debug = False
    message = ""
    running = False

    previousTime = 0
    previousMillisMoveCheck = 0
    currentMillisMoveCheck = 0
    moveCheckInterval = 0.8

    axisX = 0
    axisY = 0
    axisZ = 0
    axisW = 0
    axisXh = 0
    axisYh = 0
    axisZh = 0
    axisWh = 0
    oldAxisX = 0
    oldAxisY = 0
    oldAxisZ = 0
    oldAxisW = 0

    data = bytearray(10)
    joyData = bytearray(10)

    serialPort = None


class setPos():
    def run(self):
        if (appSettings.setPosToggle == True and appSettings.setState == 3) or appSettings.setState == 0:
            appSettings.setPosToggle = False
            appSettings.editToggle = False
            PTSapp.pushButtonSet.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #bbbbbb; border-radius: {borderRadius2}px;")
            PTSapp.pushButtonCam1.setText(camera1.name)
            PTSapp.pushButtonCam2.setText(camera2.name)
            PTSapp.pushButtonCam3.setText(camera3.name)
            PTSapp.pushButtonCam4.setText(camera4.name)
            PTSapp.pushButtonCam5.setText(camera5.name)
            PTSapp.pushButtonEdit.setText("Edit")
            PTSapp.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid grey; background-color: #405C80; border-radius: {borderRadius2}px;")
            PTSapp.pushButtonExit.hide()
            PTSapp.pushButtonLED.hide()
            PTSapp.pushButtonFileLoad.hide()
            PTSapp.pushButtonFileSave.hide()
            PTSapp.pushButtonSettings.hide()
            PTSapp.pushButtonRun.show()
            PTSapp.pushButtonSLonly.show()
            PTSapp.labelFilename.setHidden(True)
        elif (appSettings.setPosToggle == False and appSettings.setState == 3) or appSettings.setState == 1:
            appSettings.setPosToggle = True
            appSettings.editToggle = False
            PTSapp.pushButtonSet.setStyleSheet(f"border: {borderSize2}px solid #ff0000; background-color: #CC5050; border-radius: {borderRadius2}px;")
            PTSapp.pushButtonCam1.setText("Clear")
            PTSapp.pushButtonCam2.setText("Clear")
            PTSapp.pushButtonCam3.setText("Clear")
            PTSapp.pushButtonCam4.setText("Clear")
            PTSapp.pushButtonCam5.setText("Clear")
            PTSapp.pushButtonEdit.setText("Move")
            PTSapp.pushButtonEdit.setStyleSheet(f"border: {borderSize2}px solid #FFFC67; background-color: #F7BA00; border-radius: {borderRadius2}px;")
            self.pushButtonExit.show()
            PTSapp.pushButtonLED.show()
            PTSapp.pushButtonFileLoad.show()
            PTSapp.pushButtonFileSave.show()
            PTSapp.pushButtonSettings.show()
            PTSapp.pushButtonRun.hide()
            PTSapp.pushButtonSLonly.hide()
            PTSapp.labelFilename.setHidden(False)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.quit)
    MainWindow = PTSapp("")
    sys.exit(app.exec())