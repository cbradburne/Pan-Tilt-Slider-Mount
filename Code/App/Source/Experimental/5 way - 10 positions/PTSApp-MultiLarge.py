#macOS
#Kivy
#python3 -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
#
#KivyMD
#git clone https://github.com/kivymd/KivyMD.git --depth 1
#cd KivyMD
#/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 -m pip install --upgrade pip
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
#pyinstaller --additional-hooks-dir=. --onefile --windowed --icon PTSApp-Icon.icns --osx-bundle-identifier 'com.bradders' --name PTSApp-Multi PTSApp-Multi.py
#
#Windows
#pyinstaller --onefile --windowed --icon="PTSApp-Icon.ico" PTSApp-Multi.py

import asyncio
import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.utils import platform
from kivy.core.window import Window
from kivy.config import Config
from functools import partial
from kivy.properties import StringProperty

if platform == 'android':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
else:
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'window_state', 'windowed')
    #Config.set('graphics', 'width', '1900')         #test
    #Config.set('graphics', 'height', '1000')        #test
    Config.set('graphics', 'width', '1400')         # A7 Lite
    Config.set('graphics', 'height', '800')         # A7 Lite
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

oldCam1Speed = 9
oldCam2Speed = 9
oldCam3Speed = 9
oldCam4Speed = 9
oldCam5Speed = 9

cam1PTSpeed = 0
cam2PTSpeed = 0
cam3PTSpeed = 0
cam4PTSpeed = 0
cam5PTSpeed = 0

oldCam1PTSpeed = 9
oldCam2PTSpeed = 9
oldCam3PTSpeed = 9
oldCam4PTSpeed = 9
oldCam5PTSpeed = 9

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
cam4isZooming = False
cam4isRecording = False
cam5isZooming = False
cam5isRecording = False

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
serialConnection = False

joystick = ''
joystickName = ''

moveType = 3
moveTypeOld = 0
resetButtons = False

msg = ''

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass
class ThirdWindow(Screen):
    pass
class FourthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass



if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports
    from serial import Serial

#MDScreen:
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import NoTransition kivy.uix.screenmanager.NoTransition

WindowManager:
    transition: NoTransition()
    MainWindow:
    SecondWindow:
    ThirdWindow:
    FourthWindow:

<MainWindow>:
    name: 'main'
    MDScreen:
        id: main
        md_bg_color: get_color_from_hex("#21282D")

        canvas:
            Color:
                rgba: get_color_from_hex("#444444")             # Grey

            #Speed Border
            #Dividers
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*59.5)
                size: (app.xDiv*132), (app.yDiv*1)

            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*47.5)
                size: (app.xDiv*132), (app.yDiv*1)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*35.5)
                size: (app.xDiv*132), (app.yDiv*1)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*23.5)
                size: (app.xDiv*132), (app.yDiv*1)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*11.5)
                size: (app.xDiv*132), (app.yDiv*1)

            

            #Zoom
            Rectangle:
                pos: (app.xDiv*106), (app.yDiv*56)
                size: (app.xDiv*3), (app.yDiv*3)
            
            Rectangle:
                pos: (app.xDiv*106), (app.yDiv*44)
                size: (app.xDiv*3), (app.yDiv*3)
            
            Rectangle:
                pos: (app.xDiv*106), (app.yDiv*32)
                size: (app.xDiv*3), (app.yDiv*3)
            
            Rectangle:
                pos: (app.xDiv*106), (app.yDiv*20)
                size: (app.xDiv*3), (app.yDiv*3)
            
            Rectangle:
                pos: (app.xDiv*106), (app.yDiv*8)
                size: (app.xDiv*3), (app.yDiv*3)

            #Background Colour
            Color:
                rgba: (0.1, 0.1, 0.1, 1)                        # Dark Grey BG

            #PT
            Rectangle:
                pos: (app.xDiv*7), (app.yDiv*56)
                size: (app.xDiv*33), (app.yDiv*3)

            Rectangle:
                pos: (app.xDiv*7), (app.yDiv*44)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*7), (app.yDiv*32)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*7), (app.yDiv*20)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*7), (app.yDiv*8)
                size: (app.xDiv*33), (app.yDiv*3)

            #Slider
            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*56)
                size: (app.xDiv*33), (app.yDiv*3)

            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*44)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*32)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*20)
                size: (app.xDiv*33), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*55), (app.yDiv*8)
                size: (app.xDiv*33), (app.yDiv*3)


        FloatLayout:
            id: cam1PTSpd
            sizPT1: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle:
                    pos: (app.xDiv*7), (app.yDiv*56)
                    size: self.sizPT1

        FloatLayout:
            id: cam2PTSpd
            sizPT2: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*7), (app.yDiv*44)
                    size: self.sizPT2

        FloatLayout:
            id: cam3PTSpd
            sizPT3: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*7), (app.yDiv*32)
                    size: self.sizPT3

        FloatLayout:
            id: cam4PTSpd
            sizPT4: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*7), (app.yDiv*20)
                    size: self.sizPT4

        FloatLayout:
            id: cam5PTSpd
            sizPT5: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*7), (app.yDiv*8)
                    size: self.sizPT5



        FloatLayout:
            id: cam1SlSpd
            sizSl1: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*55), (app.yDiv*56)
                    size: self.sizSl1

        FloatLayout:
            id: cam2SlSpd
            sizSl2: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*55), (app.yDiv*44)
                    size: self.sizSl2

        FloatLayout:
            id: cam3SlSpd
            sizSl3: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*55), (app.yDiv*32)
                    size: self.sizSl3

        FloatLayout:
            id: cam4SlSpd
            sizSl4: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*55), (app.yDiv*20)
                    size: self.sizSl4

        FloatLayout:
            id: cam5SlSpd
            sizSl5: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*55), (app.yDiv*8)
                    size: self.sizSl5





        ScrollView:
            # Serial Read
            id: scroll_view
            always_overscroll: False
            pos: (app.xDiv*150), (app.yDiv*25)
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

        





        Button:
            id: PTJoyDotPress
            pos: app.xScreen, app.yScreen
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            background_normal: ''
            background_down: ''
            background_color: get_color_from_hex("#7D0000")
            text: ''
            #on_press: app.PTJoyDotPressed()

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
            pos: app.xScreen, app.yScreen
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            background_normal: ''
            background_down: ''
            background_color: get_color_from_hex("#7D0000")
            text: ''
            #on_press: app.SlJoyDotPressed()

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
            pos: (app.xDiv*121), (app.yDiv*64)
            size: (app.xDiv*10), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            text:"Set Pos"
            background_normal: ''
            background_color: get_color_from_hex("#666666")
            on_press: app.setPos(3)


        Button:
            id: btnCam1Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*13), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*25), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*37), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*49), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*61), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
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
            id: btnCam1Go7
            text:"7"
            pos: (app.xDiv*73), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.Cam1Go7()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam1Go8
            text:"8"
            pos: (app.xDiv*85), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.Cam1Go8()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam1Go9
            text:"9"
            pos: (app.xDiv*97), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.Cam1Go9()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam1Go10
            text:"10"
            pos: (app.xDiv*109), (app.yDiv*49)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.Cam1Go10()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam1PT-
            text: "PT-"
            halign: 'center'
            pos: (app.xDiv*1), (app.yDiv*56)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1PTSpeedDec()

        Button:
            id: btnCam1PT+
            text: "PT+"
            halign: 'center'
            pos: (app.xDiv*40), (app.yDiv*56)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1PTSpeedInc()

        Button:
            id: btnCam1Sl-
            text: "Sl-"
            halign: 'center'
            pos: (app.xDiv*49), (app.yDiv*56)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1SliderSpeedDec()

        Button:
            id: btnCam1Sl+
            text: "Sl+"
            halign: 'center'
            pos: (app.xDiv*88), (app.yDiv*56)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1SliderSpeedInc()

        Button:
            id: btnCam1Zm-
            text:"Zm OUT"
            halign: 'center'
            pos: (app.xDiv*109), (app.yDiv*56)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1ZoomOut()
            on_release: app.sendCam1ZoomStop()

        Button:
            id: btnCam1Zm+
            text:"Zm IN"
            halign: 'center'
            pos: (app.xDiv*97), (app.yDiv*56)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam1ButColour)
            on_press: app.sendCam1ZoomIn()
            on_release: app.sendCam1ZoomStop()

        Button:
            id: btnCam1Clr
            text:"Clear"
            pos: (app.xDiv*123), (app.yDiv*51)
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
            pos: (app.xDiv*1), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*13), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*25), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*37), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*49), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*61), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
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
            id: btnCam2Go7
            text:"7"
            pos: (app.xDiv*73), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.Cam2Go7()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam2Go8
            text:"8"
            pos: (app.xDiv*85), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.Cam2Go8()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam2Go9
            text:"9"
            pos: (app.xDiv*97), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.Cam2Go9()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam2Go10
            text:"10"
            pos: (app.xDiv*109), (app.yDiv*37)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.Cam2Go10()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam2PT-
            text: "PT-"
            halign: 'center'
            pos: (app.xDiv*1), (app.yDiv*44)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2PTSpeedDec()

        Button:
            id: btnCam2PT+
            text: "PT+"
            halign: 'center'
            pos: (app.xDiv*40), (app.yDiv*44)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2PTSpeedInc()

        Button:
            id: btnCam2Sl-
            text: "Sl-"
            halign: 'center'
            pos: (app.xDiv*49), (app.yDiv*44)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2SliderSpeedDec()

        Button:
            id: btnCam2Sl+
            text: "Sl+"
            halign: 'center'
            pos: (app.xDiv*88), (app.yDiv*44)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2SliderSpeedInc()

        Button:
            id: btnCam2Zm-
            text:"Zm OUT"
            halign: 'center'
            pos: (app.xDiv*109), (app.yDiv*44)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2ZoomOut()
            on_release: app.sendCam2ZoomStop()

        Button:
            id: btnCam2Zm+
            text:"Zm IN"
            halign: 'center'
            pos: (app.xDiv*97), (app.yDiv*44)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam2ButColour)
            on_press: app.sendCam2ZoomIn()
            on_release: app.sendCam2ZoomStop()

        Button:
            id: btnCam2Clr
            text:"Clear"
            pos: (app.xDiv*123), (app.yDiv*39)
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
            pos: (app.xDiv*1), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*13), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*25), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*37), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*49), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            pos: (app.xDiv*61), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
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
            id: btnCam3Go7
            text:"7"
            pos: (app.xDiv*73), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.Cam3Go7()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam3Go8
            text:"8"
            pos: (app.xDiv*85), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.Cam3Go8()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam3Go9
            text:"9"
            pos: (app.xDiv*97), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.Cam3Go9()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam3Go10
            text:"10"
            pos: (app.xDiv*109), (app.yDiv*25)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.Cam3Go10()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam3PT-
            text: "PT-"
            halign: 'center'
            pos: (app.xDiv*1), (app.yDiv*32)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3PTSpeedDec()

        Button:
            id: btnCam3PT+
            text: "PT+"
            halign: 'center'
            pos: (app.xDiv*40), (app.yDiv*32)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3PTSpeedInc()

        Button:
            id: btnCam3Sl-
            text: "Sl-"
            halign: 'center'
            pos: (app.xDiv*49), (app.yDiv*32)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3SliderSpeedDec()

        Button:
            id: btnCam3Sl+
            text: "Sl+"
            halign: 'center'
            pos: (app.xDiv*88), (app.yDiv*32)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3SliderSpeedInc()

        Button:
            id: btnCam3Zm-
            text:"Zm OUT"
            halign: 'center'
            pos: (app.xDiv*109), (app.yDiv*32)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3ZoomOut()
            on_release: app.sendCam3ZoomStop()

        Button:
            id: btnCam3Zm+
            text:"Zm IN"
            halign: 'center'
            pos: (app.xDiv*97), (app.yDiv*32)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam3ButColour)
            on_press: app.sendCam3ZoomIn()
            on_release: app.sendCam3ZoomStop()

        Button:
            id: btnCam3Clr
            text:"Clear"
            pos: (app.xDiv*123), (app.yDiv*27)
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






        Button:
            id: btnCam4Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go1()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go2
            text:"2"
            pos: (app.xDiv*13), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go2()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go3
            text:"3"
            pos: (app.xDiv*25), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go3()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go4
            text:"4"
            pos: (app.xDiv*37), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go4()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go5
            text:"5"
            pos: (app.xDiv*49), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go5()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go6
            text:"6"
            pos: (app.xDiv*61), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go6()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go7
            text:"7"
            pos: (app.xDiv*73), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go7()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go8
            text:"8"
            pos: (app.xDiv*85), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go8()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go9
            text:"9"
            pos: (app.xDiv*97), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go9()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4Go10
            text:"10"
            pos: (app.xDiv*109), (app.yDiv*13)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.Cam4Go10()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam4PT-
            text: "PT-"
            halign: 'center'
            pos: (app.xDiv*1), (app.yDiv*20)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4PTSpeedDec()

        Button:
            id: btnCam4PT+
            text: "PT+"
            halign: 'center'
            pos: (app.xDiv*40), (app.yDiv*20)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4PTSpeedInc()

        Button:
            id: btnCam4Sl-
            text: "Sl-"
            halign: 'center'
            pos: (app.xDiv*49), (app.yDiv*20)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4SliderSpeedDec()

        Button:
            id: btnCam4Sl+
            text: "Sl+"
            halign: 'center'
            pos: (app.xDiv*88), (app.yDiv*20)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4SliderSpeedInc()

        Button:
            id: btnCam4Zm-
            text:"Zm OUT"
            halign: 'center'
            pos: (app.xDiv*109), (app.yDiv*20)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4ZoomOut()
            on_release: app.sendCam4ZoomStop()

        Button:
            id: btnCam4Zm+
            text:"Zm IN"
            halign: 'center'
            pos: (app.xDiv*97), (app.yDiv*20)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendCam4ZoomIn()
            on_release: app.sendCam4ZoomStop()

        Button:
            id: btnCam4Clr
            text:"Clear"
            pos: (app.xDiv*123), (app.yDiv*15)
            size: (app.xDiv*6), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam4ButColour)
            on_press: app.sendClearCam4Pos()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height






        Button:
            id: btnCam5Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go1()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go2
            text:"2"
            pos: (app.xDiv*13), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go2()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go3
            text:"3"
            pos: (app.xDiv*25), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go3()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go4
            text:"4"
            pos: (app.xDiv*37), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go4()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go5
            text:"5"
            pos: (app.xDiv*49), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go5()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go6
            text:"6"
            pos: (app.xDiv*61), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go6()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go7
            text:"7"
            pos: (app.xDiv*73), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go7()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go8
            text:"8"
            pos: (app.xDiv*85), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go8()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go9
            text:"9"
            pos: (app.xDiv*97), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go9()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5Go10
            text:"10"
            pos: (app.xDiv*109), (app.yDiv*1)
            size: (app.xDiv*9), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*3)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.Cam5Go10()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height

        Button:
            id: btnCam5PT-
            text: "PT-"
            halign: 'center'
            pos: (app.xDiv*1), (app.yDiv*8)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5PTSpeedDec()

        Button:
            id: btnCam5PT+
            text: "PT+"
            halign: 'center'
            pos: (app.xDiv*40), (app.yDiv*8)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5PTSpeedInc()

        Button:
            id: btnCam5Sl-
            text: "Sl-"
            halign: 'center'
            pos: (app.xDiv*49), (app.yDiv*8)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5SliderSpeedDec()

        Button:
            id: btnCam5Sl+
            text: "Sl+"
            halign: 'center'
            pos: (app.xDiv*88), (app.yDiv*8)
            size: (app.xDiv*6), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5SliderSpeedInc()

        Button:
            id: btnCam5Zm-
            text:"Zm OUT"
            halign: 'center'
            pos: (app.xDiv*109), (app.yDiv*8)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5ZoomOut()
            on_release: app.sendCam5ZoomStop()

        Button:
            id: btnCam5Zm+
            text:"Zm IN"
            halign: 'center'
            pos: (app.xDiv*97), (app.yDiv*8)
            size: (app.xDiv*9), (app.yDiv*3)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendCam5ZoomIn()
            on_release: app.sendCam5ZoomStop()

        Button:
            id: btnCam5Clr
            text:"Clear"
            pos: (app.xDiv*123), (app.yDiv*3)
            size: (app.xDiv*6), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            col: .13, .13, .13, 1
            background_normal: ''
            background_color: get_color_from_hex(app.Cam5ButColour)
            on_press: app.sendClearCam5Pos()
            canvas.before:
                Color: 
                    rgba: self.col
                Line:
                    width: 4
                    rectangle: self.x, self.y, self.width, self.height




        MDFillRoundFlatButton:
            id: buttonWhichCam1
            text: "Cam 1"
            line_width: 5
            line_color: 1, 0, 0, 1
            md_bg_color: get_color_from_hex(app.Cam1ButColour)
            pos: (app.xDiv*2), (app.yDiv*64)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial1()

        MDFillRoundFlatButton:
            id: buttonWhichCam2
            text: "Cam 2"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam2ButColour)
            pos: (app.xDiv*14), (app.yDiv*64)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial2()

        MDFillRoundFlatButton:
            id: buttonWhichCam3
            text: "Cam 3"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam3ButColour)
            pos: (app.xDiv*26), (app.yDiv*64)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial3()

        MDFillRoundFlatButton:
            id: buttonWhichCam4
            text: "Cam 4"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam4ButColour)
            pos: (app.xDiv*38), (app.yDiv*64)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial4()

        MDFillRoundFlatButton:
            id: buttonWhichCam5
            text: "Cam 5"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam5ButColour)
            pos: (app.xDiv*50), (app.yDiv*64)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial5()

        MDFillRoundFlatButton:
            id: btn_ToRunPage
            text: "->"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*100), (app.yDiv*64.5)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*1.2)
            on_release: 
                if app.whichCam == "1": \
                app.root.current = "1stcam"
                if app.whichCam == "2": \
                app.root.current = "2ndcam"
                if app.whichCam == "3": \
                app.root.current = "3rdcam"

        MDFillRoundFlatButton:
            id: serialConnected
            text: "Not Connected"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: .75, .1, .1, 1
            pos: (app.xDiv*80), (app.yDiv*64.5)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*1.2)
            on_release: app.on_btn_scan_release()
                


    





















<SecondWindow>:
    name: '1stcam'

    MDScreen:
        id: 1stcam
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
            #Rectangle:
            #    pos: (app.xDiv*50.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Slider
            #Rectangle:
            #    pos: (app.xDiv*71.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Zoom
            #Rectangle:
            #    pos: (app.xDiv*92.5), (app.yDiv*0.5)
            #    size: (app.xDiv*13), (app.yDiv*23)

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
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam2 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam3 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)

            
            #Cam1 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*17)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam2 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*9)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam3 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*1)
            #    size: (app.xDiv*4), (app.yDiv*6)



        #FloatLayout:
        #    id: cam1PTSpd
        #    sizPT21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle:
        #            pos: (app.xDiv*55), (app.yDiv*17)
        #            size: self.sizPT21

        #FloatLayout:
        #    id: cam2PTSpd
        #    sizPT22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*9)
        #            size: self.sizPT22

        #FloatLayout:
        #    id: cam3PTSpd
        #    sizPT23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*1)
        #            size: self.sizPT23

        #FloatLayout:
        #    id: cam1SlSpd
        #    sizSl21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*17)
        #            size: self.sizSl21

        #FloatLayout:
        #    id: cam2SlSpd
        #    sizSl22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*9)
        #            size: self.sizSl22

        #FloatLayout:
        #    id: cam3SlSpd
        #    sizSl23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*1)
        #            size: self.sizSl23


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
            helpRGB2: (0.2, 0.2, 0.2, 1)
            canvas:
                Color:
                    rgb: self.helpRGB2
            
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

        ScrollView:
            id: scanDD
            pos: app.xScreen, app.yScreen
            size: (app.xDiv*30), app.yScreen
            size_hint: None, None
            do_scroll_x: False
            BoxLayout:
                id: box_list1
                orientation: 'vertical'
                on_parent: app.uiDict['box_list1'] = self
                size: (app.xDiv*25), (app.yDiv*6)
                size_hint: None, None
                height: max(self.parent.height, self.minimum_height)

        FloatLayout:
            TextInput:
                id: textInput
                pos: (app.xDiv*122), (app.yDiv*61)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None


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
            id: btnCam1Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*10)
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
            pos: (app.xDiv*26), (app.yDiv*10)
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
            pos: (app.xDiv*51), (app.yDiv*10)
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
            pos: (app.xDiv*76), (app.yDiv*10)
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
            pos: (app.xDiv*101), (app.yDiv*10)
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
            pos: (app.xDiv*126), (app.yDiv*10)
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


        FloatLayout:
            TextInput:
                id: textInput1ACC
                pos: (app.xDiv*12), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput1SPP
                pos: (app.xDiv*12), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'
                
            TextInput:
                id: textInput1SPS
                pos: (app.xDiv*12), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput1DLY
                pos: (app.xDiv*12), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'



            TextInput:
                id: textInput2ACC
                pos: (app.xDiv*37), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput2SPP
                pos: (app.xDiv*37), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput2SPS
                pos: (app.xDiv*37), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput2DLY
                pos: (app.xDiv*37), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput3ACC
                pos: (app.xDiv*62), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput3SPP
                pos: (app.xDiv*62), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput3SPS
                pos: (app.xDiv*62), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput3DLY
                pos: (app.xDiv*62), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput4ACC
                pos: (app.xDiv*87), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput4SPP
                pos: (app.xDiv*87), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput4SPS
                pos: (app.xDiv*87), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput4DLY
                pos: (app.xDiv*87), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'




            TextInput:
                id: textInput5ACC
                pos: (app.xDiv*112), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput5SPP
                pos: (app.xDiv*112), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput5SPS
                pos: (app.xDiv*112), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput5DLY
                pos: (app.xDiv*112), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'









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
            on_release: app.root.current = "2ndcam"

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
            on_release: app.root.current = "3rdcam"

        MDFillRoundFlatButton:
            id: btn_ToMainPage
            text: "Main"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*40), (app.yDiv*65.7)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.root.current = "main"

        Button:
            id: btn_RunCam1
            text: "R"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*52), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCam1()

        Button:
            id: btn_RunCamMoves1
            text: "Rm"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*58), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCamM1()

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












