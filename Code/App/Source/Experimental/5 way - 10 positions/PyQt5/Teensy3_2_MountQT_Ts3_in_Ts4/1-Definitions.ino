#include "Definitions.h"
//#include <Iibrary.h>  //A library I created for Arduino that contains some simple functions I commonly use. Library available at: https://github.com/isaac879/Iibrary
#include "TeensyStep.h"
#include <EEPROM.h>  //To be able to save values when powered off
#include <elapsedMillis.h>

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

//Global scope

Stepper stepper_pan(PIN_STEP_PAN, PIN_DIRECTION_PAN);
Stepper stepper_tilt(PIN_STEP_TILT, PIN_DIRECTION_TILT);
Stepper stepper_slider(PIN_STEP_SLIDER, PIN_DIRECTION_SLIDER);
Stepper stepper_zoom(PIN_STEP_ZOOM, PIN_DIRECTION_ZOOM);

StepControl multi_stepper;

StepControl step_stepperP;
StepControl step_stepperT;
StepControl step_stepperS;
StepControl step_stepperZ;

RotateControl rotate_stepperP;
RotateControl rotate_stepperT;
RotateControl rotate_stepperS;
RotateControl rotate_stepperZ;

KeyframeElement keyframe_array[10];

elapsedMillis timeElapsed;

IntervalTimer zoomLimitTimer;
IntervalTimer aliveTimer;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void initPanTilt(void) {
  getEEPROMVariables();

  //Serial.begin(BAUD_RATE);
  Serial1.begin(BAUD_RATE);
  Serial3.begin(BAUD_RATE);

  pinMode(13, OUTPUT);    // LED
  digitalWrite(13, LOW);  // LED OFF

  pinMode(PIN_SW1, INPUT_PULLUP);  // Dip Switch 1.                   HIGH (switch off) = Up-side Down
  pinMode(PIN_SW2, INPUT_PULLUP);  // Dip Switch 2.                   HIGH (switch off) = Slider Reverse
  pinMode(PIN_SW3, INPUT_PULLUP);  // Dip Switch 3.                   HIGH (switch off) = Slider Used   -  pin 10 to gnd if no slider used
  pinMode(PIN_SW4, INPUT_PULLUP);  // Dip Switch 4.                   HIGH (switch off) = 

  zoomLimitTimer.begin(zoomLimitCheck, 25000);
  zoomLimitTimer.priority(255);

  aliveTimer.begin(sendAlive, 10000000);
  aliveTimer.priority(255);

  stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
  stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
  stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
  stepper_zoom.setMaxSpeed(zoom_set_speed);
  stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
  stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
  stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
  stepper_zoom.setAcceleration(zoom_set_speed * 5);

  delay(200);

  upsideDown = digitalRead(PIN_SW1);
  slideReverse = digitalRead(PIN_SW2);
  withSlider = digitalRead(PIN_SW3);

  Serial1.println("#a");
  Serial1.println("#a");
  Serial1.println("#%");
  Serial1.println("#%");  // clear remote LEDS

if (pantilt_set_speed == pantilt_speed1) {
    Serial1.println("^@1");
    Serial1.println("^@1");
  } else if (pantilt_set_speed == pantilt_speed2) {
    Serial1.println("^@3");
    Serial1.println("^@3");
  } else if (pantilt_set_speed == pantilt_speed3) {
    Serial1.println("^@5");
    Serial1.println("^@5");
  } else if (pantilt_set_speed == pantilt_speed4) {
    Serial1.println("^@7");
    Serial1.println("^@7");
  }

  if (withSlider) {
    if (slider_set_speed == slider_speed1) {
      Serial1.println("^=1");
      Serial1.println("^=1");
    } else if (slider_set_speed == slider_speed2) {
      Serial1.println("^=3");
      Serial1.println("^=3");
    } else if (slider_set_speed == slider_speed3) {
      Serial1.println("^=5");
      Serial1.println("^=5");
    } else if (slider_set_speed == slider_speed4) {
      Serial1.println("^=7");
      Serial1.println("^=7");
    }
  }

  sendCamSettings();

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


void Serial1Flush(void) {
  while (Serial1.available() > 0) {
    c = Serial1.read();
  }
}

void Serial3Flush(void) {
  while (Serial3.available() > 0) {
    c = Serial3.read();
  }
}

void sendCamSettings() {

  Serial1.println(String("#d") + pantilt_speed1);
  Serial1.println(String("#f") + pantilt_speed2);
  Serial1.println(String("#g") + pantilt_speed3);
  Serial1.println(String("#h") + pantilt_speed4);

  if (withSlider) {
    Serial1.println(String("#j") + slider_speed1);
    Serial1.println(String("#k") + slider_speed2);
    Serial1.println(String("#l") + slider_speed3);
    Serial1.println(String("#;") + slider_speed4);
  }

  Serial1.println(String("#q") + pantilt_accel);
  if (withSlider) {
    Serial1.println(String("#Q") + slider_accel);
  }

  if (withSlider) {
    Serial1.println(String("#t") + sliderStepsToMillimetres(slideLimit));
  }
  Serial1.println(String("#w") + zoomLimit);
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
      rotate_stepperZ.stopAsync();
      isManualMove = false;
    }
  }
}

