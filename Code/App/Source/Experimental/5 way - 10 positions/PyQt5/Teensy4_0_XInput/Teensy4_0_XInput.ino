/*
    Project     Arduino XInput Library
    @author     David Madison
    @link       github.com/dmadison/ArduinoXInput
    @license    MIT - Copyright (c) 2019 David Madison

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.

    Example:      GamepadPins
    Description:  Uses all of the available pin inputs to build a 'complete'
                  Xbox gamepad, with both analog joysticks, both triggers,
                  and all of the main buttons.

 *                * Joysticks should be your typical 10k dual potentiometers.
                    To prevent random values caused by floating inputs,
                    joysticks are disabled by default.
 *                * Triggers can be either analog (pots) or digital (buttons).
                    Set the 'TriggerButtons' variable to change between the two.
 *                * Buttons use the internal pull-ups and should be connected
                    directly to ground.

                  These pins are designed around the Leonardo's layout. You
                  may need to change the pin numbers if you're using a
                  different board type

*/

#include <XInput.h>

// Setup
const boolean UseLeftJoystick   = true;  // set to true to enable left joystick
const boolean InvertLeftYAxis   = true;  // set to true to use inverted left joy Y

const boolean UseRightJoystick  = true;  // set to true to enable right joystick
const boolean InvertRightYAxis  = true;  // set to true to use inverted right joy Y

const boolean UseTriggerButtons = true;   // set to false if using analog triggers

const int ADC_Max = 1023;  // 10 bit

// Joystick Pins
const int Pin_LeftJoyX  = 23;
const int Pin_LeftJoyY  = 22;
const int Pin_RightJoyX = 20;
const int Pin_RightJoyY = 21;

// Button Pins
const int Pin_ButtonA = 2;


const int deadRange = 100;


int XdeadRangeLow = (512 - deadRange);
int XdeadRangeHigh = (512 + deadRange);
int YdeadRangeLow = (512 - deadRange);
int YdeadRangeHigh = (512 + deadRange);
int ZdeadRangeLow = (512 - deadRange);
int ZdeadRangeHigh = (512 + deadRange);
int WdeadRangeLow = (512 - deadRange);
int WdeadRangeHigh = (512 + deadRange);

int X_min = 2;
int X_max = 1023;
int Y_min = 2;
int Y_max = 1023;
int Z_min = 2;
int Z_max = 1023;
int W_min = 2;
int W_max = 1023;

short XShort = 0;
short YShort = 0;
short ZShort = 0;
short WShort = 0;



void setup() {
  // Set buttons as inputs, using internal pull-up resistors
  pinMode(Pin_ButtonA, INPUT_PULLUP);

  XInput.setJoystickRange(0, ADC_Max);  // Set joystick range to the ADC
  XInput.setAutoSend(false);  // Wait for all controls before sending

  XInput.begin();
}

void loop() {
  // Read pin values and store in variables
  // (Note the "!" to invert the state, because LOW = pressed)
  boolean buttonA = !digitalRead(Pin_ButtonA);

  // Set XInput buttons
  XInput.setButton(BUTTON_A, buttonA);

  // Set left joystick
  if (UseLeftJoystick == true) {
    int leftJoyX = analogRead(Pin_LeftJoyX);
    int leftJoyY = analogRead(Pin_LeftJoyY);

    if (leftJoyX < XdeadRangeLow) {
      XShort = map(leftJoyX, X_min, XdeadRangeLow, 0, 512);
      //Serial.println(XShort);
      if (XShort < 0) {
        XShort = 0;
      }
    } else if (leftJoyX > XdeadRangeHigh) {
      XShort = map(leftJoyX, XdeadRangeHigh, X_max, 512, 1023);
      //Serial.println(XShort);
      if (XShort > 1023) {
        XShort = 1023;
      }
    } else {
      XShort = 512;
    }

    if (leftJoyY < YdeadRangeLow) {
      YShort = map(leftJoyY, Y_min, YdeadRangeLow, 0, 512);
      //Serial.println(YShort);
      if (YShort < 0) {
        YShort = 0;
      }
    } else if (leftJoyY > YdeadRangeHigh) {
      YShort = map(leftJoyY, YdeadRangeHigh, Y_max, 512, 1023);
      //Serial.println(YShort);
      if (YShort > 1023) {
        YShort = 1023;
      }
    } else {
      YShort = 512;
    }

    boolean invert = !InvertLeftYAxis;

    XInput.setJoystickX(JOY_LEFT, XShort);
    XInput.setJoystickY(JOY_LEFT, YShort, invert);
  }

  // Set right joystick
  if (UseRightJoystick == true) {
    int rightJoyX = analogRead(Pin_RightJoyX);
    int rightJoyY = analogRead(Pin_RightJoyY);

    if (rightJoyX < ZdeadRangeLow) {
      ZShort = map(rightJoyX, Z_min, ZdeadRangeLow, 0, 512);
      //Serial.println(ZShort);
      if (ZShort < 0) {
        ZShort = 0;
      }
    } else if (rightJoyX > ZdeadRangeHigh) {
      ZShort = map(rightJoyX, ZdeadRangeHigh, Z_max, 512, 1023);
      //Serial.println(ZShort);
      if (ZShort > 1023) {
        ZShort = 1023;
      }
    } else {
      ZShort = 512;
    }

    if (rightJoyY < WdeadRangeLow) {
      WShort = map(rightJoyY, W_min, WdeadRangeLow, 0, 512);
      //Serial.println(WShort);
      if (WShort < 0) {
        WShort = 0;
      }
    } else if (rightJoyY > WdeadRangeHigh) {
      WShort = map(rightJoyY, WdeadRangeHigh, W_max, 512, 1023);
      //Serial.println(WShort);
      if (WShort > 1023) {
        WShort = 1023;
      }
    } else {
      WShort = 512;
    }

    boolean invert = !InvertRightYAxis;

    XInput.setJoystickX(JOY_RIGHT, ZShort);
    XInput.setJoystickY(JOY_RIGHT, WShort, invert);
  }

  // Send control data to the computer
  XInput.send();
}
