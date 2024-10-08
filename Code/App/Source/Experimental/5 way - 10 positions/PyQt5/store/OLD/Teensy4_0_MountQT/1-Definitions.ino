#include "Definitions.h"
#include <Iibrary.h>  //A library I created for Arduino that contains some simple functions I commonly use. Library available at: https://github.com/isaac879/Iibrary
#include "teensystep4.h"
#include <EEPROM.h>  //To be able to save values when powered off
#include <elapsedMillis.h>

using namespace TS4;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

//Global scope

Stepper stepper_pan(PIN_STEP_PAN, PIN_DIRECTION_PAN);
Stepper stepper_tilt(PIN_STEP_TILT, PIN_DIRECTION_TILT);
Stepper stepper_slider(PIN_STEP_SLIDER, PIN_DIRECTION_SLIDER);

KeyframeElement keyframe_array[10];

elapsedMillis timeElapsed;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void initPanTilt(void) {
  Serial1.begin(BAUD_RATE);
  Serial2.begin(BAUD_RATE);

  TS4::begin();

  pinMode(13, OUTPUT);              // LED
  digitalWrite(13, LOW);            // LED OFF

  pinMode(PIN_SW1, INPUT_PULLUP);   // Dip Switch 1
  pinMode(PIN_SW2, INPUT_PULLUP);   // Dip Switch 2
  pinMode(PIN_SW3, INPUT_PULLUP);   // pin 10 to gnd if no slider used

  setEEPROMVariables();

  stepper_pan.setMaxSpeed(panDegreesToSteps(pan_set_speed));
  stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));
  stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
  stepper_pan.setAcceleration(pan_accel);
  stepper_tilt.setAcceleration(tilt_accel);
  stepper_slider.setAcceleration(slider_accel);

  delay(200);

  Serial1.println("#a");
  Serial1.println("#a");
  Serial1.println("#%");
  Serial1.println("#%");            // clear remote LEDS

  if (pan_set_speed == 20) {
    Serial1.println("^@7");
    Serial1.println("^@7");
  } else if (pan_set_speed == 10) {
    Serial1.println("^@5");
    Serial1.println("^@5");
  } else if (pan_set_speed == 5) {
    Serial1.println("^@3");
    Serial1.println("^@3");
  } else if (pan_set_speed == 1) {
    Serial1.println("^@1");
    Serial1.println("^@1");
  }

  if (slider_set_speed == 160) { 
    Serial1.println("^=7"); 
    Serial1.println("^=7"); 
    }
  else if (slider_set_speed == 120) { 
    Serial1.println("^=5"); 
    Serial1.println("^=5"); 
    }
  else if (slider_set_speed == 60) { 
    Serial1.println("^=3"); 
    Serial1.println("^=3"); 
    }
  else if (slider_set_speed == 20) { 
    Serial1.println("^=1"); 
    Serial1.println("^=1"); 
    }

  Serial1.println("Camera Active");
  Serial1.println("-");
  Serial1.println("#$");

  upsideDown = digitalRead(PIN_SW1);
  slideReverse = digitalRead(PIN_SW2);
  withSlider = digitalRead(PIN_SW3);
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

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void mainLoop(void) {
  SerialData();

  if (isManualMove) {
    unsigned long currentMillisMoveCheck = millis();
    if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval) {
      previousMillisMoveCheck = currentMillisMoveCheck;
      if (stepper_pan.isMoving) {
        panRunning = false;
        stepper_pan.overrideSpeed(0);
        stepper_pan.stopAsync();
        delay(10);
      }

      if (stepper_tilt.isMoving) {
        tiltRunning = false;
        stepper_tilt.overrideSpeed(0);
        stepper_tilt.stopAsync();
        delay(10);
      }

      if (stepper_slider.isMoving) {
        sliderRunning = false;
        stepper_slider.overrideSpeed(0);
        stepper_slider.stopAsync();
        delay(10);
      }

      isManualMove = false;
    }
  }
}