<ThirdWindow>:
    name: '2ndcam'

    MDScreen:
        id: 2ndcam
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
            #Rectangle:
            #    pos: (app.xDiv*50.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Slider
            #Rectangle:
            #    pos: (app.xDiv*71.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Zoom
            #Rectangle:
            #    pos: (app.xDiv*92.5), (app.yDiv*0.5)
            #    size: (app.xDiv*13), (app.yDiv*23)

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
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam2 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam3 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)

            
            #Cam1 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*17)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam2 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*9)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam3 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*1)
            #    size: (app.xDiv*4), (app.yDiv*6)



        #FloatLayout:
        #    id: cam1PTSpd
        #    sizPT21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle:
        #            pos: (app.xDiv*55), (app.yDiv*17)
        #            size: self.sizPT21

        #FloatLayout:
        #    id: cam2PTSpd
        #    sizPT22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*9)
        #            size: self.sizPT22

        #FloatLayout:
        #    id: cam3PTSpd
        #    sizPT23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*1)
        #            size: self.sizPT23

        #FloatLayout:
        #    id: cam1SlSpd
        #    sizSl21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*17)
        #            size: self.sizSl21

        #FloatLayout:
        #    id: cam2SlSpd
        #    sizSl22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*9)
        #            size: self.sizSl22

        #FloatLayout:
        #    id: cam3SlSpd
        #    sizSl23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*1)
        #            size: self.sizSl23


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
            helpRGB3: (0.2, 0.2, 0.2, 1)
            canvas:
                Color:
                    rgb: self.helpRGB3
            
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
            opacity: 1 if self.visible else 0
            halign: "left"
            valign: "top"
            markup: True
            text: 'OSC Server Port: 6503\\nOSC Client Port: 1337\\n\\nSerial Text Commands:\\ns(int) = Pan   speed (º/s)\\nS(int) = Tilt  speed (º/s)\\na(int) = Slide speed (mm/s)\\n\\nq(float) = Pan   accel\\nQ(float) = Tilt  accel\\nw(float) = Slide accel\\n\\ne(int) = Joystick pan   accel factor (1 = 100%)\\nE(int) = Joystick tilt  accel factor (1 = 100%)\\nD(int) = Joystick slide accel factor (1 = 100%)\\n\\nd(int) = Slide speed increments\\nf(int) = Slide min speed limit\\nF(int) = Slide max speed limit\\n\\nU = Save to EEPROM\\n'

        ScrollView:
            id: scanDD
            pos: app.xScreen, app.yScreen
            size: (app.xDiv*30), app.yScreen
            size_hint: None, None
            do_scroll_x: False
            BoxLayout:
                id: box_list2
                orientation: 'vertical'
                on_parent: app.uiDict['box_list2'] = self
                size: (app.xDiv*25), (app.yDiv*6)
                size_hint: None, None
                height: max(self.parent.height, self.minimum_height)

        FloatLayout:
            TextInput:
                id: textInput
                pos: (app.xDiv*122), (app.yDiv*61)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None


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
            id: btnCam2Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*10)
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
            pos: (app.xDiv*26), (app.yDiv*10)
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
            pos: (app.xDiv*51), (app.yDiv*10)
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
            pos: (app.xDiv*76), (app.yDiv*10)
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
            pos: (app.xDiv*101), (app.yDiv*10)
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
            pos: (app.xDiv*126), (app.yDiv*10)
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


        FloatLayout:
            TextInput:
                id: textInput1ACC
                pos: (app.xDiv*12), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput1SPP
                pos: (app.xDiv*12), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput1SPS
                pos: (app.xDiv*12), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput1DLY
                pos: (app.xDiv*12), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'




            TextInput:
                id: textInput2ACC
                pos: (app.xDiv*37), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput2SPP
                pos: (app.xDiv*37), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'
                
            TextInput:
                id: textInput2SPS
                pos: (app.xDiv*37), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput2DLY
                pos: (app.xDiv*37), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput3ACC
                pos: (app.xDiv*62), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput3SPP
                pos: (app.xDiv*62), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput3SPS
                pos: (app.xDiv*62), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput3DLY
                pos: (app.xDiv*62), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput4ACC
                pos: (app.xDiv*87), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput4SPP
                pos: (app.xDiv*87), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput4SPS
                pos: (app.xDiv*87), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput4DLY
                pos: (app.xDiv*87), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'




            TextInput:
                id: textInput5ACC
                pos: (app.xDiv*112), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput5SPP
                pos: (app.xDiv*112), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput5SPS
                pos: (app.xDiv*112), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput5DLY
                pos: (app.xDiv*112), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'









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
            on_release: app.root.current = "1stcam"

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
            on_release: app.root.current = "3rdcam"

        MDFillRoundFlatButton:
            id: btn_ToMainPage
            text: "Main"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*40), (app.yDiv*65.7)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.root.current = "main"

        Button:
            id: btn_RunCam2
            text: "R"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*52), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCam2()

        Button:
            id: btn_RunCamMoves2
            text: "Rm"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*58), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCamM2()

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


















<FourthWindow>:
    name: '3rdcam'

    MDScreen:
        id: 3rdcam
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
            #Rectangle:
            #    pos: (app.xDiv*50.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Slider
            #Rectangle:
            #    pos: (app.xDiv*71.5), (app.yDiv*0.5)
            #    size: (app.xDiv*18), (app.yDiv*23)
            #Zoom
            #Rectangle:
            #    pos: (app.xDiv*92.5), (app.yDiv*0.5)
            #    size: (app.xDiv*13), (app.yDiv*23)

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
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*17)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam2 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*9)
            #    size: (app.xDiv*9), (app.yDiv*6)

            #Cam3 Speed BG
            #Rectangle:
            #    pos: (app.xDiv*55), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)
            #Rectangle:
            #    pos: (app.xDiv*76), (app.yDiv*1)
            #    size: (app.xDiv*9), (app.yDiv*6)

            
            #Cam1 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*17)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam2 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*9)
            #    size: (app.xDiv*4), (app.yDiv*6)

            #Cam3 Speed Zoom
            #Rectangle:
            #    pos: (app.xDiv*97), (app.yDiv*1)
            #    size: (app.xDiv*4), (app.yDiv*6)



        #FloatLayout:
        #    id: cam1PTSpd
        #    sizPT21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle:
        #            pos: (app.xDiv*55), (app.yDiv*17)
        #            size: self.sizPT21

        #FloatLayout:
        #    id: cam2PTSpd
        #    sizPT22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*9)
        #            size: self.sizPT22

        #FloatLayout:
        #    id: cam3PTSpd
        #    sizPT23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*55), (app.yDiv*1)
        #            size: self.sizPT23

        #FloatLayout:
        #    id: cam1SlSpd
        #    sizSl21: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*17)
        #            size: self.sizSl21

        #FloatLayout:
        #    id: cam2SlSpd
        #    sizSl22: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*9)
        #            size: self.sizSl22

        #FloatLayout:
        #    id: cam3SlSpd
        #    sizSl23: 0, 0
        #    canvas:
        #        Color:
        #            rgba: get_color_from_hex("#7D0000")
        #        Rectangle: 
        #            pos: (app.xDiv*76), (app.yDiv*1)
        #            size: self.sizSl23


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
            helpRGB4: (0.2, 0.2, 0.2, 1)
            canvas:
                Color:
                    rgb: self.helpRGB4
            
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

        ScrollView:
            id: scanDD
            pos: app.xScreen, app.yScreen
            size: (app.xDiv*30), app.yScreen
            size_hint: None, None
            do_scroll_x: False
            BoxLayout:
                id: box_list3
                orientation: 'vertical'
                on_parent: app.uiDict['box_list3'] = self
                size: (app.xDiv*25), (app.yDiv*6)
                size_hint: None, None
                height: max(self.parent.height, self.minimum_height)

        FloatLayout:
            TextInput:
                id: textInput
                pos: (app.xDiv*122), (app.yDiv*61)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None


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
            id: btnCam3Go1
            text:"1"
            pos: (app.xDiv*1), (app.yDiv*10)
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
            pos: (app.xDiv*26), (app.yDiv*10)
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
            pos: (app.xDiv*51), (app.yDiv*10)
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
            pos: (app.xDiv*76), (app.yDiv*10)
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
            pos: (app.xDiv*101), (app.yDiv*10)
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
            pos: (app.xDiv*126), (app.yDiv*10)
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


        FloatLayout:
            TextInput:
                id: textInput1ACC
                pos: (app.xDiv*12), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput1SPP
                pos: (app.xDiv*12), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput1SPS
                pos: (app.xDiv*12), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput1DLY
                pos: (app.xDiv*12), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'



            TextInput:
                id: textInput2ACC
                pos: (app.xDiv*37), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput2SPP
                pos: (app.xDiv*37), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput2SPS
                pos: (app.xDiv*37), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput2DLY
                pos: (app.xDiv*37), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput3ACC
                pos: (app.xDiv*62), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput3SPP
                pos: (app.xDiv*62), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput3SPS
                pos: (app.xDiv*62), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput3DLY
                pos: (app.xDiv*62), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'





            TextInput:
                id: textInput4ACC
                pos: (app.xDiv*87), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput4SPP
                pos: (app.xDiv*87), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput4SPS
                pos: (app.xDiv*87), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput4DLY
                pos: (app.xDiv*87), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'




            TextInput:
                id: textInput5ACC
                pos: (app.xDiv*112), (app.yDiv*18)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Acceleration'

            TextInput:
                id: textInput5SPP
                pos: (app.xDiv*112), (app.yDiv*14)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'PT Speed'

            TextInput:
                id: textInput5SPS
                pos: (app.xDiv*112), (app.yDiv*10)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Slider Speed'

            TextInput:
                id: textInput5DLY
                pos: (app.xDiv*112), (app.yDiv*6)
                size: (app.xDiv*10), (app.yDiv*3)
                size_hint: None, None
                hint_text: 'Delay'









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
            on_release: app.root.current = "1stcam"

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
            on_release: app.root.current = "2ndcam"

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
            id: btn_ToMainPage
            text: "Main"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*40), (app.yDiv*65.7)
            size: (app.xDiv*8), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.root.current = "main"

        Button:
            id: btn_RunCam3
            text: "R"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*52), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCam3()

        Button:
            id: btn_RunCamMoves3
            text: "Rm"
            user_font_size: "30sp"
            line_width: 2
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex("#757981")
            pos: (app.xDiv*58), (app.yDiv*65.7)
            size: (app.xDiv*4), (app.yDiv*4)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.btnRunCamM3()

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

#Button:
        #text: "2nd"
        #on_release: app.root.current = "1stcam"


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
    elif address == "/Cam1Go7" and args[0] == 1:
        MDApp.get_running_app().Cam1Go7()
    elif address == "/Cam1Go8" and args[0] == 1:
        MDApp.get_running_app().Cam1Go8()
    elif address == "/Cam1Go9" and args[0] == 1:
        MDApp.get_running_app().Cam1Go9()
    elif address == "/Cam1Go10" and args[0] == 1:
        MDApp.get_running_app().Cam1Go10()
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
    elif address == "/Cam2Go7" and args[0] == 1:
        MDApp.get_running_app().Cam2Go7()
    elif address == "/Cam2Go8" and args[0] == 1:
        MDApp.get_running_app().Cam2Go8()
    elif address == "/Cam2Go9" and args[0] == 1:
        MDApp.get_running_app().Cam2Go9()
    elif address == "/Cam2Go10" and args[0] == 1:
        MDApp.get_running_app().Cam2Go10()
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
    elif address == "/Cam3Go7" and args[0] == 1:
        MDApp.get_running_app().Cam3Go7()
    elif address == "/Cam3Go8" and args[0] == 1:
        MDApp.get_running_app().Cam3Go8()
    elif address == "/Cam3Go9" and args[0] == 1:
        MDApp.get_running_app().Cam3Go9()
    elif address == "/Cam3Go10" and args[0] == 1:
        MDApp.get_running_app().Cam3Go10()
    elif address == "/Cam4Go1" and args[0] == 1:
        MDApp.get_running_app().Cam4Go1()
    elif address == "/Cam4Go2" and args[0] == 1:
        MDApp.get_running_app().Cam4Go2()
    elif address == "/Cam4Go3" and args[0] == 1:
        MDApp.get_running_app().Cam4Go3()
    elif address == "/Cam4Go4" and args[0] == 1:
        MDApp.get_running_app().Cam4Go4()
    elif address == "/Cam4Go5" and args[0] == 1:
        MDApp.get_running_app().Cam4Go5()
    elif address == "/Cam4Go6" and args[0] == 1:
        MDApp.get_running_app().Cam4Go6()
    elif address == "/Cam4Go7" and args[0] == 1:
        MDApp.get_running_app().Cam4Go7()
    elif address == "/Cam4Go8" and args[0] == 1:
        MDApp.get_running_app().Cam4Go8()
    elif address == "/Cam4Go9" and args[0] == 1:
        MDApp.get_running_app().Cam4Go9()
    elif address == "/Cam4Go10" and args[0] == 1:
        MDApp.get_running_app().Cam4Go10()
    elif address == "/Cam5Go1" and args[0] == 1:
        MDApp.get_running_app().Cam5Go1()
    elif address == "/Cam5Go2" and args[0] == 1:
        MDApp.get_running_app().Cam5Go2()
    elif address == "/Cam5Go3" and args[0] == 1:
        MDApp.get_running_app().Cam5Go3()
    elif address == "/Cam5Go4" and args[0] == 1:
        MDApp.get_running_app().Cam5Go4()
    elif address == "/Cam5Go5" and args[0] == 1:
        MDApp.get_running_app().Cam5Go5()
    elif address == "/Cam5Go6" and args[0] == 1:
        MDApp.get_running_app().Cam5Go6()
    elif address == "/Cam5Go7" and args[0] == 1:
        MDApp.get_running_app().Cam5Go7()
    elif address == "/Cam5Go8" and args[0] == 1:
        MDApp.get_running_app().Cam5Go8()
    elif address == "/Cam5Go9" and args[0] == 1:
        MDApp.get_running_app().Cam5Go9()
    elif address == "/Cam5Go10" and args[0] == 1:
        MDApp.get_running_app().Cam5Go10()
        
    elif address == "/Cam1PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam1PTSpeedInc()
    elif address == "/Cam1PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam1PTSpeedDec()
    elif address == "/Cam1SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam1SlSpeedInc()
    elif address == "/Cam1SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam1SlSpeedDec()

    elif address == "/Cam2PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam2PTSpeedInc()
    elif address == "/Cam2PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam2PTSpeedDec()
    elif address == "/Cam2SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam2SlSpeedInc()
    elif address == "/Cam2SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam2SlSpeedDec()

    #elif address == "/Cam2PTSpd":
    #    MDApp.get_running_app().sendCam2PTSpeedOSC(args[0])
    #elif address == "/Cam2SlSpd":
    #    MDApp.get_running_app().sendCam2SlSpeedOSC(args[0])

    elif address == "/Cam3PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam3PTSpeedInc()
    elif address == "/Cam3PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam3PTSpeedDec()
    elif address == "/Cam3SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam3SlSpeedInc()
    elif address == "/Cam3SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam3SlSpeedDec()

    elif address == "/Cam4PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam4PTSpeedInc()
    elif address == "/Cam4PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam4PTSpeedDec()
    elif address == "/Cam4SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam4SlSpeedInc()
    elif address == "/Cam4SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam4SlSpeedDec()

    elif address == "/Cam5PTSpdInc" and args[0] == 0:
        MDApp.get_running_app().sendCam5PTSpeedInc()
    elif address == "/Cam5PTSpdDec" and args[0] == 1:
        MDApp.get_running_app().sendCam5PTSpeedDec()
    elif address == "/Cam5SlSpdInc" and args[0] == 2:
        MDApp.get_running_app().sendCam5SlSpeedInc()
    elif address == "/Cam5SlSpdDec" and args[0] == 3:
        MDApp.get_running_app().sendCam5SlSpeedDec()

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

    elif address == "/Cam4ZoomIn" and args[0] == 1:
        MDApp.get_running_app().sendCam4ZoomIn()
    elif address == "/Cam4ZoomOut" and args[0] == 1:
        MDApp.get_running_app().sendCam4ZoomOut()
    elif address == "/Cam4ZoomStop" and args[0] == 1:
        MDApp.get_running_app().sendCam4ZoomStop()

    elif address == "/Cam5ZoomIn" and args[0] == 1:
        MDApp.get_running_app().sendCam5ZoomIn()
    elif address == "/Cam5ZoomOut" and args[0] == 1:
        MDApp.get_running_app().sendCam5ZoomOut()
    elif address == "/Cam5ZoomStop" and args[0] == 1:
        MDApp.get_running_app().sendCam5ZoomStop()

    elif address == "/Cam1Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam1Pos()
    elif address == "/Cam2Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam2Pos()
    elif address == "/Cam3Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam3Pos()
    elif address == "/Cam4Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam4Pos()
    elif address == "/Cam5Clr" and args[0] == 1:
        MDApp.get_running_app().sendClearCam5Pos()

    elif address == "/Cam1Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam1RecordToggleOSC()
    elif address == "/Cam2Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam2RecordToggleOSC()
    elif address == "/Cam3Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam3RecordToggleOSC()
    elif address == "/Cam4Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam4RecordToggleOSC()
    elif address == "/Cam5Rec" and args[0] == 1:
        MDApp.get_running_app().sendCam5RecordToggleOSC()

    elif address == "/moveType" and args[0] == 1:
        moveType = 1
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 2:
        moveType = 2
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 3:
        moveType = 3
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 4:
        moveType = 4
        MDApp.get_running_app().doButtonColours()
    elif address == "/moveType" and args[0] == 5:
        moveType = 5
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

    elif address == "/Cam4Left" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'a')
    elif address == "/Cam4Right" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'd')
    elif address == "/Cam4Up" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'w')
    elif address == "/Cam4Down" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 's')
    elif address == "/Cam4SlLeft" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, ',')
    elif address == "/Cam4SlRight" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, '.')

    elif address == "/Cam4LeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'A')
    elif address == "/Cam4RightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'D')
    elif address == "/Cam4UpRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'W')
    elif address == "/Cam4DownRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, 'S')
    elif address == "/Cam4SlLeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, '<')
    elif address == "/Cam4SlRightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(4, '>')

    elif address == "/Cam5Left" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'a')
    elif address == "/Cam5Right" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'd')
    elif address == "/Cam5Up" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'w')
    elif address == "/Cam5Down" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 's')
    elif address == "/Cam5SlLeft" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, ',')
    elif address == "/Cam5SlRight" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, '.')

    elif address == "/Cam5LeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'A')
    elif address == "/Cam5RightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'D')
    elif address == "/Cam5UpRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'W')
    elif address == "/Cam5DownRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, 'S')
    elif address == "/Cam5SlLeftRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, '<')
    elif address == "/Cam5SlRightRel" and args[0] == 1:
        MDApp.get_running_app().OSC_on_press(5, '>')


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
    elif address == "/Cam4PTSpeedInc" and args[0] == 1:
        MDApp.get_running_app().sendCam4PTSpeedInc()
    elif address == "/Cam4PTSpeedDec" and args[0] == 1:
        MDApp.get_running_app().sendCam4PTSpeedDec()
    elif address == "/Cam5PTSpeedInc" and args[0] == 1:
        MDApp.get_running_app().sendCam5PTSpeedInc()
    elif address == "/Cam6PTSpeedDec" and args[0] == 1:
        MDApp.get_running_app().sendCam5PTSpeedDec()
    



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


