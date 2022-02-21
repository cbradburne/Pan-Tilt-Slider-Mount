#include "Definitions.h"
#include <Iibrary.h> //A library I created for Arduino that contains some simple functions I commonly use. Library available at: https://github.com/isaac879/Iibrary
#include "TeensyStep.h"
#include <EEPROM.h> //To be able to save values when powered off

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

//Global scope

Stepper stepper_pan(PIN_STEP_PAN, PIN_DIRECTION_PAN);
Stepper stepper_tilt(PIN_STEP_TILT, PIN_DIRECTION_TILT);
Stepper stepper_slider(PIN_STEP_SLIDER, PIN_DIRECTION_SLIDER);

StepControl multi_stepper;

StepControl step_stepperP;
StepControl step_stepperT;
StepControl step_stepperS;

RotateControl rotate_stepperP;
RotateControl rotate_stepperT;
RotateControl rotate_stepperS;

KeyframeElement keyframe_array[6];


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void initPanTilt(void) {
  Serial.begin(BAUD_RATE);
  Serial1.begin(BAUD_RATE);
  Serial2.begin(BAUD_RATE);
  Serial3.begin(BAUD_RATE);

  pinMode(13, OUTPUT);                      // LED
  digitalWrite(13, HIGH);                   // LED ON

  pinMode(PIN_SW1, INPUT_PULLUP);           // Dip Switch 1
  pinMode(PIN_SW2, INPUT_PULLUP);           // Dip Switch 2

  setEEPROMVariables();

  stepper_pan.setMaxSpeed(panDegreesToSteps(pan_set_speed));
  stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));
  stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
  stepper_pan.setAcceleration(pan_accel);
  stepper_tilt.setAcceleration(tilt_accel);
  stepper_slider.setAcceleration(slider_accel);

  delay(200);

  Serial1.println("#a");
  Serial2.println("#a");
  Serial3.println("#a");

  Serial1.println("#%");                   // clear remote LEDS
  Serial2.println("#%");
  Serial3.println("#%");

  if (pan_set_speed >= 20) {
    Serial1.println("^@7");
    Serial2.println("^@7");
    Serial3.println("^@7");
  }
  else if (pan_set_speed >= 10 && pan_set_speed < 20) {
    Serial1.println("^@5");
    Serial2.println("^@5");
    Serial3.println("^@5");
  }
  else if (pan_set_speed >= 5 && pan_set_speed < 10) {
    Serial1.println("^@3");
    Serial2.println("^@3");
    Serial3.println("^@3");
  }
  else if (pan_set_speed < 5) {
    Serial1.println("^@1");
    Serial2.println("^@1");
    Serial3.println("^@1");
  }

  LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
  Serial1.print("^=");
  Serial1.println(LEDsliderSpeed);
  Serial2.print("^=");
  Serial2.println(LEDsliderSpeed);
  Serial3.print("^=");
  Serial3.println(LEDsliderSpeed);

  Serial.println(String("Pan speed         : ") + pan_set_speed + String("°/s"));
  Serial.println(String("Tilt speed        : ") + tilt_set_speed + String("°/s"));
  Serial.println(String("Slider speed      : ") + slider_set_speed + String("mm/s"));
  Serial.println("-");

  //Serial1.println(String("Pan speed         : ") + pan_set_speed + String("°/s"));
  //Serial1.println(String("Tilt speed        : ") + tilt_set_speed + String("°/s"));
  //Serial1.println(String("Slider speed      : ") + slider_set_speed + String("mm/s"));

  Serial1.println("Camera Active");
  Serial1.println("-");
  Serial1.println("#$");

}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


float panDegreesToSteps(float angle) {
  return pan_steps_per_degree * angle;
}

float tiltDegreesToSteps(float angle) {
  return tilt_steps_per_degree * angle;
}

long sliderMillimetresToSteps(float mm) {
  return round(mm * slider_steps_per_millimetre);
}

float sliderStepsToMillimetres(long steps) {
  return (float)steps / slider_steps_per_millimetre;
}

float panStepsToDegrees(long steps) {
  return steps / pan_steps_per_degree;
}

float panStepsToDegrees(float steps) {
  return steps / pan_steps_per_degree;
}

float tiltStepsToDegrees(long steps) {
  return steps / tilt_steps_per_degree;
}

float tiltStepsToDegrees(float steps) {
  return steps / tilt_steps_per_degree;
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void SerialFlush(void) {
  while (Serial.available() > 0) {
    c = Serial.read();
  }
}

void Serial1Flush(void) {
  while (Serial1.available() > 0) {
    c = Serial1.read();
  }
}

void Serial2Flush(void) {
  while (Serial2.available() > 0) {
    c = Serial2.read();
  }
}

void Serial3Flush(void) {
  while (Serial3.available() > 0) {
    c = Serial3.read();
  }
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void mainLoop(void) {
  SerialData();

  if (isManualMove) {
    unsigned long currentMillisMoveCheck = millis();
    if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval) {
      previousMillisMoveCheck = currentMillisMoveCheck;
      rotate_stepperS.stopAsync();
      rotate_stepperP.stopAsync();
      rotate_stepperT.stopAsync();
    }
  }
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/
