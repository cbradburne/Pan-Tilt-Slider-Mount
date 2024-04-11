#macOS
#Kivy
#python3 -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
#
#KivyMD
#git clone https://github.com/kivymd/KivyMD.git --depth 1
#cd KivyMD
#/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 -m pip install --upgrade pip
#pip install .

# git clone https://github.com/kivymd/KivyMD.git
# cd KivyMD
# python3 -m pip install -e ".[dev,full]"

#
#Other
#python3 -m pip install pygame==2.0.1
#python3 -m pip install usbserial4a
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

#from kivymd.uix.button import MDButton
#from kivymd.uix.button import BaseButton
from kivymd.uix.button import MDExtendedFabButtonText

from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty

if platform == 'android':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
else:
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'window_state', 'windowed')
    #Config.set('graphics', 'width', '1900')         #test
    #Config.set('graphics', 'height', '1000')        #test
    Config.set('graphics', 'width', '1400')          # A7 Lite
    Config.set('graphics', 'height', '800')          # A7 Lite
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
from kivymd.uix.menu import MDDropdownMenu
import threading
import os, sys, re
import time
from pathlib import Path

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

Cam1ButColour = '#4C8A4C' 
Cam2ButColour = '#405C80'
Cam3ButColour = '#807100'
Cam4ButColour = '#008071'
Cam5ButColour = '#8D5395'

