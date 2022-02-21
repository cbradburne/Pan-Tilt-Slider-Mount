#macOS
#Kivy
#python3 -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
#
#KivyMD
#git clone https://github.com/kivymd/KivyMD.git --depth 1
#cd KivyMD
#pip install .
#
#Other
#python3 -m pip install pygame==2.0.1
#python3 -m pip install usbserial4a
#python3 -m pip install python-osc
#python3 -m pip install pyserial
#python3 -m pip install pyjnius
#python3 -m pip install pynput

#python3 -m pip install pyinstaller
#macOS
#pyinstaller --onefile --windowed --icon PTSApp-Icon.icns --osx-bundle-identifier 'com.bradders' --name PTSApp PTSApp.py
#
#Windows
#pyinstaller --onefile --windowed --icon="PTSApp-Icon.ico" PTSApp.py

import asyncio
import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.utils import platform
from kivy.core.window import Window
from kivy.config import Config

if platform == 'android':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
else:
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'window_state', 'windowed')
    #Config.set('graphics', 'width', '1900')         #test
    #Config.set('graphics', 'height', '1000')        #test
    Config.set('graphics', 'width', '1340')         # A7 Lite
    Config.set('graphics', 'height', '703')         # A7 Lite
    #Config.set('graphics', 'width', '2000')         # A7
    #Config.set('graphics', 'height', '1092')        # A7
    Config.set('kivy','window_icon','PTSApp-Icon.png')
    Config.write()

    #Window.size = (1340, 800)  # A7 - 2000 x 1200       # A7 Lite - 1340 x 800  (0.8775)

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty
#from pynput.keyboard import Listener
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors.focus import FocusBehavior
from kivymd.app import MDApp
import threading
import os, sys
import time
from pathlib import Path
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher

window_sizes=Window.size
xDivSet = window_sizes[0] * 0.007462686567
yDivSet = window_sizes[1] * 0.01422475107

xScreenSet = window_sizes[0]
yScreenSet = window_sizes[1]

Cam1TextColour = '55FF55'
Cam2TextColour = '9DDDFF'
Cam3TextColour = 'FFFF55'

Cam1ButColour = '#208020'
Cam2ButColour = '#405C80'
Cam3ButColour = '#807100'

cam1Pos1Set = False
cam1Pos2Set = False
cam1Pos3Set = False
cam1Pos4Set = False
cam1Pos5Set = False
cam1Pos6Set = False
cam1Pos1Run = False
cam1Pos2Run = False
cam1Pos3Run = False
cam1Pos4Run = False
cam1Pos5Run = False
cam1Pos6Run = False
cam1AtPos1 = False
cam1AtPos2 = False
cam1AtPos3 = False
cam1AtPos4 = False
cam1AtPos5 = False
cam1AtPos6 = False

cam2Pos1Set = False
cam2Pos2Set = False
cam2Pos3Set = False
cam2Pos4Set = False
cam2Pos5Set = False
cam2Pos6Set = False
cam2Pos1Run = False
cam2Pos2Run = False
cam2Pos3Run = False
cam2Pos4Run = False
cam2Pos5Run = False
cam2Pos6Run = False
cam2AtPos1 = False
cam2AtPos2 = False
cam2AtPos3 = False
cam2AtPos4 = False
cam2AtPos5 = False
cam2AtPos6 = False

cam3Pos1Set = False
cam3Pos2Set = False
cam3Pos3Set = False
cam3Pos4Set = False
cam3Pos5Set = False
cam3Pos6Set = False
cam3Pos1Run = False
cam3Pos2Run = False
cam3Pos3Run = False
cam3Pos4Run = False
cam3Pos5Run = False
cam3Pos6Run = False
cam3AtPos1 = False
cam3AtPos2 = False
cam3AtPos3 = False
cam3AtPos4 = False
cam3AtPos5 = False
cam3AtPos6 = False

OLDcam1Pos1Set = False
OLDcam1Pos2Set = False
OLDcam1Pos3Set = False
OLDcam1Pos4Set = False
OLDcam1Pos5Set = False
OLDcam1Pos6Set = False
OLDcam1AtPos1 = False
OLDcam1AtPos2 = False
OLDcam1AtPos3 = False
OLDcam1AtPos4 = False
OLDcam1AtPos5 = False
OLDcam1AtPos6 = False
OLDcam1Pos1Run = False
OLDcam1Pos2Run = False
OLDcam1Pos3Run = False
OLDcam1Pos4Run = False
OLDcam1Pos5Run = False
OLDcam1Pos6Run = False

OLDcam2Pos1Set = False
OLDcam2Pos2Set = False
OLDcam2Pos3Set = False
OLDcam2Pos4Set = False
OLDcam2Pos5Set = False
OLDcam2Pos6Set = False
OLDcam2AtPos1 = False
OLDcam2AtPos2 = False
OLDcam2AtPos3 = False
OLDcam2AtPos4 = False
OLDcam2AtPos5 = False
OLDcam2AtPos6 = False
OLDcam2Pos1Run = False
OLDcam2Pos2Run = False
OLDcam2Pos3Run = False
OLDcam2Pos4Run = False
OLDcam2Pos5Run = False
OLDcam2Pos6Run = False

OLDcam3Pos1Set = False
OLDcam3Pos2Set = False
OLDcam3Pos3Set = False
OLDcam3Pos4Set = False
OLDcam3Pos5Set = False
OLDcam3Pos6Set = False
OLDcam3AtPos1 = False
OLDcam3AtPos2 = False
OLDcam3AtPos3 = False
OLDcam3AtPos4 = False
OLDcam3AtPos5 = False
OLDcam3AtPos6 = False
OLDcam3Pos1Run = False
OLDcam3Pos2Run = False
OLDcam3Pos3Run = False
OLDcam3Pos4Run = False
OLDcam3Pos5Run = False
OLDcam3Pos6Run = False

cam1SliderSpeed = 1
cam2SliderSpeed = 1
cam3SliderSpeed = 1

oldCam1Speed = 9
oldCam2Speed = 9
oldCam3Speed = 9

cam1PTSpeed = 1
cam2PTSpeed = 1
cam3PTSpeed = 1

oldCam1PTSpeed = 9
oldCam2PTSpeed = 9
oldCam3PTSpeed = 9

SetPosToggle = False

whichCamSerial = 1

interval = 0.2
previousTicks = time.time() + interval

PTJoy = (0, 0)

abs_coord_x = None
abs_coord_y = None
abs_coords = None
arr = []
oldAxisX = 0
oldAxisY = 0
oldAxisZ = 0
axisX = 0
axisY = 0
axisZ = 0
data = bytearray(8)
hat = ()
oldHatX = 0
oldHatY = 0
previousTime = time.time()
currentMillisMoveCheck = time.time()
previousMillisMoveCheck = time.time()
moveCheckInterval = 0.3
whichCamRead = 1

mousePTClick = False
mouseSlClick = False

doKeyControl = True
doKeyControlA = False
doKeyControlD = False
doKeyControlW = False
doKeyControlS = False
PTKeyChange = False
doKeyControlSL = False
doKeyControlSR = False
SlKeyChange = False

mouseMoving = False
panKeyPressed = False
tiltKeyPressed = False
sliderKeyPressed = False

cam1isZooming = False
cam1isRecording = False
cam2isZooming = False
cam2isRecording = False
cam3isZooming = False
cam3isRecording = False

isZooming = False

clearWhichCam = 1

btn_scan_show = False
btn_help_show = False
longestSerial = 0
device = None
device_name = None
USBrequsted = False

whichCamOSC = 1
whileLoopRun = True
serialLoop = True

moveType = 3
moveTypeOld = 0
resetButtons = False

msg = ''

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports
    from serial import Serial


KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

