void RefreshLEDs() {
    if (doLEDrefresh) {
    Serial1.println("?W");
    doLEDrefresh = false;
    doLEDrefresh2 = true;
    previousMillisLED = millis();
  }
  if (doLEDrefresh2) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {
      Serial2.println("?W");
      doLEDrefresh2 = false;
      doLEDrefresh3 = true;
      previousMillisLED = currentMillisLED;
    }
  }
  if (doLEDrefresh3) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {
      Serial3.println("?W");
      doLEDrefresh3 = false;
      doLEDrefresh4 = true;
      previousMillisLED = currentMillisLED;
    }
  }
  if (doLEDrefresh4) {
    unsigned long currentMillisLED = millis();
    if (currentMillisLED - previousMillisLED > LEDInterval) {

      Serial.print("=1");
      Serial.println(cam1SlSpeed);
      Serial.print("=2");
      Serial.println(cam3SlSpeed);
      Serial.print("=3");
      Serial.println(cam3SlSpeed);

      doLEDrefresh4 = false;
    }
  }

  if (resetLEDs) {                                       //  Start "reset LEDs"
    resetLEDs = false;

    Serial1.println("#0");

    Serial.println("~100");
    Serial.println("~200");
    Serial.println("~300");

    doLEDrefresh = true;
  }
}

void sendSliderPanTiltStepSpeed(int command, short * arr, int whichCamJoy) {
  byte data[7];                               // Data array to send

  data[0] = command;
  data[1] = (arr[0] >> 8);                    // Gets the most significant byte
  data[2] = (arr[0] & 0xFF);                  // Gets the second most significant byte
  data[3] = (arr[1] >> 8);
  data[4] = (arr[1] & 0xFF);
  data[5] = (arr[2] >> 8);
  data[6] = (arr[2] & 0xFF);                  // Gets the least significant byte

  delay(20);

  if (whichCamJoy == 1) {
    Serial1.write(data, sizeof(data));        // Send the command and the 6 bytes of data
    Serial1.print("\n");
  }
  else if (whichCamJoy == 2) {
    Serial2.write(data, sizeof(data));        // Send the command and the 6 bytes of data
    Serial2.print("\n");
  }
  else if (whichCamJoy == 3) {
    Serial3.write(data, sizeof(data));        // Send the command and the 6 bytes of data
    Serial3.print("\n");
  }
}