class PTSApp(MDApp):

    xDiv = NumericProperty(xDivSet)        # 10 / 1340
    yDiv = NumericProperty(yDivSet)        # 10 / 703

    xScreen = NumericProperty(xScreenSet)
    yScreen = NumericProperty(yScreenSet)

    whichCam = StringProperty()

    def __init__(self, *args, **kwargs):
        global Cam1ButColour
        global Cam2ButColour
        global Cam3ButColour
        global Cam4ButColour
        global Cam5ButColour
        self.Cam1ButColour = Cam1ButColour
        self.Cam2ButColour = Cam2ButColour
        self.Cam3ButColour = Cam3ButColour
        self.Cam4ButColour = Cam4ButColour
        self.Cam5ButColour = Cam5ButColour
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None




        #self.port_thread_lock = threading.Lock()

        #base_path = Path(__file__).parent
        #image_path = (base_path / "./PTSApp-Icon.png").resolve()
        #self.icon = os.path.join(image_path)
        super(PTSApp, self).__init__(*args, **kwargs)

        self.event_loop_worker = None

    def build(self):
        global PTJoy
        global srvPort
        global cliPort
        self.screen = Builder.load_string(KV)

        Window.bind(on_joy_hat = self.on_joy_hat)
        Window.bind(on_joy_ball = self.on_joy_ball)
        Window.bind(on_joy_axis = self.on_joy_axis)
        Window.bind(on_joy_button_up = self.on_joy_button_up)
        Window.bind(on_joy_button_down = self.on_joy_button_down)
        
        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_touch_up = self.on_touch_up)
        Window.bind(on_request_close = self.stopping)
        Window.bind(on_key_down = self.keyDown)
        Window.bind(on_key_up = self.keyUp)
        #listener = Listener(on_press = self.on_press, on_release=self.on_release)
        #listener.start()
        Clock.schedule_interval(self.flash, 1.0)
        Clock.schedule_interval(self.doJoyMoves, 0.1)
        self.start_event_loop_thread()
        Clock.schedule_once(self.showPorts, 0)
        Clock.schedule_once(self.setWhichCam, 0)
        self.icon = 'PTSApp-Icon.png'
        return self.screen

    #def on_joy_axis(self, win, stickid, axisid, value):
        #print(win, stickid, axisid, value)

    def on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
        print('ball', stickid, ballid, (xvalue, yvalue))

    def on_joy_hat(self, win, stickid, hatid, value):
        print('hat', stickid, hatid, value)

    def on_joy_button_down(self, win, stickid, buttonid):
        print('button_down', stickid, buttonid)

    def on_joy_button_up(self, win, stickid, buttonid):
        print('button_up', stickid, buttonid)

    def keyUp(self, instance, keyboard, keycode):
        global axisX
        global axisY
        global axisZ

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        if (self.root.get_screen('1stcam').ids.textInput.focus == False) or (self.root.get_screen('2ndcam').ids.textInput.focus == False) or (self.root.get_screen('3rdcam').ids.textInput.focus == False):              #   a= 4, s= 22, d=7, w= 26, ,=54, .=55
            #print(keycode)
            if keycode == 4:
                axisX = 0
            if keycode == 7:
                axisX = 0
            if keycode == 26:
                axisY = 0
            if keycode == 22:
                axisY = 0
            if keycode == 54:
                axisZ = 0
            if keycode == 55:
                axisZ = 0

            self.doJoyMoves(1)
            self.doButtonColours()

    def keyDown(self, instance, keyboard, keycode, text, modifiers):
        global axisX
        global axisY
        global axisZ

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        global Cam4TextColour
        global Cam5TextColour
        
        if (self.root.get_screen('1stcam').ids.textInput.focus == False) or (self.root.get_screen('2ndcam').ids.textInput.focus == False) or (self.root.get_screen('3rdcam').ids.textInput.focus == False):              #   a= 4, s= 22, d=7, w= 26, ,=54, .=55
            #print(keycode)
            if keycode == 4:
                axisX = -255
            if keycode == 7:
                axisX = 255
            if keycode == 22:
                axisY = -255
            if keycode == 26:
                axisY = 255
            if keycode == 54:
                axisZ = -255
            if keycode == 55:
                axisZ = 255

            self.doJoyMoves(1)
            self.doButtonColours()
        
        if keycode == 40:                                                                   # Return key pressed
            if (self.root.get_screen('1stcam').ids.textInput.focus == True) or (self.root.get_screen('2ndcam').ids.textInput.focus == True) or (self.root.get_screen('3rdcam').ids.textInput.focus == True):
                #print("main pressed")
                global whichCamSerial
                if whichCamSerial == 1:
                    temp = "??"
                    tempInput = (self.root.get_screen('1stcam').ids.textInput.text)
                elif whichCamSerial == 2:
                    temp = "!?"
                    tempInput = (self.root.get_screen('2ndcam').ids.textInput.text)
                elif whichCamSerial == 3:
                    temp = "@?"
                    tempInput = (self.root.get_screen('3rdcam').ids.textInput.text)
                elif whichCamSerial == 4:
                    temp = "&?"
                    tempInput = (self.root.get_screen('3rdcam').ids.textInput.text)
                elif whichCamSerial == 5:
                    temp = "*?"
                    tempInput = (self.root.get_screen('3rdcam').ids.textInput.text)

                #tempInput = (self.root.get_screen('main').ids.textInput.text)
                temp += tempInput
                #print(temp)                                                                 # for debugging
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(self.clearTextInput, 0)

                    if whichCamSerial == 1:
                        self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]Sent command: " + tempInput + "[/color]\n")
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    elif whichCamSerial == 2:
                        self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]Sent command: " + tempInput + "[/color]\n")
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    elif whichCamSerial == 3:
                        self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]Sent command: " + tempInput + "[/color]\n")
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    elif whichCamSerial == 4:
                        self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam4TextColour + "]Sent command: " + tempInput + "[/color]\n")
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    elif whichCamSerial == 5:
                        self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam5TextColour + "]Sent command: " + tempInput + "[/color]\n")
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0

                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

                self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
                self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
                self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
                self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
                self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
                self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0

            elif self.root.get_screen('1stcam').ids.textInput1ACC.focus == True:
                temp = "??K1"
                tempInput = (self.root.get_screen('1stcam').ids.textInput1ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend11ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput1SPP.focus == True:
                temp = "??i1"
                tempInput = (self.root.get_screen('1stcam').ids.textInput1SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend11SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput1SPS.focus == True:
                temp = "??I1"
                tempInput = (self.root.get_screen('1stcam').ids.textInput1SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend11SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput1DLY.focus == True:
                temp = "??j1"
                tempInput = (self.root.get_screen('1stcam').ids.textInput1DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend11DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('1stcam').ids.textInput2ACC.focus == True:
                temp = "??K2"
                tempInput = (self.root.get_screen('1stcam').ids.textInput2ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend12ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput2SPP.focus == True:
                temp = "??i2"
                tempInput = (self.root.get_screen('1stcam').ids.textInput2SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend12SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput2SPS.focus == True:
                temp = "??I2"
                tempInput = (self.root.get_screen('1stcam').ids.textInput2SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend12SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput2DLY.focus == True:
                temp = "??j2"
                tempInput = (self.root.get_screen('1stcam').ids.textInput2DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend12DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('1stcam').ids.textInput3ACC.focus == True:
                temp = "??K3"
                tempInput = (self.root.get_screen('1stcam').ids.textInput3ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend13ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput3SPP.focus == True:
                temp = "??i3"
                tempInput = (self.root.get_screen('1stcam').ids.textInput3SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend13SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput3SPS.focus == True:
                temp = "??I3"
                tempInput = (self.root.get_screen('1stcam').ids.textInput3SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend13SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput3DLY.focus == True:
                temp = "??j3"
                tempInput = (self.root.get_screen('1stcam').ids.textInput3DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend13DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('1stcam').ids.textInput4ACC.focus == True:
                temp = "??K4"
                tempInput = (self.root.get_screen('1stcam').ids.textInput4ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend14ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput4SPP.focus == True:
                temp = "??i4"
                tempInput = (self.root.get_screen('1stcam').ids.textInput4SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend14SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput4SPS.focus == True:
                temp = "??I4"
                tempInput = (self.root.get_screen('1stcam').ids.textInput4SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend14SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput4DLY.focus == True:
                temp = "??j4"
                tempInput = (self.root.get_screen('1stcam').ids.textInput4DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend14DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('1stcam').ids.textInput5ACC.focus == True:
                temp = "??K5"
                tempInput = (self.root.get_screen('1stcam').ids.textInput5ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend15ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput5SPP.focus == True:
                temp = "??i5"
                tempInput = (self.root.get_screen('1stcam').ids.textInput5SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend15SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput5SPS.focus == True:
                temp = "??I5"
                tempInput = (self.root.get_screen('1stcam').ids.textInput5SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend15SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('1stcam').ids.textInput5DLY.focus == True:
                temp = "??j5"
                tempInput = (self.root.get_screen('1stcam').ids.textInput5DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend15DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)



            elif self.root.get_screen('2ndcam').ids.textInput1ACC.focus == True:
                temp = "!?K1"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput1ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend21ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput1SPP.focus == True:
                temp = "!?i1"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput1SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend21SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput1SPS.focus == True:
                temp = "!?I1"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput1SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend21SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput1DLY.focus == True:
                temp = "!?j1"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput1DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend21DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('2ndcam').ids.textInput2ACC.focus == True:
                temp = "!?K2"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput2ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend22ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput2SPP.focus == True:
                temp = "!?i2"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput2SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend22SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput2SPS.focus == True:
                temp = "!?I2"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput2SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend22SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput2DLY.focus == True:
                temp = "!?j2"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput2DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend22DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('2ndcam').ids.textInput3ACC.focus == True:
                temp = "!?K3"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput3ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend23ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput3SPP.focus == True:
                temp = "!?i3"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput3SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend23SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput3SPS.focus == True:
                temp = "!?I3"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput3SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend23SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput3DLY.focus == True:
                temp = "!?j3"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput3DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend23DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('2ndcam').ids.textInput4ACC.focus == True:
                temp = "!?K4"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput4ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend24ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput4SPP.focus == True:
                temp = "!?i4"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput4SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend24SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput4SPS.focus == True:
                temp = "!?I4"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput4SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend24SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput4DLY.focus == True:
                temp = "!?j4"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput4DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend24DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('2ndcam').ids.textInput5ACC.focus == True:
                temp = "!?K5"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput5ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend25ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput5SPP.focus == True:
                temp = "!?i5"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput5SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend25SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput5SPS.focus == True:
                temp = "!?I5"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput5SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend25SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('2ndcam').ids.textInput5DLY.focus == True:
                temp = "!?j5"
                tempInput = (self.root.get_screen('2ndcam').ids.textInput5DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend25DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            




            elif self.root.get_screen('3rdcam').ids.textInput1ACC.focus == True:
                temp = "@?K1"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput1ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend31ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput1SPP.focus == True:
                temp = "@?i1"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput1SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend31SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput1SPS.focus == True:
                temp = "@?I1"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput1SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend31SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput1DLY.focus == True:
                temp = "@?j1"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput1DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend31DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('3rdcam').ids.textInput2ACC.focus == True:
                temp = "@?K2"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput2ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend32ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput2SPP.focus == True:
                temp = "@?i2"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput2SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend32SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput2SPS.focus == True:
                temp = "@?I2"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput2SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend32SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput2DLY.focus == True:
                temp = "@?j2"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput2DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend32DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('3rdcam').ids.textInput3ACC.focus == True:
                temp = "@?K3"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput3ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend33ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput3SPP.focus == True:
                temp = "@?i3"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput3SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend33SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput3SPS.focus == True:
                temp = "@?I3"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput3SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend33SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput3DLY.focus == True:
                temp = "@?j3"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput3DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend33DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('3rdcam').ids.textInput4ACC.focus == True:
                temp = "@?K4"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput4ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend34ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput4SPP.focus == True:
                temp = "@?i4"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput4SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend34SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput4SPS.focus == True:
                temp = "@?I4"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput4SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend34SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput4DLY.focus == True:
                temp = "@?j4"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput4DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend34DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            elif self.root.get_screen('3rdcam').ids.textInput5ACC.focus == True:
                temp = "@?K5"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput5ACC.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend35ACC,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput5SPP.focus == True:
                temp = "@?i5"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput5SPP.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend35SPP,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput5SPS.focus == True:
                temp = "@?I5"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput5SPS.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend35SPS,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)
            elif self.root.get_screen('3rdcam').ids.textInput5DLY.focus == True:
                temp = "@?j5"
                tempInput = (self.root.get_screen('3rdcam').ids.textInput5DLY.text)
                temp += tempInput
                if self.serial_port and self.serial_port.is_open:
                    self.sendSerial(str(temp.encode()))
                    Clock.schedule_once(partial(self.runCommandSend35DLY,tempInput), 0)
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                    textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                    if textLength > 8000:
                        self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    Clock.schedule_once(self.clearTextInput, 0)

            

            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0

    def clearTextInput(self, dt):
        self.root.get_screen('main').ids.textInput.text = ""

    def runCommandSend11ACC(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput1ACC.text = tempInput
    def runCommandSend11SPP(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput1SPP.text = tempInput
    def runCommandSend11SPS(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput1SPS.text = tempInput
    def runCommandSend11DLY(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput1DLY.text = tempInput

    def runCommandSend12ACC(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput2ACC.text = tempInput
    def runCommandSend12SPP(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput2SPP.text = tempInput
    def runCommandSend12SPS(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput2SPS.text = tempInput
    def runCommandSend12DLY(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput2DLY.text = tempInput

    def runCommandSend13ACC(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput3ACC.text = tempInput
    def runCommandSend13SPP(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput3SPP.text = tempInput
    def runCommandSend13SPS(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput3SPS.text = tempInput
    def runCommandSend13DLY(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput3DLY.text = tempInput

    def runCommandSend14ACC(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput4ACC.text = tempInput
    def runCommandSend14SPP(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput4SPP.text = tempInput
    def runCommandSend14SPS(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput4SPS.text = tempInput
    def runCommandSend14DLY(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput4DLY.text = tempInput

    def runCommandSend15ACC(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput5ACC.text = tempInput
    def runCommandSend15SPP(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput5SPP.text = tempInput
    def runCommandSend15SPS(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput5SPS.text = tempInput
    def runCommandSend15DLY(self, tempInput, dt):
        self.root.get_screen('1stcam').ids.textInput5DLY.text = tempInput


    

    def runCommandSend21ACC(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput1ACC.text = tempInput
    def runCommandSend21SPP(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput1SPP.text = tempInput
    def runCommandSend21SPS(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput1SPS.text = tempInput
    def runCommandSend21DLY(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput1DLY.text = tempInput

    def runCommandSend22ACC(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput2ACC.text = tempInput
    def runCommandSend22SPP(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput2SPP.text = tempInput
    def runCommandSend22SPS(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput2SPS.text = tempInput
    def runCommandSend22DLY(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput2DLY.text = tempInput

    def runCommandSend23ACC(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput3ACC.text = tempInput
    def runCommandSend23SPP(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput3SPP.text = tempInput
    def runCommandSend23SPS(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput3SPS.text = tempInput
    def runCommandSend23DLY(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput3DLY.text = tempInput

    def runCommandSend24ACC(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput4ACC.text = tempInput
    def runCommandSend24SPP(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput4SPP.text = tempInput
    def runCommandSend24SPS(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput4SPS.text = tempInput
    def runCommandSend24DLY(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput4DLY.text = tempInput

    def runCommandSend25ACC(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput5ACC.text = tempInput
    def runCommandSend25SPP(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput5SPP.text = tempInput
    def runCommandSend25SPS(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput5SPS.text = tempInput
    def runCommandSend25DLY(self, tempInput, dt):
        self.root.get_screen('2ndcam').ids.textInput5DLY.text = tempInput

    

    def runCommandSend31ACC(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput1ACC.text = tempInput
    def runCommandSend31SPP(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput1SPP.text = tempInput
    def runCommandSend31SPS(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput1SPS.text = tempInput
    def runCommandSend31DLY(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput1DLY.text = tempInput

    def runCommandSend32ACC(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput2ACC.text = tempInput
    def runCommandSend32SPP(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput2SPP.text = tempInput
    def runCommandSend32SPS(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput2SPS.text = tempInput
    def runCommandSend32DLY(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput2DLY.text = tempInput

    def runCommandSend33ACC(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput3ACC.text = tempInput
    def runCommandSend33SPP(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput3SPP.text = tempInput
    def runCommandSend33SPS(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput3SPS.text = tempInput
    def runCommandSend33DLY(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput3DLY.text = tempInput

    def runCommandSend34ACC(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput4ACC.text = tempInput
    def runCommandSend34SPP(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput4SPP.text = tempInput
    def runCommandSend34SPS(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput4SPS.text = tempInput
    def runCommandSend34DLY(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput4DLY.text = tempInput

    def runCommandSend35ACC(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput5ACC.text = tempInput
    def runCommandSend35SPP(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput5SPP.text = tempInput
    def runCommandSend35SPS(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput5SPS.text = tempInput
    def runCommandSend35DLY(self, tempInput, dt):
        self.root.get_screen('3rdcam').ids.textInput5DLY.text = tempInput

    def showPorts(self, dt):
        #self.root.get_screen('main').ids.OSCSend.text = "OSC Server Port: " + str(srvPort)
        #self.root.get_screen('main').ids.OSCRec.text = "OSC Client Port: " + str(cliPort)
        return

    def setWhichCam(self, dt):
        self.whichCam = "1"

    def stopping(self, dt):
        global whileLoopRun
        global device_name

        whileLoopRun = False
        if device_name is not None:
            Serial.close(device_name)

        Clock.schedule_once(self.exitNow, 0)

    def exitNow(self, dt):
        sys.exit()

    def start_event_loop_thread(self):
        """Start the asyncio event loop thread. Bound to the top button."""
        if self.event_loop_worker is not None:
            #print("loop event worker is not NONE")
            return
        #self.root.get_screen('main').ids.btn_OSC.text = ("OSC ON")
        self.event_loop_worker = worker =  EventLoopWorker()
        #pulse_listener_label = self.root.get_screen('main').ids.pulse_listener

        def display_on_pulse(instance, text):
            self.root.get_screen('main').ids.txtInput_read.text += text
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
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
                        self.root.get_screen('main').ids.PTJoyDot.pos = (xKeySet, yKeySet)


                    
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
            

    def on_joy_axis(self, win, stickid, axisid, value):         # Joystick
        #print(win, stickid, axisid, value)
        global axisX
        global axisY
        global axisZ
        if axisid == 3:
            axisX = int(self.scale(value, (-32768, 32767), (-255,255)))
        elif axisid == 2:
            axisY = int(self.scale(value, (-32768, 32767), (-255,255)))
        elif axisid == 0:
            axisZ = int(self.scale(value, (-32768, 32767), (-255,255)))

        self.doJoyMoves(1)





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
            self.root.get_screen('main').ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('main').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.width)
            self.root.get_screen('1stcam').ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('1stcam').ids.PTJoyDotPress.pos = ((xDivSet*18), (yDivSet*49))
            self.root.get_screen('2ndcam').ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('2ndcam').ids.PTJoyDotPress.pos = ((xDivSet*18), (yDivSet*49))
            self.root.get_screen('3rdcam').ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('3rdcam').ids.PTJoyDotPress.pos = ((xDivSet*18), (yDivSet*49))
        if mouseSlClick and not sliderKeyPressed:
            mouseSlClick = False
            self.root.get_screen('main').ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('main').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.width)
            self.root.get_screen('1stcam').ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('1stcam').ids.SlJoyDotPress.pos = ((xDivSet*18), (yDivSet*27))
            self.root.get_screen('2ndcam').ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('2ndcam').ids.SlJoyDotPress.pos = ((xDivSet*18), (yDivSet*27))
            self.root.get_screen('3rdcam').ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('3rdcam').ids.SlJoyDotPress.pos = ((xDivSet*18), (yDivSet*27))

        if cam1isZooming:
            self.sendCam1ZoomStop()
        if cam2isZooming:
            self.sendCam2ZoomStop()
        if cam3isZooming:
            self.sendCam3ZoomStop()
        if cam4isZooming:
            self.sendCam4ZoomStop()
        if cam5isZooming:
            self.sendCam5ZoomStop()

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
            
            self.root.get_screen('main').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('main').ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))
            self.root.get_screen('1stcam').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('1stcam').ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))
            self.root.get_screen('2ndcam').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('2ndcam').ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))
            self.root.get_screen('3rdcam').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('3rdcam').ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))

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

            self.root.get_screen('main').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('main').ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)
            self.root.get_screen('1stcam').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('1stcam').ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)
            self.root.get_screen('2ndcam').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('2ndcam').ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)
            self.root.get_screen('3rdcam').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            self.root.get_screen('3rdcam').ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)

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
            cam1AtPos7 = False
            cam1AtPos8 = False
            cam1AtPos9 = False
            cam1AtPos10 = False
        elif whichCamSerial == 2:
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
        elif whichCamSerial == 3:
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
        elif whichCamSerial == 4:
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
        elif whichCamSerial == 5:
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
        
        if (SetPosToggle == True and state == 3) or state == 0:
            SetPosToggle = False
            client.send_message("/setPos", 0)
            client.send_message("/press/bank/4/8", 0)
            client.send_message("/press/bank/5/8", 0)
            client.send_message("/press/bank/6/8", 0)
            client.send_message("/style/bgcolor/4/8", [0, 0, 0])
            client.send_message("/style/bgcolor/5/8", [0, 0, 0])
            client.send_message("/style/bgcolor/6/8", [0, 0, 0])
            self.root.get_screen('main').ids.setPos.background_color = get_color_from_hex("#666666")
        elif (SetPosToggle == False and state == 3) or state == 1:
            SetPosToggle = True
            client.send_message("/setPos", 1)
            client.send_message("/press/bank/4/8", 1)
            client.send_message("/press/bank/5/8", 1)
            client.send_message("/press/bank/6/8", 1)
            client.send_message("/style/bgcolor/4/8", [255, 0, 0])
            client.send_message("/style/bgcolor/5/8", [255, 0, 0])
            client.send_message("/style/bgcolor/6/8", [255, 0, 0])
            self.root.get_screen('main').ids.setPos.background_color = get_color_from_hex("#7D0000")


    def sendCam1RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1.')

    def sendCam2RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('2.')

    def sendCam3RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3.')

    def sendCam4RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4.')

    def sendCam5RecordToggle(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5.')

    def sendCam1RecordToggleOSC(self):
        self.sendSerial('&1.')

    def sendCam2RecordToggleOSC(self):
        self.sendSerial('&2.')

    def sendCam3RecordToggleOSC(self):
        self.sendSerial('&3.')

    def sendCam4RecordToggleOSC(self):
        self.sendSerial('&4.')

    def sendCam5RecordToggleOSC(self):
        self.sendSerial('&5.')

    def on_btn_scan_release(self):
        global btn_scan_show
        global xDivSet
        global yDivSet
        global longestSerial
        global whichCamSerial
        global SetPosToggle

        if SetPosToggle:
            self.stopping(1)

        if not btn_scan_show:
            btn_scan_show = True
            
            self.uiDict['box_list1'].clear_widgets()
            self.uiDict['box_list2'].clear_widgets()
            self.uiDict['box_list3'].clear_widgets()
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
            usb_port3 = '/dev/ttyACM0'
            
            if (usb_port in '\t'.join(self.device_name_list)):
                try:
                    serialPortSelect = [string for string in self.device_name_list if usb_port in string]
                    self.autoSerial(serialPortSelect, 1)
                    print(usb_port)
                except:
                    pass
            elif (usb_port2 in '\t'.join(self.device_name_list)):
                try:
                    serialPortSelect = [string for string in self.device_name_list if usb_port2 in string]
                    self.autoSerial(serialPortSelect, 1)
                    print(usb_port2)
                except:
                    pass
            elif (usb_port3 in '\t'.join(self.device_name_list)):
                try:
                    serialPortSelect = [string for string in self.device_name_list if usb_port3 in string]
                    self.autoSerial(serialPortSelect, 1)
                    print(usb_port3)
                except:
                    pass
            else:
                for device_name in self.device_name_list:
                    btnText = device_name
                    if len(btnText) > longestSerial:
                        longestSerial = len(btnText)
                    button = Button(text=btnText, size_hint_y=None, height='60dp')
                    button.bind(on_release=self.on_btn_device_release)
                    if whichCamSerial == 1:
                        self.uiDict['box_list1'].add_widget(button)
                    elif whichCamSerial == 2:
                        self.uiDict['box_list2'].add_widget(button)
                    elif whichCamSerial == 3:
                        self.uiDict['box_list3'].add_widget(button)
                if whichCamSerial == 1:
                    self.root.get_screen('1stcam').ids.scanDD.pos = (((xDivSet*110)-(xDivSet*(longestSerial/2))), ((yDivSet*65) - ((yDivSet*7.4) * len(usb_device_list))))
                elif whichCamSerial == 2:
                    self.root.get_screen('2ndcam').ids.scanDD.pos = (((xDivSet*110)-(xDivSet*(longestSerial/2))), ((yDivSet*65) - ((yDivSet*7.4) * len(usb_device_list))))
                elif whichCamSerial == 3:
                    self.root.get_screen('3rdcam').ids.scanDD.pos = (((xDivSet*110)-(xDivSet*(longestSerial/2))), ((yDivSet*65) - ((yDivSet*7.4) * len(usb_device_list))))
                
                if platform == "win32" or platform == "Windows" or platform == "win":
                    if whichCamSerial == 1:
                        self.root.get_screen('1stcam').ids.box_list1.size = (((xDivSet*(longestSerial*1.4))), 0)
                    elif whichCamSerial == 2:
                        self.root.get_screen('2ndcam').ids.box_list2.size = (((xDivSet*(longestSerial*1.4))), 0)
                    elif whichCamSerial == 3:
                        self.root.get_screen('3rdcam').ids.box_list3.size = (((xDivSet*(longestSerial*1.4))), 0)
                else:
                    if whichCamSerial == 1:
                        self.root.get_screen('1stcam').ids.box_list1.size = (((xDivSet*(longestSerial*0.8))), 0)
                    elif whichCamSerial == 2:
                        self.root.get_screen('2ndcam').ids.box_list2.size = (((xDivSet*(longestSerial*0.8))), 0)
                    elif whichCamSerial == 3:
                        self.root.get_screen('3rdcam').ids.box_list3.size = (((xDivSet*(longestSerial*0.8))), 0)
        else:
            btn_scan_show = False
            self.uiDict['box_list1'].clear_widgets()
            self.uiDict['box_list2'].clear_widgets()
            self.uiDict['box_list3'].clear_widgets()


    def on_btn_help_release(self):
        global btn_help_show

        if not btn_help_show:
            btn_help_show = True

            self.root.get_screen('1stcam').ids.helpLabel.visible =  True
            self.root.get_screen('1stcam').ids.helpCanvas.visible =  True
            self.root.get_screen('2ndcam').ids.helpLabel.visible =  True
            self.root.get_screen('2ndcam').ids.helpCanvas.visible =  True
            self.root.get_screen('3rdcam').ids.helpLabel.visible =  True
            self.root.get_screen('3rdcam').ids.helpCanvas.visible =  True
        elif btn_help_show:
            btn_help_show = False

            self.root.get_screen('1stcam').ids.helpLabel.visible =  False
            self.root.get_screen('1stcam').ids.helpCanvas.visible =  False
            self.root.get_screen('2ndcam').ids.helpLabel.visible =  False
            self.root.get_screen('2ndcam').ids.helpCanvas.visible =  False
            self.root.get_screen('3rdcam').ids.helpLabel.visible =  False
            self.root.get_screen('3rdcam').ids.helpCanvas.visible =  False

    def autoSerial(self, serialPortSelect, dt):
        global btn_scan_show
        global USBrequsted
        global device
        global device_name
        global serialLoop
        global NotConnectedColour
        global ConnectedColour

        btn_scan_show = False
        device_name = serialPortSelect[0]
        self.root.get_screen('main').ids.txtInput_read.text += ("Connecting to: " + device_name + "\n")
        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        
        if platform == 'android':
            device = usb.get_usb_device(device_name)
            if USBrequsted:
                previousTicks = time.time() + 5
                if usb.has_usb_permission(device):
                    self.root.get_screen('main').ids.txtInput_read.text += "USB permissions received.\n"
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    USBrequsted = False
                else:
                    self.root.get_screen('main').ids.txtInput_read.text += "USB permissions declined.\n"
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    USBrequsted = False
            else:
                if not device:
                    self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(No devices found)\n"
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    return
                if not usb.has_usb_permission(device):
                    self.root.get_screen('main').ids.txtInput_read.text += "Requesting USB permissions.\n"
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    usb.request_usb_permission(device)
                    USBrequsted = True
                    Clock.schedule_once(self.doConnect, 1)
                    return
            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return
        else:
            try:
                self.serial_port = Serial(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return
            
        if self.serial_port.is_open and not self.read_thread:
            self.read_thread = threading.Thread(target = self.read_msg_thread)
            serialLoop = True
            self.read_thread.start()
            self.root.get_screen('main').ids.txtInput_read.text += "Serial connection made (auto).\n"
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.whichCamSerial1()
            self.sendSerial('&!')
            self.root.get_screen('main').ids.serialConnected.md_bg_color = 0.1, 0.7, 0.1, 1 #serialConnected
            self.root.get_screen('main').ids.serialConnected.text = "Connected"
        else :
            self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n"
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
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
                self.root.get_screen('main').ids.txtInput_read.text += "USB permissions received.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                USBrequsted = False
            else:
                self.root.get_screen('main').ids.txtInput_read.text += "USB permissions declined.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                USBrequsted = False

            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                USBrequsted = False
                return

            if self.read_thread:
                self.read_thread.kill()
            if self.serial_port.is_open and not self.read_thread:
                self.read_thread = threading.Thread(target = self.read_msg_thread)
                serialLoop = True
                self.read_thread.start()
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection made 2.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                self.whichCamSerial1()
                self.sendSerial('&!')
            else :
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n" + str(self.read_thread)
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                self.serial_port.close()
            return
        
    def on_btn_device_release(self, btn):
        global serialLoop
        global serialConnection

        device_name = btn.text
        self.root.get_screen('main').ids.txtInput_read.text += ("Connecting to: " + device_name + "\n")
        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        
        self.uiDict['box_list1'].clear_widgets()
        self.uiDict['box_list2'].clear_widgets()
        self.uiDict['box_list3'].clear_widgets()

        if platform == 'android':
            device = usb.get_usb_device(device_name)
            if not device:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(No devices found)\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                serialConnection = False
                return
            if not usb.has_usb_permission(device):
                self.root.get_screen('main').ids.txtInput_read.text += "Requesting USB permissions.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                usb.request_usb_permission(device)

                try:
                    self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
                except:
                    if usb.has_usb_permission(device):
                        self.root.get_screen('main').ids.txtInput_read.text += "USB permissions active.\nConnect again.\n"
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                    else:
                        self.root.get_screen('main').ids.txtInput_read.text += "USB permissinos not set.\nTry again\n"
                        self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                        return

            try:
                self.serial_port = serial4a.get_serial_port(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Get serial port)\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                serialConnection = False
                return
        else:
            try:
                self.serial_port = Serial(device_name, 38400, 8, 'N', 1, timeout=1)
            except:
                self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n"
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
                serialConnection = False
                return

        if self.serial_port.is_open and not self.read_thread:
            self.read_thread = threading.Thread(target = self.read_msg_thread)
            serialLoop = True
            self.read_thread.start()
            self.root.get_screen('main').ids.txtInput_read.text += "Serial connection made (selection).\n"
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.whichCamSerial1()
            self.sendSerial('&!')
            serialConnection = True
        else :
            self.root.get_screen('main').ids.txtInput_read.text += "Serial connection failed.\n(Port open, thread = none)\n"
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            serialConnection = False
    
    def btnToRunPage(self):
        pass

    def btnRunCam1(self):
        try:
            self.sendSerial('??J')
        except:
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0
       
    def btnRunCam2(self):
        try:
            self.sendSerial('!?J')
        except :
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0

    def btnRunCam3(self):
        try:
            self.sendSerial('@?J')
        except :
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0


    def btnRunCamM1(self):
        try:
            self.sendSerial('??L')
        except:
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0
       
    def btnRunCamM2(self):
        try:
            self.sendSerial('!?L')
        except :
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0

    def btnRunCamM3(self):
        try:
            self.sendSerial('@?L')
        except :
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
            self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
            self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0


    def btnReport(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&1r')
        elif whichCamSerial == 2:
            self.sendSerial('&2r')
        elif whichCamSerial == 3:
            self.sendSerial('&3r')
        elif whichCamSerial == 4:
            self.sendSerial('&4r')
        elif whichCamSerial == 5:
            self.sendSerial('&5r')
            
    def btnReportPos(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&1R')
        elif whichCamSerial == 2:
            self.sendSerial('&2R')
        elif whichCamSerial == 3:
            self.sendSerial('&3R')
        elif whichCamSerial == 4:
            self.sendSerial('&4R')
        elif whichCamSerial == 5:
            self.sendSerial('&5R')

    def btnReportKey(self):
        global whichCamSerial
        if whichCamSerial == 1:
            self.sendSerial('&1k')
        elif whichCamSerial == 2:
            self.sendSerial('&2k')
        elif whichCamSerial == 3:
            self.sendSerial('&3k')
        elif whichCamSerial == 4:
            self.sendSerial('&4k')
        elif whichCamSerial == 5:
            self.sendSerial('&5k')
    
    def read_msg_thread(self):
        global msg
        global serialLoop

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
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed
        global oldCam4Speed
        global oldCam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed
        global oldCam4PTSpeed
        global oldCam5PTSpeed

        while serialLoop:
            global whileLoopRun
            received_msg = ""
            if whileLoopRun == False:
                serialLoop = False
            #try:
            if not self.serial_port.is_open:
                serialLoop = False
            else:
                #try:
                while (self.serial_port.in_waiting > 0):
                    received_msg = self.serial_port.readline()#read_until(b'\n')
                    msg = bytes(received_msg).decode('utf8', "ignore")
                    self.readSerial(msg)
                #if received_msg:
                #    msg = bytes(received_msg).decode('utf8', "ignore")
                #    self.readSerial(msg)
                '''
                except:
                    self.on_stop()
                    self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Serial Port disconnected.\n[/color]"
                    self.root.get_screen('main').ids.scroll_view.scroll_y = 0
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
                '''
                
    @mainthread
    def readSerial(self, msg):
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
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed
        global oldCam4Speed
        global oldCam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed
        global oldCam4PTSpeed
        global oldCam5PTSpeed

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        global Cam4TextColour
        global Cam5TextColour

        global whichCamRead

        global xDivSet
        global yDivSet

        print(msg)
        textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
        if textLength > 8000:
            self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]

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
                self.root.get_screen('main').ids.cam1Record.background_color = get_color_from_hex("#666666")
                self.root.get_screen('main').ids.cam1Record.text = "Record"
                client.send_message("/style/bgcolor/4/16", [50, 50, 50])
            elif msg[1:4] == "124":
                cam1isRecording = True
                self.root.get_screen('main').ids.cam1Record.background_color = get_color_from_hex("#7D0000")
                self.root.get_screen('main').ids.cam1Record.text = "Recording"
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
                self.root.get_screen('main').ids.cam2Record.background_color = get_color_from_hex("#666666")
                self.root.get_screen('main').ids.cam2Record.text = "Record"
                client.send_message("/style/bgcolor/5/16", [50, 50, 50])
            elif msg[1:4] == "224":
                cam2isRecording = True
                self.root.get_screen('main').ids.cam2Record.background_color = get_color_from_hex("#7D0000")
                self.root.get_screen('main').ids.cam2Record.text = "Recording"
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
                self.root.get_screen('main').ids.cam3Record.background_color = get_color_from_hex("#666666")
                self.root.get_screen('main').ids.cam3Record.text = "Record"
                client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "324":
                cam3isRecording = True
                self.root.get_screen('main').ids.cam3Record.background_color = get_color_from_hex("#7D0000")
                self.root.get_screen('main').ids.cam3Record.text = "Recording"
                client.send_message("/style/bgcolor/6/16", [225, 0, 0])
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
                self.root.get_screen('main').ids.cam4Record.background_color = get_color_from_hex("#666666")
                self.root.get_screen('main').ids.cam4Record.text = "Record"
                client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "424":
                cam4isRecording = True
                self.root.get_screen('main').ids.cam4Record.background_color = get_color_from_hex("#7D0000")
                self.root.get_screen('main').ids.cam4Record.text = "Recording"
                client.send_message("/style/bgcolor/6/16", [225, 0, 0])
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
                self.root.get_screen('main').ids.cam5Record.background_color = get_color_from_hex("#666666")
                self.root.get_screen('main').ids.cam5Record.text = "Record"
                client.send_message("/style/bgcolor/6/16", [50, 50, 50])
            elif msg[1:4] == "524":
                cam5isRecording = True
                self.root.get_screen('main').ids.cam5Record.background_color = get_color_from_hex("#7D0000")
                self.root.get_screen('main').ids.cam5Record.text = "Recording"
                client.send_message("/style/bgcolor/6/16", [225, 0, 0])
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
        elif msg[0:2] == "#$":
            return
        elif msg[0:4] == "Cam1":
            whichCamRead = 1
            self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam2":
            whichCamRead = 2
            self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam3":
            whichCamRead = 3
            self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam4":
            whichCamRead = 4
            self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam4TextColour + "]" + msg + "[/color]")
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        elif msg[0:4] == "Cam5":
            whichCamRead = 5
            self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam5TextColour + "]" + msg + "[/color]")
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        else:
            if whichCamRead == 1:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam1TextColour + "]" + msg + "[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            elif whichCamRead == 2:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam2TextColour + "]" + msg + "[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            elif whichCamRead == 3:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam3TextColour + "]" + msg + "[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            elif whichCamRead == 4:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam4TextColour + "]" + msg + "[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            elif whichCamRead == 5:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=" + Cam5TextColour + "]" + msg + "[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
            else:
                self.root.get_screen('main').ids.txtInput_read.text += ("[color=ffffff]") + msg + ("[/color]")
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        msg = ''

        self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
        self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
        self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0

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
        global oldCam1Speed
        global oldCam2Speed
        global oldCam3Speed
        global oldCam4Speed
        global oldCam5Speed

        global cam1PTSpeed
        global cam2PTSpeed
        global cam3PTSpeed
        global cam4PTSpeed
        global cam5PTSpeed
        global oldCam1PTSpeed
        global oldCam2PTSpeed
        global oldCam3PTSpeed
        global oldCam4PTSpeed
        global oldCam5PTSpeed

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
                self.root.get_screen('main').ids.btnCam1Go1.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go1.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/1", [18, 70, 19])
                client.send_message("/style/color/3/1", [255, 0, 0])
                client.send_message("/style/bgcolor/4/1", [18, 70, 19])
                client.send_message("/style/color/4/1", [255, 0, 0])
            elif cam1Pos1Set and not cam1Pos1Run and cam1AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam1Go1.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go1.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/1", [48, 186, 49])
                client.send_message("/style/color/3/1", [255, 255, 255])
                client.send_message("/style/bgcolor/4/1", [48, 186, 49])
                client.send_message("/style/color/4/1", [255, 255, 255])
            elif not cam1Pos1Set:
                self.root.get_screen('main').ids.btnCam1Go1.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go1.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/1", [18, 70, 19])
                client.send_message("/style/color/3/1", [0, 0, 0])
                client.send_message("/style/bgcolor/4/1", [18, 70, 19])
                client.send_message("/style/color/4/1", [0, 0, 0])

        if cam1Pos2Set != OLDcam1Pos2Set or cam1Pos2Run != OLDcam1Pos2Run or cam1AtPos2 != OLDcam1AtPos2 or resetButtons:
            OLDcam1Pos2Set = cam1Pos2Set
            OLDcam1Pos2Run = cam1Pos2Run
            OLDcam1AtPos2 = cam1AtPos2
            if cam1Pos2Set and not cam1Pos2Run and not cam1AtPos2:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go2.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/2", [18, 70, 19])
                client.send_message("/style/color/3/2", [255, 0, 0])
                client.send_message("/style/bgcolor/4/2", [18, 70, 19])
                client.send_message("/style/color/4/2", [255, 0, 0])
            elif cam1Pos2Set and not cam1Pos2Run and cam1AtPos2:
                self.root.get_screen('main').ids.btnCam1Go2.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/2", [48, 186, 49])
                client.send_message("/style/color/3/2", [255, 255, 255])
                client.send_message("/style/bgcolor/4/2", [48, 186, 49])
                client.send_message("/style/color/4/2", [255, 255, 255])
            elif not cam1Pos2Set:
                self.root.get_screen('main').ids.btnCam1Go2.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/2", [18, 70, 19])
                client.send_message("/style/color/3/2", [0, 0, 0])
                client.send_message("/style/bgcolor/4/2", [18, 70, 19])
                client.send_message("/style/color/4/2", [0, 0, 0])

        if cam1Pos3Set != OLDcam1Pos3Set or cam1Pos3Run != OLDcam1Pos3Run or cam1AtPos3 != OLDcam1AtPos3 or resetButtons:
            OLDcam1Pos3Set = cam1Pos3Set
            OLDcam1Pos3Run = cam1Pos3Run
            OLDcam1AtPos3 = cam1AtPos3
            if cam1Pos3Set and not cam1Pos3Run and not cam1AtPos3:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go3.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/3", [18, 70, 19])
                client.send_message("/style/color/3/3", [255, 0, 0])
                client.send_message("/style/bgcolor/4/3", [18, 70, 19])
                client.send_message("/style/color/4/3", [255, 0, 0])
            elif cam1Pos3Set and not cam1Pos3Run and cam1AtPos3:
                self.root.get_screen('main').ids.btnCam1Go3.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/3", [48, 186, 49])
                client.send_message("/style/color/3/3", [255, 255, 255])
                client.send_message("/style/bgcolor/4/3", [48, 186, 49])
                client.send_message("/style/color/4/3", [255, 255, 255])
            elif not cam1Pos3Set:
                self.root.get_screen('main').ids.btnCam1Go3.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/3", [18, 70, 19])
                client.send_message("/style/color/3/3", [0, 0, 0])
                client.send_message("/style/bgcolor/4/3", [18, 70, 19])
                client.send_message("/style/color/4/3", [0, 0, 0])

        if cam1Pos4Set != OLDcam1Pos4Set or cam1Pos4Run != OLDcam1Pos4Run or cam1AtPos4 != OLDcam1AtPos4 or resetButtons:
            OLDcam1Pos4Set = cam1Pos4Set
            OLDcam1Pos4Run = cam1Pos4Run
            OLDcam1AtPos4 = cam1AtPos4
            if cam1Pos4Set and not cam1Pos4Run and not cam1AtPos4:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go4.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/4", [18, 70, 19])
                client.send_message("/style/color/3/4", [255, 0, 0])
                client.send_message("/style/bgcolor/4/4", [18, 70, 19])
                client.send_message("/style/color/4/4", [255, 0, 0])
            elif cam1Pos4Set and not cam1Pos4Run and cam1AtPos4:
                self.root.get_screen('main').ids.btnCam1Go4.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/4", [48, 186, 49])
                client.send_message("/style/color/3/4", [255, 255, 255])
                client.send_message("/style/bgcolor/4/4", [48, 186, 49])
                client.send_message("/style/color/4/4", [255, 255, 255])
            elif not cam1Pos4Set:
                self.root.get_screen('main').ids.btnCam1Go4.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/4", [18, 70, 19])
                client.send_message("/style/color/3/4", [0, 0, 0])
                client.send_message("/style/bgcolor/4/4", [18, 70, 19])
                client.send_message("/style/color/4/4", [0, 0, 0])

        if cam1Pos5Set != OLDcam1Pos5Set or cam1Pos5Run != OLDcam1Pos5Run or cam1AtPos5 != OLDcam1AtPos5 or resetButtons:
            OLDcam1Pos5Set = cam1Pos5Set
            OLDcam1Pos5Run = cam1Pos5Run
            OLDcam1AtPos5 = cam1AtPos5
            if cam1Pos5Set and not cam1Pos5Run and not cam1AtPos5:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go5.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/5", [18, 70, 19])
                client.send_message("/style/color/3/5", [255, 0, 0])
                client.send_message("/style/bgcolor/4/5", [18, 70, 19])
                client.send_message("/style/color/4/5", [255, 0, 0])
            elif cam1Pos5Set and not cam1Pos5Run and cam1AtPos5:
                self.root.get_screen('main').ids.btnCam1Go5.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/5", [48, 186, 49])
                client.send_message("/style/color/3/5", [255, 255, 255])
                client.send_message("/style/bgcolor/4/5", [48, 186, 49])
                client.send_message("/style/color/4/5", [255, 255, 255])
            elif not cam1Pos5Set:
                self.root.get_screen('main').ids.btnCam1Go5.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/5", [18, 70, 19])
                client.send_message("/style/color/3/5", [0, 0, 0])
                client.send_message("/style/bgcolor/4/5", [18, 70, 19])
                client.send_message("/style/color/4/5", [0, 0, 0])

        if cam1Pos6Set != OLDcam1Pos6Set or cam1Pos6Run != OLDcam1Pos6Run or cam1AtPos6 != OLDcam1AtPos6 or resetButtons:
            OLDcam1Pos6Set = cam1Pos6Set
            OLDcam1Pos6Run = cam1Pos6Run
            OLDcam1AtPos6 = cam1AtPos6
            if cam1Pos6Set and not cam1Pos6Run and not cam1AtPos6:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go6.col=(1, 0, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/6", [18, 70, 19])
                client.send_message("/style/color/3/6", [255, 0, 0])
                client.send_message("/style/bgcolor/4/6", [18, 70, 19])
                client.send_message("/style/color/4/6", [255, 0, 0])
            elif cam1Pos6Set and not cam1Pos6Run and cam1AtPos6:
                self.root.get_screen('main').ids.btnCam1Go6.col=(0, 1, 0, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/6", [48, 186, 49])
                client.send_message("/style/color/3/6", [255, 255, 255])
                client.send_message("/style/bgcolor/4/6", [48, 186, 49])
                client.send_message("/style/color/4/6", [255, 255, 255])
            elif not cam1Pos6Set:
                self.root.get_screen('main').ids.btnCam1Go6.col=(.13, .13, .13, 1)
                self.root.get_screen('1stcam').ids.btnCam1Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/6", [18, 70, 19])
                client.send_message("/style/color/3/6", [0, 0, 0])
                client.send_message("/style/bgcolor/4/6", [18, 70, 19])
                client.send_message("/style/color/4/6", [0, 0, 0])

        if cam1Pos7Set != OLDcam1Pos7Set or cam1Pos7Run != OLDcam1Pos7Run or cam1AtPos7 != OLDcam1AtPos7 or resetButtons:
            OLDcam1Pos7Set = cam1Pos7Set
            OLDcam1Pos7Run = cam1Pos7Run
            OLDcam1AtPos7 = cam1AtPos7
            if cam1Pos7Set and not cam1Pos7Run and not cam1AtPos7:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go7.col=(1, 0, 0, 1)
            elif cam1Pos7Set and not cam1Pos7Run and cam1AtPos7:
                self.root.get_screen('main').ids.btnCam1Go7.col=(0, 1, 0, 1)
            elif not cam1Pos7Set:
                self.root.get_screen('main').ids.btnCam1Go7.col=(.13, .13, .13, 1)

        if cam1Pos8Set != OLDcam1Pos8Set or cam1Pos8Run != OLDcam1Pos8Run or cam1AtPos8 != OLDcam1AtPos8 or resetButtons:
            OLDcam1Pos8Set = cam1Pos8Set
            OLDcam1Pos8Run = cam1Pos8Run
            OLDcam1AtPos8 = cam1AtPos8
            if cam1Pos8Set and not cam1Pos8Run and not cam1AtPos8:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go8.col=(1, 0, 0, 1)
            elif cam1Pos8Set and not cam1Pos8Run and cam1AtPos8:
                self.root.get_screen('main').ids.btnCam1Go8.col=(0, 1, 0, 1)
            elif not cam1Pos8Set:
                self.root.get_screen('main').ids.btnCam1Go8.col=(.13, .13, .13, 1)

        if cam1Pos9Set != OLDcam1Pos9Set or cam1Pos9Run != OLDcam1Pos9Run or cam1AtPos9 != OLDcam1AtPos9 or resetButtons:
            OLDcam1Pos9Set = cam1Pos9Set
            OLDcam1Pos9Run = cam1Pos9Run
            OLDcam1AtPos9 = cam1AtPos9
            if cam1Pos9Set and not cam1Pos9Run and not cam1AtPos9:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go9.col=(1, 0, 0, 1)
            elif cam1Pos9Set and not cam1Pos9Run and cam1AtPos9:
                self.root.get_screen('main').ids.btnCam1Go9.col=(0, 1, 0, 1)
            elif not cam1Pos9Set:
                self.root.get_screen('main').ids.btnCam1Go9.col=(.13, .13, .13, 1)

        if cam1Pos10Set != OLDcam1Pos10Set or cam1Pos10Run != OLDcam1Pos10Run or cam1AtPos10 != OLDcam1AtPos10 or resetButtons:
            OLDcam1Pos10Set = cam1Pos10Set
            OLDcam1Pos10Run = cam1Pos10Run
            OLDcam1AtPos10 = cam1AtPos10
            if cam1Pos10Set and not cam1Pos10Run and not cam1AtPos10:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go10.col=(1, 0, 0, 1)
            elif cam1Pos10Set and not cam1Pos10Run and cam1AtPos10:
                self.root.get_screen('main').ids.btnCam1Go10.col=(0, 1, 0, 1)
            elif not cam1Pos10Set:
                self.root.get_screen('main').ids.btnCam1Go10.col=(.13, .13, .13, 1)


        if cam2Pos1Set != OLDcam2Pos1Set or cam2Pos1Run != OLDcam2Pos1Run or cam2AtPos1 != OLDcam2AtPos1 or resetButtons:
            OLDcam2Pos1Set = cam2Pos1Set
            OLDcam2Pos1Run = cam2Pos1Run
            OLDcam2AtPos1 = cam2AtPos1
            if cam2Pos1Set and not cam2Pos1Run and not cam2AtPos1:                                  # Set , not Run or At
                self.root.get_screen('main').ids.btnCam2Go1.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go1.col=(1, 0, 0, 1)
                #client.send_message("/Cam2Go1", [1, "00AAAAFF"])
                client.send_message("/style/bgcolor/3/9", [35, 50, 70])
                client.send_message("/style/color/3/9", [255, 0, 0])
                client.send_message("/style/bgcolor/5/1", [35, 50, 70])
                client.send_message("/style/color/5/1", [255, 0, 0])
            elif cam2Pos1Set and not cam2Pos1Run and cam2AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam2Go1.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go1.col=(0, 1, 0, 1)
                #client.send_message("/Cam2Go1", [1, "FFFF00FF"])
                client.send_message("/style/bgcolor/3/9", [92, 133, 186])
                client.send_message("/style/color/3/9", [255, 255, 255])
                client.send_message("/style/bgcolor/5/1", [92, 133, 186])
                client.send_message("/style/color/5/1", [255, 255, 255])
            elif not cam2Pos1Set:
                self.root.get_screen('main').ids.btnCam2Go1.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go1.col=(.13, .13, .13, 1)
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
                self.root.get_screen('main').ids.btnCam2Go2.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/10", [35, 50, 70])
                client.send_message("/style/color/3/10", [255, 0, 0])
                client.send_message("/style/bgcolor/5/2", [35, 50, 70])
                client.send_message("/style/color/5/2", [255, 0, 0])
            elif cam2Pos2Set and not cam2Pos2Run and cam2AtPos2:
                self.root.get_screen('main').ids.btnCam2Go2.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/10", [92, 133, 186])
                client.send_message("/style/color/3/10", [255, 255, 255])
                client.send_message("/style/bgcolor/5/2", [92, 133, 186])
                client.send_message("/style/color/5/2", [255, 255, 255])
            elif not cam2Pos2Set:
                self.root.get_screen('main').ids.btnCam2Go2.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/10", [35, 50, 70])
                client.send_message("/style/color/3/10", [0, 0, 0])
                client.send_message("/style/bgcolor/5/2", [35, 50, 70])
                client.send_message("/style/color/5/2", [0, 0, 0])

        if cam2Pos3Set != OLDcam2Pos3Set or cam2Pos3Run != OLDcam2Pos3Run or cam2AtPos3 != OLDcam2AtPos3 or resetButtons:
            OLDcam2Pos3Set = cam2Pos3Set
            OLDcam2Pos3Run = cam2Pos3Run
            OLDcam2AtPos3 = cam2AtPos3
            if cam2Pos3Set and not cam2Pos3Run and not cam2AtPos3:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go3.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/11", [35, 50, 70])
                client.send_message("/style/color/3/11", [255, 0, 0])
                client.send_message("/style/bgcolor/5/3", [35, 50, 70])
                client.send_message("/style/color/5/3", [255, 0, 0])
            elif cam2Pos3Set and not cam2Pos3Run and cam2AtPos3:
                self.root.get_screen('main').ids.btnCam2Go3.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/11", [92, 133, 186])
                client.send_message("/style/color/3/11", [255, 255, 255])
                client.send_message("/style/bgcolor/5/3", [92, 133, 186])
                client.send_message("/style/color/5/3", [255, 255, 255])
            elif not cam2Pos3Set:
                self.root.get_screen('main').ids.btnCam2Go3.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/11", [35, 50, 70])
                client.send_message("/style/color/3/11", [0, 0, 0])
                client.send_message("/style/bgcolor/5/3", [35, 50, 70])
                client.send_message("/style/color/5/3", [0, 0, 0])

        if cam2Pos4Set != OLDcam2Pos4Set or cam2Pos4Run != OLDcam2Pos4Run or cam2AtPos4 != OLDcam2AtPos4 or resetButtons:
            OLDcam2Pos4Set = cam2Pos4Set
            OLDcam2Pos4Run = cam2Pos4Run
            OLDcam2AtPos4 = cam2AtPos4
            if cam2Pos4Set and not cam2Pos4Run and not cam2AtPos4:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go4.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/12", [35, 50, 70])
                client.send_message("/style/color/3/12", [255, 0, 0])
                client.send_message("/style/bgcolor/5/4", [35, 50, 70])
                client.send_message("/style/color/5/4", [255, 0, 0])
            elif cam2Pos4Set and not cam2Pos4Run and cam2AtPos4:
                self.root.get_screen('main').ids.btnCam2Go4.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/12", [92, 133, 186])
                client.send_message("/style/color/3/12", [255, 255, 255])
                client.send_message("/style/bgcolor/5/4", [92, 133, 186])
                client.send_message("/style/color/5/4", [255, 255, 255])
            elif not cam2Pos4Set:
                self.root.get_screen('main').ids.btnCam2Go4.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/12", [35, 50, 70])
                client.send_message("/style/color/3/12", [0, 0, 0])
                client.send_message("/style/bgcolor/5/4", [35, 50, 70])
                client.send_message("/style/color/5/4", [0, 0, 0])

        if cam2Pos5Set != OLDcam2Pos5Set or cam2Pos5Run != OLDcam2Pos5Run or cam2AtPos5 != OLDcam2AtPos5 or resetButtons:
            OLDcam2Pos5Set = cam2Pos5Set
            OLDcam2Pos5Run = cam2Pos5Run
            OLDcam2AtPos5 = cam2AtPos5
            if cam2Pos5Set and not cam2Pos5Run and not cam2AtPos5:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go5.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/13", [35, 50, 70])
                client.send_message("/style/color/3/13", [255, 0, 0])
                client.send_message("/style/bgcolor/5/5", [35, 50, 70])
                client.send_message("/style/color/5/5", [255, 0, 0])
            elif cam2Pos5Set and not cam2Pos5Run and cam2AtPos5:
                self.root.get_screen('main').ids.btnCam2Go5.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/13", [92, 133, 186])
                client.send_message("/style/color/3/13", [255, 255, 255])
                client.send_message("/style/bgcolor/5/5", [92, 133, 186])
                client.send_message("/style/color/5/5", [255, 255, 255])
            elif not cam2Pos5Set:
                self.root.get_screen('main').ids.btnCam2Go5.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/13", [35, 50, 70])
                client.send_message("/style/color/3/13", [0, 0, 0])
                client.send_message("/style/bgcolor/5/5", [35, 50, 70])
                client.send_message("/style/color/5/5", [0, 0, 0])

        if cam2Pos6Set != OLDcam2Pos6Set or cam2Pos6Run != OLDcam2Pos6Run or cam2AtPos6 != OLDcam2AtPos6 or resetButtons:
            OLDcam2Pos6Set = cam2Pos6Set
            OLDcam2Pos6Run = cam2Pos6Run
            OLDcam2AtPos6 = cam2AtPos6
            if cam2Pos6Set and not cam2Pos6Run and not cam2AtPos6:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go6.col=(1, 0, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/14", [35, 50, 70])
                client.send_message("/style/color/3/14", [255, 0, 0])
                client.send_message("/style/bgcolor/5/6", [35, 50, 70])
                client.send_message("/style/color/5/6", [255, 0, 0])
            elif cam2Pos6Set and not cam2Pos6Run and cam2AtPos6:
                self.root.get_screen('main').ids.btnCam2Go6.col=(0, 1, 0, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/14", [92, 133, 186])
                client.send_message("/style/color/3/14", [255, 255, 255])
                client.send_message("/style/bgcolor/5/6", [92, 133, 186])
                client.send_message("/style/color/5/6", [255, 255, 255])
            elif not cam2Pos6Set:
                self.root.get_screen('main').ids.btnCam2Go6.col=(.13, .13, .13, 1)
                self.root.get_screen('2ndcam').ids.btnCam2Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/14", [35, 50, 70])
                client.send_message("/style/color/3/14", [0, 0, 0])
                client.send_message("/style/bgcolor/5/6", [35, 50, 70])
                client.send_message("/style/color/5/6", [0, 0, 0])

        if cam2Pos7Set != OLDcam2Pos7Set or cam2Pos7Run != OLDcam2Pos7Run or cam2AtPos7 != OLDcam2AtPos7 or resetButtons:
            OLDcam2Pos7Set = cam2Pos7Set
            OLDcam2Pos7Run = cam2Pos7Run
            OLDcam2AtPos7 = cam2AtPos7
            if cam2Pos7Set and not cam2Pos7Run and not cam2AtPos7:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go7.col=(1, 0, 0, 1)
            elif cam2Pos7Set and not cam2Pos7Run and cam2AtPos7:
                self.root.get_screen('main').ids.btnCam2Go7.col=(0, 1, 0, 1)
            elif not cam2Pos7Set:
                self.root.get_screen('main').ids.btnCam2Go7.col=(.13, .13, .13, 1)

        if cam2Pos8Set != OLDcam2Pos8Set or cam2Pos8Run != OLDcam2Pos8Run or cam2AtPos8 != OLDcam2AtPos8 or resetButtons:
            OLDcam2Pos8Set = cam2Pos8Set
            OLDcam2Pos8Run = cam2Pos8Run
            OLDcam2AtPos8 = cam2AtPos8
            if cam2Pos8Set and not cam2Pos8Run and not cam2AtPos8:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go8.col=(1, 0, 0, 1)
            elif cam2Pos8Set and not cam2Pos8Run and cam2AtPos8:
                self.root.get_screen('main').ids.btnCam2Go8.col=(0, 1, 0, 1)
            elif not cam2Pos8Set:
                self.root.get_screen('main').ids.btnCam2Go8.col=(.13, .13, .13, 1)

        if cam2Pos9Set != OLDcam2Pos9Set or cam2Pos9Run != OLDcam2Pos9Run or cam2AtPos9 != OLDcam2AtPos9 or resetButtons:
            OLDcam2Pos9Set = cam2Pos9Set
            OLDcam2Pos9Run = cam2Pos9Run
            OLDcam2AtPos9 = cam2AtPos9
            if cam2Pos9Set and not cam2Pos9Run and not cam2AtPos9:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go9.col=(1, 0, 0, 1)
            elif cam2Pos9Set and not cam2Pos9Run and cam2AtPos9:
                self.root.get_screen('main').ids.btnCam2Go9.col=(0, 1, 0, 1)
            elif not cam2Pos9Set:
                self.root.get_screen('main').ids.btnCam2Go9.col=(.13, .13, .13, 1)

        if cam2Pos10Set != OLDcam2Pos10Set or cam2Pos10Run != OLDcam2Pos10Run or cam2AtPos10 != OLDcam2AtPos10 or resetButtons:
            OLDcam2Pos10Set = cam2Pos10Set
            OLDcam2Pos10Run = cam2Pos10Run
            OLDcam2AtPos10 = cam2AtPos10
            if cam2Pos10Set and not cam2Pos10Run and not cam2AtPos10:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go10.col=(1, 0, 0, 1)
            elif cam2Pos10Set and not cam2Pos10Run and cam2AtPos10:
                self.root.get_screen('main').ids.btnCam2Go10.col=(0, 1, 0, 1)
            elif not cam2Pos10Set:
                self.root.get_screen('main').ids.btnCam2Go10.col=(.13, .13, .13, 1)



        if cam3Pos1Set != OLDcam3Pos1Set or cam3Pos1Run != OLDcam3Pos1Run or cam3AtPos1 != OLDcam3AtPos1 or resetButtons:
            OLDcam3Pos1Set = cam3Pos1Set
            OLDcam3Pos1Run = cam3Pos1Run
            OLDcam3AtPos1 = cam3AtPos1
            if cam3Pos1Set and not cam3Pos1Run and not cam3AtPos1:                                  # Set , not Run or At
                self.root.get_screen('main').ids.btnCam3Go1.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go1.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/17", [70, 62, 1])
                client.send_message("/style/color/3/17", [255, 0, 0])
                client.send_message("/style/bgcolor/6/1", [70, 62, 1])
                client.send_message("/style/color/6/1", [255, 0, 0])
            elif cam3Pos1Set and not cam3Pos1Run and cam3AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam3Go1.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go1.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/17", [186, 164, 1])
                client.send_message("/style/color/3/17", [255, 255, 255])
                client.send_message("/style/bgcolor/6/1", [186, 164, 1])
                client.send_message("/style/color/6/1", [255, 255, 255])
            elif not cam3Pos1Set:
                self.root.get_screen('main').ids.btnCam3Go1.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go1.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/17", [70, 62, 1])
                client.send_message("/style/color/3/17", [0, 0, 0])
                client.send_message("/style/bgcolor/6/1", [70, 62, 1])
                client.send_message("/style/color/6/1", [0, 0, 0])

        if cam3Pos2Set != OLDcam3Pos2Set or cam3Pos2Run != OLDcam3Pos2Run or cam3AtPos2 != OLDcam3AtPos2 or resetButtons:
            OLDcam3Pos2Set = cam3Pos2Set
            OLDcam3Pos2Run = cam3Pos2Run
            OLDcam3AtPos2 = cam3AtPos2
            if cam3Pos2Set and not cam3Pos2Run and not cam3AtPos2:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go2.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go2.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/18", [70, 62, 1])
                client.send_message("/style/color/3/18", [255, 0, 0])
                client.send_message("/style/bgcolor/6/2", [70, 62, 1])
                client.send_message("/style/color/6/2", [255, 0, 0])
            elif cam3Pos2Set and not cam3Pos2Run and cam3AtPos2:
                self.root.get_screen('main').ids.btnCam3Go2.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go2.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/18", [186, 164, 1])
                client.send_message("/style/color/3/18", [255, 255, 255])
                client.send_message("/style/bgcolor/6/2", [186, 164, 1])
                client.send_message("/style/color/6/2", [255, 255, 255])
            elif not cam3Pos2Set:
                self.root.get_screen('main').ids.btnCam3Go2.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go2.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/18", [70, 62, 1])
                client.send_message("/style/color/3/18", [0, 0, 0])
                client.send_message("/style/bgcolor/6/2", [70, 62, 1])
                client.send_message("/style/color/6/2", [0, 0, 0])

        if cam3Pos3Set != OLDcam3Pos3Set or cam3Pos3Run != OLDcam3Pos3Run or cam3AtPos3 != OLDcam3AtPos3 or resetButtons:
            OLDcam3Pos3Set = cam3Pos3Set
            OLDcam3Pos3Run = cam3Pos3Run
            OLDcam3AtPos3 = cam3AtPos3
            if cam3Pos3Set and not cam3Pos3Run and not cam3AtPos3:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go3.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go3.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/19", [70, 62, 1])
                client.send_message("/style/color/3/19", [255, 0, 0])
                client.send_message("/style/bgcolor/6/3", [70, 62, 1])
                client.send_message("/style/color/6/3", [255, 0, 0])
            elif cam3Pos3Set and not cam3Pos3Run and cam3AtPos3:
                self.root.get_screen('main').ids.btnCam3Go3.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go3.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/19", [186, 164, 1])
                client.send_message("/style/color/3/19", [255, 255, 255])
                client.send_message("/style/bgcolor/6/3", [186, 164, 1])
                client.send_message("/style/color/6/3", [255, 255, 255])
            elif not cam3Pos3Set:
                self.root.get_screen('main').ids.btnCam3Go3.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go3.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/19", [70, 62, 1])
                client.send_message("/style/color/3/19", [0, 0, 0])
                client.send_message("/style/bgcolor/6/3", [70, 62, 1])
                client.send_message("/style/color/6/3", [0, 0, 0])

        if cam3Pos4Set != OLDcam3Pos4Set or cam3Pos4Run != OLDcam3Pos4Run or cam3AtPos4 != OLDcam3AtPos4 or resetButtons:
            OLDcam3Pos4Set = cam3Pos4Set
            OLDcam3Pos4Run = cam3Pos4Run
            OLDcam3AtPos4 = cam3AtPos4
            if cam3Pos4Set and not cam3Pos4Run and not cam3AtPos4:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go4.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go4.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/20", [70, 62, 1])
                client.send_message("/style/color/3/20", [255, 0, 0])
                client.send_message("/style/bgcolor/6/4", [70, 62, 1])
                client.send_message("/style/color/6/4", [255, 0, 0])
            elif cam3Pos4Set and not cam3Pos4Run and cam3AtPos4:
                self.root.get_screen('main').ids.btnCam3Go4.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go4.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/20", [186, 164, 1])
                client.send_message("/style/color/3/20", [255, 255, 255])
                client.send_message("/style/bgcolor/6/4", [186, 164, 1])
                client.send_message("/style/color/6/4", [255, 255, 255])
            elif not cam3Pos4Set:
                self.root.get_screen('main').ids.btnCam3Go4.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go4.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/20", [70, 62, 1])
                client.send_message("/style/color/3/20", [0, 0, 0])
                client.send_message("/style/bgcolor/6/4", [70, 62, 1])
                client.send_message("/style/color/6/4", [0, 0, 0])

        if cam3Pos5Set != OLDcam3Pos5Set or cam3Pos5Run != OLDcam3Pos5Run or cam3AtPos5 != OLDcam3AtPos5 or resetButtons:
            OLDcam3Pos5Set = cam3Pos5Set
            OLDcam3Pos5Run = cam3Pos5Run
            OLDcam3AtPos5 = cam3AtPos5
            if cam3Pos5Set and not cam3Pos5Run and not cam3AtPos5:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go5.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go5.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/21", [70, 62, 1])
                client.send_message("/style/color/3/21", [255, 0, 0])
                client.send_message("/style/bgcolor/6/5", [70, 62, 1])
                client.send_message("/style/color/6/5", [255, 0, 0])
            elif cam3Pos5Set and not cam3Pos5Run and cam3AtPos5:
                self.root.get_screen('main').ids.btnCam3Go5.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go5.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/21", [186, 164, 1])
                client.send_message("/style/color/3/21", [255, 255, 255])
                client.send_message("/style/bgcolor/6/5", [186, 164, 1])
                client.send_message("/style/color/6/5", [255, 255, 255])
            elif not cam3Pos5Set:
                self.root.get_screen('main').ids.btnCam3Go5.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go5.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/21", [70, 62, 1])
                client.send_message("/style/color/3/21", [0, 0, 0])
                client.send_message("/style/bgcolor/6/5", [70, 62, 1])
                client.send_message("/style/color/6/5", [0, 0, 0])

        if cam3Pos6Set != OLDcam3Pos6Set or cam3Pos6Run != OLDcam3Pos6Run or cam3AtPos6 != OLDcam3AtPos6 or resetButtons:
            OLDcam3Pos6Set = cam3Pos6Set
            OLDcam3Pos6Run = cam3Pos6Run
            OLDcam3AtPos6 = cam3AtPos6
            if cam3Pos6Set and not cam3Pos6Run and not cam3AtPos6:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go6.col=(1, 0, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go6.col=(1, 0, 0, 1)
                client.send_message("/style/bgcolor/3/22", [70, 62, 1])
                client.send_message("/style/color/3/22", [255, 0, 0])
                client.send_message("/style/bgcolor/6/6", [70, 62, 1])
                client.send_message("/style/color/6/6", [255, 0, 0])
            elif cam3Pos6Set and not cam3Pos6Run and cam3AtPos6:
                self.root.get_screen('main').ids.btnCam3Go6.col=(0, 1, 0, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go6.col=(0, 1, 0, 1)
                client.send_message("/style/bgcolor/3/22", [186, 164, 1])
                client.send_message("/style/color/3/22", [255, 255, 255])
                client.send_message("/style/bgcolor/6/6", [186, 164, 1])
                client.send_message("/style/color/6/6", [255, 255, 255])
            elif not cam3Pos6Set:
                self.root.get_screen('main').ids.btnCam3Go6.col=(.13, .13, .13, 1)
                self.root.get_screen('3rdcam').ids.btnCam3Go6.col=(.13, .13, .13, 1)
                client.send_message("/style/bgcolor/3/22", [70, 62, 1])
                client.send_message("/style/color/3/22", [0, 0, 0])
                client.send_message("/style/bgcolor/6/6", [70, 62, 1])
                client.send_message("/style/color/6/6", [0, 0, 0])

        if cam3Pos7Set != OLDcam3Pos7Set or cam3Pos7Run != OLDcam3Pos7Run or cam3AtPos7 != OLDcam3AtPos7 or resetButtons:
            OLDcam3Pos7Set = cam3Pos7Set
            OLDcam3Pos7Run = cam3Pos7Run
            OLDcam3AtPos7 = cam3AtPos7
            if cam3Pos7Set and not cam3Pos7Run and not cam3AtPos7:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go7.col=(1, 0, 0, 1)
            elif cam3Pos7Set and not cam3Pos7Run and cam3AtPos7:
                self.root.get_screen('main').ids.btnCam3Go7.col=(0, 1, 0, 1)
            elif not cam3Pos7Set:
                self.root.get_screen('main').ids.btnCam3Go7.col=(.13, .13, .13, 1)

        if cam3Pos8Set != OLDcam3Pos8Set or cam3Pos8Run != OLDcam3Pos8Run or cam3AtPos8 != OLDcam3AtPos8 or resetButtons:
            OLDcam3Pos8Set = cam3Pos8Set
            OLDcam3Pos8Run = cam3Pos8Run
            OLDcam3AtPos8 = cam3AtPos8
            if cam3Pos8Set and not cam3Pos8Run and not cam3AtPos8:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go8.col=(1, 0, 0, 1)
            elif cam3Pos8Set and not cam3Pos8Run and cam3AtPos8:
                self.root.get_screen('main').ids.btnCam3Go8.col=(0, 1, 0, 1)
            elif not cam3Pos8Set:
                self.root.get_screen('main').ids.btnCam3Go8.col=(.13, .13, .13, 1)

        if cam3Pos9Set != OLDcam3Pos9Set or cam3Pos9Run != OLDcam3Pos9Run or cam3AtPos9 != OLDcam3AtPos9 or resetButtons:
            OLDcam3Pos9Set = cam3Pos9Set
            OLDcam3Pos9Run = cam3Pos9Run
            OLDcam3AtPos9 = cam3AtPos9
            if cam3Pos9Set and not cam3Pos9Run and not cam3AtPos9:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go9.col=(1, 0, 0, 1)
            elif cam3Pos9Set and not cam3Pos9Run and cam3AtPos9:
                self.root.get_screen('main').ids.btnCam3Go9.col=(0, 1, 0, 1)
            elif not cam3Pos9Set:
                self.root.get_screen('main').ids.btnCam3Go9.col=(.13, .13, .13, 1)

        if cam3Pos10Set != OLDcam3Pos10Set or cam3Pos10Run != OLDcam3Pos10Run or cam3AtPos10 != OLDcam3AtPos10 or resetButtons:
            OLDcam3Pos10Set = cam3Pos10Set
            OLDcam3Pos10Run = cam3Pos10Run
            OLDcam3AtPos10 = cam3AtPos10
            if cam3Pos10Set and not cam3Pos10Run and not cam3AtPos10:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go10.col=(1, 0, 0, 1)
            elif cam3Pos10Set and not cam3Pos10Run and cam3AtPos10:
                self.root.get_screen('main').ids.btnCam3Go10.col=(0, 1, 0, 1)
            elif not cam3Pos10Set:
                self.root.get_screen('main').ids.btnCam3Go10.col=(.13, .13, .13, 1)




        if cam4Pos1Set != OLDcam4Pos1Set or cam4Pos1Run != OLDcam4Pos1Run or cam4AtPos1 != OLDcam4AtPos1 or resetButtons:
            OLDcam4Pos1Set = cam4Pos1Set
            OLDcam4Pos1Run = cam4Pos1Run
            OLDcam4AtPos1 = cam4AtPos1
            if cam4Pos1Set and not cam4Pos1Run and not cam4AtPos1:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go1.col=(1, 0, 0, 1)
            elif cam4Pos1Set and not cam4Pos1Run and cam4AtPos1:
                self.root.get_screen('main').ids.btnCam4Go1.col=(0, 1, 0, 1)
            elif not cam4Pos1Set:
                self.root.get_screen('main').ids.btnCam4Go1.col=(.13, .13, .13, 1)

        if cam4Pos2Set != OLDcam4Pos2Set or cam4Pos2Run != OLDcam4Pos2Run or cam4AtPos2 != OLDcam4AtPos2 or resetButtons:
            OLDcam4Pos2Set = cam4Pos2Set
            OLDcam4Pos2Run = cam4Pos2Run
            OLDcam4AtPos2 = cam4AtPos2
            if cam4Pos2Set and not cam4Pos2Run and not cam4AtPos2:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go2.col=(1, 0, 0, 1)
            elif cam4Pos2Set and not cam4Pos2Run and cam4AtPos2:
                self.root.get_screen('main').ids.btnCam4Go2.col=(0, 1, 0, 1)
            elif not cam4Pos2Set:
                self.root.get_screen('main').ids.btnCam4Go2.col=(.13, .13, .13, 1)

        if cam4Pos3Set != OLDcam4Pos3Set or cam4Pos3Run != OLDcam4Pos3Run or cam4AtPos3 != OLDcam4AtPos3 or resetButtons:
            OLDcam4Pos3Set = cam4Pos3Set
            OLDcam4Pos3Run = cam4Pos3Run
            OLDcam4AtPos3 = cam4AtPos3
            if cam4Pos3Set and not cam4Pos3Run and not cam4AtPos3:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go3.col=(1, 0, 0, 1)
            elif cam4Pos3Set and not cam4Pos3Run and cam4AtPos3:
                self.root.get_screen('main').ids.btnCam4Go3.col=(0, 1, 0, 1)
            elif not cam4Pos3Set:
                self.root.get_screen('main').ids.btnCam4Go3.col=(.13, .13, .13, 1)

        if cam4Pos4Set != OLDcam4Pos4Set or cam4Pos4Run != OLDcam4Pos4Run or cam4AtPos4 != OLDcam4AtPos4 or resetButtons:
            OLDcam4Pos4Set = cam4Pos4Set
            OLDcam4Pos4Run = cam4Pos4Run
            OLDcam4AtPos4 = cam4AtPos4
            if cam4Pos4Set and not cam4Pos4Run and not cam4AtPos4:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go4.col=(1, 0, 0, 1)
            elif cam4Pos4Set and not cam4Pos4Run and cam4AtPos4:
                self.root.get_screen('main').ids.btnCam4Go4.col=(0, 1, 0, 1)
            elif not cam4Pos4Set:
                self.root.get_screen('main').ids.btnCam4Go4.col=(.13, .13, .13, 1)

        if cam4Pos5Set != OLDcam4Pos5Set or cam4Pos5Run != OLDcam4Pos5Run or cam4AtPos5 != OLDcam4AtPos5 or resetButtons:
            OLDcam4Pos5Set = cam4Pos5Set
            OLDcam4Pos5Run = cam4Pos5Run
            OLDcam4AtPos5 = cam4AtPos5
            if cam4Pos5Set and not cam4Pos5Run and not cam4AtPos5:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go5.col=(1, 0, 0, 1)
            elif cam4Pos5Set and not cam4Pos5Run and cam4AtPos5:
                self.root.get_screen('main').ids.btnCam4Go5.col=(0, 1, 0, 1)
            elif not cam4Pos5Set:
                self.root.get_screen('main').ids.btnCam4Go5.col=(.13, .13, .13, 1)

        if cam4Pos6Set != OLDcam4Pos6Set or cam4Pos6Run != OLDcam4Pos6Run or cam4AtPos6 != OLDcam4AtPos6 or resetButtons:
            OLDcam4Pos6Set = cam4Pos6Set
            OLDcam4Pos6Run = cam4Pos6Run
            OLDcam4AtPos6 = cam4AtPos6
            if cam4Pos6Set and not cam4Pos6Run and not cam4AtPos6:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go6.col=(1, 0, 0, 1)
            elif cam4Pos6Set and not cam4Pos6Run and cam4AtPos6:
                self.root.get_screen('main').ids.btnCam4Go6.col=(0, 1, 0, 1)
            elif not cam4Pos6Set:
                self.root.get_screen('main').ids.btnCam4Go6.col=(.13, .13, .13, 1)

        if cam4Pos7Set != OLDcam4Pos7Set or cam4Pos7Run != OLDcam4Pos7Run or cam4AtPos7 != OLDcam4AtPos7 or resetButtons:
            OLDcam4Pos7Set = cam4Pos7Set
            OLDcam4Pos7Run = cam4Pos7Run
            OLDcam4AtPos7 = cam4AtPos7
            if cam4Pos7Set and not cam4Pos7Run and not cam4AtPos7:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go7.col=(1, 0, 0, 1)
            elif cam4Pos7Set and not cam4Pos7Run and cam4AtPos7:
                self.root.get_screen('main').ids.btnCam4Go7.col=(0, 1, 0, 1)
            elif not cam4Pos7Set:
                self.root.get_screen('main').ids.btnCam4Go7.col=(.13, .13, .13, 1)

        if cam4Pos8Set != OLDcam4Pos8Set or cam4Pos8Run != OLDcam4Pos8Run or cam4AtPos8 != OLDcam4AtPos8 or resetButtons:
            OLDcam4Pos8Set = cam4Pos8Set
            OLDcam4Pos8Run = cam4Pos8Run
            OLDcam4AtPos8 = cam4AtPos8
            if cam4Pos8Set and not cam4Pos8Run and not cam4AtPos8:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go8.col=(1, 0, 0, 1)
            elif cam4Pos8Set and not cam4Pos8Run and cam4AtPos8:
                self.root.get_screen('main').ids.btnCam4Go8.col=(0, 1, 0, 1)
            elif not cam4Pos8Set:
                self.root.get_screen('main').ids.btnCam4Go8.col=(.13, .13, .13, 1)

        if cam4Pos9Set != OLDcam4Pos9Set or cam4Pos9Run != OLDcam4Pos9Run or cam4AtPos9 != OLDcam4AtPos9 or resetButtons:
            OLDcam4Pos9Set = cam4Pos9Set
            OLDcam4Pos9Run = cam4Pos9Run
            OLDcam4AtPos9 = cam4AtPos9
            if cam4Pos9Set and not cam4Pos9Run and not cam4AtPos9:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go9.col=(1, 0, 0, 1)
            elif cam4Pos9Set and not cam4Pos9Run and cam4AtPos9:
                self.root.get_screen('main').ids.btnCam4Go9.col=(0, 1, 0, 1)
            elif not cam4Pos9Set:
                self.root.get_screen('main').ids.btnCam4Go9.col=(.13, .13, .13, 1)

        if cam4Pos10Set != OLDcam4Pos10Set or cam4Pos10Run != OLDcam4Pos10Run or cam4AtPos10 != OLDcam4AtPos10 or resetButtons:
            OLDcam4Pos10Set = cam4Pos10Set
            OLDcam4Pos10Run = cam4Pos10Run
            OLDcam4AtPos10 = cam4AtPos10
            if cam4Pos10Set and not cam4Pos10Run and not cam4AtPos10:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go10.col=(1, 0, 0, 1)
            elif cam4Pos10Set and not cam4Pos10Run and cam4AtPos10:
                self.root.get_screen('main').ids.btnCam4Go10.col=(0, 1, 0, 1)
            elif not cam4Pos10Set:
                self.root.get_screen('main').ids.btnCam4Go10.col=(.13, .13, .13, 1)


        

        if cam5Pos1Set != OLDcam5Pos1Set or cam5Pos1Run != OLDcam5Pos1Run or cam5AtPos1 != OLDcam5AtPos1 or resetButtons:
            OLDcam5Pos1Set = cam5Pos1Set
            OLDcam5Pos1Run = cam5Pos1Run
            OLDcam5AtPos1 = cam5AtPos1
            if cam5Pos1Set and not cam5Pos1Run and not cam5AtPos1:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go1.col=(1, 0, 0, 1)
            elif cam5Pos1Set and not cam5Pos1Run and cam5AtPos1:
                self.root.get_screen('main').ids.btnCam5Go1.col=(0, 1, 0, 1)
            elif not cam5Pos1Set:
                self.root.get_screen('main').ids.btnCam5Go1.col=(.13, .13, .13, 1)

        if cam5Pos2Set != OLDcam5Pos2Set or cam5Pos2Run != OLDcam5Pos2Run or cam5AtPos2 != OLDcam5AtPos2 or resetButtons:
            OLDcam5Pos2Set = cam5Pos2Set
            OLDcam5Pos2Run = cam5Pos2Run
            OLDcam5AtPos2 = cam5AtPos2
            if cam5Pos2Set and not cam5Pos2Run and not cam5AtPos2:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go2.col=(1, 0, 0, 1)
            elif cam5Pos2Set and not cam5Pos2Run and cam5AtPos2:
                self.root.get_screen('main').ids.btnCam5Go2.col=(0, 1, 0, 1)
            elif not cam5Pos2Set:
                self.root.get_screen('main').ids.btnCam5Go2.col=(.13, .13, .13, 1)

        if cam5Pos3Set != OLDcam5Pos3Set or cam5Pos3Run != OLDcam5Pos3Run or cam5AtPos3 != OLDcam5AtPos3 or resetButtons:
            OLDcam5Pos3Set = cam5Pos3Set
            OLDcam5Pos3Run = cam5Pos3Run
            OLDcam5AtPos3 = cam5AtPos3
            if cam5Pos3Set and not cam5Pos3Run and not cam5AtPos3:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go3.col=(1, 0, 0, 1)
            elif cam5Pos3Set and not cam5Pos3Run and cam5AtPos3:
                self.root.get_screen('main').ids.btnCam5Go3.col=(0, 1, 0, 1)
            elif not cam5Pos3Set:
                self.root.get_screen('main').ids.btnCam5Go3.col=(.13, .13, .13, 1)
                self.root.get_screen('main').ids.btnCam5Go3.col=(.13, .13, .13, 1)

        if cam5Pos4Set != OLDcam5Pos4Set or cam5Pos4Run != OLDcam5Pos4Run or cam5AtPos4 != OLDcam5AtPos4 or resetButtons:
            OLDcam5Pos4Set = cam5Pos4Set
            OLDcam5Pos4Run = cam5Pos4Run
            OLDcam5AtPos4 = cam5AtPos4
            if cam5Pos4Set and not cam5Pos4Run and not cam5AtPos4:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go4.col=(1, 0, 0, 1)
            elif cam5Pos4Set and not cam5Pos4Run and cam5AtPos4:
                self.root.get_screen('main').ids.btnCam5Go4.col=(0, 1, 0, 1)
            elif not cam5Pos4Set:
                self.root.get_screen('main').ids.btnCam5Go4.col=(.13, .13, .13, 1)

        if cam5Pos5Set != OLDcam5Pos5Set or cam5Pos5Run != OLDcam5Pos5Run or cam5AtPos5 != OLDcam5AtPos5 or resetButtons:
            OLDcam5Pos5Set = cam5Pos5Set
            OLDcam5Pos5Run = cam5Pos5Run
            OLDcam5AtPos5 = cam5AtPos5
            if cam5Pos5Set and not cam5Pos5Run and not cam5AtPos5:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go5.col=(1, 0, 0, 1)
            elif cam5Pos5Set and not cam5Pos5Run and cam5AtPos5:
                self.root.get_screen('main').ids.btnCam5Go5.col=(0, 1, 0, 1)
            elif not cam5Pos5Set:
                self.root.get_screen('main').ids.btnCam5Go5.col=(.13, .13, .13, 1)

        if cam5Pos6Set != OLDcam5Pos6Set or cam5Pos6Run != OLDcam5Pos6Run or cam5AtPos6 != OLDcam5AtPos6 or resetButtons:
            OLDcam5Pos6Set = cam5Pos6Set
            OLDcam5Pos6Run = cam5Pos6Run
            OLDcam5AtPos6 = cam5AtPos6
            if cam5Pos6Set and not cam5Pos6Run and not cam5AtPos6:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go6.col=(1, 0, 0, 1)
            elif cam5Pos6Set and not cam5Pos6Run and cam5AtPos6:
                self.root.get_screen('main').ids.btnCam5Go6.col=(0, 1, 0, 1)
            elif not cam5Pos6Set:
                self.root.get_screen('main').ids.btnCam5Go6.col=(.13, .13, .13, 1)

        if cam5Pos7Set != OLDcam5Pos7Set or cam5Pos7Run != OLDcam5Pos7Run or cam5AtPos7 != OLDcam5AtPos7 or resetButtons:
            OLDcam5Pos7Set = cam5Pos7Set
            OLDcam5Pos7Run = cam5Pos7Run
            OLDcam5AtPos7 = cam5AtPos7
            if cam5Pos7Set and not cam5Pos7Run and not cam5AtPos7:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go7.col=(1, 0, 0, 1)
            elif cam5Pos7Set and not cam5Pos7Run and cam5AtPos7:
                self.root.get_screen('main').ids.btnCam5Go7.col=(0, 1, 0, 1)
            elif not cam5Pos7Set:
                self.root.get_screen('main').ids.btnCam5Go7.col=(.13, .13, .13, 1)

        if cam5Pos8Set != OLDcam5Pos8Set or cam5Pos8Run != OLDcam5Pos8Run or cam5AtPos8 != OLDcam5AtPos8 or resetButtons:
            OLDcam5Pos8Set = cam5Pos8Set
            OLDcam5Pos8Run = cam5Pos8Run
            OLDcam5AtPos8 = cam5AtPos8
            if cam5Pos8Set and not cam5Pos8Run and not cam5AtPos8:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go8.col=(1, 0, 0, 1)
            elif cam5Pos8Set and not cam5Pos8Run and cam5AtPos8:
                self.root.get_screen('main').ids.btnCam5Go8.col=(0, 1, 0, 1)
            elif not cam5Pos8Set:
                self.root.get_screen('main').ids.btnCam5Go8.col=(.13, .13, .13, 1)

        if cam5Pos9Set != OLDcam5Pos9Set or cam5Pos9Run != OLDcam5Pos9Run or cam5AtPos9 != OLDcam5AtPos9 or resetButtons:
            OLDcam5Pos9Set = cam5Pos9Set
            OLDcam5Pos9Run = cam5Pos9Run
            OLDcam5AtPos9 = cam5AtPos9
            if cam5Pos9Set and not cam5Pos9Run and not cam5AtPos9:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go9.col=(1, 0, 0, 1)
            elif cam5Pos9Set and not cam5Pos9Run and cam5AtPos9:
                self.root.get_screen('main').ids.btnCam5Go9.col=(0, 1, 0, 1)
            elif not cam5Pos9Set:
                self.root.get_screen('main').ids.btnCam5Go9.col=(.13, .13, .13, 1)

        if cam5Pos10Set != OLDcam5Pos10Set or cam5Pos10Run != OLDcam5Pos10Run or cam5AtPos10 != OLDcam5AtPos10 or resetButtons:
            OLDcam5Pos10Set = cam5Pos10Set
            OLDcam5Pos10Run = cam5Pos10Run
            OLDcam5AtPos10 = cam5AtPos10
            if cam5Pos10Set and not cam5Pos10Run and not cam5AtPos10:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go10.col=(1, 0, 0, 1)
            elif cam5Pos10Set and not cam5Pos10Run and cam5AtPos10:
                self.root.get_screen('main').ids.btnCam5Go10.col=(0, 1, 0, 1)
            elif not cam5Pos10Set:
                self.root.get_screen('main').ids.btnCam5Go10.col=(.13, .13, .13, 1)





        if oldCam1PTSpeed != cam1PTSpeed:
            oldCam1PTSpeed = cam1PTSpeed
            client.send_message("/style/text/3/7", "-")
            if cam1PTSpeed == 1:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*8.25), (yDivSet*3))
                client.send_message("/style/text/3/8", "+ 1/4")
                client.send_message("/style/text/4/10", "Spd 1/4")
            elif cam1PTSpeed == 3:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*16.5), (yDivSet*3))
                client.send_message("/style/text/3/8", "+ 2/4")
                client.send_message("/style/text/4/10", "Spd 2/4")
            elif cam1PTSpeed == 5:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*24.75), (yDivSet*3))
                client.send_message("/style/text/3/8", "+ 3/4")
                client.send_message("/style/text/4/10", "Spd 3/4")
            elif cam1PTSpeed == 7:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*33), (yDivSet*3))
                client.send_message("/style/text/3/8", "+ 4/4")
                client.send_message("/style/text/4/10", "Spd 4/4")

        if oldCam2PTSpeed != cam2PTSpeed:
            oldCam2PTSpeed = cam2PTSpeed
            client.send_message("/style/text/3/15", "-")
            if cam2PTSpeed == 1:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*8.25), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 1/4")
                client.send_message("/style/text/5/10", "Spd 1/4")
            elif cam2PTSpeed == 3:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*16.5), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/5/10", "Spd 2/4")
            elif cam2PTSpeed == 5:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*24.75), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/5/10", "Spd 3/4")
            elif cam2PTSpeed == 7:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*33), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/5/10", "Spd 4/4")

        if oldCam3PTSpeed != cam3PTSpeed:
            oldCam3PTSpeed = cam3PTSpeed
            client.send_message("/style/text/3/23", "-")
            if cam3PTSpeed == 1:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*8.25), (yDivSet*3))
                client.send_message("/style/text/3/24", "+ 1/4")
                client.send_message("/style/text/6/10", "Spd 1/4")
            elif cam3PTSpeed == 3:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*16.5), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/6/10", "Spd 2/4")
            elif cam3PTSpeed == 5:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*24.75), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/6/10", "Spd 3/4")
            elif cam3PTSpeed == 7:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*33), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/6/10", "Spd 4/4")

        if oldCam4PTSpeed != cam4PTSpeed:
            oldCam4PTSpeed = cam4PTSpeed
            client.send_message("/style/text/3/23", "-")
            if cam4PTSpeed == 1:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*8.25), (yDivSet*3))
                client.send_message("/style/text/3/24", "+ 1/4")
                client.send_message("/style/text/6/10", "Spd 1/4")
            elif cam4PTSpeed == 3:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*16.5), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/6/10", "Spd 2/4")
            elif cam4PTSpeed == 5:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*24.75), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/6/10", "Spd 3/4")
            elif cam4PTSpeed == 7:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*33), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/6/10", "Spd 4/4")

        if oldCam5PTSpeed != cam5PTSpeed:
            oldCam5PTSpeed = cam5PTSpeed
            client.send_message("/style/text/3/23", "-")
            if cam5PTSpeed == 1:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*8.25), (yDivSet*3))
                client.send_message("/style/text/3/24", "+ 1/4")
                client.send_message("/style/text/6/10", "Spd 1/4")
            elif cam5PTSpeed == 3:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*16.5), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 2/4")
                client.send_message("/style/text/6/10", "Spd 2/4")
            elif cam5PTSpeed == 5:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*24.75), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 3/4")
                client.send_message("/style/text/6/10", "Spd 3/4")
            elif cam5PTSpeed == 7:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*33), (yDivSet*3))
                client.send_message("/style/text/3/16", "+ 4/4")
                client.send_message("/style/text/6/10", "Spd 4/4")

        if oldCam1Speed != cam1SliderSpeed:
            oldCam1Speed = cam1SliderSpeed
            if cam1SliderSpeed == 1:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*4.71), (yDivSet*3))
            elif cam1SliderSpeed == 2:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*9.43), (yDivSet*3))
            elif cam1SliderSpeed == 3:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*14.14), (yDivSet*3))
            elif cam1SliderSpeed == 4:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*18.86), (yDivSet*3))
            elif cam1SliderSpeed == 5:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*25.57), (yDivSet*3))
            elif cam1SliderSpeed == 6:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*28.29), (yDivSet*3))
            elif cam1SliderSpeed == 7:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*33), (yDivSet*3))

        if oldCam2Speed != cam2SliderSpeed:
            oldCam2Speed = cam2SliderSpeed
            if cam2SliderSpeed == 1:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*4.71), (yDivSet*3))
            elif cam2SliderSpeed == 2:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*9.43), (yDivSet*3))
            elif cam2SliderSpeed == 3:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*14.14), (yDivSet*3))
            elif cam2SliderSpeed == 4:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*18.86), (yDivSet*3))
            elif cam2SliderSpeed == 5:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*25.57), (yDivSet*3))
            elif cam2SliderSpeed == 6:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*28.29), (yDivSet*3))
            elif cam2SliderSpeed == 7:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*33), (yDivSet*3))

        if oldCam3Speed != cam3SliderSpeed:
            oldCam3Speed = cam3SliderSpeed
            if cam3SliderSpeed == 1:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*4.71), (yDivSet*3))
            elif cam3SliderSpeed == 2:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*9.43), (yDivSet*3))
            elif cam3SliderSpeed == 3:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*14.14), (yDivSet*3))
            elif cam3SliderSpeed == 4:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*18.86), (yDivSet*3))
            elif cam3SliderSpeed == 5:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*25.57), (yDivSet*3))
            elif cam3SliderSpeed == 6:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*28.29), (yDivSet*3))
            elif cam3SliderSpeed == 7:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*33), (yDivSet*3))

        if oldCam4Speed != cam4SliderSpeed:
            oldCam4Speed = cam4SliderSpeed
            if cam4SliderSpeed == 1:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*4.71), (yDivSet*3))
            elif cam4SliderSpeed == 2:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*9.43), (yDivSet*3))
            elif cam4SliderSpeed == 3:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*14.14), (yDivSet*3))
            elif cam4SliderSpeed == 4:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*18.86), (yDivSet*3))
            elif cam4SliderSpeed == 5:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*25.57), (yDivSet*3))
            elif cam4SliderSpeed == 6:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*28.29), (yDivSet*3))
            elif cam4SliderSpeed == 7:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*33), (yDivSet*3))

        if oldCam5Speed != cam5SliderSpeed:
            oldCam5Speed = cam5SliderSpeed
            if cam5SliderSpeed == 1:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*4.71), (yDivSet*3))
            elif cam5SliderSpeed == 2:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*9.43), (yDivSet*3))
            elif cam5SliderSpeed == 3:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*14.14), (yDivSet*3))
            elif cam5SliderSpeed == 4:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*18.86), (yDivSet*3))
            elif cam5SliderSpeed == 5:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*25.57), (yDivSet*3))
            elif cam5SliderSpeed == 6:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*28.29), (yDivSet*3))
            elif cam5SliderSpeed == 7:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*33), (yDivSet*3))

        resetButtons = False

    def whichCamSerial1(self):
        global whichCamSerial
        whichCamSerial = 1
        self.whichCam = "1"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('1stcam').ids.buttonWhichCam1.line_color=(1, 0, 0, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('2ndcam').ids.buttonWhichCam1.line_color=(1, 0, 0, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('3rdcam').ids.buttonWhichCam1.line_color=(1, 0, 0, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial2(self):
        global whichCamSerial
        whichCamSerial = 2
        self.whichCam = "2"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('1stcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('2ndcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('3rdcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial3(self):
        global whichCamSerial
        whichCamSerial = 3
        self.whichCam = "3"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('1stcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('2ndcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('3rdcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial4(self):
        global whichCamSerial
        whichCamSerial = 4
        self.whichCam = "4"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('1stcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam4.line_color=(1, 0, 0, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

        self.root.get_screen('2ndcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam4.line_color=(1, 0, 0, 1)

        self.root.get_screen('3rdcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam4.line_color=(1, 0, 0, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial5(self):
        global whichCamSerial
        whichCamSerial = 5
        self.whichCam = "5"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(1, 0, 0, 1)

        self.root.get_screen('1stcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('1stcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('1stcam').ids.buttonWhichCam5.line_color=(1, 0, 0, 1)

        self.root.get_screen('2ndcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('2ndcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('2ndcam').ids.buttonWhichCam5.line_color=(1, 0, 0, 1)

        self.root.get_screen('3rdcam').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('3rdcam').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        #self.root.get_screen('3rdcam').ids.buttonWhichCam5.line_color=(1, 0, 0, 1)
        
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
            self.sendSerial('&1Z')
            return
        elif cam1Pos1Set and not cam1AtPos1:
            self.sendSerial('&1z')

    def Cam1Go2(self):
        global SetPosToggle
        global cam1Pos2Set
        global cam1AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1X')
            return
        elif cam1Pos2Set and not cam1AtPos2:
            self.sendSerial('&1x')

    def Cam1Go3(self):
        global SetPosToggle
        global cam1Pos3Set
        global cam1AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1C')
            return
        elif cam1Pos3Set and not cam1AtPos3:
            self.sendSerial('&1c')

    def Cam1Go4(self):
        global SetPosToggle
        global cam1Pos4Set
        global cam1AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1V')
            return
        elif cam1Pos4Set and not cam1AtPos4:
            self.sendSerial('&1v')

    def Cam1Go5(self):
        global SetPosToggle
        global cam1Pos5Set
        global cam1AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1B')
            return
        elif cam1Pos5Set and not cam1AtPos5:
            self.sendSerial('&1b')

    def Cam1Go6(self):
        global SetPosToggle
        global cam1Pos6Set
        global cam1AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1N')
            return
        elif cam1Pos6Set and not cam1AtPos6:
            self.sendSerial('&1n')

    def Cam1Go7(self):
        global SetPosToggle
        global cam1Pos7Set
        global cam1AtPos7
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1M')
            return
        elif cam1Pos7Set and not cam1AtPos7:
            self.sendSerial('&1m')

    def Cam1Go8(self):
        global SetPosToggle
        global cam1Pos8Set
        global cam1AtPos8
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1<')
            return
        elif cam1Pos8Set and not cam1AtPos8:
            self.sendSerial('&1,')

    def Cam1Go9(self):
        global SetPosToggle
        global cam1Pos9Set
        global cam1AtPos9
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1>')
            return
        elif cam1Pos9Set and not cam1AtPos9:
            self.sendSerial('&1.')

    def Cam1Go10(self):
        global SetPosToggle
        global cam1Pos10Set
        global cam1AtPos10
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1?')
            return
        elif cam1Pos10Set and not cam1AtPos10:
            self.sendSerial('&1/')




    def Cam2Go1(self):
        global SetPosToggle
        global cam2Pos1Set
        global cam2AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2Z')
            return
        elif cam2Pos1Set and not cam2AtPos1:
            self.sendSerial('&2z')

    def Cam2Go2(self):
        global SetPosToggle
        global cam2Pos2Set
        global cam2AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2X')
            return
        elif cam2Pos2Set and not cam2AtPos2:
            self.sendSerial('&2x')

    def Cam2Go3(self):
        global SetPosToggle
        global cam2Pos3Set
        global cam2AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2C')
            return
        elif cam2Pos3Set and not cam2AtPos3:
            self.sendSerial('&2c')

    def Cam2Go4(self):
        global SetPosToggle
        global cam2Pos4Set
        global cam2AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2V')
            return
        elif cam2Pos4Set and not cam2AtPos4:
            self.sendSerial('&2v')

    def Cam2Go5(self):
        global SetPosToggle
        global cam2Pos5Set
        global cam2AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2B')
            return
        elif cam2Pos5Set and not cam2AtPos5:
            self.sendSerial('&2b')

    def Cam2Go6(self):
        global SetPosToggle
        global cam2Pos6Set
        global cam2AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2N')
            return
        elif cam2Pos6Set and not cam2AtPos6:
            self.sendSerial('&2n')

    def Cam2Go7(self):
        global SetPosToggle
        global cam2Pos7Set
        global cam2AtPos7
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2M')
            return
        elif cam2Pos7Set and not cam2AtPos7:
            self.sendSerial('&2m')

    def Cam2Go8(self):
        global SetPosToggle
        global cam2Pos8Set
        global cam2AtPos8
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2<')
            return
        elif cam2Pos8Set and not cam2AtPos8:
            self.sendSerial('&2,')

    def Cam2Go9(self):
        global SetPosToggle
        global cam2Pos9Set
        global cam2AtPos9
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2>')
            return
        elif cam2Pos9Set and not cam2AtPos9:
            self.sendSerial('&2.')

    def Cam2Go10(self):
        global SetPosToggle
        global cam2Pos10Set
        global cam2AtPos10
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2?')
            return
        elif cam2Pos10Set and not cam2AtPos10:
            self.sendSerial('&2/')




    def Cam3Go1(self):
        global SetPosToggle
        global cam3Pos1Set
        global cam3AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3Z')
            return
        elif cam3Pos1Set and not cam3AtPos1:
            self.sendSerial('&3z')

    def Cam3Go2(self):
        global SetPosToggle
        global cam3Pos2Set
        global cam3AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3X')
            return
        elif cam3Pos2Set and not cam3AtPos2:
            self.sendSerial('&3x')

    def Cam3Go3(self):
        global SetPosToggle
        global cam3Pos3Set
        global cam3AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3C')
            return
        elif cam3Pos3Set and not cam3AtPos3:
            self.sendSerial('&3c')

    def Cam3Go4(self):
        global SetPosToggle
        global cam3Pos4Set
        global cam3AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3V')
            return
        elif cam3Pos4Set and not cam3AtPos4:
            self.sendSerial('&3v')

    def Cam3Go5(self):
        global SetPosToggle
        global cam3Pos5Set
        global cam3AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3B')
            return
        elif cam3Pos5Set and not cam3AtPos5:
            self.sendSerial('&3b')

    def Cam3Go6(self):
        global SetPosToggle
        global cam3Pos6Set
        global cam3AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3N')
            return
        elif cam3Pos6Set and not cam3AtPos6:
            self.sendSerial('&3N')

    def Cam3Go7(self):
        global SetPosToggle
        global cam3Pos7Set
        global cam3AtPos7
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3M')
            return
        elif cam3Pos7Set and not cam3AtPos7:
            self.sendSerial('&3m')

    def Cam3Go8(self):
        global SetPosToggle
        global cam3Pos8Set
        global cam3AtPos8
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3<')
            return
        elif cam3Pos8Set and not cam3AtPos8:
            self.sendSerial('&3,')

    def Cam3Go9(self):
        global SetPosToggle
        global cam3Pos9Set
        global cam3AtPos9
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3>')
            return
        elif cam3Pos9Set and not cam3AtPos9:
            self.sendSerial('&3.')

    def Cam3Go10(self):
        global SetPosToggle
        global cam3Pos10Set
        global cam3AtPos10
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3?')
            return
        elif cam3Pos10Set and not cam3AtPos10:
            self.sendSerial('&3/')




    def Cam4Go1(self):
        global SetPosToggle
        global cam4Pos1Set
        global cam4AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4Z')
            return
        elif cam4Pos1Set and not cam4AtPos1:
            self.sendSerial('&4z')

    def Cam4Go2(self):
        global SetPosToggle
        global cam4Pos2Set
        global cam4AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4X')
            return
        elif cam4Pos2Set and not cam4AtPos2:
            self.sendSerial('&4x')

    def Cam4Go3(self):
        global SetPosToggle
        global cam4Pos3Set
        global cam4AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4C')
            return
        elif cam4Pos3Set and not cam4AtPos3:
            self.sendSerial('&4C')

    def Cam4Go4(self):
        global SetPosToggle
        global cam4Pos4Set
        global cam4AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4V')
            return
        elif cam4Pos4Set and not cam4AtPos4:
            self.sendSerial('&4v')

    def Cam4Go5(self):
        global SetPosToggle
        global cam4Pos5Set
        global cam4AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4B')
            return
        elif cam4Pos5Set and not cam4AtPos5:
            self.sendSerial('&4b')

    def Cam4Go6(self):
        global SetPosToggle
        global cam4Pos6Set
        global cam4AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4N')
            return
        elif cam4Pos6Set and not cam4AtPos6:
            self.sendSerial('&4n')

    def Cam4Go7(self):
        global SetPosToggle
        global cam4Pos7Set
        global cam4AtPos7
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4M')
            return
        elif cam4Pos7Set and not cam4AtPos7:
            self.sendSerial('&4m')

    def Cam4Go8(self):
        global SetPosToggle
        global cam4Pos8Set
        global cam4AtPos8
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4<')
            return
        elif cam4Pos8Set and not cam4AtPos8:
            self.sendSerial('&4,')

    def Cam4Go9(self):
        global SetPosToggle
        global cam4Pos9Set
        global cam4AtPos9
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4>')
            return
        elif cam4Pos9Set and not cam4AtPos9:
            self.sendSerial('&4.')

    def Cam4Go10(self):
        global SetPosToggle
        global cam4Pos10Set
        global cam4AtPos10
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4?')
            return
        elif cam4Pos10Set and not cam4AtPos10:
            self.sendSerial('&4/')




    def Cam5Go1(self):
        global SetPosToggle
        global cam5Pos1Set
        global cam5AtPos1
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5Z')
            return
        elif cam5Pos1Set and not cam5AtPos1:
            self.sendSerial('&5z')

    def Cam5Go2(self):
        global SetPosToggle
        global cam5Pos2Set
        global cam5AtPos2
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5X')
            return
        elif cam5Pos2Set and not cam5AtPos2:
            self.sendSerial('&5x')

    def Cam5Go3(self):
        global SetPosToggle
        global cam5Pos3Set
        global cam5AtPos3
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5C')
            return
        elif cam5Pos3Set and not cam5AtPos3:
            self.sendSerial('&5c')

    def Cam5Go4(self):
        global SetPosToggle
        global cam5Pos4Set
        global cam5AtPos4
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5V')
            return
        elif cam5Pos4Set and not cam5AtPos4:
            self.sendSerial('&5v')

    def Cam5Go5(self):
        global SetPosToggle
        global cam5Pos5Set
        global cam5AtPos5
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5B')
            return
        elif cam5Pos5Set and not cam5AtPos5:
            self.sendSerial('&5b')

    def Cam5Go6(self):
        global SetPosToggle
        global cam5Pos6Set
        global cam5AtPos6
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5N')
            return
        elif cam5Pos6Set and not cam5AtPos6:
            self.sendSerial('&5n')

    def Cam5Go7(self):
        global SetPosToggle
        global cam5Pos7Set
        global cam5AtPos7
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5M')
            return
        elif cam5Pos7Set and not cam5AtPos7:
            self.sendSerial('&5m')

    def Cam5Go8(self):
        global SetPosToggle
        global cam5Pos8Set
        global cam5AtPos8
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5<')
            return
        elif cam5Pos8Set and not cam5AtPos8:
            self.sendSerial('&5,')

    def Cam5Go9(self):
        global SetPosToggle
        global cam5Pos9Set
        global cam5AtPos9
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5>')
            return
        elif cam5Pos9Set and not cam5AtPos9:
            self.sendSerial('&5.')

    def Cam5Go10(self):
        global SetPosToggle
        global cam5Pos10Set
        global cam5AtPos10
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5?')
            return
        elif cam5Pos10Set and not cam5AtPos10:
            self.sendSerial('&5/')



    def sendCam1PTSpeedInc(self):
        global cam1PTSpeed
        if cam1PTSpeed == 1:
            self.sendSerial('&1s3')
        elif cam1PTSpeed == 3:
            self.sendSerial('&1s2')
        elif cam1PTSpeed == 5:
            self.sendSerial('&1s1')
        elif cam1PTSpeed == 7:
            return
        
    def sendCam1PTSpeedDec(self):
        global cam1PTSpeed
        if cam1PTSpeed == 7:
            self.sendSerial('&1s2')
        elif cam1PTSpeed == 5:
            self.sendSerial('&1s3')
        elif cam1PTSpeed == 3:
            self.sendSerial('&1s4')
        elif cam1PTSpeed == 1:
            return



    def sendCam2PTSpeedInc(self):
        global cam2PTSpeed
        if cam2PTSpeed == 1:
            self.sendSerial('&2s3')
        elif cam2PTSpeed == 3:
            self.sendSerial('&2s2')
        elif cam2PTSpeed == 5:
            self.sendSerial('&2s1')
        elif cam2PTSpeed == 7:
            return
        
    def sendCam2PTSpeedDec(self):
        global cam2PTSpeed
        if cam2PTSpeed == 7:
            self.sendSerial('&2s2')
        elif cam2PTSpeed == 5:
            self.sendSerial('&2s3')
        elif cam2PTSpeed == 3:
            self.sendSerial('&2s4')
        elif cam2PTSpeed == 1:
            return



    def sendCam3PTSpeedInc(self):
        global cam3PTSpeed
        if cam3PTSpeed == 1:
            self.sendSerial('&3s3')
        elif cam3PTSpeed == 3:
            self.sendSerial('&3s2')
        elif cam3PTSpeed == 5:
            self.sendSerial('&3s1')
        elif cam3PTSpeed == 7:
            return
        
    def sendCam3PTSpeedDec(self):
        global cam3PTSpeed
        if cam3PTSpeed == 7:
            self.sendSerial('&3s2')
        elif cam3PTSpeed == 5:
            self.sendSerial('&3s3')
        elif cam3PTSpeed == 3:
            self.sendSerial('&3s4')
        elif cam3PTSpeed == 1:
            return



    def sendCam4PTSpeedInc(self):
        global cam4PTSpeed
        if cam4PTSpeed == 1:
            self.sendSerial('&4s3')
        elif cam4PTSpeed == 3:
            self.sendSerial('&4s2')
        elif cam4PTSpeed == 5:
            self.sendSerial('&4s1')
        elif cam4PTSpeed == 7:
            return
        
    def sendCam4PTSpeedDec(self):
        global cam4PTSpeed
        if cam4PTSpeed == 7:
            self.sendSerial('&4s2')
        elif cam4PTSpeed == 5:
            self.sendSerial('&4s3')
        elif cam4PTSpeed == 3:
            self.sendSerial('&4s4')
        elif cam4PTSpeed == 1:
            return



    def sendCam5PTSpeedInc(self):
        global cam5PTSpeed
        if cam5PTSpeed == 1:
            self.sendSerial('&5s3')
        elif cam5PTSpeed == 5:
            self.sendSerial('&5s2')
        elif cam5PTSpeed == 5:
            self.sendSerial('&5s1')
        elif cam5PTSpeed == 7:
            return
        
    def sendCam5PTSpeedDec(self):
        global cam5PTSpeed
        if cam5PTSpeed == 7:
            self.sendSerial('&5s2')
        elif cam5PTSpeed == 5:
            self.sendSerial('&5s3')
        elif cam5PTSpeed == 5:
            self.sendSerial('&5s4')
        elif cam5PTSpeed == 1:
            return


    



    def sendCam2PTSpeedOSC(self, OSC):
        #print(OSC)
        if OSC == 0:
            self.sendSerial('&2s4')
        elif OSC == 1:
            self.sendSerial('&2s3')
        elif OSC == 2:
            self.sendSerial('&2s2')
        elif OSC == 3:
            self.sendSerial('&2s1')




    def sendCam1SliderSpeedInc(self):
        self.sendSerial('&1W')

    def sendCam1SliderSpeedDec(self):
        self.sendSerial('&1w')

    def sendCam2SliderSpeedInc(self):
        self.sendSerial('&2W')

    def sendCam2SliderSpeedDec(self):
        self.sendSerial('&2w')

    def sendCam3SliderSpeedInc(self):
        self.sendSerial('&3W')

    def sendCam3SliderSpeedDec(self):
        self.sendSerial('&3w')

    def sendCam4SliderSpeedInc(self):
        self.sendSerial('&4W')

    def sendCam4SliderSpeedDec(self):
        self.sendSerial('&4w')

    def sendCam5SliderSpeedInc(self):
        self.sendSerial('&5W')

    def sendCam5SliderSpeedDec(self):
        self.sendSerial('&5w')

    def sendCam1ZoomIn(self):
        global cam1isZooming
        cam1isZooming = True
        self.sendSerial('&1<')
    def sendCam1ZoomOut(self):
        global cam1isZooming
        cam1isZooming = True
        self.sendSerial('&1,')
    def sendCam1ZoomStop(self):
        global cam1isZooming
        cam1isZooming = False
        self.sendSerial('&1>')

    def sendCam2ZoomIn(self):
        global cam2isZooming
        cam2isZooming = True
        self.sendSerial('&2<')
    def sendCam2ZoomOut(self):
        global cam2isZooming
        cam2isZooming = True
        self.sendSerial('&2,')
    def sendCam2ZoomStop(self):
        global cam2isZooming
        cam2isZooming = False
        self.sendSerial('&2>')

    def sendCam3ZoomIn(self):
        global cam3isZooming
        cam3isZooming = True
        self.sendSerial('&3<')
    def sendCam3ZoomOut(self):
        global cam3isZooming
        cam3isZooming = True
        self.sendSerial('&3,')
    def sendCam3ZoomStop(self):
        global cam3isZooming
        cam3isZooming = False
        self.sendSerial('&3>')

    def sendCam4ZoomIn(self):
        global cam4isZooming
        cam4isZooming = True
        self.sendSerial('&4<')
    def sendCam4ZoomOut(self):
        global cam4isZooming
        cam4isZooming = True
        self.sendSerial('&4,')
    def sendCam4ZoomStop(self):
        global cam4isZooming
        cam4isZooming = False
        self.sendSerial('&4>')

    def sendCam5ZoomIn(self):
        global cam5isZooming
        cam5isZooming = True
        self.sendSerial('&5<')
    def sendCam5ZoomOut(self):
        global cam5isZooming
        cam5isZooming = True
        self.sendSerial('&5,')
    def sendCam5ZoomStop(self):
        global cam5isZooming
        cam5isZooming = False
        self.sendSerial('&5>')



    def sendClearCam1Pos(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&1D')

    def sendClearCam2Pos(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&2D')

    def sendClearCam3Pos(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&3D')

    def sendClearCam4Pos(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&4D')

    def sendClearCam5Pos(self):
        global SetPosToggle
        if SetPosToggle:
            self.setPos(3)
            self.sendSerial('&5D')


    def flash(self, dt):
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

        if cam1Pos1Run and not cam1AtPos1:
            self.root.get_screen('main').ids.btnCam1Go1.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/1", [48, 186, 49])
            client.send_message("/style/color/3/1", [200, 200, 0])
            client.send_message("/style/bgcolor/4/1", [48, 186, 49])
            client.send_message("/style/color/4/1", [200, 200, 0])
        if cam1Pos2Run and not cam1AtPos2:
            self.root.get_screen('main').ids.btnCam1Go2.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/2", [48, 186, 49])
            client.send_message("/style/color/3/2", [200, 200, 0])
            client.send_message("/style/bgcolor/4/2", [48, 186, 49])
            client.send_message("/style/color/4/2", [200, 200, 0])
        if cam1Pos3Run and not cam1AtPos3:
            self.root.get_screen('main').ids.btnCam1Go3.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/3", [48, 186, 49])
            client.send_message("/style/color/3/3", [200, 200, 0])
            client.send_message("/style/bgcolor/4/3", [48, 186, 49])
            client.send_message("/style/color/4/3", [200, 200, 0])
        if cam1Pos4Run and not cam1AtPos4:
            self.root.get_screen('main').ids.btnCam1Go4.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/4", [48, 186, 49])
            client.send_message("/style/color/3/4", [200, 200, 0])
            client.send_message("/style/bgcolor/4/4", [48, 186, 49])
            client.send_message("/style/color/4/4", [200, 200, 0])
        if cam1Pos5Run and not cam1AtPos5:
            self.root.get_screen('main').ids.btnCam1Go5.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/5", [48, 186, 49])
            client.send_message("/style/color/3/5", [200, 200, 0])
            client.send_message("/style/bgcolor/4/5", [48, 186, 49])
            client.send_message("/style/color/4/5", [200, 200, 0])
        if cam1Pos6Run and not cam1AtPos6:
            self.root.get_screen('main').ids.btnCam1Go6.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/6", [48, 186, 49])
            client.send_message("/style/color/3/6", [200, 200, 0])
            client.send_message("/style/bgcolor/4/6", [48, 186, 49])
            client.send_message("/style/color/4/6", [200, 200, 0])
        if cam1Pos7Run and not cam1AtPos7:
            self.root.get_screen('main').ids.btnCam1Go7.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go7.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/7", [48, 186, 49])
            client.send_message("/style/color/3/7", [200, 200, 0])
            client.send_message("/style/bgcolor/4/7", [48, 186, 49])
            client.send_message("/style/color/4/7", [200, 200, 0])
        if cam1Pos8Run and not cam1AtPos8:
            self.root.get_screen('main').ids.btnCam1Go8.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go8.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/8", [48, 186, 49])
            client.send_message("/style/color/3/8", [200, 200, 0])
            client.send_message("/style/bgcolor/4/8", [48, 186, 49])
            client.send_message("/style/color/4/8", [200, 200, 0])
        if cam1Pos9Run and not cam1AtPos9:
            self.root.get_screen('main').ids.btnCam1Go9.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go9.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/9", [48, 186, 49])
            client.send_message("/style/color/3/9", [200, 200, 0])
            client.send_message("/style/bgcolor/4/9", [48, 186, 49])
            client.send_message("/style/color/4/9", [200, 200, 0])
        if cam1Pos10Run and not cam1AtPos10:
            self.root.get_screen('main').ids.btnCam1Go10.col=(1, 1, 0, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go10.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/10", [48, 186, 49])
            client.send_message("/style/color/3/10", [200, 200, 0])
            client.send_message("/style/bgcolor/4/10", [48, 186, 49])
            client.send_message("/style/color/4/10", [200, 200, 0])

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.get_screen('main').ids.btnCam2Go1.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/9", [92, 133, 186])
            client.send_message("/style/color/3/9", [200, 200, 0])
            client.send_message("/style/bgcolor/5/1", [92, 133, 186])
            client.send_message("/style/color/5/1", [200, 200, 0])
            #client.send_message("/Cam1Go1", [1, "AAAA00FF"])
        if cam2Pos2Run and not cam2AtPos2:
            self.root.get_screen('main').ids.btnCam2Go2.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/10", [92, 133, 186])
            client.send_message("/style/color/3/10", [200, 200, 0])
            client.send_message("/style/bgcolor/5/2", [92, 133, 186])
            client.send_message("/style/color/5/2", [200, 200, 0])
        if cam2Pos3Run and not cam2AtPos3:
            self.root.get_screen('main').ids.btnCam2Go3.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/11", [92, 133, 186])
            client.send_message("/style/color/3/11", [200, 200, 0])
            client.send_message("/style/bgcolor/5/3", [92, 133, 186])
            client.send_message("/style/color/5/3", [200, 200, 0])
        if cam2Pos4Run and not cam2AtPos4:
            self.root.get_screen('main').ids.btnCam2Go4.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/12", [92, 133, 186])
            client.send_message("/style/color/3/12", [200, 200, 0])
            client.send_message("/style/bgcolor/5/4", [92, 133, 186])
            client.send_message("/style/color/5/4", [200, 200, 0])
        if cam2Pos5Run and not cam2AtPos5:
            self.root.get_screen('main').ids.btnCam2Go5.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/13", [92, 133, 186])
            client.send_message("/style/color/3/13", [200, 200, 0])
            client.send_message("/style/bgcolor/5/5", [92, 133, 186])
            client.send_message("/style/color/5/5", [200, 200, 0])
        if cam2Pos6Run and not cam2AtPos6:
            self.root.get_screen('main').ids.btnCam2Go6.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/6", [92, 133, 186])
            client.send_message("/style/color/5/6", [200, 200, 0])
        if cam2Pos7Run and not cam2AtPos7:
            self.root.get_screen('main').ids.btnCam2Go7.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go7.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/7", [92, 133, 186])
            client.send_message("/style/color/5/7", [200, 200, 0])
        if cam2Pos8Run and not cam2AtPos8:
            self.root.get_screen('main').ids.btnCam2Go8.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go8.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/8", [92, 133, 186])
            client.send_message("/style/color/5/8", [200, 200, 0])
        if cam2Pos9Run and not cam2AtPos9:
            self.root.get_screen('main').ids.btnCam2Go9.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go9.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/9", [92, 133, 186])
            client.send_message("/style/color/5/9", [200, 200, 0])
        if cam2Pos10Run and not cam2AtPos10:
            self.root.get_screen('main').ids.btnCam2Go10.col=(1, 1, 0, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go10.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/14", [92, 133, 186])
            client.send_message("/style/color/3/14", [200, 200, 0])
            client.send_message("/style/bgcolor/5/10", [92, 133, 186])
            client.send_message("/style/color/5/10", [200, 200, 0])

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.get_screen('main').ids.btnCam3Go1.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/17", [186, 164, 1])
            client.send_message("/style/color/3/17", [200, 200, 0])
            client.send_message("/style/bgcolor/6/1", [186, 164, 1])
            client.send_message("/style/color/6/1", [200, 200, 0])
        if cam3Pos2Run and not cam3AtPos2:
            self.root.get_screen('main').ids.btnCam3Go2.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/18", [186, 164, 1])
            client.send_message("/style/color/3/18", [200, 200, 0])
            client.send_message("/style/bgcolor/6/2", [186, 164, 1])
            client.send_message("/style/color/6/2", [200, 200, 0])
        if cam3Pos3Run and not cam3AtPos3:
            self.root.get_screen('main').ids.btnCam3Go3.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/19", [186, 164, 1])
            client.send_message("/style/color/3/19", [200, 200, 0])
            client.send_message("/style/bgcolor/6/3", [186, 164, 1])
            client.send_message("/style/color/6/3", [200, 200, 0])
        if cam3Pos4Run and not cam3AtPos4:
            self.root.get_screen('main').ids.btnCam3Go4.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/20", [186, 164, 1])
            client.send_message("/style/color/3/20", [200, 200, 0])
            client.send_message("/style/bgcolor/6/4", [186, 164, 1])
            client.send_message("/style/color/6/4", [200, 200, 0])
        if cam3Pos5Run and not cam3AtPos5:
            self.root.get_screen('main').ids.btnCam3Go5.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/5", [186, 164, 1])
            client.send_message("/style/color/6/5", [200, 200, 0])
        if cam3Pos6Run and not cam3AtPos6:
            self.root.get_screen('main').ids.btnCam3Go6.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/22", [186, 164, 1])
            client.send_message("/style/color/3/22", [200, 200, 0])
            client.send_message("/style/bgcolor/6/6", [186, 164, 1])
            client.send_message("/style/color/6/6", [200, 200, 0])
        if cam3Pos7Run and not cam3AtPos7:
            self.root.get_screen('main').ids.btnCam3Go7.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go7.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/7", [186, 164, 1])
            client.send_message("/style/color/6/7", [200, 200, 0])
        if cam3Pos8Run and not cam3AtPos8:
            self.root.get_screen('main').ids.btnCam3Go8.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go8.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/8", [186, 164, 1])
            client.send_message("/style/color/6/8", [200, 200, 0])
        if cam3Pos9Run and not cam3AtPos9:
            self.root.get_screen('main').ids.btnCam3Go9.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go9.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/9", [186, 164, 1])
            client.send_message("/style/color/6/9", [200, 200, 0])
        if cam3Pos10Run and not cam3AtPos10:
            self.root.get_screen('main').ids.btnCam3Go10.col=(1, 1, 0, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go10.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/10", [186, 164, 1])
            client.send_message("/style/color/6/10", [200, 200, 0])

        
        if cam4Pos1Run and not cam4AtPos1:
            self.root.get_screen('main').ids.btnCam4Go1.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/17", [186, 164, 1])
            client.send_message("/style/color/3/17", [200, 200, 0])
            client.send_message("/style/bgcolor/6/1", [186, 164, 1])
            client.send_message("/style/color/6/1", [200, 200, 0])
        if cam4Pos2Run and not cam4AtPos2:
            self.root.get_screen('main').ids.btnCam4Go2.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/18", [186, 164, 1])
            client.send_message("/style/color/3/18", [200, 200, 0])
            client.send_message("/style/bgcolor/6/2", [186, 164, 1])
            client.send_message("/style/color/6/2", [200, 200, 0])
        if cam4Pos3Run and not cam4AtPos3:
            self.root.get_screen('main').ids.btnCam4Go3.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/19", [186, 164, 1])
            client.send_message("/style/color/3/19", [200, 200, 0])
            client.send_message("/style/bgcolor/6/3", [186, 164, 1])
            client.send_message("/style/color/6/3", [200, 200, 0])
        if cam4Pos4Run and not cam4AtPos4:
            self.root.get_screen('main').ids.btnCam4Go4.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/20", [186, 164, 1])
            client.send_message("/style/color/3/20", [200, 200, 0])
            client.send_message("/style/bgcolor/6/4", [186, 164, 1])
            client.send_message("/style/color/6/4", [200, 200, 0])
        if cam4Pos5Run and not cam4AtPos5:
            self.root.get_screen('main').ids.btnCam4Go5.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/5", [186, 164, 1])
            client.send_message("/style/color/6/5", [200, 200, 0])
        if cam4Pos6Run and not cam4AtPos6:
            self.root.get_screen('main').ids.btnCam4Go6.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/22", [186, 164, 1])
            client.send_message("/style/color/3/22", [200, 200, 0])
            client.send_message("/style/bgcolor/6/6", [186, 164, 1])
            client.send_message("/style/color/6/6", [200, 200, 0])
        if cam4Pos7Run and not cam4AtPos7:
            self.root.get_screen('main').ids.btnCam4Go7.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go7.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/7", [186, 164, 1])
            client.send_message("/style/color/6/7", [200, 200, 0])
        if cam4Pos8Run and not cam4AtPos8:
            self.root.get_screen('main').ids.btnCam4Go8.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go8.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/8", [186, 164, 1])
            client.send_message("/style/color/6/8", [200, 200, 0])
        if cam4Pos9Run and not cam4AtPos9:
            self.root.get_screen('main').ids.btnCam4Go9.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go9.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/9", [186, 164, 1])
            client.send_message("/style/color/6/9", [200, 200, 0])
        if cam4Pos10Run and not cam4AtPos10:
            self.root.get_screen('main').ids.btnCam4Go10.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go10.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/10", [186, 164, 1])
            client.send_message("/style/color/6/10", [200, 200, 0])

        
        if cam5Pos1Run and not cam5AtPos1:
            self.root.get_screen('main').ids.btnCam5Go1.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go1.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/17", [186, 164, 1])
            client.send_message("/style/color/3/17", [200, 200, 0])
            client.send_message("/style/bgcolor/6/1", [186, 164, 1])
            client.send_message("/style/color/6/1", [200, 200, 0])
        if cam5Pos2Run and not cam5AtPos2:
            self.root.get_screen('main').ids.btnCam5Go2.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go2.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/18", [186, 164, 1])
            client.send_message("/style/color/3/18", [200, 200, 0])
            client.send_message("/style/bgcolor/6/2", [186, 164, 1])
            client.send_message("/style/color/6/2", [200, 200, 0])
        if cam5Pos3Run and not cam5AtPos3:
            self.root.get_screen('main').ids.btnCam5Go3.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go3.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/19", [186, 164, 1])
            client.send_message("/style/color/3/19", [200, 200, 0])
            client.send_message("/style/bgcolor/6/3", [186, 164, 1])
            client.send_message("/style/color/6/3", [200, 200, 0])
        if cam5Pos4Run and not cam5AtPos4:
            self.root.get_screen('main').ids.btnCam5Go4.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go4.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/20", [186, 164, 1])
            client.send_message("/style/color/3/20", [200, 200, 0])
            client.send_message("/style/bgcolor/6/4", [186, 164, 1])
            client.send_message("/style/color/6/4", [200, 200, 0])
        if cam5Pos5Run and not cam5AtPos5:
            self.root.get_screen('main').ids.btnCam5Go5.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go5.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/5", [186, 164, 1])
            client.send_message("/style/color/6/5", [200, 200, 0])
        if cam5Pos6Run and not cam5AtPos6:
            self.root.get_screen('main').ids.btnCam5Go6.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go6.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/22", [186, 164, 1])
            client.send_message("/style/color/3/22", [200, 200, 0])
            client.send_message("/style/bgcolor/6/6", [186, 164, 1])
            client.send_message("/style/color/6/6", [200, 200, 0])
        if cam5Pos7Run and not cam5AtPos7:
            self.root.get_screen('main').ids.btnCam5Go7.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go7.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/7", [186, 164, 1])
            client.send_message("/style/color/6/7", [200, 200, 0])
        if cam5Pos8Run and not cam5AtPos8:
            self.root.get_screen('main').ids.btnCam5Go8.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go8.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/8", [186, 164, 1])
            client.send_message("/style/color/6/8", [200, 200, 0])
        if cam5Pos9Run and not cam5AtPos9:
            self.root.get_screen('main').ids.btnCam5Go9.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go9.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/9", [186, 164, 1])
            client.send_message("/style/color/6/9", [200, 200, 0])
        if cam5Pos10Run and not cam5AtPos10:
            self.root.get_screen('main').ids.btnCam5Go10.col=(1, 1, 0, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go10.col=(1, 1, 0, 1)
            client.send_message("/style/bgcolor/3/21", [186, 164, 1])
            client.send_message("/style/color/3/21", [200, 200, 0])
            client.send_message("/style/bgcolor/6/10", [186, 164, 1])
            client.send_message("/style/color/6/10", [200, 200, 0])

        Clock.schedule_once(self.setNormal, 0.5)

    def setNormal(self, dt):
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
        
        if cam1Pos1Run and not cam1AtPos1:
            self.root.get_screen('main').ids.btnCam1Go1.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/1", [18, 70, 19])
            client.send_message("/style/color/3/1", [50, 50, 0])
            client.send_message("/style/bgcolor/4/1", [18, 70, 19])
            client.send_message("/style/color/4/1", [50, 50, 0])
        if cam1Pos2Run and not cam1AtPos2:
            self.root.get_screen('main').ids.btnCam1Go2.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/2", [18, 70, 19])
            client.send_message("/style/color/3/2", [50, 50, 0])
            client.send_message("/style/bgcolor/4/2", [18, 70, 19])
            client.send_message("/style/color/4/2", [50, 50, 0])
        if cam1Pos3Run and not cam1AtPos3:
            self.root.get_screen('main').ids.btnCam1Go3.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/3", [18, 70, 19])
            client.send_message("/style/color/3/3", [50, 50, 0])
            client.send_message("/style/bgcolor/4/3", [18, 70, 19])
            client.send_message("/style/color/4/3", [50, 50, 0])
        if cam1Pos4Run and not cam1AtPos4:
            self.root.get_screen('main').ids.btnCam1Go4.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/4", [18, 70, 19])
            client.send_message("/style/color/3/4", [50, 50, 0])
            client.send_message("/style/bgcolor/4/4", [18, 70, 19])
            client.send_message("/style/color/4/4", [50, 50, 0])
        if cam1Pos5Run and not cam1AtPos5:
            self.root.get_screen('main').ids.btnCam1Go5.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/5", [18, 70, 19])
            client.send_message("/style/color/3/5", [50, 50, 0])
            client.send_message("/style/bgcolor/4/5", [18, 70, 19])
            client.send_message("/style/color/4/5", [50, 50, 0])
        if cam1Pos6Run and not cam1AtPos6:
            self.root.get_screen('main').ids.btnCam1Go6.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/6", [18, 70, 19])
            client.send_message("/style/color/3/6", [50, 50, 0])
            client.send_message("/style/bgcolor/4/6", [18, 70, 19])
            client.send_message("/style/color/4/6", [50, 50, 0])
        if cam1Pos7Run and not cam1AtPos7:
            self.root.get_screen('main').ids.btnCam1Go7.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go7.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/7", [18, 70, 19])
            client.send_message("/style/color/3/7", [50, 50, 0])
            client.send_message("/style/bgcolor/4/7", [18, 70, 19])
            client.send_message("/style/color/4/7", [50, 50, 0])
        if cam1Pos8Run and not cam1AtPos8:
            self.root.get_screen('main').ids.btnCam1Go8.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go8.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/8", [18, 70, 19])
            client.send_message("/style/color/3/8", [50, 50, 0])
            client.send_message("/style/bgcolor/4/8", [18, 70, 19])
            client.send_message("/style/color/4/8", [50, 50, 0])
        if cam1Pos9Run and not cam1AtPos9:
            self.root.get_screen('main').ids.btnCam1Go9.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go9.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/9", [18, 70, 19])
            client.send_message("/style/color/3/9", [50, 50, 0])
            client.send_message("/style/bgcolor/4/9", [18, 70, 19])
            client.send_message("/style/color/4/9", [50, 50, 0])
        if cam1Pos10Run and not cam1AtPos10:
            self.root.get_screen('main').ids.btnCam1Go10.col=(.1, .1, .1, 1)
            self.root.get_screen('1stcam').ids.btnCam1Go10.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/10", [18, 70, 19])
            client.send_message("/style/color/3/10", [50, 50, 0])
            client.send_message("/style/bgcolor/4/10", [18, 70, 19])
            client.send_message("/style/color/4/10", [50, 50, 0])

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.get_screen('main').ids.btnCam2Go1.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/9", [35, 50, 70])
            client.send_message("/style/color/3/9", [50, 50, 0])
            client.send_message("/style/bgcolor/5/1", [35, 50, 70])
            client.send_message("/style/color/5/1", [50, 50, 0])
            #client.send_message("/Cam1Go1", [1, "000000FF"])
        if cam2Pos2Run and not cam2AtPos2:
            self.root.get_screen('main').ids.btnCam2Go2.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/10", [35, 50, 70])
            client.send_message("/style/color/3/10", [50, 50, 0])
            client.send_message("/style/bgcolor/5/2", [35, 50, 70])
            client.send_message("/style/color/5/2", [50, 50, 0])
        if cam2Pos3Run and not cam2AtPos3:
            self.root.get_screen('main').ids.btnCam2Go3.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/11", [35, 50, 70])
            client.send_message("/style/color/3/11", [50, 50, 0])
            client.send_message("/style/bgcolor/5/3", [35, 50, 70])
            client.send_message("/style/color/5/3", [50, 50, 0])
        if cam2Pos4Run and not cam2AtPos4:
            self.root.get_screen('main').ids.btnCam2Go4.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/12", [35, 50, 70])
            client.send_message("/style/color/3/12", [50, 50, 0])
            client.send_message("/style/bgcolor/5/4", [35, 50, 70])
            client.send_message("/style/color/5/4", [50, 50, 0])
        if cam2Pos5Run and not cam2AtPos5:
            self.root.get_screen('main').ids.btnCam2Go5.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/13", [35, 50, 70])
            client.send_message("/style/color/3/13", [50, 50, 0])
            client.send_message("/style/bgcolor/5/5", [35, 50, 70])
            client.send_message("/style/color/5/5", [50, 50, 0])
        if cam2Pos6Run and not cam2AtPos6:
            self.root.get_screen('main').ids.btnCam2Go6.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/6", [35, 50, 70])
            client.send_message("/style/color/5/6", [50, 50, 0])
        if cam2Pos7Run and not cam2AtPos7:
            self.root.get_screen('main').ids.btnCam2Go7.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go7.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/7", [35, 50, 70])
            client.send_message("/style/color/5/7", [50, 50, 0])
        if cam2Pos8Run and not cam2AtPos8:
            self.root.get_screen('main').ids.btnCam2Go8.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go8.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/8", [35, 50, 70])
            client.send_message("/style/color/5/8", [50, 50, 0])
        if cam2Pos9Run and not cam2AtPos9:
            self.root.get_screen('main').ids.btnCam2Go9.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go9.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/9", [35, 50, 70])
            client.send_message("/style/color/5/9", [50, 50, 0])
        if cam2Pos10Run and not cam2AtPos10:
            self.root.get_screen('main').ids.btnCam2Go10.col=(.1, .1, .1, 1)
            self.root.get_screen('2ndcam').ids.btnCam2Go10.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/14", [35, 50, 70])
            client.send_message("/style/color/3/14", [50, 50, 0])
            client.send_message("/style/bgcolor/5/10", [35, 50, 70])
            client.send_message("/style/color/5/10", [50, 50, 0])

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.get_screen('main').ids.btnCam3Go1.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/17", [70, 62, 1])
            client.send_message("/style/color/3/17", [50, 50, 0])
            client.send_message("/style/bgcolor/6/1", [70, 62, 1])
            client.send_message("/style/color/6/1", [50, 50, 0])
        if cam3Pos2Run and not cam3AtPos2:
            self.root.get_screen('main').ids.btnCam3Go2.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/18", [70, 62, 1])
            client.send_message("/style/color/3/18", [50, 50, 0])
            client.send_message("/style/bgcolor/6/2", [70, 62, 1])
            client.send_message("/style/color/6/2", [50, 50, 0])
        if cam3Pos3Run and not cam3AtPos3:
            self.root.get_screen('main').ids.btnCam3Go3.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/19", [70, 62, 1])
            client.send_message("/style/color/3/19", [50, 50, 0])
            client.send_message("/style/bgcolor/6/3", [70, 62, 1])
            client.send_message("/style/color/6/3", [50, 50, 0])
        if cam3Pos4Run and not cam3AtPos4:
            self.root.get_screen('main').ids.btnCam3Go4.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/4", [70, 62, 1])
            client.send_message("/style/color/6/4", [50, 50, 0])
        if cam3Pos5Run and not cam3AtPos5:
            self.root.get_screen('main').ids.btnCam3Go5.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/21", [70, 62, 1])
            client.send_message("/style/color/3/21", [50, 50, 0])
            client.send_message("/style/bgcolor/6/5", [70, 62, 1])
            client.send_message("/style/color/6/5", [50, 50, 0])
        if cam3Pos6Run and not cam3AtPos6:
            self.root.get_screen('main').ids.btnCam3Go6.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/22", [70, 62, 1])
            client.send_message("/style/color/3/22", [50, 50, 0])
            client.send_message("/style/bgcolor/6/6", [70, 62, 1])
            client.send_message("/style/color/6/6", [50, 50, 0])
        if cam3Pos7Run and not cam3AtPos7:
            self.root.get_screen('main').ids.btnCam3Go7.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go7.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/7", [70, 62, 1])
            client.send_message("/style/color/6/7", [50, 50, 0])
        if cam3Pos8Run and not cam3AtPos8:
            self.root.get_screen('main').ids.btnCam3Go8.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go8.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/8", [70, 62, 1])
            client.send_message("/style/color/6/8", [50, 50, 0])
        if cam3Pos9Run and not cam3AtPos9:
            self.root.get_screen('main').ids.btnCam3Go9.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go9.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/9", [70, 62, 1])
            client.send_message("/style/color/6/9", [50, 50, 0])
        if cam3Pos10Run and not cam3AtPos10:
            self.root.get_screen('main').ids.btnCam3Go10.col=(.1, .1, .1, 1)
            self.root.get_screen('3rdcam').ids.btnCam3Go10.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/10", [70, 62, 1])
            client.send_message("/style/color/6/10", [50, 50, 0])

        
        if cam4Pos1Run and not cam4AtPos1:
            self.root.get_screen('main').ids.btnCam4Go1.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/17", [70, 62, 1])
            client.send_message("/style/color/3/17", [50, 50, 0])
            client.send_message("/style/bgcolor/6/1", [70, 62, 1])
            client.send_message("/style/color/6/1", [50, 50, 0])
        if cam4Pos2Run and not cam4AtPos2:
            self.root.get_screen('main').ids.btnCam4Go2.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/18", [70, 62, 1])
            client.send_message("/style/color/3/18", [50, 50, 0])
            client.send_message("/style/bgcolor/6/2", [70, 62, 1])
            client.send_message("/style/color/6/2", [50, 50, 0])
        if cam4Pos3Run and not cam4AtPos3:
            self.root.get_screen('main').ids.btnCam4Go3.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/19", [70, 62, 1])
            client.send_message("/style/color/3/19", [50, 50, 0])
            client.send_message("/style/bgcolor/6/3", [70, 62, 1])
            client.send_message("/style/color/6/3", [50, 50, 0])
        if cam4Pos4Run and not cam4AtPos4:
            self.root.get_screen('main').ids.btnCam4Go4.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/4", [70, 62, 1])
            client.send_message("/style/color/6/4", [50, 50, 0])
        if cam4Pos5Run and not cam4AtPos5:
            self.root.get_screen('main').ids.btnCam4Go5.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/21", [70, 62, 1])
            client.send_message("/style/color/3/21", [50, 50, 0])
            client.send_message("/style/bgcolor/6/5", [70, 62, 1])
            client.send_message("/style/color/6/5", [50, 50, 0])
        if cam4Pos6Run and not cam4AtPos6:
            self.root.get_screen('main').ids.btnCam4Go6.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/22", [70, 62, 1])
            client.send_message("/style/color/3/22", [50, 50, 0])
            client.send_message("/style/bgcolor/6/6", [70, 62, 1])
            client.send_message("/style/color/6/6", [50, 50, 0])
        if cam4Pos7Run and not cam4AtPos7:
            self.root.get_screen('main').ids.btnCam4Go7.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go7.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/7", [70, 62, 1])
            client.send_message("/style/color/6/7", [50, 50, 0])
        if cam4Pos8Run and not cam4AtPos8:
            self.root.get_screen('main').ids.btnCam4Go8.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go8.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/8", [70, 62, 1])
            client.send_message("/style/color/6/8", [50, 50, 0])
        if cam4Pos9Run and not cam4AtPos9:
            self.root.get_screen('main').ids.btnCam4Go9.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go9.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/9", [70, 62, 1])
            client.send_message("/style/color/6/9", [50, 50, 0])
        if cam4Pos10Run and not cam4AtPos10:
            self.root.get_screen('main').ids.btnCam4Go10.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam4Go10.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/10", [70, 62, 1])
            client.send_message("/style/color/6/10", [50, 50, 0])

        
        if cam5Pos1Run and not cam5AtPos1:
            self.root.get_screen('main').ids.btnCam5Go1.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go1.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/17", [70, 62, 1])
            client.send_message("/style/color/3/17", [50, 50, 0])
            client.send_message("/style/bgcolor/6/1", [70, 62, 1])
            client.send_message("/style/color/6/1", [50, 50, 0])
        if cam5Pos2Run and not cam5AtPos2:
            self.root.get_screen('main').ids.btnCam5Go2.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go2.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/18", [70, 62, 1])
            client.send_message("/style/color/3/18", [50, 50, 0])
            client.send_message("/style/bgcolor/6/2", [70, 62, 1])
            client.send_message("/style/color/6/2", [50, 50, 0])
        if cam5Pos3Run and not cam5AtPos3:
            self.root.get_screen('main').ids.btnCam5Go3.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go3.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/19", [70, 62, 1])
            client.send_message("/style/color/3/19", [50, 50, 0])
            client.send_message("/style/bgcolor/6/3", [70, 62, 1])
            client.send_message("/style/color/6/3", [50, 50, 0])
        if cam5Pos4Run and not cam5AtPos4:
            self.root.get_screen('main').ids.btnCam5Go4.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go4.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/4", [70, 62, 1])
            client.send_message("/style/color/6/4", [50, 50, 0])
        if cam5Pos5Run and not cam5AtPos5:
            self.root.get_screen('main').ids.btnCam5Go5.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go5.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/21", [70, 62, 1])
            client.send_message("/style/color/3/21", [50, 50, 0])
            client.send_message("/style/bgcolor/6/5", [70, 62, 1])
            client.send_message("/style/color/6/5", [50, 50, 0])
        if cam5Pos6Run and not cam5AtPos6:
            self.root.get_screen('main').ids.btnCam5Go6.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go6.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/22", [70, 62, 1])
            client.send_message("/style/color/3/22", [50, 50, 0])
            client.send_message("/style/bgcolor/6/6", [70, 62, 1])
            client.send_message("/style/color/6/6", [50, 50, 0])
        if cam5Pos7Run and not cam5AtPos7:
            self.root.get_screen('main').ids.btnCam5Go7.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go7.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/7", [70, 62, 1])
            client.send_message("/style/color/6/7", [50, 50, 0])
        if cam5Pos8Run and not cam5AtPos8:
            self.root.get_screen('main').ids.btnCam5Go8.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go8.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/8", [70, 62, 1])
            client.send_message("/style/color/6/8", [50, 50, 0])
        if cam5Pos9Run and not cam5AtPos9:
            self.root.get_screen('main').ids.btnCam5Go9.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go9.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/9", [70, 62, 1])
            client.send_message("/style/color/6/9", [50, 50, 0])
        if cam5Pos10Run and not cam5AtPos10:
            self.root.get_screen('main').ids.btnCam5Go10.col=(.1, .1, .1, 1)
            #self.root.get_screen('3rdcam').ids.btnCam5Go10.col=(.1, .1, .1, 1)
            client.send_message("/style/bgcolor/3/20", [70, 62, 1])
            client.send_message("/style/color/3/20", [50, 50, 0])
            client.send_message("/style/bgcolor/6/10", [70, 62, 1])
            client.send_message("/style/color/6/10", [50, 50, 0])

    
    def sendSerial(self, sendData):
        #print(sendData)
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
                self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
                textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
                if textLength > 8000:
                    self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
                self.root.get_screen('main').ids.scroll_view.scroll_y = 0
        else:
            self.root.get_screen('main').ids.txtInput_read.text += "[color=#FFFFFF]Port not connected.\n[/color]"
            textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
            if textLength > 8000:
                self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
            self.root.get_screen('main').ids.scroll_view.scroll_y = 0

        self.root.get_screen('1stcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('2ndcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('3rdcam').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text
        self.root.get_screen('1stcam').ids.scroll_view.scroll_y = 0
        self.root.get_screen('2ndcam').ids.scroll_view.scroll_y = 0
        self.root.get_screen('3rdcam').ids.scroll_view.scroll_y = 0


if __name__ == '__main__':
    PTSApp().run()