MDScreen:

    md_bg_color: get_color_from_hex("#21282D")

    canvas:
        # Joystick
        Color:
            rgba: get_color_from_hex("#7D0000")             # Red
        Rectangle:
            pos: (app.xDiv*1.6), (app.yDiv*25.3)
            size: (app.xDiv*36.8), (app.yDiv*44)

        Color:
            rgba: get_color_from_hex("#444444")             # Grey

        #Speed Border
        #PT
        Rectangle:
            pos: (app.xDiv*50.5), (app.yDiv*0.5)
            size: (app.xDiv*18), (app.yDiv*23)
        #Slider
        Rectangle:
            pos: (app.xDiv*71.5), (app.yDiv*0.5)
            size: (app.xDiv*18), (app.yDiv*23)
        #Zoom
        Rectangle:
            pos: (app.xDiv*92.5), (app.yDiv*0.5)
            size: (app.xDiv*13), (app.yDiv*23)

        #Background Colour
        Color:
            rgba: (0.1, 0.1, 0.1, 1)                        # Dark Grey BG
        #Joy PT Background
        Rectangle:
            pos: (app.xDiv*2), (app.yDiv*33)
            size: (app.xDiv*36), (app.yDiv*36)
        #Joy Slider Background
        Rectangle:
            pos: (app.xDiv*2), (app.yDiv*25.6)
            size: (app.xDiv*36), (app.yDiv*7)

        #Cam1 Speed BG
        Rectangle:
            pos: (app.xDiv*55), (app.yDiv*17)
            size: (app.xDiv*9), (app.yDiv*6)
        Rectangle:
            pos: (app.xDiv*76), (app.yDiv*17)
            size: (app.xDiv*9), (app.yDiv*6)

        #Cam2 Speed BG
        Rectangle:
            pos: (app.xDiv*55), (app.yDiv*9)
            size: (app.xDiv*9), (app.yDiv*6)
        Rectangle:
            pos: (app.xDiv*76), (app.yDiv*9)
            size: (app.xDiv*9), (app.yDiv*6)

        #Cam3 Speed BG
        Rectangle:
            pos: (app.xDiv*55), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
        Rectangle:
            pos: (app.xDiv*76), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)

        
        #Cam1 Speed Zoom
        Rectangle:
            pos: (app.xDiv*97), (app.yDiv*17)
            size: (app.xDiv*4), (app.yDiv*6)

        #Cam2 Speed Zoom
        Rectangle:
            pos: (app.xDiv*97), (app.yDiv*9)
            size: (app.xDiv*4), (app.yDiv*6)

        #Cam3 Speed Zoom
        Rectangle:
            pos: (app.xDiv*97), (app.yDiv*1)
            size: (app.xDiv*4), (app.yDiv*6)



    FloatLayout:
        id: cam1PTSpd
        sizPT1: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*17)
                size: self.sizPT1

    FloatLayout:
        id: cam2PTSpd
        sizPT2: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle: 
                pos: (app.xDiv*55), (app.yDiv*9)
                size: self.sizPT2

    FloatLayout:
        id: cam3PTSpd
        sizPT3: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle: 
                pos: (app.xDiv*55), (app.yDiv*1)
                size: self.sizPT3

    FloatLayout:
        id: cam1SlSpd
        sizSl1: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle: 
                pos: (app.xDiv*76), (app.yDiv*17)
                size: self.sizSl1

    FloatLayout:
        id: cam2SlSpd
        sizSl2: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle: 
                pos: (app.xDiv*76), (app.yDiv*9)
                size: self.sizSl2

    FloatLayout:
        id: cam3SlSpd
        sizSl3: 0, 0
        canvas:
            Color:
                rgba: get_color_from_hex("#7D0000")
            Rectangle: 
                pos: (app.xDiv*76), (app.yDiv*1)
                size: self.sizSl3


    ScrollView:
        # Serial Read
        id: scroll_view
        always_overscroll: False
        pos: (app.xDiv*50), (app.yDiv*25)
        size: (app.xDiv*83), (app.yDiv*40)
        size_hint: None, None
        do_scroll_x: False
        do_scroll_y: True

        canvas.before:
            Color:
                rgba: (0.1, 0.1, 0.1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: get_color_from_hex("#333333")
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height
        Label:
            id: txtInput_read
            font_name: "RobotoMono-Regular"
            size_hint: None, None
            size: self.texture_size
            padding: 5, 2
            halign: "left"
            valign: "top"
            markup: True
            text: ''

    
    FloatLayout:
        id: helpCanvas
        visible: False
        opacity: 1 if self.visible else 0
        helpRGB: (0.2, 0.2, 0.2, 1)
        canvas:
            Color:
                rgb: self.helpRGB
        
            Rectangle:
                pos: (app.xDiv*76), (app.yDiv*25)
                size: (app.xDiv*45), (app.yDiv*40)

    Label:
        id: helpLabel
        visible: False
        font_name: "RobotoMono-Regular"
        font_size: '13dp' #(app.yDiv*1.4)
        pos: (app.xDiv*59), (app.yDiv*14)
        size_hint: None, None
        size: (app.xDiv*80), (app.yDiv*60)
        #size_hint_x: 1 if self.visible else 0
        opacity: 1 if self.visible else 0
        halign: "left"
        valign: "top"
        markup: True
        text: 'OSC Server Port: 6503\\nOSC Client Port: 1337\\n\\nSerial Text Commands:\\ns(int) = Pan   speed (º/s)\\nS(int) = Tilt  speed (º/s)\\na(int) = Slide speed (mm/s)\\n\\nq(float) = Pan   accel\\nQ(float) = Tilt  accel\\nw(float) = Slide accel\\n\\ne(int) = Joystick pan   accel factor (1 = 100%)\\nE(int) = Joystick tilt  accel factor (1 = 100%)\\nD(int) = Joystick slide accel factor (1 = 100%)\\n\\nd(int) = Slide speed increments\\nf(int) = Slide min speed limit\\nF(int) = Slide max speed limit\\n\\nU = Save to EEPROM\\n'
    

    FloatLayout:
        TextInput:
            id: textInput
            pos: (app.xDiv*122), (app.yDiv*61)
            size: (app.xDiv*10), (app.yDiv*3)
            size_hint: None, None


    ScrollView:
        id: scanDD
        pos: app.xScreen, app.yScreen
        size: (app.xDiv*30), app.yScreen
        size_hint: None, None
        do_scroll_x: False
        BoxLayout:
            id: box_list
            orientation: 'vertical'
            on_parent: app.uiDict['box_list'] = self
            size: (app.xDiv*25), (app.yDiv*6)
            size_hint: None, None
            height: max(self.parent.height, self.minimum_height)






    #Label:
    #    id: OSCSend
    #    font_name: "RobotoMono-Regular"
    #    pos: (app.xDiv*45), (app.yDiv*65.7)
    #    size_hint: None, None
    #    size: (app.xDiv*8), (app.yDiv*6)
    #    halign: "left"
    #    valign: "top"
    #    markup: True
    #    text: 'Test'
    
    #Label:
    #    id: OSCRec
    #    font_name: "RobotoMono-Regular"
    #    pos: (app.xDiv*45), (app.yDiv*63.7)
    #    size_hint: None, None
    #    size: (app.xDiv*8), (app.yDiv*6)
    #    halign: "left"
    #    valign: "top"
    #    markup: True
    #    text: 'Test2'



    Button:
        id: btnL10
        pos: (app.xDiv*3), (app.yDiv*48)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joyL10()

    Button:
        id: btnL1
        pos: (app.xDiv*10), (app.yDiv*48)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:".1"
        on_press: app.joyL1()

    Button:
        id: btnR1
        pos: (app.xDiv*24), (app.yDiv*48)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:".1"
        on_press: app.joyR1()

    Button:
        id: btnR10
        pos: (app.xDiv*31), (app.yDiv*48)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joyR10()

    Button:
        id: btnU10
        pos: (app.xDiv*17), (app.yDiv*62)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joyU10()

    Button:
        id: btnU1
        pos: (app.xDiv*17), (app.yDiv*55)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:".1"
        on_press: app.joyU1()

    Button:
        id: btnD1
        pos: (app.xDiv*17), (app.yDiv*41)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:".1"
        on_press: app.joyD1()

    Button:
        id: btnD10
        pos: (app.xDiv*17), (app.yDiv*34)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joyD10()

    Button:
        id: btnSL100
        pos: (app.xDiv*3), (app.yDiv*26)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"100"
        on_press: app.joySL100()

    Button:
        id: btnSL10
        pos: (app.xDiv*10), (app.yDiv*26)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joySL10()

    Button:
        id: btnSR10
        pos: (app.xDiv*24), (app.yDiv*26)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"10"
        on_press: app.joySR10()

    Button:
        id: btnSR100
        pos: (app.xDiv*31), (app.yDiv*26)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        text:"100"
        on_press: app.joySR100()


    Button:
        id: PTJoyDotPress
        pos: (app.xDiv*18), (app.yDiv*49)
        size: (app.xDiv*4), (app.yDiv*4)
        size_hint: None, None
        background_normal: ''
        background_down: ''
        background_color: get_color_from_hex("#7D0000")
        text: ''
        on_press: app.PTJoyDotPressed()

    Button:
        id: PTJoyDot
        pos: app.xScreen, app.yScreen
        size: (app.xDiv*4), (app.yDiv*4)
        size_hint: None, None
        background_normal: ''
        background_down: ''
        background_color: get_color_from_hex("#7D0000")
        text: ''

    Button:
        id: SlJoyDotPress
        pos: (app.xDiv*18), (app.yDiv*27)
        size: (app.xDiv*4), (app.yDiv*4)
        size_hint: None, None
        background_normal: ''
        background_down: ''
        background_color: get_color_from_hex("#7D0000")
        text: ''
        on_press: app.SlJoyDotPressed()

    Button:
        id: SlJoyDot
        pos: app.xScreen, app.yScreen
        size: (app.xDiv*4), (app.yDiv*4)
        size_hint: None, None
        background_normal: ''
        background_down: ''
        background_color: get_color_from_hex("#7D0000")
        text: ''



    Button:
        id: setPos
        pos: (app.xDiv*39.5), (app.yDiv*27)
        size: (app.xDiv*9), (app.yDiv*4)
        size_hint: None, None
        font_size: (app.yDiv*2)
        text:"Set Pos"
        background_normal: ''
        background_color: get_color_from_hex("#666666")
        on_press: app.setPos(3)


    Button:
        id: btnCam1Go1
        text:"1"
        pos: (app.xDiv*1), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go1()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1Go2
        text:"2"
        pos: (app.xDiv*9), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go2()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1Go3
        text:"3"
        pos: (app.xDiv*17), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go3()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1Go4
        text:"4"
        pos: (app.xDiv*25), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1 
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go4()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1Go5
        text:"5"
        pos: (app.xDiv*33), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go5()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1Go6
        text:"6"
        pos: (app.xDiv*41), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.Cam1Go6()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam1PT-
        text: "PT\\n-"
        halign: 'center'
        pos: (app.xDiv*51), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1PTSpeedDec()

    Button:
        id: btnCam1PT+
        text: "PT\\n+"
        halign: 'center'
        pos: (app.xDiv*64), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1PTSpeedInc()

    Button:
        id: btnCam1Sl-
        text: "Sl\\n-"
        halign: 'center'
        pos: (app.xDiv*72), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1SliderSpeedDec()

    Button:
        id: btnCam1Sl+
        text: "Sl\\n+"
        halign: 'center'
        pos: (app.xDiv*85), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1SliderSpeedInc()

    Button:
        id: btnCam1Zm-
        text:"Zm\\nOUT"
        halign: 'center'
        pos: (app.xDiv*93), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1ZoomOut()
        #on_release: app.sendCam1ZoomStop()

    Button:
        id: btnCam1Zm+
        text:"Zm\\nIN"
        halign: 'center'
        pos: (app.xDiv*101), (app.yDiv*17)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendCam1ZoomIn()
        #on_release: app.sendCam1ZoomStop()
    
    Button:
        id: cam1Record
        pos: (app.xDiv*110), (app.yDiv*18)
        size: (app.xDiv*11), (app.yDiv*4)
        size_hint: None, None
        font_size: (app.yDiv*2)
        text: "Record"
        background_normal: ''
        background_color: get_color_from_hex("#666666")
        on_press: app.sendCam1RecordToggle()

    Button:
        id: btnCam1Clr
        text:"Clear"
        pos: (app.xDiv*126), (app.yDiv*17)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam1ButColour)
        on_press: app.sendClearCam1Pos()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height






    Button:
        id: btnCam2Go1
        text:"1"
        pos: (app.xDiv*1), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go1()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2Go2
        text:"2"
        pos: (app.xDiv*9), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go2()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2Go3
        text:"3"
        pos: (app.xDiv*17), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go3()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2Go4
        text:"4"
        pos: (app.xDiv*25), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go4()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2Go5
        text:"5"
        pos: (app.xDiv*33), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go5()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2Go6
        text:"6"
        pos: (app.xDiv*41), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.Cam2Go6()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam2PT-
        text: "PT\\n-"
        halign: 'center'
        pos: (app.xDiv*51), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2PTSpeedDec()

    Button:
        id: btnCam2PT+
        text: "PT\\n+"
        halign: 'center'
        pos: (app.xDiv*64), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2PTSpeedInc()

    Button:
        id: btnCam2Sl-
        text: "Sl\\n-"
        halign: 'center'
        pos: (app.xDiv*72), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2SliderSpeedDec()

    Button:
        id: btnCam2Sl+
        text: "Sl\\n+"
        halign: 'center'
        pos: (app.xDiv*85), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2SliderSpeedInc()

    Button:
        id: btnCam2Zm-
        text:"Zm\\nOUT"
        halign: 'center'
        pos: (app.xDiv*93), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2ZoomOut()
        #on_release: app.sendCam2ZoomStop()

    Button:
        id: btnCam2Zm+
        text:"Zm\\nIN"
        halign: 'center'
        pos: (app.xDiv*101), (app.yDiv*9)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendCam2ZoomIn()
        #on_release: app.sendCam2ZoomStop()
    
    Button:
        id: cam2Record
        #size_hint: 0.08, 0.056
        #pos_hint: {'x':.825, 'y':.15}
        pos: (app.xDiv*110), (app.yDiv*10)
        size: (app.xDiv*11), (app.yDiv*4)
        size_hint: None, None
        font_size: (app.yDiv*2)
        text: "Record"
        background_normal: ''
        background_color: get_color_from_hex("#666666")
        on_press: app.sendCam2RecordToggle()

    Button:
        id: btnCam2Clr
        text:"Clear"
        #size_hint: 0.046, 0.086
        #pos_hint: {'x':.94, 'y':.135}
        pos: (app.xDiv*126), (app.yDiv*9)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam2ButColour)
        on_press: app.sendClearCam2Pos()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height







    Button:
        id: btnCam3Go1
        text:"1"
        pos: (app.xDiv*1), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go1()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3Go2
        text:"2"
        pos: (app.xDiv*9), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go2()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3Go3
        text:"3"
        pos: (app.xDiv*17), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go3()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3Go4
        text:"4"
        pos: (app.xDiv*25), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go4()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3Go5
        text:"5"
        pos: (app.xDiv*33), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go5()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3Go6
        text:"6"
        pos: (app.xDiv*41), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*3)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.Cam3Go6()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height

    Button:
        id: btnCam3PT-
        text: "PT\\n-"
        halign: 'center'
        pos: (app.xDiv*51), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3PTSpeedDec()

    Button:
        id: btnCam3PT+
        text: "PT\\n+"
        halign: 'center'
        pos: (app.xDiv*64), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3PTSpeedInc()

    Button:
        id: btnCam3Sl-
        text: "Sl\\n-"
        halign: 'center'
        pos: (app.xDiv*72), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3SliderSpeedDec()

    Button:
        id: btnCam3Sl+
        text: "Sl\\n+"
        halign: 'center'
        pos: (app.xDiv*85), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3SliderSpeedInc()

    Button:
        id: btnCam3Zm-
        text:"Zm\\nOUT"
        halign: 'center'
        pos: (app.xDiv*93), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3ZoomOut()
        #on_release: app.sendCam3ZoomStop()

    Button:
        id: btnCam3Zm+
        text:"Zm\\nIN"
        halign: 'center'
        pos: (app.xDiv*101), (app.yDiv*1)
        size: (app.xDiv*4), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendCam3ZoomIn()
        #on_release: app.sendCam3ZoomStop()
    
    Button:
        id: cam3Record
        #size_hint: 0.08, 0.056
        #pos_hint: {'x':.825, 'y':.04}
        pos: (app.xDiv*110), (app.yDiv*2)
        size: (app.xDiv*11), (app.yDiv*4)
        size_hint: None, None
        font_size: (app.yDiv*2)
        text: "Record"
        background_normal: ''
        background_color: get_color_from_hex("#666666")
        on_press: app.sendCam3RecordToggle()

    Button:
        id: btnCam3Clr
        text:"Clear"
        #size_hint: 0.046, 0.086
        #pos_hint: {'x':.94, 'y':.025}
        pos: (app.xDiv*126), (app.yDiv*1)
        size: (app.xDiv*6), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        col: .13, .13, .13, 1
        background_normal: ''
        background_color: get_color_from_hex(app.Cam3ButColour)
        on_press: app.sendClearCam3Pos()
        canvas.before:
            Color: 
                rgba: self.col
            Line:
                width: 4
                rectangle: self.x, self.y, self.width, self.height




    MDFillRoundFlatButton:
        id: buttonWhichCam1
        text: "Cam 1"
        #user_font_size: "30sp"
        line_width: 5
        line_color: 1, 0, 0, 1
        md_bg_color: get_color_from_hex("#208020")
        pos: (app.xDiv*39.5), (app.yDiv*57)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.whichCamSerial1()

    MDFillRoundFlatButton:
        id: buttonWhichCam2
        text: "Cam 2"
        #user_font_size: "30sp"
        line_width: 5
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#405C80")
        pos: (app.xDiv*39.5), (app.yDiv*49)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.whichCamSerial2()

    MDFillRoundFlatButton:
        id: buttonWhichCam3
        text: "Cam 3"
        #user_font_size: "30sp"
        line_width: 5
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#807100")
        pos: (app.xDiv*39.5), (app.yDiv*41)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.whichCamSerial3()



    MDFillRoundFlatButton:
        id: btn_Report
        text: "Report"
        user_font_size: "30sp"
        line_width: 2
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#757981")
        pos: (app.xDiv*65), (app.yDiv*65.7)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.btnReport()

    MDFillRoundFlatButton:
        id: btn_Report
        text: "Report Pos"
        user_font_size: "30sp"
        line_width: 2
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#757981")
        pos: (app.xDiv*78), (app.yDiv*65.7)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.btnReportPos()

    MDFillRoundFlatButton:
        id: btn_Report
        text: "Report Key"
        user_font_size: "30sp"
        line_width: 2
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#757981")
        pos: (app.xDiv*94), (app.yDiv*65.7)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.btnReportKey()

    MDFillRoundFlatButton:
        id: btn_scan
        text: "Scan Ports"
        user_font_size: "30sp"
        line_width: 2
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#757981")
        pos: (app.xDiv*109), (app.yDiv*65.7)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.on_btn_scan_release()

    MDFillRoundFlatButton:
        id: btn_help
        text: "Help"
        user_font_size: "30sp"
        line_width: 2
        line_color: .13, .13, .13, 1
        md_bg_color: get_color_from_hex("#757981")
        pos: (app.xDiv*124), (app.yDiv*65.7)
        size: (app.xDiv*8), (app.yDiv*6)
        size_hint: None, None
        font_size: (app.yDiv*2)
        on_release: app.on_btn_help_release()

    

    """




def filter_handler(address, *args):
    global moveType
    #print(f"{address}: {args}")                        # Debug - Watch incomming OSC events
    if address == "/setPos":
        MDApp.get_running_app().setPos(args[0])
    elif address == "/Cam1Go1" and args[0] == 1:
        MDApp.get_running_app().Cam1Go1()
    elif address == "/Cam1Go2" and args[0] == 1:
        MDApp.get_running_app().Cam1Go2()
    elif address == "/Cam1Go3" and args[0] == 1:
        MDApp.get_running_app().Cam1Go3()
    elif address == "/Cam1Go4" and args[0] == 1:
        MDApp.get_running_app().Cam1Go4()
    elif address == "/Cam1Go5" and args[0] == 1:
        MDApp.get_running_app().Cam1Go5()
    elif address == "/Cam1Go6" and args[0] == 1:
        MDApp.get_running_app().Cam1Go6()
    elif address == "/Cam2Go1" and args[0] == 1:
        MDApp.get_running_app().Cam2Go1()
    elif address == "/Cam2Go2" and args[0] == 1:
        MDApp.get_running_app().Cam2Go2()
    elif address == "/Cam2Go3" and args[0] == 1:
        MDApp.get_running_app().Cam2Go3()
    elif address == "/Cam2Go4" and args[0] == 1:
        MDApp.get_running_app().Cam2Go4()
    elif address == "/Cam2Go5" and args[0] == 1:
        MDApp.get_running_app().Cam2Go5()
    elif address == "/Cam2Go6" and args[0] == 1:
        MDApp.get_running_app().Cam2Go6()
    elif address == "/Cam3Go1" and args[0] == 1:
        MDApp.get_running_app().Cam3Go1()
    elif address == "/Cam3Go2" and args[0] == 1:
        MDApp.get_running_app().Cam3Go2()
    elif address == "/Cam3Go3" and args[0] == 1:
        MDApp.get_running_app().Cam3Go3()
    elif address == "/Cam3Go4" and args[0] == 1:
        MDApp.get_running_app().Cam3Go4()
    elif address == "/Cam3Go5" and args[0] == 1:
        MDApp.get_running_app().Cam3Go5()
    elif address == "/Cam3Go6" and args[0] == 1:
        MDApp.get_running_app().Cam3Go6()
    elif address == "/Cam1PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam1PTSpeedInc()
    elif address == "/Cam1PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam1PTSpeedDec()
    elif address == "/Cam1SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam1SlSpeedInc()
    elif address == "/Cam1SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam1SlSpeedDec()
    elif address == "/Cam2PTSpd":
        MDApp.get_running_app().sendCam2PTSpeedOSC(args[0])
    elif address == "/Cam2SlSpd":
        MDApp.get_running_app().sendCam2SlSpeedOSC(args[0])

    elif address == "/Cam3PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam3PTSpeedInc()
    elif address == "/Cam3PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam3PTSpeedDec()
    elif address == "/Cam3SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam3SlSpeedInc()
    elif address == "/Cam3SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam3SlSpeedDec()

    elif address == "/Cam1ZoomIn" and args[0] == 1:
        MDApp.get_running_app().sendCam1ZoomIn()
    elif address == "/Cam1ZoomOut" and args[0] == 1:
        MDApp.get_running_app().sendCam1ZoomOut()
    elif address == "/Cam1ZoomStop" and args[0] == 1:
        MDApp.get_running_app().sendCam1ZoomStop()

    elif address == "/Cam2ZoomIn" and args[0] == 1:
        MDApp.get_running_app().sendCam2ZoomIn()
    elif address == "/Cam2ZoomOut" and args[0] == 1:
        MDApp.get_running_app().sendCam2ZoomOut()
    elif address == "/Cam2ZoomStop" and args[0] == 1:
        MDApp.get_running_app().sendCam2ZoomStop()

    elif address == "/Cam3ZoomIn" and args[0] == 1:
        MDApp.get_running_app().sendCam3ZoomIn()
    elif address == "/Cam3ZoomOut" and args[0] == 1:
        MDApp.get_running_app().sendCam3ZoomOut()
    elif address == "/Cam3ZoomStop" and args[0] == 1:
        MDApp.get_running_app().sendCam3ZoomStop()


    elif address == "/Cam1Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam1Pos()
    elif address == "/Cam2Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam2Pos()
    elif address == "/Cam3Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam3Pos()

    elif address == "/Cam1Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam1RecordToggleOSC()
    elif address == "/Cam2Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam2RecordToggleOSC()
    elif address == "/Cam3Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam3RecordToggleOSC()

    elif address == "/moveType" and args[0] == 1:
        moveType = 1
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 2:
        moveType = 2
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 3:
        moveType = 3
        MDApp.get_running_app().doButtonColours()

    elif address == "/Cam1Left" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'a')
    elif address == "/Cam1Right" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'd')
    elif address == "/Cam1Up" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'w')
    elif address == "/Cam1Down" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 's')
    elif address == "/Cam1SlLeft" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, ',')
    elif address == "/Cam1SlRight" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, '.')

    elif address == "/Cam1LeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'A')
    elif address == "/Cam1RightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'D')
    elif address == "/Cam1UpRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'W')
    elif address == "/Cam1DownRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, 'S')
    elif address == "/Cam1SlLeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, '<')
    elif address == "/Cam1SlRightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(1, '>')

    elif address == "/Cam2Left" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'a')
    elif address == "/Cam2Right" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'd')
    elif address == "/Cam2Up" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'w')
    elif address == "/Cam2Down" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 's')
    elif address == "/Cam2SlLeft" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, ',')
    elif address == "/Cam2SlRight" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, '.')

    elif address == "/Cam2LeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'A')
    elif address == "/Cam2RightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'D')
    elif address == "/Cam2UpRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'W')
    elif address == "/Cam2DownRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, 'S')
    elif address == "/Cam2SlLeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, '<')
    elif address == "/Cam2SlRightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(2, '>')

    elif address == "/Cam3Left" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'a')
    elif address == "/Cam3Right" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'd')
    elif address == "/Cam3Up" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'w')
    elif address == "/Cam3Down" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 's')
    elif address == "/Cam3SlLeft" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, ',')
    elif address == "/Cam3SlRight" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, '.')

    elif address == "/Cam3LeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'A')
    elif address == "/Cam3RightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'D')
    elif address == "/Cam3UpRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'W')
    elif address == "/Cam3DownRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, 'S')
    elif address == "/Cam3SlLeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, '<')
    elif address == "/Cam3SlRightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(3, '>')


    elif address == "/Cam1PTSpeedInc" and args[0] == 1:
        MDApp.get_running_app().sendCam1PTSpeedInc()
    elif address == "/Cam1PTSpeedDec" and args[0] == 1:
        MDApp.get_running_app().sendCam1PTSpeedDec()
    elif address == "/Cam2PTSpeedInc" and args[0] == 1:
        MDApp.get_running_app().sendCam2PTSpeedInc()
    elif address == "/Cam2PTSpeedDec" and args[0] == 1:
        MDApp.get_running_app().sendCam2PTSpeedDec()
    elif address == "/Cam3PTSpeedInc" and args[0] == 1:
        MDApp.get_running_app().sendCam3PTSpeedInc()
    elif address == "/Cam3PTSpeedDec" and args[0] == 1:
        MDApp.get_running_app().sendCam3PTSpeedDec()
    



dispatcher = Dispatcher()
dispatcher.map("/*", filter_handler)

ip = "127.0.0.1"
srvPort = 6503
cliPort = 1337

client = SimpleUDPClient(ip, cliPort)

class EventLoopWorker(EventDispatcher):

    __events__ = ('on_pulse',)  # defines this EventDispatcher's sole event

    def __init__(self):
        super().__init__()
        self._thread = threading.Thread(target=self._run_loop)  # note the Thread target here
        self._thread.daemon = True
        self.loop = None
        # the following are for the pulse() coroutine, see below
        self._default_pulse = ['OSC Enabled\n']
        self._pulse = None
        self._pulse_task = None

    def _run_loop(self):
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)

        self._restart_pulse()
        # this example doesn't include any cleanup code, see the docs on how
        # to properly set up and tear down an asyncio event loop
        self.loop.run_forever()

    def start(self):
        self._thread.start()

    async def pulse(self):
        """Core coroutine of this asyncio event loop.
        Repeats a pulse message in a short interval on three channels:
        - using `print()`
        - by dispatching a Kivy event `on_pulse` with the help of `@mainthread`
        - on the Kivy thread through `kivy_update_status()` with the help of
          `@mainthread`
        The decorator `@mainthread` is a convenience wrapper around
        `Clock.schedule_once()` which ensures the callables run on the Kivy
        thread.
        """
        #for msg in self._pulse_messages():
            # show it through the console:
            #print(msg)

            # `EventLoopWorker` is an `EventDispatcher` to which others can
            # subscribe. See `display_on_pulse()` in `start_event_loop_thread()`
            # on how it is bound to the `on_pulse` event.  The indirection
            # through the `notify()` function is necessary to apply the
            # `@mainthread` decorator (left label):
        #    @mainthread
        #    def notify(text):
        #        self.dispatch('on_pulse', text)

        #    notify(msg)  # dispatch the on_pulse event

            # Same, but with a direct call instead of an event (right label):
            #@mainthread
            #def kivy_update_status(text):
            #    status_label = App.get_running_app().root.ids.status
            #    status_label.text = text

            #kivy_update_status(msg)  # control a Label directly

        await asyncio.sleep(0.1)
        server = AsyncIOOSCUDPServer((ip, srvPort), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

        global resetButtons
        resetButtons = True

    def set_pulse_text(self, text):
        self._pulse = text
        self._restart_pulse()

    def _restart_pulse(self):
        """Helper to start/reset the pulse task when the pulse changes."""
        if self._pulse_task is not None:
            self._pulse_task.cancel()
        self._pulse_task = self.loop.create_task(self.pulse())

    def on_pulse(self, *_):
        """An EventDispatcher event must have a corresponding method."""
        pass

    def _pulse_messages(self):
        """A generator providing an inexhaustible supply of pulse messages."""
        while True:
            if isinstance(self._pulse, str) and self._pulse != '':
                pulse = self._pulse.split()
                yield from pulse
            else:
                yield from self._default_pulse


class KivyPTS(MDApp):

    xDiv = NumericProperty(xDivSet)        # 10 / 1340
    yDiv = NumericProperty(yDivSet)        # 10 / 703

    xScreen = NumericProperty(xScreenSet)
    yScreen = NumericProperty(yScreenSet)

    def __init__(self, *args, **kwargs):
        global Cam1ButColour
        global Cam2ButColour
        global Cam3ButColour
        self.Cam1ButColour = Cam1ButColour
        self.Cam2ButColour = Cam2ButColour
        self.Cam3ButColour = Cam3ButColour
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None
        #self.port_thread_lock = threading.Lock()

        #base_path = Path(__file__).parent
        #image_path = (base_path / "./PTSApp-Icon.png").resolve()
        #self.icon = os.path.join(image_path)
        super(KivyPTS, self).__init__(*args, **kwargs)
        self.event_loop_worker = None

    def build(self):
        global PTJoy
        global srvPort
        global cliPort
        self.screen = Builder.load_string(KV)
        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_touch_up = self.on_touch_up)
        Window.bind(on_request_close = self.stopping)
        Window.bind(on_key_down = self.keyDown)
        #listener = Listener(on_press = self.on_press, on_release=self.on_release)
        #listener.start()
        Clock.schedule_interval(self.flash, 1.0)
        Clock.schedule_interval(self.doJoyMoves, 0.1)
        self.start_event_loop_thread()
        Clock.schedule_once(self.showPorts, 0)
        self.icon = 'PTSApp-Icon.png'
        return self.screen

    def keyDown(self, instance, keyboard, keycode, text, modifiers):
        global axisX
        global axisY
        global axisZ

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        
        if self.root.ids.textInput.focus == False:              #   a= 4, s= 22, d=7, w= 26, ,=54, .=55
            #print(keycode)
            if keycode == 4:
                axisX = -255
            if keycode == 7:
                axisX = 255
            if keycode == 26:
                axisY = -255
            if keycode == 22:
                axisY = 255
            if keycode == 54:
                axisZ = -255
            if keycode == 55:
                axisZ = 255

            self.doJoyMoves(1)
            self.doButtonColours()

        if keycode == 40 and (self.root.ids.textInput.focus == True):
            global whichCamSerial
            if whichCamSerial == 1:
                temp = "??"
            elif whichCamSerial == 2:
                temp = "!?"
            elif whichCamSerial == 3:
                temp = "@?"

            tempInput = (self.root.ids.textInput.text)
            temp += tempInput
            #print(temp)                                                                 # for debugging
            if self.serial_port and self.serial_port.is_open:
                self.sendSerial(str(temp.encode()))
                Clock.schedule_once(self.clearTextInput, 0)

                if whichCamSerial == 1:
                    self.root.ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]Sent command: " + tempInput + "[/color]\n")
                    self.root.ids.scroll_view.scroll_y = 0
                elif whichCamSerial == 2:
                    self.root.ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]Sent command: " + tempInput + "[/color]\n")
                    self.root.ids.scroll_view.scroll_y = 0
                elif whichCamSerial == 3:
                    self.root.ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]Sent command: " + tempInput + "[/color]\n")
                    self.root.ids.scroll_view.scroll_y = 0

            else:
                self.root.ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                textLength = len(self.root.ids.txtInput_read.text)
                if textLength > 8000:
                    self.root.ids.txtInput_read.text = self.root.ids.txtInput_read.text[1000:textLength]
                self.root.ids.scroll_view.scroll_y = 0
                Clock.schedule_once(self.clearTextInput, 0)

    def clearTextInput(self, dt):
        self.root.ids.textInput.text = ""

    def showPorts(self, dt):
        #self.root.ids.OSCSend.text = "OSC Server Port: " + str(srvPort)
        #self.root.ids.OSCRec.text = "OSC Client Port: " + str(cliPort)
        return

    def stopping(self, dt):
        global whileLoopRun
        whileLoopRun = False
        sys.exit()

    def start_event_loop_thread(self):
        """Start the asyncio event loop thread. Bound to the top button."""
        if self.event_loop_worker is not None:
            print("loop event worker is not NONE")
            return
        #self.root.ids.btn_OSC.text = ("OSC ON")
        self.event_loop_worker = worker =  EventLoopWorker()
        #pulse_listener_label = self.root.ids.pulse_listener

        def display_on_pulse(instance, text):
            self.root.ids.txtInput_read.text += text
            self.root.ids.scroll_view.scroll_y = 0
            #print(text)
            #pulse_listener_label.text = text

        # make the label react to the worker's `on_pulse` event:
        worker.bind(on_pulse=display_on_pulse)
        worker.start()

    def submit_pulse_text(self, text):
        """Send the TextInput string over to the asyncio event loop worker."""
        worker = self.event_loop_worker
        if worker is not None:
            loop = self.event_loop_worker.loop
            # use the thread safe variant to run it on the asyncio event loop:
            loop.call_soon_threadsafe(worker.set_pulse_text, text)

    '''
    def on_press(self, key):
        global axisX
        global axisY
        global axisZ
        global doKeyControlA
        global doKeyControlD
        global doKeyControlW
        global doKeyControlS
        global doKeyControlSL
        global doKeyControlSR
        global panKeyPressed
        global sliderKeyPressed
        global PTKeyChange
        global SlKeyChange
        global doKeyControl
        global whichCamSerial
        global xDivSet
        global yDivSet

        StreamDeck = True
    '''
    '''
        if doKeyControl:
            try:
                if hasattr(key, 'char'):
                    if key.char == 'a':
                        axisX = -255
                        doKeyControlA = True
                        PTKeyChange = True
                        xKeySet = (xDivSet*4)
                    elif key.char == 'd':
                        axisX = 255
                        doKeyControlD = True
                        PTKeyChange = True
                        xKeySet = (xDivSet*36)
                    elif key.char == 'w':
                        axisY = -255
                        doKeyControlW = True
                        PTKeyChange = True
                        yKeySet = (yDivSet*67)
                    elif key.char == 's':
                        axisY = 255
                        doKeyControlS = True
                        PTKeyChange = True
                        yKeySet = (yDivSet*35)
                    elif key.char == 'z':
                        axisZ = -255
                        doKeyControlSL = True
                        SlKeyChange = True
                    elif key.char == 'x':
                        axisZ = 255
                        doKeyControlSR = True
                        SlKeyChange = True

                    elif key.char == 'r':
                        if StreamDeck and cam1Pos1Set and not cam1AtPos1:
                            self.sendSerial('&z')
                    elif key.char == 'f':
                        if StreamDeck and cam2Pos1Set and not cam2AtPos1:
                            self.sendSerial('&a')
                    elif key.char == 'v':
                        if StreamDeck and cam3Pos1Set and not cam3AtPos1:
                            self.sendSerial('&q')
                    elif key.char == 'R':
                        if StreamDeck:
                            self.sendSerial('&Z')
                    elif key.char == 'F':
                        if StreamDeck:
                            self.sendSerial('&A')
                    elif key.char == 'V':
                        if StreamDeck:
                            self.sendSerial('&Q')

                    elif key.char == 't':
                        if StreamDeck and cam1Pos2Set and not cam1AtPos2:
                            self.sendSerial('&x')
                    elif key.char == 'g':
                        if StreamDeck and cam2Pos2Set and not cam2AtPos2:
                            self.sendSerial('&s')
                    elif key.char == 'b':
                        if StreamDeck and cam3Pos2Set and not cam3AtPos2:
                            self.sendSerial('&w')
                    elif key.char == 'T':
                        if StreamDeck:
                            self.sendSerial('&X')
                    elif key.char == 'G':
                        if StreamDeck:
                            self.sendSerial('&S')
                    elif key.char == 'B':
                        if StreamDeck:
                            self.sendSerial('&W')

                    elif key.char == 'y':
                        if StreamDeck and cam1Pos3Set and not cam1AtPos3:
                            self.sendSerial('&c')
                    elif key.char == 'h':
                        if StreamDeck and cam2Pos3Set and not cam2AtPos3:
                            self.sendSerial('&d')
                    elif key.char == 'n':
                        if StreamDeck and cam3Pos3Set and not cam3AtPos3:
                            self.sendSerial('&e')
                    elif key.char == 'Y':
                        if StreamDeck:
                            self.sendSerial('&C')
                    elif key.char == 'H':
                        if StreamDeck:
                            self.sendSerial('&D')
                    elif key.char == 'N':
                        if StreamDeck:
                            self.sendSerial('&E')

                    elif key.char == 'u':
                        if StreamDeck and cam1Pos4Set and not cam1AtPos4:
                            self.sendSerial('&v')
                    elif key.char == 'j':
                        if StreamDeck and cam2Pos4Set and not cam2AtPos4:
                            self.sendSerial('&f')
                    elif key.char == 'm':
                        if StreamDeck and cam3Pos4Set and not cam3AtPos4:
                            self.sendSerial('&r')
                    elif key.char == 'U':
                        if StreamDeck:
                            self.sendSerial('&V')
                    elif key.char == 'J':
                        if StreamDeck:
                            self.sendSerial('&F')
                    elif key.char == 'M':
                        if StreamDeck:
                            self.sendSerial('&R')

                    elif key.char == 'i':
                        if StreamDeck and cam1Pos5Set and not cam1AtPos5:
                            self.sendSerial('&b')
                    elif key.char == 'k':
                        if StreamDeck and cam2Pos5Set and not cam2AtPos5:
                            self.sendSerial('&g')
                    elif key.char == ',':
                        if StreamDeck and cam3Pos5Set and not cam3AtPos5:
                            self.sendSerial('&t')
                    elif key.char == 'I':
                        if StreamDeck:
                            self.sendSerial('&B')
                    elif key.char == 'K':
                        if StreamDeck:
                            self.sendSerial('&G')
                    elif key.char == '<':
                        if StreamDeck:
                            self.sendSerial('&T')

                    elif key.char == 'o':
                        if StreamDeck and cam1Pos6Set and not cam1AtPos6:
                            self.sendSerial('&n')
                    elif key.char == 'l':
                        if StreamDeck and cam2Pos6Set and not cam2AtPos6:
                            self.sendSerial('&h')
                    elif key.char == '.':
                        if StreamDeck and cam3Pos6Set and not cam3AtPos6:
                            self.sendSerial('&y')
                    elif key.char == 'O':
                        if StreamDeck:
                            self.sendSerial('&N')
                    elif key.char == 'L':
                        if StreamDeck:
                            self.sendSerial('&H')
                    elif key.char == '>':
                        if StreamDeck:
                            self.sendSerial('&Y')

                    if not mousePTClick:
                        self.root.ids.PTJoyDot.pos = (xKeySet, yKeySet)


                    
            #PTXMin = (xDivSet*4)
            #PTXMax = (xDivSet*36)
            #PTYMin = (yDivSet*35)
            #PTYMax = (yDivSet*67)

                elif key.name == 'tab':
                    if whichCamSerial == 1:
                        whichCamSerial = 2;
                    elif whichCamSerial == 2:
                        whichCamSerial = 3;
                    elif whichCamSerial == 3:
                        whichCamSerial = 1;
            except:
                return
            if (doKeyControlA or doKeyControlD or doKeyControlW or doKeyControlS):
                panKeyPressed = True

            if (doKeyControlSL or doKeyControlSR):
                sliderKeyPressed = True
    '''

    '''
    def on_release(self, key):
        global axisX
        global axisY
        global axisZ
        global doKeyControlA
        global doKeyControlD
        global doKeyControlW
        global doKeyControlS
        global doKeyControlSL
        global doKeyControlSR
        global PTKeyChange
        global SlKeyChange
        global doKeyControl
        global panKeyPressed
        global sliderKeyPressed
        global xDivSet
        global yDivSet
    '''
    '''
        if doKeyControl:
            try:
                if hasattr(key, 'char'):
                    if key.char == 'a':
                        doKeyControlA = False
                        PTKeyChange = True
                        if not doKeyControlD:
                            axisX = 0
                        else:
                            axisX = 255
                    elif key.char == 'd':
                        doKeyControlD = False
                        PTKeyChange = True
                        if not doKeyControlA:
                            axisX = 0
                        else:
                            axisX = -255
                    elif key.char == 'w':
                        doKeyControlW = False
                        PTKeyChange = True
                        if not doKeyControlS:
                            axisY = 0
                        else:
                            axisY = -255
                    elif key.char == 's':
                        doKeyControlS = False
                        PTKeyChange = True
                        if not doKeyControlW:
                            axisY = 0
                        else:
                            axisY = 255
                    elif key.char == ',':
                        doKeyControlSL = False
                        SlKeyChange = True
                        if not doKeyControlSR:
                            axisZ = 0
                        else:
                            axisZ = 255
                    elif key.char == '.':
                        doKeyControlSR = False
                        SlKeyChange = True
                        if not doKeyControlSL:
                            axisZ = 0
                        else:
                            axisZ = -255
            except:
                return
            
            if (not doKeyControlA and not doKeyControlD and not doKeyControlW and not doKeyControlS):
                panKeyPressed = False

            if (doKeyControlSL and not doKeyControlSR):
                sliderKeyPressed = False
    '''

    def on_stop(self):
        if self.serial_port:
            self.read_thread = None


    def on_touch_up(self, obj, obj_prop):
        global mousePTClick
        global mouseSlClick
        global panKeyPressed
        global sliderKeyPressed
        global axisX
        global axisY
        global axisZ
        global xDivSet
        global yDivSet

        if mousePTClick and not panKeyPressed:
            mousePTClick = False
            self.root.ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.ids.PTJoyDotPress.pos = ((xDivSet*18), (yDivSet*49))
        if mouseSlClick and not sliderKeyPressed:
            mouseSlClick = False
            self.root.ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.ids.SlJoyDotPress.pos = ((xDivSet*18), (yDivSet*27))

        if cam1isZooming:
            self.sendCam1ZoomStop()
        if cam2isZooming:
            self.sendCam2ZoomStop()
        if cam3isZooming:
            self.sendCam3ZoomStop()

        axisX = 0
        axisY = 0
        axisZ = 0

        self.doJoyMoves(1)

    def mouse_pos(self, window, pos):
        global abs_coord_x
        global abs_coord_y
        global abs_coords
        global mousePTClick
        global mouseSlClick
        global axisX
        global axisY
        global axisZ
        global xDivSet
        global yDivSet

        abs_coord_x = pos[0]
        abs_coord_y = pos[1]
        abs_coords = (abs_coord_x, abs_coord_y)

        if mousePTClick:
            PTXMin = (xDivSet*4)
            PTXMax = (xDivSet*36)
            PTYMin = (yDivSet*35)
            PTYMax = (yDivSet*67)

            if abs_coord_x < PTXMin: #29:
                abs_coord_x = PTXMin #29
            elif abs_coord_x > PTXMax: #352:
                abs_coord_x = PTXMax #352

            if abs_coord_y > PTYMax: #674:
                abs_coord_y = PTYMax #674
            elif abs_coord_y < PTYMin: #351:
                abs_coord_y = PTYMin #351
            
            self.root.ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))

            axisX = int(self.scale((abs_coord_x), (PTXMin, PTXMax), (-255,255)))
            axisY = int(self.scale((abs_coord_y), (PTYMin, PTYMax), (-255,255)))
            self.doJoyMoves(1)

        if mouseSlClick:
            SlXMin = (xDivSet*4)
            SlXMax = (xDivSet*36)
            SlY = (yDivSet*27)

            if abs_coord_x < SlXMin: #29:
                abs_coord_x = SlXMin #29
            elif abs_coord_x > SlXMax: #352:
                abs_coord_x = SlXMax #352

            self.root.ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)

            axisZ = int(self.scale((abs_coord_x), (SlXMin, SlXMax), (-255,255)))
            self.doJoyMoves(1)

    def PTJoyDotPressed(self):
        global abs_coord_x
        global abs_coord_y
        global mousePTClick
        mousePTClick = True

    def SlJoyDotPressed(self):
        global abs_coord_x
        global abs_coord_y
        global mouseSlClick
        mouseSlClick = True

    def doJoyMoves(self, dt):
        global axisX
        global axisY
        global axisZ
        global oldAxisX
        global oldAxisY
        global oldAxisZ
        global arr
        global currentMillisMoveCheck
        global previousMillisMoveCheck
        global previousTime

        if (axisX == oldAxisX) and (axisY == oldAxisY) and (axisZ == oldAxisZ) and ((abs(axisX) + abs(axisY) + abs(axisZ)) != 0):
            currentMillisMoveCheck = time.time()
            if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval):
                previousMillisMoveCheck = currentMillisMoveCheck
                #arr = [4, axisZh, axisXh, axisYh]                                          # for debugging
                self.sendJoystick(arr)
        elif ((axisX != oldAxisX) or (axisY != oldAxisY) or (axisZ != oldAxisZ)): # or doKeyControlA or doKeyControlD or doKeyControlW or doKeyControlS or doKeyControlSL or doKeyControlSR) and ((time.time() - previousTime) > 0.03) :
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

    def sendJoystick(self, arr):
        global data
        global whichCamSerial
        global whichCamOSC
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        
        sliderInt = int(arr[1], 16)
        panInt = int(arr[2], 16)
        tiltInt = int(arr[3], 16)

        data[0] = 4
        
        if ((sliderInt > 0) and (sliderInt < 256)):
            data[1] = 0
            data[2] = sliderInt
        elif sliderInt > 257:
            data[1] = 255
            data[2] = (sliderInt-65281)
        else:
            data[1] = 0
            data[2] = 0

        if ((panInt > 0) and (panInt < 256)):
            data[3] = 0
            data[4] = panInt
        elif panInt > 257:
            data[3] = 255
            data[4] = (panInt-65281)
        else:
            data[3] = 0
            data[4] = 0

        if ((tiltInt > 0) and (tiltInt < 256)):
            data[5] = 0
            data[6] = tiltInt
        elif tiltInt > 257:
            data[5] = 255
            data[6] = (tiltInt-65281)
        else:
            data[5] = 0
            data[6] = 0

        if whichCamOSC > 3:
            data[7] = whichCamOSC - 3
        else:
            data[7] = whichCamSerial
        
        if not self.serial_port:
            pass
        else:
            self.serial_port.write(data)
            #print(data)                                    # for debugging

        if whichCamSerial == 1:
            cam1AtPos1 = False
            cam1AtPos2 = False
            cam1AtPos3 = False
            cam1AtPos4 = False
            cam1AtPos5 = False
            cam1AtPos6 = False
        elif whichCamSerial == 2:
            cam2AtPos1 = False
            cam2AtPos2 = False
            cam2AtPos3 = False
            cam2AtPos4 = False
            cam2AtPos5 = False
            cam2AtPos6 = False
        elif whichCamSerial == 3:
            cam3AtPos1 = False
            cam3AtPos2 = False
            cam3AtPos3 = False
            cam3AtPos4 = False
            cam3AtPos5 = False
            cam3AtPos6 = False

        self.doButtonColours()

    def OSC_on_press(self, cam, key):
        global moveType
        global data
        global whichCamSerial
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global previousMillisMoveCheck
        global whichCamOSC
        global axisX
        global axisY
        global axisZ

        oldAxisX = 0
        oldAxisY = 0
        oldAxisZ = 0

        if moveType == 1:
            if key == 'a':
                self.joyL1OSC(cam)
            if key == 'd':
                self.joyR1OSC(cam)
            if key == 'w':
                self.joyU1OSC(cam)
            if key == 's':
                self.joyD1OSC(cam)
            if key == ',':
                self.joySL10OSC(cam)
            if key == '.':
                self.joySR10OSC(cam)
        elif moveType == 2:
            if key == 'a':
                self.joyL10OSC(cam)
            if key == 'd':
                self.joyR10OSC(cam)
            if key == 'w':
                self.joyU10OSC(cam)
            if key == 's':
                self.joyD10OSC(cam)
            if key == ',':
                self.joySL100OSC(cam)
            if key == '.':
                self.joySR100OSC(cam)
        elif moveType == 3:
            if key == 'a':
                axisX = -255
            elif key == 'A':
                axisX = 0
            if key == 'd':
                axisX = 255
            elif key == 'D':
                axisX = 0
            if key == 'w':
                axisY = 255
            elif key == 'W':
                axisY = 0
            if key == 's':
                axisY = -255
            elif key == 'S':
                axisY = 0
            if key == ',':
                axisZ = -255
            elif key == '<':
                axisZ = 0
            if key == '.':
                axisZ = 255
            elif key == '>':
                axisZ = 0

            if (axisX != oldAxisX) or (axisY != oldAxisY) or (axisZ != oldAxisZ):
                oldAxisX = axisX
                oldAxisY = axisY
                oldAxisZ = axisZ

                whichCamOSC = cam + 3

                self.doJoyMoves(1)

            self.doButtonColours()

    def scale(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    def toHex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def setPos(self, state):
        global SetPosToggle
        global xDivSet
        global yDivSet
        
        if (SetPosToggle and state == 3) or state == 0:
            SetPosToggle = False
            client.send_message("/setPos", 0)
            client.send_message("/press/bank/4/8", 0)
            client.send_message("/press/bank/5/8", 0)
            client.send_message("/press/bank/6/8", 0)
            client.send_message("/style/bgcolor/4/8", [0, 0, 0])
            client.send_message("/style/bgcolor/5/8", [0, 0, 0])
            client.send_message("/style/bgcolor/6/8", [0, 0, 0])
            self.root.ids.setPos.background_color = get_color_from_hex("#666666")
        elif (not SetPosToggle and state == 3) or state == 1:
            SetPosToggle = True
            client.send_message("/setPos", 1)
            client.send_message("/press/bank/4/8", 1)
            client.send_message("/press/bank/5/8", 1)
            client.send_message("/press/bank/6/8", 1)
            client.send_message("/style/bgcolor/4/8", [255, 0, 0])
            client.send_message("/style/bgcolor/5/8", [255, 0, 0])
            client.send_message("/style/bgcolor/6/8", [255, 0, 0])
            self.root.ids.setPos.background_color = get_color_from_hex("#7D0000")

    def sendCam1RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&.')

    def sendCam2RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&l')

    def sendCam3RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&o')

    def sendCam1RecordToggleOSC(self):
        self.sendSerial('&.')

    def sendCam2RecordToggleOSC(self):
        self.sendSerial('&l')

    def sendCam3RecordToggleOSC(self):
        self.sendSerial('&o')

    def on_btn_scan_release(self):
        global btn_scan_show
        global xDivSet
        global yDivSet
        global longestSerial

        if not btn_scan_show:
            btn_scan_show = True
            
            self.uiDict['box_list'].clear_widgets()
            self.device_name_list = []

            if platform == 'android':
                usb_device_list = usb.get_usb_device_list()
                self.device_name_list = [
                    device.getDeviceName() for device in usb_device_list
                ]
            else:
                usb_device_list = list_ports.comports()
                self.device_name_list = [port.device for port in usb_device_list]

            usb_port = 'usbmodem'
            usb_port2 = 'usb/00'
            
            if (usb_port in '\t'.join(self.device_name_list)):
                try:
                    serialPortSelect = [string for string in self.device_name_list if usb_port in string]
                    self.autoSerial(serialPortSelect, 1)
                except:
                    pass
            elif (usb_port2 in '\t'.join(self.device_name_list)):
                try:
                    serialPortSelect = [string for string in self.device_name_list if usb_port2 in string]
                    self.autoSerial(serialPortSelect, 1)
                except:
                    pass
            else:
                for device_name in self.device_name_list:
                    btnText = device_name
                    if len(btnText) > longestSerial:
                        longestSerial = len(btnText)
                    button = Button(text=btnText, size_hint_y=None, height='60dp')
                    button.bind(on_release=self.on_btn_device_release)
                    self.uiDict['box_list'].add_widget(button)
                self.root.ids.scanDD.pos = (((xDivSet*120)-(xDivSet*(longestSerial/2))), ((yDivSet*65) - ((yDivSet*7.4) * len(usb_device_list))))
                if platform == "win32" or platform == "Windows" or platform == "win":
                    self.root.ids.box_list.size = (((xDivSet*(longestSerial*1.4))), 0)
                else:
                    self.root.ids.box_list.size = (((xDivSet*(longestSerial*0.8))), 0)
        else:
            btn_scan_show = False
            self.uiDict['box_list'].clear_widgets()


    def on_btn_help_release(self):
        global btn_help_show

        if not btn_help_show:
            btn_help_show = True

            self.root.ids.helpLabel.visible =  True
            self.root.ids.helpCanvas.visible =  True
        elif btn_help_show:
            btn_help_show = False

            self.root.ids.helpLabel.visible =  False
            self.root.ids.helpCanvas.visible =  False

    def autoSerial(self, serialPortSelect, dt):
        global btn_scan_show
        global USBrequsted
        global device
        global device_name
        global serialLoop

        btn_scan_show = False
        device_name = serialPortSelect[0]
        self.root.ids.txtInput_read.text += ("Connecting to: " + device_name + "\n")
        self.root.ids.scroll_view.scroll_y = 0
        
        if platform == 'android':
            device = usb.get_usb_device(device_name)
            if USBrequsted:
                previousTicks = time.time() + 5
                if usb.has_usb_permission(device):
                    self.root.ids.txtInput_read.text += "USB permissions received.\n"
                    self.root.ids.scroll_view.scroll_y = 0
                    USBrequsted = False
                else:
                    self.root.ids.txtInput_read.text += "USB permissions declined.\n"
                    self.root.ids.scroll_view.scroll_y = 0
                    USBrequsted = False
            else:
                if not device:
                    self.root.ids.txtInput_read.text += "Serial connection failed.\n(No devices found)\n"
                    self.root.ids.scroll_view.scroll_y = 0
                    return
                if not usb.has_usb_permission(device):
                    self.root.ids.txtInput_read.text += "Requesting USB permissions.\n"
                    self.root.ids.scroll_view.scroll_y = 0
                    usb.request_usb_permission(device)
                    USBrequsted = True
                    Clock.schedule_once(self.doConnect, 1)
                    return
            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return
        else:
            try:
                self.serial_port = Serial(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n"
                self.root.ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return
            
        if self.serial_port.is_open and not self.read_thread:
            self.read_thread = threading.Thread(target = self.read_msg_thread)
            serialLoop = True
            self.read_thread.start()
            self.root.ids.txtInput_read.text += "Serial connection made 1.\n"
            self.root.ids.scroll_view.scroll_y = 0
            self.whichCamSerial1()
            self.sendSerial('&!')
        else :
            self.root.ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n"
            self.root.ids.scroll_view.scroll_y = 0
            self.serial_port.close()
        return

    def doConnect(self, dt):
        global device
        global USBrequsted
        global device_name
        global serialLoop
        
        if platform == 'android':
            previousTicks = time.time() + 5
            while not usb.has_usb_permission(device) or (previousTicks <= time.time()):
                c = 1
            
            if usb.has_usb_permission(device):
                self.root.ids.txtInput_read.text += "USB permissions received.\n"
                self.root.ids.scroll_view.scroll_y = 0
                USBrequsted = False
            else:
                self.root.ids.txtInput_read.text += "USB permissions declined.\n"
                self.root.ids.scroll_view.scroll_y = 0
                USBrequsted = False

            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return

            if self.read_thread:
                self.read_thread.kill()
            if self.serial_port.is_open and not self.read_thread:
                self.read_thread = threading.Thread(target = self.read_msg_thread)
                serialLoop = True
                self.read_thread.start()
                self.root.ids.txtInput_read.text += "Serial connection made 2.\n"
                self.root.ids.scroll_view.scroll_y = 0
                self.whichCamSerial1()
                self.sendSerial('&!')
            else :
                self.root.ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n" + str(self.read_thread)
                self.root.ids.scroll_view.scroll_y = 0
                self.serial_port.close()
            return
        
    def on_btn_device_release(self, btn):
        global serialLoop

        device_name = btn.text
        self.root.ids.txtInput_read.text += ("Connecting to: " + device_name + "\n")
        self.root.ids.scroll_view.scroll_y = 0
        
        self.uiDict['box_list'].clear_widgets()

        if platform == 'android':
            device = usb.get_usb_device(device_name)
            if not device:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n(No devices found)\n"
                self.root.ids.scroll_view.scroll_y = 0
                return
            if not usb.has_usb_permission(device):
                self.root.ids.txtInput_read.text += "Requesting USB permissions.\n"
                self.root.ids.scroll_view.scroll_y = 0
                usb.request_usb_permission(device)

                try:
                    self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
                except:
                    if usb.has_usb_permission(device):
                        self.root.ids.txtInput_read.text += "USB permissions active.\nConnect again.\n"
                        self.root.ids.scroll_view.scroll_y = 0
                    else:
                        self.root.ids.txtInput_read.text += "USB permissinos not set.\nTry again\n"
                        self.root.ids.scroll_view.scroll_y = 0
                        return

            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.ids.scroll_view.scroll_y = 0
                return
        else:
            try:
                self.serial_port = Serial(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.ids.txtInput_read.text += "Serial connection failed.\n"
                self.root.ids.scroll_view.scroll_y = 0
                return

        if self.serial_port.is_open and not self.read_thread:
            self.read_thread = threading.Thread(target = self.read_msg_thread)
            serialLoop = True
            self.read_thread.start()
            self.root.ids.txtInput_read.text += "Serial connection made 3.\n"
            self.root.ids.scroll_view.scroll_y = 0
            self.whichCamSerial1()
            self.sendSerial('&!')
        else :
            self.root.ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n"
            self.root.ids.scroll_view.scroll_y = 0
    
    def btnReport(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&(1')
        elif whichCamSerial == 2:
            self.sendSerial('&(2')
        elif whichCamSerial == 3:
            self.sendSerial('&(3')
            
    def btnReportPos(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&)1')
        elif whichCamSerial == 2:
            self.sendSerial('&)2')
        elif whichCamSerial == 3:
            self.sendSerial('&)3')

    def btnReportKey(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&-1')
        elif whichCamSerial == 2:
            self.sendSerial('&-2')
        elif whichCamSerial == 3:
            self.sendSerial('&-3')
    
    def read_msg_thread(self):
        global msg
        global serialLoop

        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3isRecording
        global cam3isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed

        while serialLoop:
            global whileLoopRun
            if whileLoopRun == False:
                serialLoop = False
            try:
                if not self.serial_port.is_open:
                    serialLoop = False
                received_msg = self.serial_port.readline(self.serial_port.in_waiting)
                if received_msg:
                    msg = bytes(received_msg).decode('utf8')
                    self.readSerial(msg)
            except:
                self.on_stop()
                self.root.ids.txtInput_read.text += "[color=#FFFFFF]Serial Port disconnected.\n[/color]"
                self.root.ids.scroll_view.scroll_y = 0
                cam1PTSpeed = 1
                cam2PTSpeed = 1
                cam3PTSpeed = 1
                cam1SliderSpeed = 1
                cam1SliderSpeed = 1
                cam1SliderSpeed = 1


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

                self.doButtonColours()

                serialLoop = False
                
    @mainthread
    def readSerial(self, msg):
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam3isRecording
        global cam3isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour

        global whichCamRead

        global xDivSet
        global yDivSet

        #print(msg)
        textLength = len(self.root.ids.txtInput_read.text)
        if textLength > 8000:
            self.root.ids.txtInput_read.text = self.root.ids.txtInput_read.text[1000:textLength]

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
            elif msg[1:4] == "112":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos1Run = True
            elif msg[1:4] == "122":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos2Run = True
            elif msg[1:4] == "132":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos3Run = True
            elif msg[1:4] == "142":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos4Run = True
            elif msg[1:4] == "152":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos5Run = True
            elif msg[1:4] == "162":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
                cam1Pos6Run = True
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
            elif msg[1:4] == "114":
                cam1isRecording = False
                self.root.ids.cam1Record.background_color = get_color_from_hex("#666666")
                self.root.ids.cam1Record.text = "Record"
                client.send_message("/style/bgcolor/4/16", [50, 50, 50])
            elif msg[1:4] == "124":
                cam1isRecording = True
                self.root.ids.cam1Record.background_color = get_color_from_hex("#7D0000")
                self.root.ids.cam1Record.text = "Recording"
                client.send_message("/style/bgcolor/4/16", [225, 0, 0])
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
            elif msg[1:4] == "212":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos1Run = True
            elif msg[1:4] == "222":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos2Run = True
            elif msg[1:4] == "232":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos3Run = True
            elif msg[1:4] == "242":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos4Run = True
            elif msg[1:4] == "252":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos5Run = True
            elif msg[1:4] == "262":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
                cam2Pos6Run = True
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
            elif msg[1:4] == "214":
                cam2isRecording = False
                self.root.ids.cam2Record.background_color = get_color_from_hex("#666666")
                self.root.ids.cam2Record.text = "Record"
                client.send_message("/style/bgcolor/5/16", [50, 50, 50])
            elif msg[1:4] == "224":
                cam2isRecording = True
                self.root.ids.cam2Record.background_color = get_color_from_hex("#7D0000")
                self.root.ids.cam2Record.text = "Recording"
                client.send_message("/style/bgcolor/5/16", [225, 0, 0])
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
            elif msg[1:4] == "312":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos1Run = True
            elif msg[1:4] == "322":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos2Run = True
            elif msg[1:4] == "332":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos3Run = True
            elif msg[1:4] == "342":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos4Run = True
            elif msg[1:4] == "352":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos5Run = True
            elif msg[1:4] == "362":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
                cam3Pos6Run = True
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
            elif msg[1:4] == "314":
                cam3isRecording = False
                self.root.ids.cam3Record.background_color = get_color_from_hex("#666666")
                self.root.ids.cam3Record.text = "Record"
                client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "324":
                cam3isRecording = True
                self.root.ids.cam3Record.background_color = get_color_from_hex("#7D0000")
                self.root.ids.cam3Record.text = "Recording"
                client.send_message("/style/bgcolor/6/16", [225, 0, 0])
            elif msg[1] == "?":
                cam1AtPos1 = False
                cam1AtPos2 = False
                cam1AtPos3 = False
                cam1AtPos4 = False
                cam1AtPos5 = False
                cam1AtPos6 = False
            elif msg[1] == "!":
                cam2AtPos1 = False
                cam2AtPos2 = False
                cam2AtPos3 = False
                cam2AtPos4 = False
                cam2AtPos5 = False
                cam2AtPos6 = False
            elif msg[1] == "@":
                cam3AtPos1 = False
                cam3AtPos2 = False
                cam3AtPos3 = False
                cam3AtPos4 = False
                cam3AtPos5 = False
                cam3AtPos6 = False
        elif msg[0:2] == "=1":
            cam1SliderSpeed = int(msg[2])
        elif msg[0:2] == "=2":
            cam2SliderSpeed = int(msg[2])
        elif msg[0:2] == "=3":
            cam3SliderSpeed = int(msg[2])
        elif msg[0:3] == "=@1":
            cam1PTSpeed = int(msg[3])
        elif msg[0:3] == "=@2":
            cam2PTSpeed = int(msg[3])
        elif msg[0:3] == "=@3":
            cam3PTSpeed = int(msg[3])
        elif msg[0:2] == "#$":
            return
        elif msg[0:4] == "Cam1":
            whichCamRead = 1
            self.root.ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
            self.root.ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam2":
            whichCamRead = 2
            self.root.ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
            self.root.ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam3":
            whichCamRead = 3
            self.root.ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
            self.root.ids.scroll_view.scroll_y = 0
        else:
            if whichCamRead == 1:
                self.root.ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
                self.root.ids.scroll_view.scroll_y = 0
            elif whichCamRead == 2:
                self.root.ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
                self.root.ids.scroll_view.scroll_y = 0
            elif whichCamRead == 3:
                self.root.ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
                self.root.ids.scroll_view.scroll_y = 0
            else:
                self.root.ids.txtInput_read.text += ("[color=ffffff]") + msg + ("[/color]")
                self.root.ids.scroll_view.scroll_y = 0
        msg = ''

        self.doButtonColours()

        

    def resetButtonColours(self):
        global resetButtons
        resetButtons = True

        self.doButtonColours()

    def doButtonColours(self):
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam1Pos1Set
        global cam1Pos2Set
        global cam1Pos3Set
        global cam1Pos4Set
        global cam1Pos5Set
        global cam1Pos6Set
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global OLDcam1AtPos1
        global OLDcam1AtPos2
        global OLDcam1AtPos3
        global OLDcam1AtPos4
        global OLDcam1AtPos5
        global OLDcam1AtPos6
        global OLDcam1Pos1Set
        global OLDcam1Pos2Set
        global OLDcam1Pos3Set
        global OLDcam1Pos4Set
        global OLDcam1Pos5Set
        global OLDcam1Pos6Set
        global OLDcam1Pos1Run
        global OLDcam1Pos2Run
        global OLDcam1Pos3Run
        global OLDcam1Pos4Run
        global OLDcam1Pos5Run
        global OLDcam1Pos6Run
        global cam1isRecording
        global cam1isZooming

        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam2Pos1Set
        global cam2Pos2Set
        global cam2Pos3Set
        global cam2Pos4Set
        global cam2Pos5Set
        global cam2Pos6Set
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global OLDcam2AtPos1
        global OLDcam2AtPos2
        global OLDcam2AtPos3
        global OLDcam2AtPos4
        global OLDcam2AtPos5
        global OLDcam2AtPos6
        global OLDcam2Pos1Set
        global OLDcam2Pos2Set
        global OLDcam2Pos3Set
        global OLDcam2Pos4Set
        global OLDcam2Pos5Set
        global OLDcam2Pos6Set
        global OLDcam2Pos1Run
        global OLDcam2Pos2Run
        global OLDcam2Pos3Run
        global OLDcam2Pos4Run
        global OLDcam2Pos5Run
        global OLDcam2Pos6Run
        global cam2isRecording
        global cam2isZooming

        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        global cam3Pos1Set
        global cam3Pos2Set
        global cam3Pos3Set
        global cam3Pos4Set
        global cam3Pos5Set
        global cam3Pos6Set
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run

        global OLDcam3AtPos1
        global OLDcam3AtPos2
        global OLDcam3AtPos3
        global OLDcam3AtPos4
        global OLDcam3AtPos5
        global OLDcam3AtPos6
        global OLDcam3Pos1Set
        global OLDcam3Pos2Set
        global OLDcam3Pos3Set
        global OLDcam3Pos4Set
        global OLDcam3Pos5Set
        global OLDcam3Pos6Set
        global OLDcam3Pos1Run
        global OLDcam3Pos2Run
        global OLDcam3Pos3Run
        global OLDcam3Pos4Run
        global OLDcam3Pos5Run
        global OLDcam3Pos6Run
        global cam3isRecording
        global cam3isZooming

        global cam1SliderSpeed
        global cam2SliderSpeed
        global cam3SliderSpeed
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed

        global moveType
        global moveTypeOld
        global resetButtons

        if (moveType == 1) and ((moveTypeOld != moveType) or resetButtons):
            moveTypeOld = moveType
            client.send_message("/style/bgcolor/4/12", [0, 200, 0])
            client.send_message("/style/bgcolor/5/12", [0, 200, 0])
            client.send_message("/style/bgcolor/6/12", [0, 200, 0])
            client.send_message("/style/bgcolor/4/20", [0, 50, 0])
            client.send_message("/style/bgcolor/5/20", [0, 50, 0])
            client.send_message("/style/bgcolor/6/20", [0, 50, 0])
            client.send_message("/style/bgcolor/4/28", [0, 50, 0])
            client.send_message("/style/bgcolor/5/28", [0, 50, 0])
            client.send_message("/style/bgcolor/6/28", [0, 50, 0])
        elif (moveType == 2) and ((moveTypeOld != moveType) or resetButtons):
            moveTypeOld = moveType
            client.send_message("/style/bgcolor/4/12", [0, 50, 0])
            client.send_message("/style/bgcolor/5/12", [0, 50, 0])
            client.send_message("/style/bgcolor/6/12", [0, 50, 0])
            client.send_message("/style/bgcolor/4/20", [0, 200, 0])
            client.send_message("/style/bgcolor/5/20", [0, 200, 0])
            client.send_message("/style/bgcolor/6/20", [0, 200, 0])
            client.send_message("/style/bgcolor/4/28", [0, 50, 0])
            client.send_message("/style/bgcolor/5/28", [0, 50, 0])
            client.send_message("/style/bgcolor/6/28", [0, 50, 0])
        elif (moveType == 3) and ((moveTypeOld != moveType) or resetButtons):
            moveTypeOld = moveType
            client.send_message("/style/bgcolor/4/12", [0, 50, 0])
            client.send_message("/style/bgcolor/5/12", [0, 50, 0])
            client.send_message("/style/bgcolor/6/12", [0, 50, 0])
            client.send_message("/style/bgcolor/4/20", [0, 50, 0])
            client.send_message("/style/bgcolor/5/20", [0, 50, 0])
            client.send_message("/style/bgcolor/6/20", [0, 50, 0])
            client.send_message("/style/bgcolor/4/28", [0, 200, 0])
            client.send_message("/style/bgcolor/5/28", [0, 200, 0])
            client.send_message("/style/bgcolor/6/28", [0, 200, 0])

        if cam1Pos1Set != OLDcam1Pos1Set or cam1Pos1Run != OLDcam1Pos1Run or cam1AtPos1 != OLDcam1AtPos1 or resetButtons:
            OLDcam1Pos1Set = cam1Pos1Set
            OLDcam1Pos1Run = cam1Pos1Run
            OLDcam1AtPos1 = cam1AtPos1
            if cam1Pos1Set and not cam1Pos1Run and not cam1AtPos1:                                  # Set , not Run or At
                self.root.ids.btnCam1Go1.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/1", [18, 70, 19])
                client.send_message("/style/color/3/1", [255, 0, 0])
                client.send_message("/style/bgcolor/4/1", [18, 70, 19])
                client.send_message("/style/color/4/1", [255, 0, 0])
            elif cam1Pos1Set and not cam1Pos1Run and cam1AtPos1:                                    # Set & At, not Run
                self.root.ids.btnCam1Go1.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/1", [48, 186, 49])
                client.send_message("/style/color/3/1", [255, 255, 255])
                client.send_message("/style/bgcolor/4/1", [48, 186, 49])
                client.send_message("/style/color/4/1", [255, 255, 255])
            elif not cam1Pos1Set:
                self.root.ids.btnCam1Go1.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/1", [18, 70, 19])
                client.send_message("/style/color/3/1", [0, 0, 0])
                client.send_message("/style/bgcolor/4/1", [18, 70, 19])
                client.send_message("/style/color/4/1", [0, 0, 0])

        if cam1Pos2Set != OLDcam1Pos2Set or cam1Pos2Run != OLDcam1Pos2Run or cam1AtPos2 != OLDcam1AtPos2 or resetButtons:
            OLDcam1Pos2Set = cam1Pos2Set
            OLDcam1Pos2Run = cam1Pos2Run
            OLDcam1AtPos2 = cam1AtPos2
            if cam1Pos2Set and not cam1Pos2Run and not cam1AtPos2:                                  # Position LEDs Cam1
                self.root.ids.btnCam1Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/2", [18, 70, 19])
                client.send_message("/style/color/3/2", [255, 0, 0])
                client.send_message("/style/bgcolor/4/2", [18, 70, 19])
                client.send_message("/style/color/4/2", [255, 0, 0])
            elif cam1Pos2Set and not cam1Pos2Run and cam1AtPos2:
                self.root.ids.btnCam1Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/2", [48, 186, 49])
                client.send_message("/style/color/3/2", [255, 255, 255])
                client.send_message("/style/bgcolor/4/2", [48, 186, 49])
                client.send_message("/style/color/4/2", [255, 255, 255])
            elif not cam1Pos2Set:
                self.root.ids.btnCam1Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/2", [18, 70, 19])
                client.send_message("/style/color/3/2", [0, 0, 0])
                client.send_message("/style/bgcolor/4/2", [18, 70, 19])
                client.send_message("/style/color/4/2", [0, 0, 0])

        if cam1Pos3Set != OLDcam1Pos3Set or cam1Pos3Run != OLDcam1Pos3Run or cam1AtPos3 != OLDcam1AtPos3 or resetButtons:
            OLDcam1Pos3Set = cam1Pos3Set
            OLDcam1Pos3Run = cam1Pos3Run
            OLDcam1AtPos3 = cam1AtPos3
            if cam1Pos3Set and not cam1Pos3Run and not cam1AtPos3:                                  # Position LEDs Cam1
                self.root.ids.btnCam1Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/3", [18, 70, 19])
                client.send_message("/style/color/3/3", [255, 0, 0])
                client.send_message("/style/bgcolor/4/3", [18, 70, 19])
                client.send_message("/style/color/4/3", [255, 0, 0])
            elif cam1Pos3Set and not cam1Pos3Run and cam1AtPos3:
                self.root.ids.btnCam1Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/3", [48, 186, 49])
                client.send_message("/style/color/3/3", [255, 255, 255])
                client.send_message("/style/bgcolor/4/3", [48, 186, 49])
                client.send_message("/style/color/4/3", [255, 255, 255])
            elif not cam1Pos3Set:
                self.root.ids.btnCam1Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/3", [18, 70, 19])
                client.send_message("/style/color/3/3", [0, 0, 0])
                client.send_message("/style/bgcolor/4/3", [18, 70, 19])
                client.send_message("/style/color/4/3", [0, 0, 0])

        if cam1Pos4Set != OLDcam1Pos4Set or cam1Pos4Run != OLDcam1Pos4Run or cam1AtPos4 != OLDcam1AtPos4 or resetButtons:
            OLDcam1Pos4Set = cam1Pos4Set
            OLDcam1Pos4Run = cam1Pos4Run
            OLDcam1AtPos4 = cam1AtPos4
            if cam1Pos4Set and not cam1Pos4Run and not cam1AtPos4:                                  # Position LEDs Cam1
                self.root.ids.btnCam1Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/4", [18, 70, 19])
                client.send_message("/style/color/3/4", [255, 0, 0])
                client.send_message("/style/bgcolor/4/4", [18, 70, 19])
                client.send_message("/style/color/4/4", [255, 0, 0])
            elif cam1Pos4Set and not cam1Pos4Run and cam1AtPos4:
                self.root.ids.btnCam1Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/4", [48, 186, 49])
                client.send_message("/style/color/3/4", [255, 255, 255])
                client.send_message("/style/bgcolor/4/4", [48, 186, 49])
                client.send_message("/style/color/4/4", [255, 255, 255])
            elif not cam1Pos4Set:
                self.root.ids.btnCam1Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/4", [18, 70, 19])
                client.send_message("/style/color/3/4", [0, 0, 0])
                client.send_message("/style/bgcolor/4/4", [18, 70, 19])
                client.send_message("/style/color/4/4", [0, 0, 0])

        if cam1Pos5Set != OLDcam1Pos5Set or cam1Pos5Run != OLDcam1Pos5Run or cam1AtPos5 != OLDcam1AtPos5 or resetButtons:
            OLDcam1Pos5Set = cam1Pos5Set
            OLDcam1Pos5Run = cam1Pos5Run
            OLDcam1AtPos5 = cam1AtPos5
            if cam1Pos5Set and not cam1Pos5Run and not cam1AtPos5:                                  # Position LEDs Cam1
                self.root.ids.btnCam1Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/5", [18, 70, 19])
                client.send_message("/style/color/3/5", [255, 0, 0])
                client.send_message("/style/bgcolor/4/5", [18, 70, 19])
                client.send_message("/style/color/4/5", [255, 0, 0])
            elif cam1Pos5Set and not cam1Pos5Run and cam1AtPos5:
                self.root.ids.btnCam1Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/5", [48, 186, 49])
                client.send_message("/style/color/3/5", [255, 255, 255])
                client.send_message("/style/bgcolor/4/5", [48, 186, 49])
                client.send_message("/style/color/4/5", [255, 255, 255])
            elif not cam1Pos5Set:
                self.root.ids.btnCam1Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/5", [18, 70, 19])
                client.send_message("/style/color/3/5", [0, 0, 0])
                client.send_message("/style/bgcolor/4/5", [18, 70, 19])
                client.send_message("/style/color/4/5", [0, 0, 0])

        if cam1Pos6Set != OLDcam1Pos6Set or cam1Pos6Run != OLDcam1Pos6Run or cam1AtPos6 != OLDcam1AtPos6 or resetButtons:
            OLDcam1Pos6Set = cam1Pos6Set
            OLDcam1Pos6Run = cam1Pos6Run
            OLDcam1AtPos6 = cam1AtPos6
            if cam1Pos6Set and not cam1Pos6Run and not cam1AtPos6:                                  # Position LEDs Cam1
                self.root.ids.btnCam1Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/6", [18, 70, 19])
                client.send_message("/style/color/3/6", [255, 0, 0])
                client.send_message("/style/bgcolor/4/6", [18, 70, 19])
                client.send_message("/style/color/4/6", [255, 0, 0])
            elif cam1Pos6Set and not cam1Pos6Run and cam1AtPos6:
                self.root.ids.btnCam1Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/6", [48, 186, 49])
                client.send_message("/style/color/3/6", [255, 255, 255])
                client.send_message("/style/bgcolor/4/6", [48, 186, 49])
                client.send_message("/style/color/4/6", [255, 255, 255])
            elif not cam1Pos6Set:
                self.root.ids.btnCam1Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/6", [18, 70, 19])
                client.send_message("/style/color/3/6", [0, 0, 0])
                client.send_message("/style/bgcolor/4/6", [18, 70, 19])
                client.send_message("/style/color/4/6", [0, 0, 0])


        if cam2Pos1Set != OLDcam2Pos1Set or cam2Pos1Run != OLDcam2Pos1Run or cam2AtPos1 != OLDcam2AtPos1 or resetButtons:
            OLDcam2Pos1Set = cam2Pos1Set
            OLDcam2Pos1Run = cam2Pos1Run
            OLDcam2AtPos1 = cam2AtPos1
            if cam2Pos1Set and not cam2Pos1Run and not cam2AtPos1:                                  # Set , not Run or At
                self.root.ids.btnCam2Go1.col=(1, 0, 0, 1)
                #client.send_message("/Cam2Go1", [1, "00AAAAFF"])
                client.send_message("/style/bgcolor/3/9", [35, 50, 70])
                client.send_message("/style/color/3/9", [255, 0, 0])
                client.send_message("/style/bgcolor/5/1", [35, 50, 70])
                client.send_message("/style/color/5/1", [255, 0, 0])
            elif cam2Pos1Set and not cam2Pos1Run and cam2AtPos1:                                    # Set & At, not Run
                self.root.ids.btnCam2Go1.col=(0, 1, 0, 1)
                #client.send_message("/Cam2Go1", [1, "FFFF00FF"])
                client.send_message("/style/bgcolor/3/9", [92, 133, 186])
                client.send_message("/style/color/3/9", [255, 255, 255])
                client.send_message("/style/bgcolor/5/1", [92, 133, 186])
                client.send_message("/style/color/5/1", [255, 255, 255])
            elif not cam2Pos1Set:
                self.root.ids.btnCam2Go1.col=(.13, .13, .13, 1)
                #client.send_message("/Cam2Go1", [0, "FFFF00FF"])
                client.send_message("/style/bgcolor/3/9", [35, 50, 70])
                client.send_message("/style/color/3/9", [0, 0, 0])
                client.send_message("/style/bgcolor/5/1", [35, 50, 70])
                client.send_message("/style/color/5/1", [0, 0, 0])

        if cam2Pos2Set != OLDcam2Pos2Set or cam2Pos2Run != OLDcam2Pos2Run or cam2AtPos2 != OLDcam2AtPos2 or resetButtons:
            OLDcam2Pos2Set = cam2Pos2Set
            OLDcam2Pos2Run = cam2Pos2Run
            OLDcam2AtPos2 = cam2AtPos2
            if cam2Pos2Set and not cam2Pos2Run and not cam2AtPos2:                                  # Position LEDs Cam2
                self.root.ids.btnCam2Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/10", [35, 50, 70])
                client.send_message("/style/color/3/10", [255, 0, 0])
                client.send_message("/style/bgcolor/5/2", [35, 50, 70])
                client.send_message("/style/color/5/2", [255, 0, 0])
            elif cam2Pos2Set and not cam2Pos2Run and cam2AtPos2:
                self.root.ids.btnCam2Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/10", [92, 133, 186])
                client.send_message("/style/color/3/10", [255, 255, 255])
                client.send_message("/style/bgcolor/5/2", [92, 133, 186])
                client.send_message("/style/color/5/2", [255, 255, 255])
            elif not cam2Pos2Set:
                self.root.ids.btnCam2Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/10", [35, 50, 70])
                client.send_message("/style/color/3/10", [0, 0, 0])
                client.send_message("/style/bgcolor/5/2", [35, 50, 70])
                client.send_message("/style/color/5/2", [0, 0, 0])

        if cam2Pos3Set != OLDcam2Pos3Set or cam2Pos3Run != OLDcam2Pos3Run or cam2AtPos3 != OLDcam2AtPos3 or resetButtons:
            OLDcam2Pos3Set = cam2Pos3Set
            OLDcam2Pos3Run = cam2Pos3Run
            OLDcam2AtPos3 = cam2AtPos3
            if cam2Pos3Set and not cam2Pos3Run and not cam2AtPos3:                                  # Position LEDs Cam2
                self.root.ids.btnCam2Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/11", [35, 50, 70])
                client.send_message("/style/color/3/11", [255, 0, 0])
                client.send_message("/style/bgcolor/5/3", [35, 50, 70])
                client.send_message("/style/color/5/3", [255, 0, 0])
            elif cam2Pos3Set and not cam2Pos3Run and cam2AtPos3:
                self.root.ids.btnCam2Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/11", [92, 133, 186])
                client.send_message("/style/color/3/11", [255, 255, 255])
                client.send_message("/style/bgcolor/5/3", [92, 133, 186])
                client.send_message("/style/color/5/3", [255, 255, 255])
            elif not cam2Pos3Set:
                self.root.ids.btnCam2Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/11", [35, 50, 70])
                client.send_message("/style/color/3/11", [0, 0, 0])
                client.send_message("/style/bgcolor/5/3", [35, 50, 70])
                client.send_message("/style/color/5/3", [0, 0, 0])

        if cam2Pos4Set != OLDcam2Pos4Set or cam2Pos4Run != OLDcam2Pos4Run or cam2AtPos4 != OLDcam2AtPos4 or resetButtons:
            OLDcam2Pos4Set = cam2Pos4Set
            OLDcam2Pos4Run = cam2Pos4Run
            OLDcam2AtPos4 = cam2AtPos4
            if cam2Pos4Set and not cam2Pos4Run and not cam2AtPos4:                                  # Position LEDs Cam2
                self.root.ids.btnCam2Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/12", [35, 50, 70])
                client.send_message("/style/color/3/12", [255, 0, 0])
                client.send_message("/style/bgcolor/5/4", [35, 50, 70])
                client.send_message("/style/color/5/4", [255, 0, 0])
            elif cam2Pos4Set and not cam2Pos4Run and cam2AtPos4:
                self.root.ids.btnCam2Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/12", [92, 133, 186])
                client.send_message("/style/color/3/12", [255, 255, 255])
                client.send_message("/style/bgcolor/5/4", [92, 133, 186])
                client.send_message("/style/color/5/4", [255, 255, 255])
            elif not cam2Pos4Set:
                self.root.ids.btnCam2Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/12", [35, 50, 70])
                client.send_message("/style/color/3/12", [0, 0, 0])
                client.send_message("/style/bgcolor/5/4", [35, 50, 70])
                client.send_message("/style/color/5/4", [0, 0, 0])

        if cam2Pos5Set != OLDcam2Pos5Set or cam2Pos5Run != OLDcam2Pos5Run or cam2AtPos5 != OLDcam2AtPos5 or resetButtons:
            OLDcam2Pos5Set = cam2Pos5Set
            OLDcam2Pos5Run = cam2Pos5Run
            OLDcam2AtPos5 = cam2AtPos5
            if cam2Pos5Set and not cam2Pos5Run and not cam2AtPos5:                                  # Position LEDs Cam2
                self.root.ids.btnCam2Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/13", [35, 50, 70])
                client.send_message("/style/color/3/13", [255, 0, 0])
                client.send_message("/style/bgcolor/5/5", [35, 50, 70])
                client.send_message("/style/color/5/5", [255, 0, 0])
            elif cam2Pos5Set and not cam2Pos5Run and cam2AtPos5:
                self.root.ids.btnCam2Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/13", [92, 133, 186])
                client.send_message("/style/color/3/13", [255, 255, 255])
                client.send_message("/style/bgcolor/5/5", [92, 133, 186])
                client.send_message("/style/color/5/5", [255, 255, 255])
            elif not cam2Pos5Set:
                self.root.ids.btnCam2Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/13", [35, 50, 70])
                client.send_message("/style/color/3/13", [0, 0, 0])
                client.send_message("/style/bgcolor/5/5", [35, 50, 70])
                client.send_message("/style/color/5/5", [0, 0, 0])

        if cam2Pos6Set != OLDcam2Pos6Set or cam2Pos6Run != OLDcam2Pos6Run or cam2AtPos6 != OLDcam2AtPos6 or resetButtons:
            OLDcam2Pos6Set = cam2Pos6Set
            OLDcam2Pos6Run = cam2Pos6Run
            OLDcam2AtPos6 = cam2AtPos6
            if cam2Pos6Set and not cam2Pos6Run and not cam2AtPos6:                                  # Position LEDs Cam2
                self.root.ids.btnCam2Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/14", [35, 50, 70])
                client.send_message("/style/color/3/14", [255, 0, 0])
                client.send_message("/style/bgcolor/5/6", [35, 50, 70])
                client.send_message("/style/color/5/6", [255, 0, 0])
            elif cam2Pos6Set and not cam2Pos6Run and cam2AtPos6:
                self.root.ids.btnCam2Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/14", [92, 133, 186])
                client.send_message("/style/color/3/14", [255, 255, 255])
                client.send_message("/style/bgcolor/5/6", [92, 133, 186])
                client.send_message("/style/color/5/6", [255, 255, 255])
            elif not cam2Pos6Set:
                self.root.ids.btnCam2Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/14", [35, 50, 70])
                client.send_message("/style/color/3/14", [0, 0, 0])
                client.send_message("/style/bgcolor/5/6", [35, 50, 70])
                client.send_message("/style/color/5/6", [0, 0, 0])



        if cam3Pos1Set != OLDcam3Pos1Set or cam3Pos1Run != OLDcam3Pos1Run or cam3AtPos1 != OLDcam3AtPos1 or resetButtons:
            OLDcam3Pos1Set = cam3Pos1Set
            OLDcam3Pos1Run = cam3Pos1Run
            OLDcam3AtPos1 = cam3AtPos1
            if cam3Pos1Set and not cam3Pos1Run and not cam3AtPos1:                                  # Set , not Run or At
                self.root.ids.btnCam3Go1.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/17", [70, 62, 1])
                client.send_message("/style/color/3/17", [255, 0, 0])
                client.send_message("/style/bgcolor/6/1", [70, 62, 1])
                client.send_message("/style/color/6/1", [255, 0, 0])
            elif cam3Pos1Set and not cam3Pos1Run and cam3AtPos1:                                    # Set & At, not Run
                self.root.ids.btnCam3Go1.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/17", [186, 164, 1])
                client.send_message("/style/color/3/17", [255, 255, 255])
                client.send_message("/style/bgcolor/6/1", [186, 164, 1])
                client.send_message("/style/color/6/1", [255, 255, 255])
            elif not cam3Pos1Set:
                self.root.ids.btnCam3Go1.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/17", [70, 62, 1])
                client.send_message("/style/color/3/17", [0, 0, 0])
                client.send_message("/style/bgcolor/6/1", [70, 62, 1])
                client.send_message("/style/color/6/1", [0, 0, 0])

        if cam3Pos2Set != OLDcam3Pos2Set or cam3Pos2Run != OLDcam3Pos2Run or cam3AtPos2 != OLDcam3AtPos2 or resetButtons:
            OLDcam3Pos2Set = cam3Pos2Set
            OLDcam3Pos2Run = cam3Pos2Run
            OLDcam3AtPos2 = cam3AtPos2
            if cam3Pos2Set and not cam3Pos2Run and not cam3AtPos2:                                  # Position LEDs Cam3
                self.root.ids.btnCam3Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/18", [70, 62, 1])
                client.send_message("/style/color/3/18", [255, 0, 0])
                client.send_message("/style/bgcolor/6/2", [70, 62, 1])
                client.send_message("/style/color/6/2", [255, 0, 0])
            elif cam3Pos2Set and not cam3Pos2Run and cam3AtPos2:
                self.root.ids.btnCam3Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/18", [186, 164, 1])
                client.send_message("/style/color/3/18", [255, 255, 255])
                client.send_message("/style/bgcolor/6/2", [186, 164, 1])
                client.send_message("/style/color/6/2", [255, 255, 255])
            elif not cam3Pos2Set:
                self.root.ids.btnCam3Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/18", [70, 62, 1])
                client.send_message("/style/color/3/18", [0, 0, 0])
                client.send_message("/style/bgcolor/6/2", [70, 62, 1])
                client.send_message("/style/color/6/2", [0, 0, 0])

        if cam3Pos3Set != OLDcam3Pos3Set or cam3Pos3Run != OLDcam3Pos3Run or cam3AtPos3 != OLDcam3AtPos3 or resetButtons:
            OLDcam3Pos3Set = cam3Pos3Set
            OLDcam3Pos3Run = cam3Pos3Run
            OLDcam3AtPos3 = cam3AtPos3
            if cam3Pos3Set and not cam3Pos3Run and not cam3AtPos3:                                  # Position LEDs Cam3
                self.root.ids.btnCam3Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/19", [70, 62, 1])
                client.send_message("/style/color/3/19", [255, 0, 0])
                client.send_message("/style/bgcolor/6/3", [70, 62, 1])
                client.send_message("/style/color/6/3", [255, 0, 0])
            elif cam3Pos3Set and not cam3Pos3Run and cam3AtPos3:
                self.root.ids.btnCam3Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/19", [186, 164, 1])
                client.send_message("/style/color/3/19", [255, 255, 255])
                client.send_message("/style/bgcolor/6/3", [186, 164, 1])
                client.send_message("/style/color/6/3", [255, 255, 255])
            elif not cam3Pos3Set:
                self.root.ids.btnCam3Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/19", [70, 62, 1])
                client.send_message("/style/color/3/19", [0, 0, 0])
                client.send_message("/style/bgcolor/6/3", [70, 62, 1])
                client.send_message("/style/color/6/3", [0, 0, 0])

        if cam3Pos4Set != OLDcam3Pos4Set or cam3Pos4Run != OLDcam3Pos4Run or cam3AtPos4 != OLDcam3AtPos4 or resetButtons:
            OLDcam3Pos4Set = cam3Pos4Set
            OLDcam3Pos4Run = cam3Pos4Run
            OLDcam3AtPos4 = cam3AtPos4
            if cam3Pos4Set and not cam3Pos4Run and not cam3AtPos4:                                  # Position LEDs Cam3
                self.root.ids.btnCam3Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/20", [70, 62, 1])
                client.send_message("/style/color/3/20", [255, 0, 0])
                client.send_message("/style/bgcolor/6/4", [70, 62, 1])
                client.send_message("/style/color/6/4", [255, 0, 0])
            elif cam3Pos4Set and not cam3Pos4Run and cam3AtPos4:
                self.root.ids.btnCam3Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/20", [186, 164, 1])
                client.send_message("/style/color/3/20", [255, 255, 255])
                client.send_message("/style/bgcolor/6/4", [186, 164, 1])
                client.send_message("/style/color/6/4", [255, 255, 255])
            elif not cam3Pos4Set:
                self.root.ids.btnCam3Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/20", [70, 62, 1])
                client.send_message("/style/color/3/20", [0, 0, 0])
                client.send_message("/style/bgcolor/6/4", [70, 62, 1])
                client.send_message("/style/color/6/4", [0, 0, 0])

        if cam3Pos5Set != OLDcam3Pos5Set or cam3Pos5Run != OLDcam3Pos5Run or cam3AtPos5 != OLDcam3AtPos5 or resetButtons:
            OLDcam3Pos5Set = cam3Pos5Set
            OLDcam3Pos5Run = cam3Pos5Run
            OLDcam3AtPos5 = cam3AtPos5
            if cam3Pos5Set and not cam3Pos5Run and not cam3AtPos5:                                  # Position LEDs Cam3
                self.root.ids.btnCam3Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/21", [70, 62, 1])
                client.send_message("/style/color/3/21", [255, 0, 0])
                client.send_message("/style/bgcolor/6/5", [70, 62, 1])
                client.send_message("/style/color/6/5", [255, 0, 0])
            elif cam3Pos5Set and not cam3Pos5Run and cam3AtPos5:
                self.root.ids.btnCam3Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/21", [186, 164, 1])
                client.send_message("/style/color/3/21", [255, 255, 255])
                client.send_message("/style/bgcolor/6/5", [186, 164, 1])
                client.send_message("/style/color/6/5", [255, 255, 255])
            elif not cam3Pos5Set:
                self.root.ids.btnCam3Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/21", [70, 62, 1])
                client.send_message("/style/color/3/21", [0, 0, 0])
                client.send_message("/style/bgcolor/6/5", [70, 62, 1])
                client.send_message("/style/color/6/5", [0, 0, 0])

        if cam3Pos6Set != OLDcam3Pos6Set or cam3Pos6Run != OLDcam3Pos6Run or cam3AtPos6 != OLDcam3AtPos6 or resetButtons:
            OLDcam3Pos6Set = cam3Pos6Set
            OLDcam3Pos6Run = cam3Pos6Run
            OLDcam3AtPos6 = cam3AtPos6
            if cam3Pos6Set and not cam3Pos6Run and not cam3AtPos6:                                  # Position LEDs Cam3
                self.root.ids.btnCam3Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/22", [70, 62, 1])
                client.send_message("/style/color/3/22", [255, 0, 0])
                client.send_message("/style/bgcolor/6/6", [70, 62, 1])
                client.send_message("/style/color/6/6", [255, 0, 0])
            elif cam3Pos6Set and not cam3Pos6Run and cam3AtPos6:
                self.root.ids.btnCam3Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/22", [186, 164, 1])
                client.send_message("/style/color/3/22", [255, 255, 255])
                client.send_message("/style/bgcolor/6/6", [186, 164, 1])
                client.send_message("/style/color/6/6", [255, 255, 255])
            elif not cam3Pos6Set:
                self.root.ids.btnCam3Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/22", [70, 62, 1])
                client.send_message("/style/color/3/22", [0, 0, 0])
                client.send_message("/style/bgcolor/6/6", [70, 62, 1])
                client.send_message("/style/color/6/6", [0, 0, 0])

        if oldCam1PTSpeed != cam1PTSpeed:
            oldCam1PTSpeed = cam1PTSpeed
            client.send_message("/style/text/3/7", "-")
            if cam1PTSpeed == 1:
                self.root.ids.cam1PTSpd.sizPT1=((xDivSet*2.25), (yDivSet*6))
                client.send_message("/style/text/3/8", "+ 1/4")
                client.send_message("/style/text/4/10", "Spd 1/4")
            elif cam1PTSpeed == 3:
                self.root.ids.cam1PTSpd.sizPT1=((xDivSet*4.5), (yDivSet*6))
                client.send_message("/style/text/3/8", "+ 2/4")
                client.send_message("/style/text/4/10", "Spd 2/4")
            elif cam1PTSpeed == 5:
                self.root.ids.cam1PTSpd.sizPT1=((xDivSet*6.75), (yDivSet*6))
                client.send_message("/style/text/3/8", "+ 3/4")
                client.send_message("/style/text/4/10", "Spd 3/4")
            elif cam1PTSpeed == 7:
                self.root.ids.cam1PTSpd.sizPT1=((xDivSet*9), (yDivSet*6))
                client.send_message("/style/text/3/8", "+ 4/4")
                client.send_message("/style/text/4/10", "Spd 4/4")

        if oldCam2PTSpeed != cam2PTSpeed:
            oldCam2PTSpeed = cam2PTSpeed
            client.send_message("/style/text/3/15", "-")
            if cam2PTSpeed == 1:
                self.root.ids.cam2PTSpd.sizPT2=((xDivSet*2.25), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 1/4")
                client.send_message("/style/text/5/10", "Spd 1/4")
            elif cam2PTSpeed == 3:
                self.root.ids.cam2PTSpd.sizPT2=((xDivSet*4.5), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/5/10", "Spd 2/4")
            elif cam2PTSpeed == 5:
                self.root.ids.cam2PTSpd.sizPT2=((xDivSet*6.75), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/5/10", "Spd 3/4")
            elif cam2PTSpeed == 7:
                self.root.ids.cam2PTSpd.sizPT2=((xDivSet*9), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/5/10", "Spd 4/4")

        if oldCam3PTSpeed != cam3PTSpeed:
            oldCam3PTSpeed = cam3PTSpeed
            client.send_message("/style/text/3/23", "-")
            if cam3PTSpeed == 1:
                self.root.ids.cam3PTSpd.sizPT3=((xDivSet*2.25), (yDivSet*6))
                client.send_message("/style/text/3/24", "+ 1/4")
                client.send_message("/style/text/6/10", "Spd 1/4")
            elif cam3PTSpeed == 3:
                self.root.ids.cam3PTSpd.sizPT3=((xDivSet*4.5), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/6/10", "Spd 2/4")
            elif cam3PTSpeed == 5:
                self.root.ids.cam3PTSpd.sizPT3=((xDivSet*6.75), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/6/10", "Spd 3/4")
            elif cam3PTSpeed == 7:
                self.root.ids.cam3PTSpd.sizPT3=((xDivSet*9), (yDivSet*6))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/6/10", "Spd 4/4")

        if oldCam1Speed != cam1SliderSpeed:
            oldCam1Speed = cam1SliderSpeed
            if cam1SliderSpeed == 1:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*1.29), (yDivSet*6))
            elif cam1SliderSpeed == 2:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*2.57), (yDivSet*6))
            elif cam1SliderSpeed == 3:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*3.86), (yDivSet*6))
            elif cam1SliderSpeed == 4:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*5.14), (yDivSet*6))
            elif cam1SliderSpeed == 5:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*6.43), (yDivSet*6))
            elif cam1SliderSpeed == 6:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*7.71), (yDivSet*6))
            elif cam1SliderSpeed == 7:
                self.root.ids.cam1SlSpd.sizSl1=((xDivSet*9), (yDivSet*6))

        if oldCam2Speed != cam2SliderSpeed:
            oldCam2Speed = cam2SliderSpeed
            if cam2SliderSpeed == 1:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*1.29), (yDivSet*6))
            elif cam2SliderSpeed == 2:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*2.57), (yDivSet*6))
            elif cam2SliderSpeed == 3:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*3.86), (yDivSet*6))
            elif cam2SliderSpeed == 4:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*5.14), (yDivSet*6))
            elif cam2SliderSpeed == 5:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*6.43), (yDivSet*6))
            elif cam2SliderSpeed == 6:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*7.71), (yDivSet*6))
            elif cam2SliderSpeed == 7:
                self.root.ids.cam2SlSpd.sizSl2=((xDivSet*9), (yDivSet*6))

        if oldCam3Speed != cam3SliderSpeed:
            oldCam3Speed = cam3SliderSpeed
            if cam3SliderSpeed == 1:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*1.29), (yDivSet*6))
            elif cam3SliderSpeed == 2:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*2.57), (yDivSet*6))
            elif cam3SliderSpeed == 3:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*3.86), (yDivSet*6))
            elif cam3SliderSpeed == 4:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*5.14), (yDivSet*6))
            elif cam3SliderSpeed == 5:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*6.43), (yDivSet*6))
            elif cam3SliderSpeed == 6:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*7.71), (yDivSet*6))
            elif cam3SliderSpeed == 7:
                self.root.ids.cam3SlSpd.sizSl3=((xDivSet*9), (yDivSet*6))

        resetButtons = False

    def whichCamSerial1(self):
        global whichCamSerial
        whichCamSerial = 1
        self.root.ids.buttonWhichCam1.line_color=(1, 0, 0, 1)
        self.root.ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)

    def whichCamSerial2(self):
        global whichCamSerial
        whichCamSerial = 2
        self.root.ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)

    def whichCamSerial3(self):
        global whichCamSerial
        whichCamSerial = 3
        self.root.ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        
    def joyL10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??P-10')
        elif whichCamSerial == 2:
            self.sendSerial('!?P-10')
        elif whichCamSerial == 3:
            self.sendSerial('@?P-10')
    def joyL1(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??P-0.5')
        elif whichCamSerial == 2:
            self.sendSerial('!?P-0.5')
        elif whichCamSerial == 3:
            self.sendSerial('@?P-0.5')
    def joyR1(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??P0.5')
        elif whichCamSerial == 2:
            self.sendSerial('!?P0.5')
        elif whichCamSerial == 3:
            self.sendSerial('@?P0.5')
    def joyR10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??P10')
        elif whichCamSerial == 2:
            self.sendSerial('!?P10')
        elif whichCamSerial == 3:
            self.sendSerial('@?P10')

    def joyU10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??T10')
        elif whichCamSerial == 2:
            self.sendSerial('!?T10')
        elif whichCamSerial == 3:
            self.sendSerial('@?T10')
    def joyU1(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??T0.5')
        elif whichCamSerial == 2:
            self.sendSerial('!?T0.5')
        elif whichCamSerial == 3:
            self.sendSerial('@?T0.5')
    def joyD1(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??T-0.5')
        elif whichCamSerial == 2:
            self.sendSerial('!?T-0.5')
        elif whichCamSerial == 3:
            self.sendSerial('@?T-0.5')
    def joyD10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??T-10')
        elif whichCamSerial == 2:
            self.sendSerial('!?T-10')
        elif whichCamSerial == 3:
            self.sendSerial('@?T-10')

    def joySL100(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??X-100')
        elif whichCamSerial == 2:
            self.sendSerial('!?X-100')
        elif whichCamSerial == 3:
            self.sendSerial('@?X-100')
    def joySL10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??X-10')
        elif whichCamSerial == 2:
            self.sendSerial('!?X-10')
        elif whichCamSerial == 3:
            self.sendSerial('@?X-10')
    def joySR10(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??X10')
        elif whichCamSerial == 2:
            self.sendSerial('!?X10')
        elif whichCamSerial == 3:
            self.sendSerial('@?X10')
    def joySR100(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('??X100')
        elif whichCamSerial == 2:
            self.sendSerial('!?X100')
        elif whichCamSerial == 3:
            self.sendSerial('@?X100')





    def joyL10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??P-10')
        elif cam == 2:
            self.sendSerial('!?P-10')
        elif cam == 3:
            self.sendSerial('@?P-10')
    def joyL1OSC(self, cam):
        if cam == 1:
            self.sendSerial('??P-0.1')
        elif cam == 2:
            self.sendSerial('!?P-0.1')
        elif cam == 3:
            self.sendSerial('@?P-0.1')
    def joyR1OSC(self, cam):
        if cam == 1:
            self.sendSerial('??P0.1')
        elif cam == 2:
            self.sendSerial('!?P0.1')
        elif cam == 3:
            self.sendSerial('@?P0.1')
    def joyR10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??P10')
        elif cam == 2:
            self.sendSerial('!?P10')
        elif cam == 3:
            self.sendSerial('@?P10')

    def joyU10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??T10')
        elif cam == 2:
            self.sendSerial('!?T10')
        elif cam == 3:
            self.sendSerial('@?T10')
    def joyU1OSC(self, cam):
        if cam == 1:
            self.sendSerial('??T0.1')
        elif cam == 2:
            self.sendSerial('!?T0.1')
        elif cam == 3:
            self.sendSerial('@?T0.1')
    def joyD1OSC(self, cam):
        if cam == 1:
            self.sendSerial('??T-0.1')
        elif cam == 2:
            self.sendSerial('!?T-0.1')
        elif cam == 3:
            self.sendSerial('@?T-0.1')
    def joyD10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??T-10')
        elif cam == 2:
            self.sendSerial('!?T-10')
        elif cam == 3:
            self.sendSerial('@?T-10')

    def joySL100OSC(self, cam):
        if cam == 1:
            self.sendSerial('??X-100')
        elif cam == 2:
            self.sendSerial('!?X-100')
        elif cam == 3:
            self.sendSerial('@?X-100')
    def joySL10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??X-10')
        elif cam == 2:
            self.sendSerial('!?X-10')
        elif cam == 3:
            self.sendSerial('@?X-10')
    def joySR10OSC(self, cam):
        if cam == 1:
            self.sendSerial('??X10')
        elif cam == 2:
            self.sendSerial('!?X10')
        elif cam == 3:
            self.sendSerial('@?X10')
    def joySR100OSC(self, cam):
        if cam == 1:
            self.sendSerial('??X100')
        elif cam == 2:
            self.sendSerial('!?X100')
        elif cam == 3:
            self.sendSerial('@?X100')

    def Cam1Go1(self):
        global SetPosToggle
        global cam1Pos1Set
        global cam1AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&Z')
            return
        elif cam1Pos1Set and not cam1AtPos1:
            self.sendSerial('&z')

    def Cam1Go2(self):
        global SetPosToggle
        global cam1Pos2Set
        global cam1AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&X')
            return
        elif cam1Pos2Set and not cam1AtPos2:
            self.sendSerial('&x')

    def Cam1Go3(self):
        global SetPosToggle
        global cam1Pos3Set
        global cam1AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&C')
            return
        elif cam1Pos3Set and not cam1AtPos3:
            self.sendSerial('&c')

    def Cam1Go4(self):
        global SetPosToggle
        global cam1Pos4Set
        global cam1AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&V')
            return
        elif cam1Pos4Set and not cam1AtPos4:
            self.sendSerial('&v')

    def Cam1Go5(self):
        global SetPosToggle
        global cam1Pos5Set
        global cam1AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&B')
            return
        elif cam1Pos5Set and not cam1AtPos5:
            self.sendSerial('&b')

    def Cam1Go6(self):
        global SetPosToggle
        global cam1Pos6Set
        global cam1AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&N')
            return
        elif cam1Pos6Set and not cam1AtPos6:
            self.sendSerial('&n')




    def Cam2Go1(self):
        global SetPosToggle
        global cam2Pos1Set
        global cam2AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&A')
            return
        elif cam2Pos1Set and not cam2AtPos1:
            self.sendSerial('&a')

    def Cam2Go2(self):
        global SetPosToggle
        global cam2Pos2Set
        global cam2AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&S')
            return
        elif cam2Pos2Set and not cam2AtPos2:
            self.sendSerial('&s')

    def Cam2Go3(self):
        global SetPosToggle
        global cam2Pos3Set
        global cam2AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&D')
            return
        elif cam2Pos3Set and not cam2AtPos3:
            self.sendSerial('&d')

    def Cam2Go4(self):
        global SetPosToggle
        global cam2Pos4Set
        global cam2AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&F')
            return
        elif cam2Pos4Set and not cam2AtPos4:
            self.sendSerial('&f')

    def Cam2Go5(self):
        global SetPosToggle
        global cam2Pos5Set
        global cam2AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&G')
            return
        elif cam2Pos5Set and not cam2AtPos5:
            self.sendSerial('&g')

    def Cam2Go6(self):
        global SetPosToggle
        global cam2Pos6Set
        global cam2AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&H')
            return
        elif cam2Pos6Set and not cam2AtPos6:
            self.sendSerial('&h')




    def Cam3Go1(self):
        global SetPosToggle
        global cam3Pos1Set
        global cam3AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&Q')
            return
        elif cam3Pos1Set and not cam3AtPos1:
            self.sendSerial('&q')

    def Cam3Go2(self):
        global SetPosToggle
        global cam3Pos2Set
        global cam3AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&W')
            return
        elif cam3Pos2Set and not cam3AtPos2:
            self.sendSerial('&w')

    def Cam3Go3(self):
        global SetPosToggle
        global cam3Pos3Set
        global cam3AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&E')
            return
        elif cam3Pos3Set and not cam3AtPos3:
            self.sendSerial('&e')

    def Cam3Go4(self):
        global SetPosToggle
        global cam3Pos4Set
        global cam3AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&R')
            return
        elif cam3Pos4Set and not cam3AtPos4:
            self.sendSerial('&r')

    def Cam3Go5(self):
        global SetPosToggle
        global cam3Pos5Set
        global cam3AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&T')
            return
        elif cam3Pos5Set and not cam3AtPos5:
            self.sendSerial('&t')

    def Cam3Go6(self):
        global SetPosToggle
        global cam3Pos6Set
        global cam3AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&Y')
            return
        elif cam3Pos6Set and not cam3AtPos6:
            self.sendSerial('&y')



    def sendCam1PTSpeedInc(self):
        global cam1PTSpeed
        if cam1PTSpeed == 1:
            self.sendSerial('&+13')
        elif cam1PTSpeed == 3:
            self.sendSerial('&+12')
        elif cam1PTSpeed == 5:
            self.sendSerial('&+11')
        elif cam1PTSpeed == 7:
            return
        
    def sendCam1PTSpeedDec(self):
        global cam1PTSpeed
        if cam1PTSpeed == 7:
            self.sendSerial('&+12')
        elif cam1PTSpeed == 5:
            self.sendSerial('&+13')
        elif cam1PTSpeed == 3:
            self.sendSerial('&+14')
        elif cam1PTSpeed == 1:
            return



    def sendCam2PTSpeedInc(self):
        global cam2PTSpeed
        if cam2PTSpeed == 1:
            self.sendSerial('&+23')
        elif cam2PTSpeed == 3:
            self.sendSerial('&+22')
        elif cam2PTSpeed == 5:
            self.sendSerial('&+21')
        elif cam2PTSpeed == 7:
            return
        
    def sendCam2PTSpeedDec(self):
        global cam2PTSpeed
        if cam2PTSpeed == 7:
            self.sendSerial('&+22')
        elif cam2PTSpeed == 5:
            self.sendSerial('&+23')
        elif cam2PTSpeed == 3:
            self.sendSerial('&+24')
        elif cam2PTSpeed == 1:
            return



    def sendCam3PTSpeedInc(self):
        global cam3PTSpeed
        if cam3PTSpeed == 1:
            self.sendSerial('&+33')
        elif cam3PTSpeed == 3:
            self.sendSerial('&+32')
        elif cam3PTSpeed == 5:
            self.sendSerial('&+31')
        elif cam3PTSpeed == 7:
            return
        
    def sendCam3PTSpeedDec(self):
        global cam3PTSpeed
        if cam3PTSpeed == 7:
            self.sendSerial('&+32')
        elif cam3PTSpeed == 5:
            self.sendSerial('&+33')
        elif cam3PTSpeed == 3:
            self.sendSerial('&+34')
        elif cam3PTSpeed == 1:
            return


    



    def sendCam2PTSpeedOSC(self, OSC):
        #print(OSC)
        if OSC == 0:
            self.sendSerial('&+24')
        elif OSC == 1:
            self.sendSerial('&+23')
        elif OSC == 2:
            self.sendSerial('&+22')
        elif OSC == 3:
            self.sendSerial('&+21')




    def sendCam1SliderSpeedInc(self):
        self.sendSerial('&M')

    def sendCam1SliderSpeedDec(self):
        self.sendSerial('&m')

    def sendCam2SliderSpeedInc(self):
        self.sendSerial('&J')

    def sendCam2SliderSpeedDec(self):
        self.sendSerial('&j')

    def sendCam3SliderSpeedInc(self):
        self.sendSerial('&U')

    def sendCam3SliderSpeedDec(self):
        self.sendSerial('&u')

    def sendCam1ZoomIn(self):
        global cam1isZooming
        cam1isZooming = True
        self.sendSerial('&<')
    def sendCam1ZoomOut(self):
        global cam1isZooming
        cam1isZooming = True
        self.sendSerial('&,')
    def sendCam1ZoomStop(self):
        global cam1isZooming
        cam1isZooming = False
        self.sendSerial('&>')

    def sendCam2ZoomIn(self):
        global cam2isZooming
        cam2isZooming = True
        self.sendSerial('&K')
    def sendCam2ZoomOut(self):
        global cam2isZooming
        cam2isZooming = True
        self.sendSerial('&k')
    def sendCam2ZoomStop(self):
        global cam2isZooming
        cam2isZooming = False
        self.sendSerial('&L')

    def sendCam3ZoomIn(self):
        global cam3isZooming
        cam3isZooming = True
        self.sendSerial('&I')
    def sendCam3ZoomOut(self):
        global cam3isZooming
        cam3isZooming = True
        self.sendSerial('&i')
    def sendCam3ZoomStop(self):
        global cam3isZooming
        cam3isZooming = False
        self.sendSerial('&O')



    def sendClearCam1Pos(self):
        self.sendSerial('&%')

    def sendClearCam2Pos(self):
        self.sendSerial('&^')

    def sendClearCam3Pos(self):
        self.sendSerial('&&')


    def flash(self, dt):
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        if cam1Pos1Run and not cam1AtPos1:
            self.root.ids.btnCam1Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/1", [48, 186, 49])
            client.send_message("/style/color/3/1", [200, 200, 0])
            client.send_message("/style/bgcolor/4/1", [48, 186, 49])
            client.send_message("/style/color/4/1", [200, 200, 0])
        if cam1Pos2Run and not cam1AtPos2:
            self.root.ids.btnCam1Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/2", [48, 186, 49])
            client.send_message("/style/color/3/2", [200, 200, 0])
            client.send_message("/style/bgcolor/4/2", [48, 186, 49])
            client.send_message("/style/color/4/2", [200, 200, 0])
        if cam1Pos3Run and not cam1AtPos3:
            self.root.ids.btnCam1Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/3", [48, 186, 49])
            client.send_message("/style/color/3/3", [200, 200, 0])
            client.send_message("/style/bgcolor/4/3", [48, 186, 49])
            client.send_message("/style/color/4/3", [200, 200, 0])
        if cam1Pos4Run and not cam1AtPos4:
            self.root.ids.btnCam1Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/4", [48, 186, 49])
            client.send_message("/style/color/3/4", [200, 200, 0])
            client.send_message("/style/bgcolor/4/4", [48, 186, 49])
            client.send_message("/style/color/4/4", [200, 200, 0])
        if cam1Pos5Run and not cam1AtPos5:
            self.root.ids.btnCam1Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/5", [48, 186, 49])
            client.send_message("/style/color/3/5", [200, 200, 0])
            client.send_message("/style/bgcolor/4/5", [48, 186, 49])
            client.send_message("/style/color/4/5", [200, 200, 0])
        if cam1Pos6Run and not cam1AtPos6:
            self.root.ids.btnCam1Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/6", [48, 186, 49])
            client.send_message("/style/color/3/6", [200, 200, 0])
            client.send_message("/style/bgcolor/4/6", [48, 186, 49])
            client.send_message("/style/color/4/6", [200, 200, 0])

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.ids.btnCam2Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/9", [92, 133, 186])
            client.send_message("/style/color/3/9", [200, 200, 0])
            client.send_message("/style/bgcolor/5/1", [92, 133, 186])
            client.send_message("/style/color/5/1", [200, 200, 0])
            #client.send_message("/Cam1Go1", [1, "AAAA00FF"])
        if cam2Pos2Run and not cam2AtPos2:
            self.root.ids.btnCam2Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/10", [92, 133, 186])
            client.send_message("/style/color/3/10", [200, 200, 0])
            client.send_message("/style/bgcolor/5/2", [92, 133, 186])
            client.send_message("/style/color/5/2", [200, 200, 0])
        if cam2Pos3Run and not cam2AtPos3:
            self.root.ids.btnCam2Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/11", [92, 133, 186])
            client.send_message("/style/color/3/11", [200, 200, 0])
            client.send_message("/style/bgcolor/5/3", [92, 133, 186])
            client.send_message("/style/color/5/3", [200, 200, 0])
        if cam2Pos4Run and not cam2AtPos4:
            self.root.ids.btnCam2Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/12", [92, 133, 186])
            client.send_message("/style/color/3/12", [200, 200, 0])
            client.send_message("/style/bgcolor/5/4", [92, 133, 186])
            client.send_message("/style/color/5/4", [200, 200, 0])
        if cam2Pos5Run and not cam2AtPos5:
            self.root.ids.btnCam2Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/13", [92, 133, 186])
            client.send_message("/style/color/3/13", [200, 200, 0])
            client.send_message("/style/bgcolor/5/5", [92, 133, 186])
            client.send_message("/style/color/5/5", [200, 200, 0])
        if cam2Pos6Run and not cam2AtPos6:
            self.root.ids.btnCam2Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/6", [92, 133, 186])
            client.send_message("/style/color/5/6", [200, 200, 0])

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.ids.btnCam3Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/17", [186, 164, 1])
            client.send_message("/style/color/3/17", [200, 200, 0])
            client.send_message("/style/bgcolor/6/1", [186, 164, 1])
            client.send_message("/style/color/6/1", [200, 200, 0])
        if cam3Pos2Run and not cam3AtPos2:
            self.root.ids.btnCam3Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/18", [186, 164, 1])
            client.send_message("/style/color/3/18", [200, 200, 0])
            client.send_message("/style/bgcolor/6/2", [186, 164, 1])
            client.send_message("/style/color/6/2", [200, 200, 0])
        if cam3Pos3Run and not cam3AtPos3:
            self.root.ids.btnCam3Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/19", [186, 164, 1])
            client.send_message("/style/color/3/19", [200, 200, 0])
            client.send_message("/style/bgcolor/6/3", [186, 164, 1])
            client.send_message("/style/color/6/3", [200, 200, 0])
        if cam3Pos4Run and not cam3AtPos4:
            self.root.ids.btnCam3Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/20", [186, 164, 1])
            client.send_message("/style/color/3/20", [200, 200, 0])
            client.send_message("/style/bgcolor/6/4", [186, 164, 1])
            client.send_message("/style/color/6/4", [200, 200, 0])
        if cam3Pos5Run and not cam3AtPos5:
            self.root.ids.btnCam3Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/5", [186, 164, 1])
            client.send_message("/style/color/6/5", [200, 200, 0])
        if cam3Pos6Run and not cam3AtPos6:
            self.root.ids.btnCam3Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/22", [186, 164, 1])
            client.send_message("/style/color/3/22", [200, 200, 0])
            client.send_message("/style/bgcolor/6/6", [186, 164, 1])
            client.send_message("/style/color/6/6", [200, 200, 0])

        Clock.schedule_once(self.setNormal, 0.5)

    def setNormal(self, dt):
        global cam1Pos1Run
        global cam1Pos2Run
        global cam1Pos3Run
        global cam1Pos4Run
        global cam1Pos5Run
        global cam1Pos6Run
        global cam2Pos1Run
        global cam2Pos2Run
        global cam2Pos3Run
        global cam2Pos4Run
        global cam2Pos5Run
        global cam2Pos6Run
        global cam3Pos1Run
        global cam3Pos2Run
        global cam3Pos3Run
        global cam3Pos4Run
        global cam3Pos5Run
        global cam3Pos6Run
        global cam1AtPos1
        global cam1AtPos2
        global cam1AtPos3
        global cam1AtPos4
        global cam1AtPos5
        global cam1AtPos6
        global cam2AtPos1
        global cam2AtPos2
        global cam2AtPos3
        global cam2AtPos4
        global cam2AtPos5
        global cam2AtPos6
        global cam3AtPos1
        global cam3AtPos2
        global cam3AtPos3
        global cam3AtPos4
        global cam3AtPos5
        global cam3AtPos6
        
        if cam1Pos1Run and not cam1AtPos1:
            self.root.ids.btnCam1Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/1", [18, 70, 19])
            client.send_message("/style/color/3/1", [50, 50, 0])
            client.send_message("/style/bgcolor/4/1", [18, 70, 19])
            client.send_message("/style/color/4/1", [50, 50, 0])
        if cam1Pos2Run and not cam1AtPos2:
            self.root.ids.btnCam1Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/2", [18, 70, 19])
            client.send_message("/style/color/3/2", [50, 50, 0])
            client.send_message("/style/bgcolor/4/2", [18, 70, 19])
            client.send_message("/style/color/4/2", [50, 50, 0])
        if cam1Pos3Run and not cam1AtPos3:
            self.root.ids.btnCam1Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/3", [18, 70, 19])
            client.send_message("/style/color/3/3", [50, 50, 0])
            client.send_message("/style/bgcolor/4/3", [18, 70, 19])
            client.send_message("/style/color/4/3", [50, 50, 0])
        if cam1Pos4Run and not cam1AtPos4:
            self.root.ids.btnCam1Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/4", [18, 70, 19])
            client.send_message("/style/color/3/4", [50, 50, 0])
            client.send_message("/style/bgcolor/4/4", [18, 70, 19])
            client.send_message("/style/color/4/4", [50, 50, 0])
        if cam1Pos5Run and not cam1AtPos5:
            self.root.ids.btnCam1Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/5", [18, 70, 19])
            client.send_message("/style/color/3/5", [50, 50, 0])
            client.send_message("/style/bgcolor/4/5", [18, 70, 19])
            client.send_message("/style/color/4/5", [50, 50, 0])
        if cam1Pos6Run and not cam1AtPos6:
            self.root.ids.btnCam1Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/6", [18, 70, 19])
            client.send_message("/style/color/3/6", [50, 50, 0])
            client.send_message("/style/bgcolor/4/6", [18, 70, 19])
            client.send_message("/style/color/4/6", [50, 50, 0])

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.ids.btnCam2Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/9", [35, 50, 70])
            client.send_message("/style/color/3/9", [50, 50, 0])
            client.send_message("/style/bgcolor/5/1", [35, 50, 70])
            client.send_message("/style/color/5/1", [50, 50, 0])
            #client.send_message("/Cam1Go1", [1, "000000FF"])
        if cam2Pos2Run and not cam2AtPos2:
            self.root.ids.btnCam2Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/10", [35, 50, 70])
            client.send_message("/style/color/3/10", [50, 50, 0])
            client.send_message("/style/bgcolor/5/2", [35, 50, 70])
            client.send_message("/style/color/5/2", [50, 50, 0])
        if cam2Pos3Run and not cam2AtPos3:
            self.root.ids.btnCam2Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/11", [35, 50, 70])
            client.send_message("/style/color/3/11", [50, 50, 0])
            client.send_message("/style/bgcolor/5/3", [35, 50, 70])
            client.send_message("/style/color/5/3", [50, 50, 0])
        if cam2Pos4Run and not cam2AtPos4:
            self.root.ids.btnCam2Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/12", [35, 50, 70])
            client.send_message("/style/color/3/12", [50, 50, 0])
            client.send_message("/style/bgcolor/5/4", [35, 50, 70])
            client.send_message("/style/color/5/4", [50, 50, 0])
        if cam2Pos5Run and not cam2AtPos5:
            self.root.ids.btnCam2Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/13", [35, 50, 70])
            client.send_message("/style/color/3/13", [50, 50, 0])
            client.send_message("/style/bgcolor/5/5", [35, 50, 70])
            client.send_message("/style/color/5/5", [50, 50, 0])
        if cam2Pos6Run and not cam2AtPos6:
            self.root.ids.btnCam2Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/6", [35, 50, 70])
            client.send_message("/style/color/5/6", [50, 50, 0])

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.ids.btnCam3Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/17", [70, 62, 1])
            client.send_message("/style/color/3/17", [50, 50, 0])
            client.send_message("/style/bgcolor/6/1", [70, 62, 1])
            client.send_message("/style/color/6/1", [50, 50, 0])
        if cam3Pos2Run and not cam3AtPos2:
            self.root.ids.btnCam3Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/18", [70, 62, 1])
            client.send_message("/style/color/3/18", [50, 50, 0])
            client.send_message("/style/bgcolor/6/2", [70, 62, 1])
            client.send_message("/style/color/6/2", [50, 50, 0])
        if cam3Pos3Run and not cam3AtPos3:
            self.root.ids.btnCam3Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/19", [70, 62, 1])
            client.send_message("/style/color/3/19", [50, 50, 0])
            client.send_message("/style/bgcolor/6/3", [70, 62, 1])
            client.send_message("/style/color/6/3", [50, 50, 0])
        if cam3Pos4Run and not cam3AtPos4:
            self.root.ids.btnCam3Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/4", [70, 62, 1])
            client.send_message("/style/color/6/4", [50, 50, 0])
        if cam3Pos5Run and not cam3AtPos5:
            self.root.ids.btnCam3Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/21", [70, 62, 1])
            client.send_message("/style/color/3/21", [50, 50, 0])
            client.send_message("/style/bgcolor/6/5", [70, 62, 1])
            client.send_message("/style/color/6/5", [50, 50, 0])
        if cam3Pos6Run and not cam3AtPos6:
            self.root.ids.btnCam3Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/22", [70, 62, 1])
            client.send_message("/style/color/3/22", [50, 50, 0])
            client.send_message("/style/bgcolor/6/6", [70, 62, 1])
            client.send_message("/style/color/6/6", [50, 50, 0])

    
    def sendSerial(self, sendData):
        if self.serial_port and self.serial_port.is_open:
            if sys.version_info < (3, 0):
                data = bytes(sendData + '\n')
            else:
                data = bytes((sendData + '\n'), 'utf8')
            try:
                self.serial_port.write(data)
                #print(data)
            except:
                self.on_stop()
                self.root.ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                textLength = len(self.root.ids.txtInput_read.text)
                if textLength > 8000:
                    self.root.ids.txtInput_read.text = self.root.ids.txtInput_read.text[1000:textLength]
                self.root.ids.scroll_view.scroll_y = 0
        else:
            self.root.ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.ids.txtInput_read.text)
            if textLength > 8000:
                self.root.ids.txtInput_read.text = self.root.ids.txtInput_read.text[1000:textLength]
            self.root.ids.scroll_view.scroll_y = 0


if __name__ == '__main__':
    KivyPTS().run()