butBorderColour = '#808080'

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
oldAxisW = 0
axisX = 0
axisY = 0
axisZ = 0
axisW = 0
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
        md_bg_color: get_color_from_hex("#181e23")

        canvas:
            Color:
                rgba: get_color_from_hex("#1e252a")             # Grey

            
            # Camera Groups
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*51)
                size: (app.xDiv*132), (app.yDiv*10)

            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*40)
                size: (app.xDiv*132), (app.yDiv*10)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*29)
                size: (app.xDiv*132), (app.yDiv*10)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*18)
                size: (app.xDiv*132), (app.yDiv*10)
            
            Rectangle:
                pos: (app.xDiv*1), (app.yDiv*7)
                size: (app.xDiv*132), (app.yDiv*10)

            


            #Dark Bkgd for speed display
            Color:
                rgba: (0.1, 0.1, 0.1, 1)                        # Dark Grey BG

            #PT
            Rectangle:
                pos: (app.xDiv*103), (app.yDiv*52)
                size: (app.xDiv*12.5), (app.yDiv*3)

            Rectangle:
                pos: (app.xDiv*103), (app.yDiv*41)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*103), (app.yDiv*30)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*103), (app.yDiv*19)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*103), (app.yDiv*8)
                size: (app.xDiv*12.5), (app.yDiv*3)

            #Slider
            Rectangle:
                pos: (app.xDiv*119), (app.yDiv*52)
                size: (app.xDiv*12.5), (app.yDiv*3)

            Rectangle:
                pos: (app.xDiv*119), (app.yDiv*41)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*119), (app.yDiv*30)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*119), (app.yDiv*19)
                size: (app.xDiv*12.5), (app.yDiv*3)
                
            Rectangle:
                pos: (app.xDiv*119), (app.yDiv*8)
                size: (app.xDiv*12.5), (app.yDiv*3)


        FloatLayout:
            id: cam1PTSpd
            sizPT1: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle:
                    pos: (app.xDiv*103), (app.yDiv*52)
                    size: self.sizPT1

        FloatLayout:
            id: cam2PTSpd
            sizPT2: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*103), (app.yDiv*41)
                    size: self.sizPT2

        FloatLayout:
            id: cam3PTSpd
            sizPT3: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*103), (app.yDiv*30)
                    size: self.sizPT3

        FloatLayout:
            id: cam4PTSpd
            sizPT4: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*103), (app.yDiv*19)
                    size: self.sizPT4

        FloatLayout:
            id: cam5PTSpd
            sizPT5: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*103), (app.yDiv*8)
                    size: self.sizPT5



        FloatLayout:
            id: cam1SlSpd
            sizSl1: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*119), (app.yDiv*52)
                    size: self.sizSl1

        FloatLayout:
            id: cam2SlSpd
            sizSl2: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*119), (app.yDiv*41)
                    size: self.sizSl2

        FloatLayout:
            id: cam3SlSpd
            sizSl3: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*119), (app.yDiv*30)
                    size: self.sizSl3

        FloatLayout:
            id: cam4SlSpd
            sizSl4: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#7D0000")
                Rectangle: 
                    pos: (app.xDiv*119), (app.yDiv*19)
                    size: self.sizSl4

        FloatLayout:
            id: cam5SlSpd
            sizSl5: 0, 0
            canvas:
                Color:
                    rgba: get_color_from_hex("#aaaa00")
                Rectangle: 
                    pos: (app.xDiv*119), (app.yDiv*8)
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



            

            

        MDFillRoundFlatButton:
            id: pushButtonEdit
            text: "Cam 1"
            line_width: 5
            line_color: 1, 0, 0, 1
            md_bg_color: get_color_from_hex(app.Cam1ButColour)
            pos: (app.xDiv*2), (app.yDiv*63)
            size: (app.xDiv*5), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2.2)
            on_release: app.setPos(3)
        
        MDFillRoundFlatButton:
            id: buttonWhichCam1
            text: "Cam 1"
            line_width: 5
            line_color: 1, 0, 0, 1
            md_bg_color: get_color_from_hex(app.Cam1ButColour)
            pos: (app.xDiv*39), (app.yDiv*63)
            size: (app.xDiv*5), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial1()

        MDFillRoundFlatButton:
            id: buttonWhichCam2
            text: "Cam 2"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam2ButColour)
            pos: (app.xDiv*51), (app.yDiv*63)
            size: (app.xDiv*5), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial2()

        MDFillRoundFlatButton:
            id: buttonWhichCam3
            text: "Cam 3"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam3ButColour)
            pos: (app.xDiv*63), (app.yDiv*63)
            size: (app.xDiv*5), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial3()

        MDFillRoundFlatButton:
            id: buttonWhichCam4
            text: "Cam 4"
            line_width: 5
            line_color: .13, .13, .13, 1
            md_bg_color: get_color_from_hex(app.Cam4ButColour)
            pos: (app.xDiv*75), (app.yDiv*63)
            size: (app.xDiv*5), (app.yDiv*6)
            size_hint: None, None
            font_size: (app.yDiv*2)
            on_release: app.whichCamSerial4()

        #MDRectangleFlatButton:
        #MDFlatButton:
        MDFloatingActionButton:
            md_bg_color: get_color_from_hex(app.Cam5ButColour)

            size_hint_x: (app.xDiv*0.003)
            size_hint_y: (app.xDiv*0.003)

            line_color: "red"
            line_width: 3

            pos: (app.xDiv*87), (app.yDiv*63)


        #MDFillRoundFlatButton:
        #    id: buttonWhichCam5
        #    text: "Cam 5"
        #    line_width: 5
        #    line_color: .13, .13, .13, 1
        #    md_bg_color: get_color_from_hex(app.Cam5ButColour)


        #    pos: (app.xDiv*87), (app.yDiv*63)
            #size: (app.xDiv*5), (app.yDiv*29)
            #size_hint: None, None
        #    font_size: (app.yDiv*2)
        #    on_release: app.whichCamSerial5()

        #    size: 30, 30
        #    size_hint: None, None
        #    _min_width: 300
        #    _min_height: 300
        #    set_radius:
        
    """


class PTSApp(MDApp):

    xDiv = NumericProperty(xDivSet)        # 10 / 1340
    yDiv = NumericProperty(yDivSet)        # 10 / 703

    xScreen = NumericProperty(xScreenSet)
    yScreen = NumericProperty(yScreenSet)

    whichCam = StringProperty()

    def __init__(self, *args, **kwargs):
        super(PTSApp, self).__init__(*args, **kwargs)
        global Cam1ButColour
        global Cam2ButColour
        global Cam3ButColour
        global Cam4ButColour
        global Cam5ButColour
        global butBorderColour

        self.Cam1ButColour = Cam1ButColour
        self.Cam2ButColour = Cam2ButColour
        self.Cam3ButColour = Cam3ButColour
        self.Cam4ButColour = Cam4ButColour
        self.Cam5ButColour = Cam5ButColour
        self.butBorderColour = butBorderColour
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None

        #Window.bind(on_joy_hat=self.on_joy_hat)
        #Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        #Window.bind(on_joy_button_up=self.on_joy_button_up)
        #Window.bind(on_joy_button_down=self.on_joy_button_down)\
    
        self.event_loop_worker = None

    def build(self):
        global PTJoy
        self.screen = Builder.load_string(KV)

        #Window.bind(on_joy_hat = self.on_joy_hat)
        #Window.bind(on_joy_ball = self.on_joy_ball)
        #Window.bind(on_joy_button_up = self.on_joy_button_up)
        #Window.bind(on_joy_button_down = self.on_joy_button_down)
        
        #Window.bind(mouse_pos=self.mouse_pos)
        #Window.bind(on_touch_up = self.on_touch_up)
        #Window.bind(on_request_close = self.stopping)
        #Window.bind(on_key_down = self.keyDown)
        #Window.bind(on_key_up = self.keyUp)
        #listener = Listener(on_press = self.on_press, on_release=self.on_release)
        #listener.start()
        Clock.schedule_interval(self.flash, 1.0)
        Clock.schedule_interval(self.doJoyMoves, 0.1)
        Clock.schedule_once(self.setWhichCam, 0)
        self.icon = 'PTSApp-Icon.png'
        return self.screen

    
    def removes_marks_all_chips(self, selected_instance_chip):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    '''
    def on_joy_axis(self, win, stickid, axisid, value):
        print(win, stickid, axisid, value)

    def on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
        print('ball', stickid, ballid, (xvalue, yvalue))

    def on_joy_hat(self, win, stickid, hatid, value):
        print('hat', stickid, hatid, value)

    def on_joy_button_down(self, win, stickid, buttonid):
        print('button_down', stickid, buttonid)

    def on_joy_button_up(self, win, stickid, buttonid):
        print('button_up', stickid, buttonid)
    '''
    

    def keyUp(self, instance, keyboard, keycode):
        global axisX
        global axisY
        global axisZ
        global axisW

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
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
        global axisW

        global Cam1TextColour
        global Cam2TextColour
        global Cam3TextColour
        global Cam4TextColour
        global Cam5TextColour
        
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
        
        #if keycode == 40:                                                                   # Return key pressed
            


    def clearTextInput(self, dt):
        self.root.get_screen('main').ids.textInput.text = ""

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


    def on_stop(self):
        if self.serial_port:
            self.read_thread = None
            

    def on_joy_axis(self, win, stickid, axisid, value):         # Joystick
        #print(axisid, value)
        
        global axisX
        global axisY
        global axisZ
        global axisW
        #if axisid == 3:
        #    axisX = int(self.scale(value, (-32768, 32767), (-255,255)))
        #elif axisid == 2:
        #    axisY = int(self.scale(value, (-32768, 32767), (-255,255)))
        #elif axisid == 0:
        #    axisZ = int(self.scale(value, (-32768, 32767), (-255,255)))



        
        deadRange = 6000


        #joyName = str(key.joystick)
        #joyName = joyName.lower()

        #if re.search('xbox', joyName):
            #print(key.number)

        if axisid == 2:
            if (value < -deadRange):
                axisX = int(self.scale(value, (-32767, -deadRange), (-255, 0)))
            elif (value > deadRange):
                axisX = int(self.scale(value, (32767, deadRange), (255, 0)))
            else:
                axisX = 0
            
            #axisX = int(self.scale(value, (-1, 1), (-255,255)))
        elif axisid == 3:
            if (value < -deadRange):
                axisY = int(self.scale(value, (-32767, -deadRange), (-255, 0)))
            elif (value > deadRange):
                axisY = int(self.scale(value, (32767, deadRange), (255, 0)))
            else:
                axisY = 0

            #axisY = int(self.scale(value, (-1, 1), (255,-255)))
        elif axisid == 0:
            if (value < -deadRange):
                axisZ = int(self.scale(value, (-32767, -deadRange), (-255, 0)))
            elif (value > deadRange):
                axisZ = int(self.scale(value, (32767, deadRange), (255, 0)))
            else:
                axisZ = 0

            #axisZ = int(self.scale(value, (-1, 1), (-255,255)))
        elif axisid == 1:
            if (value < -deadRange):
                axisW = int(self.scale(value, (-32767, -(deadRange*2)), (-8, 0)))
            elif (value > deadRange):
                axisW = int(self.scale(value, (32767, (deadRange*2)), (8, 0)))
            else:
                axisW = 0
        #print(axisX, axisY, axisZ, axisW)
            #axisW = int(self.scale(value, (-1, 1), (8,-8)))
        '''
        elif joyType[-6:] == "tton 0" and (value == 0):
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
                axisX = int(self.scale(value, (-1, 1), (-255,255)))
            elif joyType[-6:] == "Axis 2":
                axisY = int(self.scale(value, (-1, 1), (-255,255)))
            elif joyType[-6:] == "Axis 0":
                axisZ = int(self.scale(value, (-1, 1), (-255,255)))
            elif joyType[-6:] == "Axis 1":
                axisW = int(self.scale(value, (-1, 1), (-8,8)))
        '''
        self.doJoyMoves(1)





    def on_touch_up(self, obj, obj_prop):
        global mousePTClick
        global mouseSlClick
        global panKeyPressed
        global sliderKeyPressed
        global axisX
        global axisY
        global axisZ
        global axisW
        global xDivSet
        global yDivSet

        if mousePTClick and not panKeyPressed:
            mousePTClick = False
            #self.root.get_screen('main').ids.PTJoyDot.pos = (self.screen.width, self.screen.height)
            #self.root.get_screen('main').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.width)
        if mouseSlClick and not sliderKeyPressed:
            mouseSlClick = False
            #self.root.get_screen('main').ids.SlJoyDot.pos = (self.screen.width, self.screen.height)
            #self.root.get_screen('main').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.width)

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
        axisW = 0

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
        global axisW
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
            
            #self.root.get_screen('main').ids.PTJoyDotPress.pos = (self.screen.width, self.screen.height)
            #self.root.get_screen('main').ids.PTJoyDot.pos = ((abs_coord_x - (xDivSet*2)), (abs_coord_y - (yDivSet*2)))

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

            #self.root.get_screen('main').ids.SlJoyDotPress.pos = (self.screen.width, self.screen.height)
            #self.root.get_screen('main').ids.SlJoyDot.pos = ((abs_coord_x - (xDivSet*2)), SlY)

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
        global axisW
        global oldAxisX
        global oldAxisY
        global oldAxisZ
        global oldAxisW
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

        if (axisW != oldAxisW):                                     # ZOOM
            oldAxisW = axisW
            zoomSerial = "&"
            if whichCamSerial == 1: zoomSerial = zoomSerial + "1"
            elif whichCamSerial == 2: zoomSerial = zoomSerial + "2"
            elif whichCamSerial == 3: zoomSerial = zoomSerial + "3"
            elif whichCamSerial == 4: zoomSerial = zoomSerial + "4"
            elif whichCamSerial == 5: zoomSerial = zoomSerial + "5"

            if axisW == -8: self.sendSerial(zoomSerial + 'A8')
            elif axisW == -7: self.sendSerial(zoomSerial + 'A7')
            elif axisW == -6: self.sendSerial(zoomSerial + 'A6')
            elif axisW == -5: self.sendSerial(zoomSerial + 'A5')
            elif axisW == -4: self.sendSerial(zoomSerial + 'A4')
            elif axisW == -3: self.sendSerial(zoomSerial + 'A3')
            elif axisW == -2: self.sendSerial(zoomSerial + 'A2')
            elif axisW == -1: self.sendSerial(zoomSerial + 'A1')
            elif axisW == 1: self.sendSerial(zoomSerial + 'a1')
            elif axisW == 2: self.sendSerial(zoomSerial + 'a2')
            elif axisW == 3: self.sendSerial(zoomSerial + 'a3')
            elif axisW == 4: self.sendSerial(zoomSerial + 'a4')
            elif axisW == 5: self.sendSerial(zoomSerial + 'a5')
            elif axisW == 6: self.sendSerial(zoomSerial + 'a6')
            elif axisW == 7: self.sendSerial(zoomSerial + 'a7')
            elif axisW == 8: self.sendSerial(zoomSerial + 'a8')
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
            self.root.get_screen('main').ids.pushButtonSet.background_color = get_color_from_hex("#666666")
        elif (SetPosToggle == False and state == 3) or state == 1:
            SetPosToggle = True
            self.root.get_screen('main').ids.pushButtonSet.background_color = get_color_from_hex("#7D0000")


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

    def open_menu(self, item):
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
            menu_items = [
                {
                    "text": f"{device_name}",
                    "on_release": lambda x=f"{device_name}": self.menu_callback(x),
                }    for device_name in self.device_name_list
             ]
            self.menu = MDDropdownMenu(items=menu_items)
            self.callback(item)


    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        portText = text_item.rsplit('/', 1)[-1]

        self.root.get_screen('main').ids.drop_text.text = portText
        #self.root.get_screen('main').ids.drop_text.font_size = "1"

        self.menu.dismiss()
        self.autoSerial(text_item, 1)



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
                    #self.root.get_screen('1stcam').ids.scanDD.pos = (((xDivSet*110)-(xDivSet*(longestSerial/2))), ((yDivSet*65) - ((yDivSet*7.4) * len(usb_device_list))))
                    pass

                if platform == "win32" or platform == "Windows" or platform == "win":
                    if whichCamSerial == 1:
                        #self.root.get_screen('1stcam').ids.box_list1.size = (((xDivSet*(longestSerial*1.4))), 0)
                        pass
                else:
                    if whichCamSerial == 1:
                        #self.root.get_screen('1stcam').ids.box_list1.size = (((xDivSet*(longestSerial*0.8))), 0)
                        pass
        else:
            btn_scan_show = False


    def on_btn_help_release(self):
        global btn_help_show

        if not btn_help_show:
            btn_help_show = True

            #self.root.get_screen('1stcam').ids.helpLabel.visible =  True
            #self.root.get_screen('1stcam').ids.helpCanvas.visible =  True
        elif btn_help_show:
            btn_help_show = False

            #self.root.get_screen('1stcam').ids.helpLabel.visible =  False
            #self.root.get_screen('1stcam').ids.helpCanvas.visible =  False

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
        #textLength = len(self.root.get_screen('main').ids.txtInput_read.text)
        #if textLength > 8000:
        #    self.root.get_screen('main').ids.txtInput_read.text = self.root.get_screen('main').ids.txtInput_read.text[1000:textLength]
        
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
            elif msg[1:4] == "124":
                cam1isRecording = True
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
            elif msg[1:4] == "224":
                cam2isRecording = True
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
            elif msg[1:4] == "324":
                cam3isRecording = True
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
            elif msg[1:4] == "424":
                cam4isRecording = True
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
            elif msg[1:4] == "524":
                cam5isRecording = True
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
            cam5ZoomLimit = int(msg[3:-5])

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
        elif (moveType == 2) and ((moveTypeOld != moveType) or resetButtons):
            moveTypeOld = moveType
        elif (moveType == 3) and ((moveTypeOld != moveType) or resetButtons):
            moveTypeOld = moveType

        if cam1Pos1Set != OLDcam1Pos1Set or cam1Pos1Run != OLDcam1Pos1Run or cam1AtPos1 != OLDcam1AtPos1 or resetButtons:
            OLDcam1Pos1Set = cam1Pos1Set
            OLDcam1Pos1Run = cam1Pos1Run
            OLDcam1AtPos1 = cam1AtPos1
            if cam1Pos1Set and not cam1Pos1Run and not cam1AtPos1:                                  # Set , not Run or At
                self.root.get_screen('main').ids.btnCam1Go1.line_color=(1, 0, 0, 1)
            elif cam1Pos1Set and not cam1Pos1Run and cam1AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam1Go1.line_color=(0, 1, 0, 1)
            elif not cam1Pos1Set:
                self.root.get_screen('main').ids.btnCam1Go1.line_color=(.13, .13, .13, 1)

        if cam1Pos2Set != OLDcam1Pos2Set or cam1Pos2Run != OLDcam1Pos2Run or cam1AtPos2 != OLDcam1AtPos2 or resetButtons:
            OLDcam1Pos2Set = cam1Pos2Set
            OLDcam1Pos2Run = cam1Pos2Run
            OLDcam1AtPos2 = cam1AtPos2
            if cam1Pos2Set and not cam1Pos2Run and not cam1AtPos2:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go2.line_color=(1, 0, 0, 1)
            elif cam1Pos2Set and not cam1Pos2Run and cam1AtPos2:
                self.root.get_screen('main').ids.btnCam1Go2.line_color=(0, 1, 0, 1)
            elif not cam1Pos2Set:
                self.root.get_screen('main').ids.btnCam1Go2.line_color=(.13, .13, .13, 1)

        if cam1Pos3Set != OLDcam1Pos3Set or cam1Pos3Run != OLDcam1Pos3Run or cam1AtPos3 != OLDcam1AtPos3 or resetButtons:
            OLDcam1Pos3Set = cam1Pos3Set
            OLDcam1Pos3Run = cam1Pos3Run
            OLDcam1AtPos3 = cam1AtPos3
            if cam1Pos3Set and not cam1Pos3Run and not cam1AtPos3:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go3.line_color=(1, 0, 0, 1)
            elif cam1Pos3Set and not cam1Pos3Run and cam1AtPos3:
                self.root.get_screen('main').ids.btnCam1Go3.line_color=(0, 1, 0, 1)
            elif not cam1Pos3Set:
                self.root.get_screen('main').ids.btnCam1Go3.line_color=(.13, .13, .13, 1)

        if cam1Pos4Set != OLDcam1Pos4Set or cam1Pos4Run != OLDcam1Pos4Run or cam1AtPos4 != OLDcam1AtPos4 or resetButtons:
            OLDcam1Pos4Set = cam1Pos4Set
            OLDcam1Pos4Run = cam1Pos4Run
            OLDcam1AtPos4 = cam1AtPos4
            if cam1Pos4Set and not cam1Pos4Run and not cam1AtPos4:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go4.line_color=(1, 0, 0, 1)
            elif cam1Pos4Set and not cam1Pos4Run and cam1AtPos4:
                self.root.get_screen('main').ids.btnCam1Go4.line_color=(0, 1, 0, 1)
            elif not cam1Pos4Set:
                self.root.get_screen('main').ids.btnCam1Go4.line_color=(.13, .13, .13, 1)

        if cam1Pos5Set != OLDcam1Pos5Set or cam1Pos5Run != OLDcam1Pos5Run or cam1AtPos5 != OLDcam1AtPos5 or resetButtons:
            OLDcam1Pos5Set = cam1Pos5Set
            OLDcam1Pos5Run = cam1Pos5Run
            OLDcam1AtPos5 = cam1AtPos5
            if cam1Pos5Set and not cam1Pos5Run and not cam1AtPos5:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go5.line_color=(1, 0, 0, 1)
            elif cam1Pos5Set and not cam1Pos5Run and cam1AtPos5:
                self.root.get_screen('main').ids.btnCam1Go5.line_color=(0, 1, 0, 1)
            elif not cam1Pos5Set:
                self.root.get_screen('main').ids.btnCam1Go5.line_color=(.13, .13, .13, 1)

        if cam1Pos6Set != OLDcam1Pos6Set or cam1Pos6Run != OLDcam1Pos6Run or cam1AtPos6 != OLDcam1AtPos6 or resetButtons:
            OLDcam1Pos6Set = cam1Pos6Set
            OLDcam1Pos6Run = cam1Pos6Run
            OLDcam1AtPos6 = cam1AtPos6
            if cam1Pos6Set and not cam1Pos6Run and not cam1AtPos6:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go6.line_color=(1, 0, 0, 1)
            elif cam1Pos6Set and not cam1Pos6Run and cam1AtPos6:
                self.root.get_screen('main').ids.btnCam1Go6.line_color=(0, 1, 0, 1)
            elif not cam1Pos6Set:
                self.root.get_screen('main').ids.btnCam1Go6.line_color=(.13, .13, .13, 1)

        if cam1Pos7Set != OLDcam1Pos7Set or cam1Pos7Run != OLDcam1Pos7Run or cam1AtPos7 != OLDcam1AtPos7 or resetButtons:
            OLDcam1Pos7Set = cam1Pos7Set
            OLDcam1Pos7Run = cam1Pos7Run
            OLDcam1AtPos7 = cam1AtPos7
            if cam1Pos7Set and not cam1Pos7Run and not cam1AtPos7:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go7.line_color=(1, 0, 0, 1)
            elif cam1Pos7Set and not cam1Pos7Run and cam1AtPos7:
                self.root.get_screen('main').ids.btnCam1Go7.line_color=(0, 1, 0, 1)
            elif not cam1Pos7Set:
                self.root.get_screen('main').ids.btnCam1Go7.line_color=(.13, .13, .13, 1)

        if cam1Pos8Set != OLDcam1Pos8Set or cam1Pos8Run != OLDcam1Pos8Run or cam1AtPos8 != OLDcam1AtPos8 or resetButtons:
            OLDcam1Pos8Set = cam1Pos8Set
            OLDcam1Pos8Run = cam1Pos8Run
            OLDcam1AtPos8 = cam1AtPos8
            if cam1Pos8Set and not cam1Pos8Run and not cam1AtPos8:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go8.line_color=(1, 0, 0, 1)
            elif cam1Pos8Set and not cam1Pos8Run and cam1AtPos8:
                self.root.get_screen('main').ids.btnCam1Go8.line_color=(0, 1, 0, 1)
            elif not cam1Pos8Set:
                self.root.get_screen('main').ids.btnCam1Go8.line_color=(.13, .13, .13, 1)

        if cam1Pos9Set != OLDcam1Pos9Set or cam1Pos9Run != OLDcam1Pos9Run or cam1AtPos9 != OLDcam1AtPos9 or resetButtons:
            OLDcam1Pos9Set = cam1Pos9Set
            OLDcam1Pos9Run = cam1Pos9Run
            OLDcam1AtPos9 = cam1AtPos9
            if cam1Pos9Set and not cam1Pos9Run and not cam1AtPos9:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go9.line_color=(1, 0, 0, 1)
            elif cam1Pos9Set and not cam1Pos9Run and cam1AtPos9:
                self.root.get_screen('main').ids.btnCam1Go9.line_color=(0, 1, 0, 1)
            elif not cam1Pos9Set:
                self.root.get_screen('main').ids.btnCam1Go9.line_color=(.13, .13, .13, 1)

        if cam1Pos10Set != OLDcam1Pos10Set or cam1Pos10Run != OLDcam1Pos10Run or cam1AtPos10 != OLDcam1AtPos10 or resetButtons:
            OLDcam1Pos10Set = cam1Pos10Set
            OLDcam1Pos10Run = cam1Pos10Run
            OLDcam1AtPos10 = cam1AtPos10
            if cam1Pos10Set and not cam1Pos10Run and not cam1AtPos10:                                  # Position LEDs Cam1
                self.root.get_screen('main').ids.btnCam1Go10.line_color=(1, 0, 0, 1)
            elif cam1Pos10Set and not cam1Pos10Run and cam1AtPos10:
                self.root.get_screen('main').ids.btnCam1Go10.line_color=(0, 1, 0, 1)
            elif not cam1Pos10Set:
                self.root.get_screen('main').ids.btnCam1Go10.line_color=(.13, .13, .13, 1)


        if cam2Pos1Set != OLDcam2Pos1Set or cam2Pos1Run != OLDcam2Pos1Run or cam2AtPos1 != OLDcam2AtPos1 or resetButtons:
            OLDcam2Pos1Set = cam2Pos1Set
            OLDcam2Pos1Run = cam2Pos1Run
            OLDcam2AtPos1 = cam2AtPos1
            if cam2Pos1Set and not cam2Pos1Run and not cam2AtPos1:                                  # Set , not Run or At
                self.root.get_screen('main').ids.btnCam2Go1.line_color=(1, 0, 0, 1)
            elif cam2Pos1Set and not cam2Pos1Run and cam2AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam2Go1.line_color=(0, 1, 0, 1)
            elif not cam2Pos1Set:
                self.root.get_screen('main').ids.btnCam2Go1.line_color=(.13, .13, .13, 1)

        if cam2Pos2Set != OLDcam2Pos2Set or cam2Pos2Run != OLDcam2Pos2Run or cam2AtPos2 != OLDcam2AtPos2 or resetButtons:
            OLDcam2Pos2Set = cam2Pos2Set
            OLDcam2Pos2Run = cam2Pos2Run
            OLDcam2AtPos2 = cam2AtPos2
            if cam2Pos2Set and not cam2Pos2Run and not cam2AtPos2:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go2.line_color=(1, 0, 0, 1)
            elif cam2Pos2Set and not cam2Pos2Run and cam2AtPos2:
                self.root.get_screen('main').ids.btnCam2Go2.line_color=(0, 1, 0, 1)
            elif not cam2Pos2Set:
                self.root.get_screen('main').ids.btnCam2Go2.line_color=(.13, .13, .13, 1)

        if cam2Pos3Set != OLDcam2Pos3Set or cam2Pos3Run != OLDcam2Pos3Run or cam2AtPos3 != OLDcam2AtPos3 or resetButtons:
            OLDcam2Pos3Set = cam2Pos3Set
            OLDcam2Pos3Run = cam2Pos3Run
            OLDcam2AtPos3 = cam2AtPos3
            if cam2Pos3Set and not cam2Pos3Run and not cam2AtPos3:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go3.line_color=(1, 0, 0, 1)
            elif cam2Pos3Set and not cam2Pos3Run and cam2AtPos3:
                self.root.get_screen('main').ids.btnCam2Go3.line_color=(0, 1, 0, 1)
            elif not cam2Pos3Set:
                self.root.get_screen('main').ids.btnCam2Go3.line_color=(.13, .13, .13, 1)

        if cam2Pos4Set != OLDcam2Pos4Set or cam2Pos4Run != OLDcam2Pos4Run or cam2AtPos4 != OLDcam2AtPos4 or resetButtons:
            OLDcam2Pos4Set = cam2Pos4Set
            OLDcam2Pos4Run = cam2Pos4Run
            OLDcam2AtPos4 = cam2AtPos4
            if cam2Pos4Set and not cam2Pos4Run and not cam2AtPos4:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go4.line_color=(1, 0, 0, 1)
            elif cam2Pos4Set and not cam2Pos4Run and cam2AtPos4:
                self.root.get_screen('main').ids.btnCam2Go4.line_color=(0, 1, 0, 1)
            elif not cam2Pos4Set:
                self.root.get_screen('main').ids.btnCam2Go4.line_color=(.13, .13, .13, 1)

        if cam2Pos5Set != OLDcam2Pos5Set or cam2Pos5Run != OLDcam2Pos5Run or cam2AtPos5 != OLDcam2AtPos5 or resetButtons:
            OLDcam2Pos5Set = cam2Pos5Set
            OLDcam2Pos5Run = cam2Pos5Run
            OLDcam2AtPos5 = cam2AtPos5
            if cam2Pos5Set and not cam2Pos5Run and not cam2AtPos5:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go5.line_color=(1, 0, 0, 1)
            elif cam2Pos5Set and not cam2Pos5Run and cam2AtPos5:
                self.root.get_screen('main').ids.btnCam2Go5.line_color=(0, 1, 0, 1)
            elif not cam2Pos5Set:
                self.root.get_screen('main').ids.btnCam2Go5.line_color=(.13, .13, .13, 1)

        if cam2Pos6Set != OLDcam2Pos6Set or cam2Pos6Run != OLDcam2Pos6Run or cam2AtPos6 != OLDcam2AtPos6 or resetButtons:
            OLDcam2Pos6Set = cam2Pos6Set
            OLDcam2Pos6Run = cam2Pos6Run
            OLDcam2AtPos6 = cam2AtPos6
            if cam2Pos6Set and not cam2Pos6Run and not cam2AtPos6:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go6.line_color=(1, 0, 0, 1)
            elif cam2Pos6Set and not cam2Pos6Run and cam2AtPos6:
                self.root.get_screen('main').ids.btnCam2Go6.line_color=(0, 1, 0, 1)
            elif not cam2Pos6Set:
                self.root.get_screen('main').ids.btnCam2Go6.line_color=(.13, .13, .13, 1)

        if cam2Pos7Set != OLDcam2Pos7Set or cam2Pos7Run != OLDcam2Pos7Run or cam2AtPos7 != OLDcam2AtPos7 or resetButtons:
            OLDcam2Pos7Set = cam2Pos7Set
            OLDcam2Pos7Run = cam2Pos7Run
            OLDcam2AtPos7 = cam2AtPos7
            if cam2Pos7Set and not cam2Pos7Run and not cam2AtPos7:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go7.line_color=(1, 0, 0, 1)
            elif cam2Pos7Set and not cam2Pos7Run and cam2AtPos7:
                self.root.get_screen('main').ids.btnCam2Go7.line_color=(0, 1, 0, 1)
            elif not cam2Pos7Set:
                self.root.get_screen('main').ids.btnCam2Go7.line_color=(.13, .13, .13, 1)

        if cam2Pos8Set != OLDcam2Pos8Set or cam2Pos8Run != OLDcam2Pos8Run or cam2AtPos8 != OLDcam2AtPos8 or resetButtons:
            OLDcam2Pos8Set = cam2Pos8Set
            OLDcam2Pos8Run = cam2Pos8Run
            OLDcam2AtPos8 = cam2AtPos8
            if cam2Pos8Set and not cam2Pos8Run and not cam2AtPos8:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go8.line_color=(1, 0, 0, 1)
            elif cam2Pos8Set and not cam2Pos8Run and cam2AtPos8:
                self.root.get_screen('main').ids.btnCam2Go8.line_color=(0, 1, 0, 1)
            elif not cam2Pos8Set:
                self.root.get_screen('main').ids.btnCam2Go8.line_color=(.13, .13, .13, 1)

        if cam2Pos9Set != OLDcam2Pos9Set or cam2Pos9Run != OLDcam2Pos9Run or cam2AtPos9 != OLDcam2AtPos9 or resetButtons:
            OLDcam2Pos9Set = cam2Pos9Set
            OLDcam2Pos9Run = cam2Pos9Run
            OLDcam2AtPos9 = cam2AtPos9
            if cam2Pos9Set and not cam2Pos9Run and not cam2AtPos9:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go9.line_color=(1, 0, 0, 1)
            elif cam2Pos9Set and not cam2Pos9Run and cam2AtPos9:
                self.root.get_screen('main').ids.btnCam2Go9.line_color=(0, 1, 0, 1)
            elif not cam2Pos9Set:
                self.root.get_screen('main').ids.btnCam2Go9.line_color=(.13, .13, .13, 1)

        if cam2Pos10Set != OLDcam2Pos10Set or cam2Pos10Run != OLDcam2Pos10Run or cam2AtPos10 != OLDcam2AtPos10 or resetButtons:
            OLDcam2Pos10Set = cam2Pos10Set
            OLDcam2Pos10Run = cam2Pos10Run
            OLDcam2AtPos10 = cam2AtPos10
            if cam2Pos10Set and not cam2Pos10Run and not cam2AtPos10:                                  # Position LEDs Cam2
                self.root.get_screen('main').ids.btnCam2Go10.line_color=(1, 0, 0, 1)
            elif cam2Pos10Set and not cam2Pos10Run and cam2AtPos10:
                self.root.get_screen('main').ids.btnCam2Go10.line_color=(0, 1, 0, 1)
            elif not cam2Pos10Set:
                self.root.get_screen('main').ids.btnCam2Go10.line_color=(.13, .13, .13, 1)



        if cam3Pos1Set != OLDcam3Pos1Set or cam3Pos1Run != OLDcam3Pos1Run or cam3AtPos1 != OLDcam3AtPos1 or resetButtons:
            OLDcam3Pos1Set = cam3Pos1Set
            OLDcam3Pos1Run = cam3Pos1Run
            OLDcam3AtPos1 = cam3AtPos1
            if cam3Pos1Set and not cam3Pos1Run and not cam3AtPos1:                                  # Set , not Run or At
                self.root.get_screen('main').ids.btnCam3Go1.line_color=(1, 0, 0, 1)
            elif cam3Pos1Set and not cam3Pos1Run and cam3AtPos1:                                    # Set & At, not Run
                self.root.get_screen('main').ids.btnCam3Go1.line_color=(0, 1, 0, 1)
            elif not cam3Pos1Set:
                self.root.get_screen('main').ids.btnCam3Go1.line_color=(.13, .13, .13, 1)

        if cam3Pos2Set != OLDcam3Pos2Set or cam3Pos2Run != OLDcam3Pos2Run or cam3AtPos2 != OLDcam3AtPos2 or resetButtons:
            OLDcam3Pos2Set = cam3Pos2Set
            OLDcam3Pos2Run = cam3Pos2Run
            OLDcam3AtPos2 = cam3AtPos2
            if cam3Pos2Set and not cam3Pos2Run and not cam3AtPos2:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go2.line_color=(1, 0, 0, 1)
            elif cam3Pos2Set and not cam3Pos2Run and cam3AtPos2:
                self.root.get_screen('main').ids.btnCam3Go2.line_color=(0, 1, 0, 1)
            elif not cam3Pos2Set:
                self.root.get_screen('main').ids.btnCam3Go2.line_color=(.13, .13, .13, 1)

        if cam3Pos3Set != OLDcam3Pos3Set or cam3Pos3Run != OLDcam3Pos3Run or cam3AtPos3 != OLDcam3AtPos3 or resetButtons:
            OLDcam3Pos3Set = cam3Pos3Set
            OLDcam3Pos3Run = cam3Pos3Run
            OLDcam3AtPos3 = cam3AtPos3
            if cam3Pos3Set and not cam3Pos3Run and not cam3AtPos3:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go3.line_color=(1, 0, 0, 1)
            elif cam3Pos3Set and not cam3Pos3Run and cam3AtPos3:
                self.root.get_screen('main').ids.btnCam3Go3.line_color=(0, 1, 0, 1)
            elif not cam3Pos3Set:
                self.root.get_screen('main').ids.btnCam3Go3.line_color=(.13, .13, .13, 1)

        if cam3Pos4Set != OLDcam3Pos4Set or cam3Pos4Run != OLDcam3Pos4Run or cam3AtPos4 != OLDcam3AtPos4 or resetButtons:
            OLDcam3Pos4Set = cam3Pos4Set
            OLDcam3Pos4Run = cam3Pos4Run
            OLDcam3AtPos4 = cam3AtPos4
            if cam3Pos4Set and not cam3Pos4Run and not cam3AtPos4:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go4.line_color=(1, 0, 0, 1)
            elif cam3Pos4Set and not cam3Pos4Run and cam3AtPos4:
                self.root.get_screen('main').ids.btnCam3Go4.line_color=(0, 1, 0, 1)
            elif not cam3Pos4Set:
                self.root.get_screen('main').ids.btnCam3Go4.line_color=(.13, .13, .13, 1)

        if cam3Pos5Set != OLDcam3Pos5Set or cam3Pos5Run != OLDcam3Pos5Run or cam3AtPos5 != OLDcam3AtPos5 or resetButtons:
            OLDcam3Pos5Set = cam3Pos5Set
            OLDcam3Pos5Run = cam3Pos5Run
            OLDcam3AtPos5 = cam3AtPos5
            if cam3Pos5Set and not cam3Pos5Run and not cam3AtPos5:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go5.line_color=(1, 0, 0, 1)
            elif cam3Pos5Set and not cam3Pos5Run and cam3AtPos5:
                self.root.get_screen('main').ids.btnCam3Go5.line_color=(0, 1, 0, 1)
            elif not cam3Pos5Set:
                self.root.get_screen('main').ids.btnCam3Go5.line_color=(.13, .13, .13, 1)

        if cam3Pos6Set != OLDcam3Pos6Set or cam3Pos6Run != OLDcam3Pos6Run or cam3AtPos6 != OLDcam3AtPos6 or resetButtons:
            OLDcam3Pos6Set = cam3Pos6Set
            OLDcam3Pos6Run = cam3Pos6Run
            OLDcam3AtPos6 = cam3AtPos6
            if cam3Pos6Set and not cam3Pos6Run and not cam3AtPos6:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go6.line_color=(1, 0, 0, 1)
            elif cam3Pos6Set and not cam3Pos6Run and cam3AtPos6:
                self.root.get_screen('main').ids.btnCam3Go6.line_color=(0, 1, 0, 1)
            elif not cam3Pos6Set:
                self.root.get_screen('main').ids.btnCam3Go6.line_color=(.13, .13, .13, 1)

        if cam3Pos7Set != OLDcam3Pos7Set or cam3Pos7Run != OLDcam3Pos7Run or cam3AtPos7 != OLDcam3AtPos7 or resetButtons:
            OLDcam3Pos7Set = cam3Pos7Set
            OLDcam3Pos7Run = cam3Pos7Run
            OLDcam3AtPos7 = cam3AtPos7
            if cam3Pos7Set and not cam3Pos7Run and not cam3AtPos7:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go7.line_color=(1, 0, 0, 1)
            elif cam3Pos7Set and not cam3Pos7Run and cam3AtPos7:
                self.root.get_screen('main').ids.btnCam3Go7.line_color=(0, 1, 0, 1)
            elif not cam3Pos7Set:
                self.root.get_screen('main').ids.btnCam3Go7.line_color=(.13, .13, .13, 1)

        if cam3Pos8Set != OLDcam3Pos8Set or cam3Pos8Run != OLDcam3Pos8Run or cam3AtPos8 != OLDcam3AtPos8 or resetButtons:
            OLDcam3Pos8Set = cam3Pos8Set
            OLDcam3Pos8Run = cam3Pos8Run
            OLDcam3AtPos8 = cam3AtPos8
            if cam3Pos8Set and not cam3Pos8Run and not cam3AtPos8:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go8.line_color=(1, 0, 0, 1)
            elif cam3Pos8Set and not cam3Pos8Run and cam3AtPos8:
                self.root.get_screen('main').ids.btnCam3Go8.line_color=(0, 1, 0, 1)
            elif not cam3Pos8Set:
                self.root.get_screen('main').ids.btnCam3Go8.line_color=(.13, .13, .13, 1)

        if cam3Pos9Set != OLDcam3Pos9Set or cam3Pos9Run != OLDcam3Pos9Run or cam3AtPos9 != OLDcam3AtPos9 or resetButtons:
            OLDcam3Pos9Set = cam3Pos9Set
            OLDcam3Pos9Run = cam3Pos9Run
            OLDcam3AtPos9 = cam3AtPos9
            if cam3Pos9Set and not cam3Pos9Run and not cam3AtPos9:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go9.line_color=(1, 0, 0, 1)
            elif cam3Pos9Set and not cam3Pos9Run and cam3AtPos9:
                self.root.get_screen('main').ids.btnCam3Go9.line_color=(0, 1, 0, 1)
            elif not cam3Pos9Set:
                self.root.get_screen('main').ids.btnCam3Go9.line_color=(.13, .13, .13, 1)

        if cam3Pos10Set != OLDcam3Pos10Set or cam3Pos10Run != OLDcam3Pos10Run or cam3AtPos10 != OLDcam3AtPos10 or resetButtons:
            OLDcam3Pos10Set = cam3Pos10Set
            OLDcam3Pos10Run = cam3Pos10Run
            OLDcam3AtPos10 = cam3AtPos10
            if cam3Pos10Set and not cam3Pos10Run and not cam3AtPos10:                                  # Position LEDs Cam3
                self.root.get_screen('main').ids.btnCam3Go10.line_color=(1, 0, 0, 1)
            elif cam3Pos10Set and not cam3Pos10Run and cam3AtPos10:
                self.root.get_screen('main').ids.btnCam3Go10.line_color=(0, 1, 0, 1)
            elif not cam3Pos10Set:
                self.root.get_screen('main').ids.btnCam3Go10.line_color=(.13, .13, .13, 1)




        if cam4Pos1Set != OLDcam4Pos1Set or cam4Pos1Run != OLDcam4Pos1Run or cam4AtPos1 != OLDcam4AtPos1 or resetButtons:
            OLDcam4Pos1Set = cam4Pos1Set
            OLDcam4Pos1Run = cam4Pos1Run
            OLDcam4AtPos1 = cam4AtPos1
            if cam4Pos1Set and not cam4Pos1Run and not cam4AtPos1:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go1.line_color=(1, 0, 0, 1)
            elif cam4Pos1Set and not cam4Pos1Run and cam4AtPos1:
                self.root.get_screen('main').ids.btnCam4Go1.line_color=(0, 1, 0, 1)
            elif not cam4Pos1Set:
                self.root.get_screen('main').ids.btnCam4Go1.line_color=(.13, .13, .13, 1)

        if cam4Pos2Set != OLDcam4Pos2Set or cam4Pos2Run != OLDcam4Pos2Run or cam4AtPos2 != OLDcam4AtPos2 or resetButtons:
            OLDcam4Pos2Set = cam4Pos2Set
            OLDcam4Pos2Run = cam4Pos2Run
            OLDcam4AtPos2 = cam4AtPos2
            if cam4Pos2Set and not cam4Pos2Run and not cam4AtPos2:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go2.line_color=(1, 0, 0, 1)
            elif cam4Pos2Set and not cam4Pos2Run and cam4AtPos2:
                self.root.get_screen('main').ids.btnCam4Go2.line_color=(0, 1, 0, 1)
            elif not cam4Pos2Set:
                self.root.get_screen('main').ids.btnCam4Go2.line_color=(.13, .13, .13, 1)

        if cam4Pos3Set != OLDcam4Pos3Set or cam4Pos3Run != OLDcam4Pos3Run or cam4AtPos3 != OLDcam4AtPos3 or resetButtons:
            OLDcam4Pos3Set = cam4Pos3Set
            OLDcam4Pos3Run = cam4Pos3Run
            OLDcam4AtPos3 = cam4AtPos3
            if cam4Pos3Set and not cam4Pos3Run and not cam4AtPos3:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go3.line_color=(1, 0, 0, 1)
            elif cam4Pos3Set and not cam4Pos3Run and cam4AtPos3:
                self.root.get_screen('main').ids.btnCam4Go3.line_color=(0, 1, 0, 1)
            elif not cam4Pos3Set:
                self.root.get_screen('main').ids.btnCam4Go3.line_color=(.13, .13, .13, 1)

        if cam4Pos4Set != OLDcam4Pos4Set or cam4Pos4Run != OLDcam4Pos4Run or cam4AtPos4 != OLDcam4AtPos4 or resetButtons:
            OLDcam4Pos4Set = cam4Pos4Set
            OLDcam4Pos4Run = cam4Pos4Run
            OLDcam4AtPos4 = cam4AtPos4
            if cam4Pos4Set and not cam4Pos4Run and not cam4AtPos4:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go4.line_color=(1, 0, 0, 1)
            elif cam4Pos4Set and not cam4Pos4Run and cam4AtPos4:
                self.root.get_screen('main').ids.btnCam4Go4.line_color=(0, 1, 0, 1)
            elif not cam4Pos4Set:
                self.root.get_screen('main').ids.btnCam4Go4.line_color=(.13, .13, .13, 1)

        if cam4Pos5Set != OLDcam4Pos5Set or cam4Pos5Run != OLDcam4Pos5Run or cam4AtPos5 != OLDcam4AtPos5 or resetButtons:
            OLDcam4Pos5Set = cam4Pos5Set
            OLDcam4Pos5Run = cam4Pos5Run
            OLDcam4AtPos5 = cam4AtPos5
            if cam4Pos5Set and not cam4Pos5Run and not cam4AtPos5:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go5.line_color=(1, 0, 0, 1)
            elif cam4Pos5Set and not cam4Pos5Run and cam4AtPos5:
                self.root.get_screen('main').ids.btnCam4Go5.line_color=(0, 1, 0, 1)
            elif not cam4Pos5Set:
                self.root.get_screen('main').ids.btnCam4Go5.line_color=(.13, .13, .13, 1)

        if cam4Pos6Set != OLDcam4Pos6Set or cam4Pos6Run != OLDcam4Pos6Run or cam4AtPos6 != OLDcam4AtPos6 or resetButtons:
            OLDcam4Pos6Set = cam4Pos6Set
            OLDcam4Pos6Run = cam4Pos6Run
            OLDcam4AtPos6 = cam4AtPos6
            if cam4Pos6Set and not cam4Pos6Run and not cam4AtPos6:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go6.line_color=(1, 0, 0, 1)
            elif cam4Pos6Set and not cam4Pos6Run and cam4AtPos6:
                self.root.get_screen('main').ids.btnCam4Go6.line_color=(0, 1, 0, 1)
            elif not cam4Pos6Set:
                self.root.get_screen('main').ids.btnCam4Go6.line_color=(.13, .13, .13, 1)

        if cam4Pos7Set != OLDcam4Pos7Set or cam4Pos7Run != OLDcam4Pos7Run or cam4AtPos7 != OLDcam4AtPos7 or resetButtons:
            OLDcam4Pos7Set = cam4Pos7Set
            OLDcam4Pos7Run = cam4Pos7Run
            OLDcam4AtPos7 = cam4AtPos7
            if cam4Pos7Set and not cam4Pos7Run and not cam4AtPos7:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go7.line_color=(1, 0, 0, 1)
            elif cam4Pos7Set and not cam4Pos7Run and cam4AtPos7:
                self.root.get_screen('main').ids.btnCam4Go7.line_color=(0, 1, 0, 1)
            elif not cam4Pos7Set:
                self.root.get_screen('main').ids.btnCam4Go7.line_color=(.13, .13, .13, 1)

        if cam4Pos8Set != OLDcam4Pos8Set or cam4Pos8Run != OLDcam4Pos8Run or cam4AtPos8 != OLDcam4AtPos8 or resetButtons:
            OLDcam4Pos8Set = cam4Pos8Set
            OLDcam4Pos8Run = cam4Pos8Run
            OLDcam4AtPos8 = cam4AtPos8
            if cam4Pos8Set and not cam4Pos8Run and not cam4AtPos8:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go8.line_color=(1, 0, 0, 1)
            elif cam4Pos8Set and not cam4Pos8Run and cam4AtPos8:
                self.root.get_screen('main').ids.btnCam4Go8.line_color=(0, 1, 0, 1)
            elif not cam4Pos8Set:
                self.root.get_screen('main').ids.btnCam4Go8.line_color=(.13, .13, .13, 1)

        if cam4Pos9Set != OLDcam4Pos9Set or cam4Pos9Run != OLDcam4Pos9Run or cam4AtPos9 != OLDcam4AtPos9 or resetButtons:
            OLDcam4Pos9Set = cam4Pos9Set
            OLDcam4Pos9Run = cam4Pos9Run
            OLDcam4AtPos9 = cam4AtPos9
            if cam4Pos9Set and not cam4Pos9Run and not cam4AtPos9:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go9.line_color=(1, 0, 0, 1)
            elif cam4Pos9Set and not cam4Pos9Run and cam4AtPos9:
                self.root.get_screen('main').ids.btnCam4Go9.line_color=(0, 1, 0, 1)
            elif not cam4Pos9Set:
                self.root.get_screen('main').ids.btnCam4Go9.line_color=(.13, .13, .13, 1)

        if cam4Pos10Set != OLDcam4Pos10Set or cam4Pos10Run != OLDcam4Pos10Run or cam4AtPos10 != OLDcam4AtPos10 or resetButtons:
            OLDcam4Pos10Set = cam4Pos10Set
            OLDcam4Pos10Run = cam4Pos10Run
            OLDcam4AtPos10 = cam4AtPos10
            if cam4Pos10Set and not cam4Pos10Run and not cam4AtPos10:                                  # Position LEDs cam4
                self.root.get_screen('main').ids.btnCam4Go10.line_color=(1, 0, 0, 1)
            elif cam4Pos10Set and not cam4Pos10Run and cam4AtPos10:
                self.root.get_screen('main').ids.btnCam4Go10.line_color=(0, 1, 0, 1)
            elif not cam4Pos10Set:
                self.root.get_screen('main').ids.btnCam4Go10.line_color=(.13, .13, .13, 1)


        

        if cam5Pos1Set != OLDcam5Pos1Set or cam5Pos1Run != OLDcam5Pos1Run or cam5AtPos1 != OLDcam5AtPos1 or resetButtons:
            OLDcam5Pos1Set = cam5Pos1Set
            OLDcam5Pos1Run = cam5Pos1Run
            OLDcam5AtPos1 = cam5AtPos1
            if cam5Pos1Set and not cam5Pos1Run and not cam5AtPos1:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go1.line_color=(1, 0, 0, 1)
            elif cam5Pos1Set and not cam5Pos1Run and cam5AtPos1:
                self.root.get_screen('main').ids.btnCam5Go1.line_color=(0, 1, 0, 1)
            elif not cam5Pos1Set:
                self.root.get_screen('main').ids.btnCam5Go1.line_color=(.13, .13, .13, 1)

        if cam5Pos2Set != OLDcam5Pos2Set or cam5Pos2Run != OLDcam5Pos2Run or cam5AtPos2 != OLDcam5AtPos2 or resetButtons:
            OLDcam5Pos2Set = cam5Pos2Set
            OLDcam5Pos2Run = cam5Pos2Run
            OLDcam5AtPos2 = cam5AtPos2
            if cam5Pos2Set and not cam5Pos2Run and not cam5AtPos2:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go2.line_color=(1, 0, 0, 1)
            elif cam5Pos2Set and not cam5Pos2Run and cam5AtPos2:
                self.root.get_screen('main').ids.btnCam5Go2.line_color=(0, 1, 0, 1)
            elif not cam5Pos2Set:
                self.root.get_screen('main').ids.btnCam5Go2.line_color=(.13, .13, .13, 1)

        if cam5Pos3Set != OLDcam5Pos3Set or cam5Pos3Run != OLDcam5Pos3Run or cam5AtPos3 != OLDcam5AtPos3 or resetButtons:
            OLDcam5Pos3Set = cam5Pos3Set
            OLDcam5Pos3Run = cam5Pos3Run
            OLDcam5AtPos3 = cam5AtPos3
            if cam5Pos3Set and not cam5Pos3Run and not cam5AtPos3:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go3.line_color=(1, 0, 0, 1)
            elif cam5Pos3Set and not cam5Pos3Run and cam5AtPos3:
                self.root.get_screen('main').ids.btnCam5Go3.line_color=(0, 1, 0, 1)
            elif not cam5Pos3Set:
                self.root.get_screen('main').ids.btnCam5Go3.line_color=(.13, .13, .13, 1)
                self.root.get_screen('main').ids.btnCam5Go3.line_color=(.13, .13, .13, 1)

        if cam5Pos4Set != OLDcam5Pos4Set or cam5Pos4Run != OLDcam5Pos4Run or cam5AtPos4 != OLDcam5AtPos4 or resetButtons:
            OLDcam5Pos4Set = cam5Pos4Set
            OLDcam5Pos4Run = cam5Pos4Run
            OLDcam5AtPos4 = cam5AtPos4
            if cam5Pos4Set and not cam5Pos4Run and not cam5AtPos4:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go4.line_color=(1, 0, 0, 1)
            elif cam5Pos4Set and not cam5Pos4Run and cam5AtPos4:
                self.root.get_screen('main').ids.btnCam5Go4.line_color=(0, 1, 0, 1)
            elif not cam5Pos4Set:
                self.root.get_screen('main').ids.btnCam5Go4.line_color=(.13, .13, .13, 1)

        if cam5Pos5Set != OLDcam5Pos5Set or cam5Pos5Run != OLDcam5Pos5Run or cam5AtPos5 != OLDcam5AtPos5 or resetButtons:
            OLDcam5Pos5Set = cam5Pos5Set
            OLDcam5Pos5Run = cam5Pos5Run
            OLDcam5AtPos5 = cam5AtPos5
            if cam5Pos5Set and not cam5Pos5Run and not cam5AtPos5:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go5.line_color=(1, 0, 0, 1)
            elif cam5Pos5Set and not cam5Pos5Run and cam5AtPos5:
                self.root.get_screen('main').ids.btnCam5Go5.line_color=(0, 1, 0, 1)
            elif not cam5Pos5Set:
                self.root.get_screen('main').ids.btnCam5Go5.line_color=(.13, .13, .13, 1)

        if cam5Pos6Set != OLDcam5Pos6Set or cam5Pos6Run != OLDcam5Pos6Run or cam5AtPos6 != OLDcam5AtPos6 or resetButtons:
            OLDcam5Pos6Set = cam5Pos6Set
            OLDcam5Pos6Run = cam5Pos6Run
            OLDcam5AtPos6 = cam5AtPos6
            if cam5Pos6Set and not cam5Pos6Run and not cam5AtPos6:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go6.line_color=(1, 0, 0, 1)
            elif cam5Pos6Set and not cam5Pos6Run and cam5AtPos6:
                self.root.get_screen('main').ids.btnCam5Go6.line_color=(0, 1, 0, 1)
            elif not cam5Pos6Set:
                self.root.get_screen('main').ids.btnCam5Go6.line_color=(.13, .13, .13, 1)

        if cam5Pos7Set != OLDcam5Pos7Set or cam5Pos7Run != OLDcam5Pos7Run or cam5AtPos7 != OLDcam5AtPos7 or resetButtons:
            OLDcam5Pos7Set = cam5Pos7Set
            OLDcam5Pos7Run = cam5Pos7Run
            OLDcam5AtPos7 = cam5AtPos7
            if cam5Pos7Set and not cam5Pos7Run and not cam5AtPos7:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go7.line_color=(1, 0, 0, 1)
            elif cam5Pos7Set and not cam5Pos7Run and cam5AtPos7:
                self.root.get_screen('main').ids.btnCam5Go7.line_color=(0, 1, 0, 1)
            elif not cam5Pos7Set:
                self.root.get_screen('main').ids.btnCam5Go7.line_color=(.13, .13, .13, 1)

        if cam5Pos8Set != OLDcam5Pos8Set or cam5Pos8Run != OLDcam5Pos8Run or cam5AtPos8 != OLDcam5AtPos8 or resetButtons:
            OLDcam5Pos8Set = cam5Pos8Set
            OLDcam5Pos8Run = cam5Pos8Run
            OLDcam5AtPos8 = cam5AtPos8
            if cam5Pos8Set and not cam5Pos8Run and not cam5AtPos8:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go8.line_color=(1, 0, 0, 1)
            elif cam5Pos8Set and not cam5Pos8Run and cam5AtPos8:
                self.root.get_screen('main').ids.btnCam5Go8.line_color=(0, 1, 0, 1)
            elif not cam5Pos8Set:
                self.root.get_screen('main').ids.btnCam5Go8.line_color=(.13, .13, .13, 1)

        if cam5Pos9Set != OLDcam5Pos9Set or cam5Pos9Run != OLDcam5Pos9Run or cam5AtPos9 != OLDcam5AtPos9 or resetButtons:
            OLDcam5Pos9Set = cam5Pos9Set
            OLDcam5Pos9Run = cam5Pos9Run
            OLDcam5AtPos9 = cam5AtPos9
            if cam5Pos9Set and not cam5Pos9Run and not cam5AtPos9:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go9.line_color=(1, 0, 0, 1)
            elif cam5Pos9Set and not cam5Pos9Run and cam5AtPos9:
                self.root.get_screen('main').ids.btnCam5Go9.line_color=(0, 1, 0, 1)
            elif not cam5Pos9Set:
                self.root.get_screen('main').ids.btnCam5Go9.line_color=(.13, .13, .13, 1)

        if cam5Pos10Set != OLDcam5Pos10Set or cam5Pos10Run != OLDcam5Pos10Run or cam5AtPos10 != OLDcam5AtPos10 or resetButtons:
            OLDcam5Pos10Set = cam5Pos10Set
            OLDcam5Pos10Run = cam5Pos10Run
            OLDcam5AtPos10 = cam5AtPos10
            if cam5Pos10Set and not cam5Pos10Run and not cam5AtPos10:                                  # Position LEDs cam5
                self.root.get_screen('main').ids.btnCam5Go10.line_color=(1, 0, 0, 1)
            elif cam5Pos10Set and not cam5Pos10Run and cam5AtPos10:
                self.root.get_screen('main').ids.btnCam5Go10.line_color=(0, 1, 0, 1)
            elif not cam5Pos10Set:
                self.root.get_screen('main').ids.btnCam5Go10.line_color=(.13, .13, .13, 1)





        if oldCam1PTSpeed != cam1PTSpeed:
            oldCam1PTSpeed = cam1PTSpeed
            if cam1PTSpeed == 1:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*3.125), (yDivSet*3))
            elif cam1PTSpeed == 3:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*6.25), (yDivSet*3))
            elif cam1PTSpeed == 5:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*9.375), (yDivSet*3))
            elif cam1PTSpeed == 7:
                self.root.get_screen('main').ids.cam1PTSpd.sizPT1=((xDivSet*12.5), (yDivSet*3))

        if oldCam2PTSpeed != cam2PTSpeed:
            oldCam2PTSpeed = cam2PTSpeed
            if cam2PTSpeed == 1:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*3.125), (yDivSet*3))
            elif cam2PTSpeed == 3:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*6.25), (yDivSet*3))
            elif cam2PTSpeed == 5:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*9.375), (yDivSet*3))
            elif cam2PTSpeed == 7:
                self.root.get_screen('main').ids.cam2PTSpd.sizPT2=((xDivSet*12.5), (yDivSet*3))

        if oldCam3PTSpeed != cam3PTSpeed:
            oldCam3PTSpeed = cam3PTSpeed
            if cam3PTSpeed == 1:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*3.125), (yDivSet*3))
            elif cam3PTSpeed == 3:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*6.25), (yDivSet*3))
            elif cam3PTSpeed == 5:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*9.375), (yDivSet*3))
            elif cam3PTSpeed == 7:
                self.root.get_screen('main').ids.cam3PTSpd.sizPT3=((xDivSet*12.5), (yDivSet*3))

        if oldCam4PTSpeed != cam4PTSpeed:
            oldCam4PTSpeed = cam4PTSpeed
            if cam4PTSpeed == 1:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*3.125), (yDivSet*3))
            elif cam4PTSpeed == 3:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*6.25), (yDivSet*3))
            elif cam4PTSpeed == 5:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*9.375), (yDivSet*3))
            elif cam4PTSpeed == 7:
                self.root.get_screen('main').ids.cam4PTSpd.sizPT4=((xDivSet*12.5), (yDivSet*3))

        if oldCam5PTSpeed != cam5PTSpeed:
            oldCam5PTSpeed = cam5PTSpeed
            if cam5PTSpeed == 1:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*3.125), (yDivSet*3))
            elif cam5PTSpeed == 3:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*6.25), (yDivSet*3))
            elif cam5PTSpeed == 5:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*9.375), (yDivSet*3))
            elif cam5PTSpeed == 7:
                self.root.get_screen('main').ids.cam5PTSpd.sizPT5=((xDivSet*12.5), (yDivSet*3))

        if oldCam1Speed != cam1SliderSpeed:
            oldCam1Speed = cam1SliderSpeed
            if cam1SliderSpeed == 1:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*3.125), (yDivSet*3))
            elif cam1SliderSpeed == 3:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*6.25), (yDivSet*3))
            elif cam1SliderSpeed == 5:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*9.375), (yDivSet*3))
            elif cam1SliderSpeed == 7:
                self.root.get_screen('main').ids.cam1SlSpd.sizSl1=((xDivSet*12.5), (yDivSet*3))

        if oldCam2Speed != cam2SliderSpeed:
            oldCam2Speed = cam2SliderSpeed
            if cam2SliderSpeed == 1:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*3.125), (yDivSet*3))
            elif cam2SliderSpeed == 3:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*6.25), (yDivSet*3))
            elif cam2SliderSpeed == 5:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*9.375), (yDivSet*3))
            elif cam2SliderSpeed == 7:
                self.root.get_screen('main').ids.cam2SlSpd.sizSl2=((xDivSet*12.5), (yDivSet*3))

        if oldCam3Speed != cam3SliderSpeed:
            oldCam3Speed = cam3SliderSpeed
            if cam3SliderSpeed == 1:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*3.125), (yDivSet*3))
            elif cam3SliderSpeed == 3:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*6.25), (yDivSet*3))
            elif cam3SliderSpeed == 5:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*9.375), (yDivSet*3))
            elif cam3SliderSpeed == 7:
                self.root.get_screen('main').ids.cam3SlSpd.sizSl3=((xDivSet*12.5), (yDivSet*3))

        if oldCam4Speed != cam4SliderSpeed:
            oldCam4Speed = cam4SliderSpeed
            if cam4SliderSpeed == 1:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*3.125), (yDivSet*3))
            elif cam4SliderSpeed == 3:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*6.25), (yDivSet*3))
            elif cam4SliderSpeed == 5:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*9.375), (yDivSet*3))
            elif cam4SliderSpeed == 7:
                self.root.get_screen('main').ids.cam4SlSpd.sizSl4=((xDivSet*12.5), (yDivSet*3))

        if oldCam5Speed != cam5SliderSpeed:
            oldCam5Speed = cam5SliderSpeed
            if cam5SliderSpeed == 1:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*3.125), (yDivSet*3))
            elif cam5SliderSpeed == 3:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*6.25), (yDivSet*3))
            elif cam5SliderSpeed == 5:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*9.375), (yDivSet*3))
            elif cam5SliderSpeed == 7:
                self.root.get_screen('main').ids.cam5SlSpd.sizSl5=((xDivSet*12.5), (yDivSet*3))

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

    def whichCamSerial2(self):
        global whichCamSerial
        whichCamSerial = 2
        self.whichCam = "2"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial3(self):
        global whichCamSerial
        whichCamSerial = 3
        self.whichCam = "3"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial4(self):
        global whichCamSerial
        whichCamSerial = 4
        self.whichCam = "4"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(1, 0, 0, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(.13, .13, .13, 1)

    def whichCamSerial5(self):
        global whichCamSerial
        whichCamSerial = 5
        self.whichCam = "5"
        self.root.get_screen('main').ids.buttonWhichCam1.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam2.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam3.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam4.line_color=(.13, .13, .13, 1)
        self.root.get_screen('main').ids.buttonWhichCam5.line_color=(1, 0, 0, 1)
        
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



    def Cam1Go1(self):
        global SetPosToggle
        global cam1Pos1Set
        global cam1AtPos1
        self.root.get_screen('main').ids.btnCam1Go1.line_color= (1, 0, 0, 1)
        print("Test")
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
            self.root.get_screen('main').ids.btnCam1Go1.line_color=(1, 1, 0, 1)
        if cam1Pos2Run and not cam1AtPos2:
            self.root.get_screen('main').ids.btnCam1Go2.line_color=(1, 1, 0, 1)
        if cam1Pos3Run and not cam1AtPos3:
            self.root.get_screen('main').ids.btnCam1Go3.line_color=(1, 1, 0, 1)
        if cam1Pos4Run and not cam1AtPos4:
            self.root.get_screen('main').ids.btnCam1Go4.line_color=(1, 1, 0, 1)
        if cam1Pos5Run and not cam1AtPos5:
            self.root.get_screen('main').ids.btnCam1Go5.line_color=(1, 1, 0, 1)
        if cam1Pos6Run and not cam1AtPos6:
            self.root.get_screen('main').ids.btnCam1Go6.line_color=(1, 1, 0, 1)
        if cam1Pos7Run and not cam1AtPos7:
            self.root.get_screen('main').ids.btnCam1Go7.line_color=(1, 1, 0, 1)
        if cam1Pos8Run and not cam1AtPos8:
            self.root.get_screen('main').ids.btnCam1Go8.line_color=(1, 1, 0, 1)
        if cam1Pos9Run and not cam1AtPos9:
            self.root.get_screen('main').ids.btnCam1Go9.line_color=(1, 1, 0, 1)
        if cam1Pos10Run and not cam1AtPos10:
            self.root.get_screen('main').ids.btnCam1Go10.line_color=(1, 1, 0, 1)

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.get_screen('main').ids.btnCam2Go1.line_color=(1, 1, 0, 1)
        if cam2Pos2Run and not cam2AtPos2:
            self.root.get_screen('main').ids.btnCam2Go2.line_color=(1, 1, 0, 1)
        if cam2Pos3Run and not cam2AtPos3:
            self.root.get_screen('main').ids.btnCam2Go3.line_color=(1, 1, 0, 1)
        if cam2Pos4Run and not cam2AtPos4:
            self.root.get_screen('main').ids.btnCam2Go4.line_color=(1, 1, 0, 1)
        if cam2Pos5Run and not cam2AtPos5:
            self.root.get_screen('main').ids.btnCam2Go5.line_color=(1, 1, 0, 1)
        if cam2Pos6Run and not cam2AtPos6:
            self.root.get_screen('main').ids.btnCam2Go6.line_color=(1, 1, 0, 1)
        if cam2Pos7Run and not cam2AtPos7:
            self.root.get_screen('main').ids.btnCam2Go7.line_color=(1, 1, 0, 1)
        if cam2Pos8Run and not cam2AtPos8:
            self.root.get_screen('main').ids.btnCam2Go8.line_color=(1, 1, 0, 1)
        if cam2Pos9Run and not cam2AtPos9:
            self.root.get_screen('main').ids.btnCam2Go9.line_color=(1, 1, 0, 1)
        if cam2Pos10Run and not cam2AtPos10:
            self.root.get_screen('main').ids.btnCam2Go10.line_color=(1, 1, 0, 1)

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.get_screen('main').ids.btnCam3Go1.line_color=(1, 1, 0, 1)
        if cam3Pos2Run and not cam3AtPos2:
            self.root.get_screen('main').ids.btnCam3Go2.line_color=(1, 1, 0, 1)
        if cam3Pos3Run and not cam3AtPos3:
            self.root.get_screen('main').ids.btnCam3Go3.line_color=(1, 1, 0, 1)
        if cam3Pos4Run and not cam3AtPos4:
            self.root.get_screen('main').ids.btnCam3Go4.line_color=(1, 1, 0, 1)
        if cam3Pos5Run and not cam3AtPos5:
            self.root.get_screen('main').ids.btnCam3Go5.line_color=(1, 1, 0, 1)
        if cam3Pos6Run and not cam3AtPos6:
            self.root.get_screen('main').ids.btnCam3Go6.line_color=(1, 1, 0, 1)
        if cam3Pos7Run and not cam3AtPos7:
            self.root.get_screen('main').ids.btnCam3Go7.line_color=(1, 1, 0, 1)
        if cam3Pos8Run and not cam3AtPos8:
            self.root.get_screen('main').ids.btnCam3Go8.line_color=(1, 1, 0, 1)
        if cam3Pos9Run and not cam3AtPos9:
            self.root.get_screen('main').ids.btnCam3Go9.line_color=(1, 1, 0, 1)
        if cam3Pos10Run and not cam3AtPos10:
            self.root.get_screen('main').ids.btnCam3Go10.line_color=(1, 1, 0, 1)

        
        if cam4Pos1Run and not cam4AtPos1:
            self.root.get_screen('main').ids.btnCam4Go1.line_color=(1, 1, 0, 1)
        if cam4Pos2Run and not cam4AtPos2:
            self.root.get_screen('main').ids.btnCam4Go2.line_color=(1, 1, 0, 1)
        if cam4Pos3Run and not cam4AtPos3:
            self.root.get_screen('main').ids.btnCam4Go3.line_color=(1, 1, 0, 1)
        if cam4Pos4Run and not cam4AtPos4:
            self.root.get_screen('main').ids.btnCam4Go4.line_color=(1, 1, 0, 1)
        if cam4Pos5Run and not cam4AtPos5:
            self.root.get_screen('main').ids.btnCam4Go5.line_color=(1, 1, 0, 1)
        if cam4Pos6Run and not cam4AtPos6:
            self.root.get_screen('main').ids.btnCam4Go6.line_color=(1, 1, 0, 1)
        if cam4Pos7Run and not cam4AtPos7:
            self.root.get_screen('main').ids.btnCam4Go7.line_color=(1, 1, 0, 1)
        if cam4Pos8Run and not cam4AtPos8:
            self.root.get_screen('main').ids.btnCam4Go8.line_color=(1, 1, 0, 1)
        if cam4Pos9Run and not cam4AtPos9:
            self.root.get_screen('main').ids.btnCam4Go9.line_color=(1, 1, 0, 1)
        if cam4Pos10Run and not cam4AtPos10:
            self.root.get_screen('main').ids.btnCam4Go10.line_color=(1, 1, 0, 1)

        
        if cam5Pos1Run and not cam5AtPos1:
            self.root.get_screen('main').ids.btnCam5Go1.line_color=(1, 1, 0, 1)
        if cam5Pos2Run and not cam5AtPos2:
            self.root.get_screen('main').ids.btnCam5Go2.line_color=(1, 1, 0, 1)
        if cam5Pos3Run and not cam5AtPos3:
            self.root.get_screen('main').ids.btnCam5Go3.line_color=(1, 1, 0, 1)
        if cam5Pos4Run and not cam5AtPos4:
            self.root.get_screen('main').ids.btnCam5Go4.line_color=(1, 1, 0, 1)
        if cam5Pos5Run and not cam5AtPos5:
            self.root.get_screen('main').ids.btnCam5Go5.line_color=(1, 1, 0, 1)
        if cam5Pos6Run and not cam5AtPos6:
            self.root.get_screen('main').ids.btnCam5Go6.line_color=(1, 1, 0, 1)
        if cam5Pos7Run and not cam5AtPos7:
            self.root.get_screen('main').ids.btnCam5Go7.line_color=(1, 1, 0, 1)
        if cam5Pos8Run and not cam5AtPos8:
            self.root.get_screen('main').ids.btnCam5Go8.line_color=(1, 1, 0, 1)
        if cam5Pos9Run and not cam5AtPos9:
            self.root.get_screen('main').ids.btnCam5Go9.line_color=(1, 1, 0, 1)
        if cam5Pos10Run and not cam5AtPos10:
            self.root.get_screen('main').ids.btnCam5Go10.line_color=(1, 1, 0, 1)

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
            self.root.get_screen('main').ids.btnCam1Go1.line_color=(.1, .1, .1, 1)
        if cam1Pos2Run and not cam1AtPos2:
            self.root.get_screen('main').ids.btnCam1Go2.line_color=(.1, .1, .1, 1)
        if cam1Pos3Run and not cam1AtPos3:
            self.root.get_screen('main').ids.btnCam1Go3.line_color=(.1, .1, .1, 1)
        if cam1Pos4Run and not cam1AtPos4:
            self.root.get_screen('main').ids.btnCam1Go4.line_color=(.1, .1, .1, 1)
        if cam1Pos5Run and not cam1AtPos5:
            self.root.get_screen('main').ids.btnCam1Go5.line_color=(.1, .1, .1, 1)
        if cam1Pos6Run and not cam1AtPos6:
            self.root.get_screen('main').ids.btnCam1Go6.line_color=(.1, .1, .1, 1)
        if cam1Pos7Run and not cam1AtPos7:
            self.root.get_screen('main').ids.btnCam1Go7.line_color=(.1, .1, .1, 1)
        if cam1Pos8Run and not cam1AtPos8:
            self.root.get_screen('main').ids.btnCam1Go8.line_color=(.1, .1, .1, 1)
        if cam1Pos9Run and not cam1AtPos9:
            self.root.get_screen('main').ids.btnCam1Go9.line_color=(.1, .1, .1, 1)
        if cam1Pos10Run and not cam1AtPos10:
            self.root.get_screen('main').ids.btnCam1Go10.line_color=(.1, .1, .1, 1)

        
        if cam2Pos1Run and not cam2AtPos1:
            self.root.get_screen('main').ids.btnCam2Go1.line_color=(.1, .1, .1, 1)
        if cam2Pos2Run and not cam2AtPos2:
            self.root.get_screen('main').ids.btnCam2Go2.line_color=(.1, .1, .1, 1)
        if cam2Pos3Run and not cam2AtPos3:
            self.root.get_screen('main').ids.btnCam2Go3.line_color=(.1, .1, .1, 1)
        if cam2Pos4Run and not cam2AtPos4:
            self.root.get_screen('main').ids.btnCam2Go4.line_color=(.1, .1, .1, 1)
        if cam2Pos5Run and not cam2AtPos5:
            self.root.get_screen('main').ids.btnCam2Go5.line_color=(.1, .1, .1, 1)
        if cam2Pos6Run and not cam2AtPos6:
            self.root.get_screen('main').ids.btnCam2Go6.line_color=(.1, .1, .1, 1)
        if cam2Pos7Run and not cam2AtPos7:
            self.root.get_screen('main').ids.btnCam2Go7.line_color=(.1, .1, .1, 1)
        if cam2Pos8Run and not cam2AtPos8:
            self.root.get_screen('main').ids.btnCam2Go8.line_color=(.1, .1, .1, 1)
        if cam2Pos9Run and not cam2AtPos9:
            self.root.get_screen('main').ids.btnCam2Go9.line_color=(.1, .1, .1, 1)
        if cam2Pos10Run and not cam2AtPos10:
            self.root.get_screen('main').ids.btnCam2Go10.line_color=(.1, .1, .1, 1)

        
        if cam3Pos1Run and not cam3AtPos1:
            self.root.get_screen('main').ids.btnCam3Go1.line_color=(.1, .1, .1, 1)
        if cam3Pos2Run and not cam3AtPos2:
            self.root.get_screen('main').ids.btnCam3Go2.line_color=(.1, .1, .1, 1)
        if cam3Pos3Run and not cam3AtPos3:
            self.root.get_screen('main').ids.btnCam3Go3.line_color=(.1, .1, .1, 1)
        if cam3Pos4Run and not cam3AtPos4:
            self.root.get_screen('main').ids.btnCam3Go4.line_color=(.1, .1, .1, 1)
        if cam3Pos5Run and not cam3AtPos5:
            self.root.get_screen('main').ids.btnCam3Go5.line_color=(.1, .1, .1, 1)
        if cam3Pos6Run and not cam3AtPos6:
            self.root.get_screen('main').ids.btnCam3Go6.line_color=(.1, .1, .1, 1)
        if cam3Pos7Run and not cam3AtPos7:
            self.root.get_screen('main').ids.btnCam3Go7.line_color=(.1, .1, .1, 1)
        if cam3Pos8Run and not cam3AtPos8:
            self.root.get_screen('main').ids.btnCam3Go8.line_color=(.1, .1, .1, 1)
        if cam3Pos9Run and not cam3AtPos9:
            self.root.get_screen('main').ids.btnCam3Go9.line_color=(.1, .1, .1, 1)
        if cam3Pos10Run and not cam3AtPos10:
            self.root.get_screen('main').ids.btnCam3Go10.line_color=(.1, .1, .1, 1)

        
        if cam4Pos1Run and not cam4AtPos1:
            self.root.get_screen('main').ids.btnCam4Go1.line_color=(.1, .1, .1, 1)
        if cam4Pos2Run and not cam4AtPos2:
            self.root.get_screen('main').ids.btnCam4Go2.line_color=(.1, .1, .1, 1)
        if cam4Pos3Run and not cam4AtPos3:
            self.root.get_screen('main').ids.btnCam4Go3.line_color=(.1, .1, .1, 1)
        if cam4Pos4Run and not cam4AtPos4:
            self.root.get_screen('main').ids.btnCam4Go4.line_color=(.1, .1, .1, 1)
        if cam4Pos5Run and not cam4AtPos5:
            self.root.get_screen('main').ids.btnCam4Go5.line_color=(.1, .1, .1, 1)
        if cam4Pos6Run and not cam4AtPos6:
            self.root.get_screen('main').ids.btnCam4Go6.line_color=(.1, .1, .1, 1)
        if cam4Pos7Run and not cam4AtPos7:
            self.root.get_screen('main').ids.btnCam4Go7.line_color=(.1, .1, .1, 1)
        if cam4Pos8Run and not cam4AtPos8:
            self.root.get_screen('main').ids.btnCam4Go8.line_color=(.1, .1, .1, 1)
        if cam4Pos9Run and not cam4AtPos9:
            self.root.get_screen('main').ids.btnCam4Go9.line_color=(.1, .1, .1, 1)
        if cam4Pos10Run and not cam4AtPos10:
            self.root.get_screen('main').ids.btnCam4Go10.line_color=(.1, .1, .1, 1)

        
        if cam5Pos1Run and not cam5AtPos1:
            self.root.get_screen('main').ids.btnCam5Go1.line_color=(.1, .1, .1, 1)
        if cam5Pos2Run and not cam5AtPos2:
            self.root.get_screen('main').ids.btnCam5Go2.line_color=(.1, .1, .1, 1)
        if cam5Pos3Run and not cam5AtPos3:
            self.root.get_screen('main').ids.btnCam5Go3.line_color=(.1, .1, .1, 1)
        if cam5Pos4Run and not cam5AtPos4:
            self.root.get_screen('main').ids.btnCam5Go4.line_color=(.1, .1, .1, 1)
        if cam5Pos5Run and not cam5AtPos5:
            self.root.get_screen('main').ids.btnCam5Go5.line_color=(.1, .1, .1, 1)
        if cam5Pos6Run and not cam5AtPos6:
            self.root.get_screen('main').ids.btnCam5Go6.line_color=(.1, .1, .1, 1)
        if cam5Pos7Run and not cam5AtPos7:
            self.root.get_screen('main').ids.btnCam5Go7.line_color=(.1, .1, .1, 1)
        if cam5Pos8Run and not cam5AtPos8:
            self.root.get_screen('main').ids.btnCam5Go8.line_color=(.1, .1, .1, 1)
        if cam5Pos9Run and not cam5AtPos9:
            self.root.get_screen('main').ids.btnCam5Go9.line_color=(.1, .1, .1, 1)
        if cam5Pos10Run and not cam5AtPos10:
            self.root.get_screen('main').ids.btnCam5Go10.line_color=(.1, .1, .1, 1)

    
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


if __name__ == '__main__':
    PTSApp().run()