void zoomLimitCheck() {
  if (findingHome == false){
    if ((stepper_zoom.getPosition() > zoomLimit) && (zoomRunning == true) && (zoomedIn == false)) {
      rotate_stepperZ.emergencyStop();
      zoomRunning = false;
      zoomedIn = true;
      zoomedOut = false;
      stepper_zoom.setTargetRel(-20);
      step_stepperZ.move(stepper_zoom);
      //Serial1.println("Zoomed Fully IN"); 
    } 
    else if ((stepper_zoom.getPosition() < 0) && (zoomRunning == true) && (zoomedOut == false)) {
      rotate_stepperZ.emergencyStop();
      zoomRunning = false;
      zoomedIn = false;
      zoomedOut = true;
      stepper_zoom.setTargetRel(20);
      step_stepperZ.move(stepper_zoom);
      //Serial1.println("Zoomed Fully OUT"); 
    }


    if ((stepper_zoom.getPosition() > 20) && (zoomedOut == true)) {
      zoomedOut = false;
      //Serial1.println("Zoomed OUT reset"); 
    }
    if ((stepper_zoom.getPosition() < (zoomLimit - 20)) && (zoomedIn == true)) {
      zoomedIn = false;
      //Serial1.println("Zoomed IN reset");
    }

    
    if (slideReverse) {
      if ((stepper_slider.getPosition() < (slideLimit * -1)) && (sliderRunning == true) && (sliderAtLimit == false)) {
        // IS reversed - position over slide limit - motor running - AtLimit not set
        rotate_stepperS.emergencyStop();
        Serial1.print("Slider @ Limit - ");
        Serial1.println(stepper_slider.getPosition());
        sliderRunning = false;
        sliderAtLimit = true;
        sliderAtZero = false;
        stepper_slider.setTargetRel(20);
        step_stepperS.move(stepper_slider);
        //Serial1.println("Slider @ Limit"); 
      }
      else if ((stepper_slider.getPosition() > 0) && (sliderRunning == true) && (sliderAtZero == false)) {
        // IS reversed - position less than zero - motor running - AtZero not set
        rotate_stepperS.emergencyStop();
        Serial1.print("Slider @ Zero - ");
        Serial1.println(stepper_slider.getPosition());
        sliderRunning = false;
        sliderAtLimit = false;
        sliderAtZero = true;
        stepper_slider.setTargetRel(-20);
        step_stepperS.move(stepper_slider);
        //Serial1.println("Slider @ Zero"); 
      }

      if ((stepper_slider.getPosition() < ((slideLimit * -1) * 0.03)) && (sliderAtZero == true)) {
        sliderAtZero = false;
        //Serial1.println("Slider Zero reset"); 
      }
      if ((stepper_slider.getPosition() > ((slideLimit * -1) * 0.97)) && (sliderAtLimit == true)) {
        sliderAtLimit = false;
        //Serial1.println("Slider Limit reset");
      }
    }
    else {
      if ((stepper_slider.getPosition() > slideLimit) && (sliderRunning == true) && (sliderAtLimit == false)) {
        // Not reversed - position over slide limit - motor running - AtLimit not set
        rotate_stepperS.emergencyStop();
        Serial1.print("Slider @ Limit - ");
        Serial1.println(stepper_slider.getPosition());
        sliderRunning = false;
        sliderAtLimit = true;
        sliderAtZero = false;
        stepper_slider.setTargetRel(-20);
        step_stepperS.move(stepper_slider);
        //Serial1.println("Slider @ Limit"); 
      } 
      else if ((stepper_slider.getPosition() < 0) && (sliderRunning == true) && (sliderAtZero == false)) {
        // Not reversed - position less than zero - motor running - AtZero not set
        rotate_stepperS.emergencyStop();
        Serial1.print("Slider @ Zero - ");
        Serial1.println(stepper_slider.getPosition());
        sliderRunning = false;
        sliderAtLimit = false;
        sliderAtZero = true;
        stepper_slider.setTargetRel(20);
        step_stepperS.move(stepper_slider);
        //Serial1.println("Slider @ Zero"); 
      }

      if ((stepper_slider.getPosition() > (slideLimit * 0.03)) && (sliderAtZero == true)) {
        sliderAtZero = false;
        //Serial1.println("Slider Zero reset"); 
      }
      if ((stepper_slider.getPosition() < (slideLimit * 0.97)) && (sliderAtLimit == true)) {
        sliderAtLimit = false;
        //Serial1.println("Slider Limit reset");
      }
    }
  }
}

void sendAlive() {
  Serial1.println("#+");
}