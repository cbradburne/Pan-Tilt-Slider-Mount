// STM32F1xx
// VDTx

#include "Adafruit_GFX.h"
#include "Adafruit_HT1632.h"

#include "Definitions.h"

void setup() {
  initPTS();
}

void loop() {

  doShuttle();

  doJog();

  doJoystick();

  readSerial1();
  readSerial3();
  readSerial4();
  readSerial();

  unsigned long currentMillisKeyboard = millis();
  if (currentMillisKeyboard - previousMillisKeyboard > keyboardInterval) {
    previousMillisKeyboard = currentMillisKeyboard;
    doKeyboard();
  }

  unsigned long currentMillisTick = millis();                                   //  Delay to make "go to" LEDs blink
  if (currentMillisTick - previousMillisTick > tickInterval) {
    previousMillisTick = currentMillisTick;
    runTick1 = !runTick1;
    runTick2 = !runTick2;
    runTick3 = !runTick3;
    displayUpdate = true;
  }

  doDisplay();

  if (displayCommand != 000) {                          //  Start display timer
    if (startDisplayRefresh) {
      previousMillisDisplay = millis();
      startDisplayRefresh = false;
    }
    unsigned long currentMillisDisplay = millis();
    if (currentMillisDisplay - previousMillisDisplay > displayInterval) {
      previousMillisDisplay = currentMillisDisplay;
      displayCommand = 000;
      doDisplay();
      startDisplayRefresh = true;
    }
  }

  if (setClear) {                                       //  Start "clear pos" button timer
    if (startClear) {
      previousMillisClear = millis();
      startClear = false;
    }
    unsigned long currentMillisClear = millis();
    if (currentMillisClear - previousMillisClear > clearInterval) {
      previousMillisClear = currentMillisClear;
      setClear = false;
      startClear = true;
      if (whichCam == 1) {
        Serial1.println("?Y");
      }
      else if (whichCam == 2) {
        Serial3.println("?Y");
      }
      else if (whichCam == 3) {
        Serial4.println("?Y");
      }
    }
  }

  if (doLEDrefresh) {
    Serial1.println("?W");
    doLEDrefresh = false;
    doLEDrefresh2 = true;
    previousMillisLED = millis();
  }
  if (doLEDrefresh2) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {
      Serial3.println("?W");
      doLEDrefresh2 = false;
      doLEDrefresh3 = true;
      previousMillisLED = currentMillisLED;
    }
  }
  if (doLEDrefresh3) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {
      Serial4.println("?W");
      doLEDrefresh3 = false;
      doLEDrefresh4 = true;
      previousMillisLED = currentMillisLED;
    }
  }
  if (doLEDrefresh4) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {

      Serial.print("=1");
      Serial.println(s1Speed);
      Serial.print("=2");
      Serial.println(s2Speed);
      Serial.print("=3");
      Serial.println(s3Speed);

      doLEDrefresh4 = false;
    }
  }

  if (resetLEDs) {                                       //  Start "reset LEDs" button timer
    if (startLEDs) {
      previousMillisLEDs = millis();
      startLEDs = false;
    }
    unsigned long currentMillisLEDs = millis();
    if (currentMillisLEDs - previousMillisLEDs > LEDsInterval) {
      previousMillisLEDs = currentMillisLEDs;
      resetLEDs = false;
      startLEDs = true;
      
      Serial1.println("#0");
      Serial3.println("#0");
      Serial4.println("#0");
      
      Serial.println("~100");
      Serial.println("~200");
      Serial.println("~300");

      cam1pos1run = false;
      cam1pos1set = false;
      cam1atPos1 = false;
      cam1pos2run = false;
      cam1pos2set = false;
      cam1atPos2 = false;
      cam1pos3run = false;
      cam1pos3set = false;
      cam1atPos3 = false;
      cam1pos4run = false;
      cam1pos4set = false;
      cam1atPos4 = false;
      cam1pos5run = false;
      cam1pos5set = false;
      cam1atPos5 = false;
      cam1pos6run = false;
      cam1pos6set = false;
      cam1atPos6 = false;

      cam2pos1run = false;
      cam2pos1set = false;
      cam2atPos1 = false;
      cam2pos2run = false;
      cam2pos2set = false;
      cam2atPos2 = false;
      cam2pos3run = false;
      cam2pos3set = false;
      cam2atPos3 = false;
      cam2pos4run = false;
      cam2pos4set = false;
      cam2atPos4 = false;
      cam2pos5run = false;
      cam2pos5set = false;
      cam2atPos5 = false;
      cam2pos6run = false;
      cam2pos6set = false;
      cam2atPos6 = false;

      cam3pos1run = false;
      cam3pos1set = false;
      cam3atPos1 = false;
      cam3pos2run = false;
      cam3pos2set = false;
      cam3atPos2 = false;
      cam3pos3run = false;
      cam3pos3set = false;
      cam3atPos3 = false;
      cam3pos4run = false;
      cam3pos4set = false;
      cam3atPos4 = false;
      cam3pos5run = false;
      cam3pos5set = false;
      cam3atPos5 = false;
      cam3pos6run = false;
      cam3pos6set = false;
      cam3atPos6 = false;
      
      cam1PTSpeed = 0;
      cam2PTSpeed = 0;
      cam3PTSpeed = 0;

      s1Speed = 0;
      s2Speed = 0;
      s3Speed = 0;
      
      doLEDrefresh = true;
    }
  }
}


void setLEDs() {                                        //  Send "Clock Pulse" for LEDs
  delay(10);
  digitalWrite(LEDCP, HIGH);
  delay(10);
  digitalWrite(LEDCP, LOW);
}
