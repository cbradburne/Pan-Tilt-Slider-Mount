//  Receive Serial data, and process


void SerialData(void) {
  char instruction;
  if (Serial.available() > 0) {
    instruction = Serial.read();
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial.available() < 6) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial1Flush();                                     //  Clear the Serial1 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;

      short sliderStepSpeed = (Serial.read() << 8) + Serial.read();
      short panStepSpeed = (Serial.read() << 8) + Serial.read();
      short tiltStepSpeed = (Serial.read() << 8) + Serial.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -panMaxFactor, panMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -tiltMaxFactor, tiltMaxFactor);

      if (speedFactorS == 0) {
        rotate_stepperS.stopAsync();
      }
      else {
        rotate_stepperS.rotateAsync(stepper_slider);
        rotate_stepperS.overrideAcceleration(sliderAccelJoy);         // to make accel less when using joystick
        rotate_stepperS.overrideSpeed(speedFactorS);
      }

      if (speedFactorP == 0) {
        rotate_stepperP.stopAsync();
      }
      else {
        rotate_stepperP.rotateAsync(stepper_pan);
        rotate_stepperP.overrideAcceleration(panAccelJoy);            // to make accel less when using joystick
        rotate_stepperP.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0) {
        rotate_stepperT.stopAsync();
      }
      else {
        rotate_stepperT.rotateAsync(stepper_tilt);
        rotate_stepperT.overrideAcceleration(tiltAccelJoy);           // to make accel less when using joystick
        rotate_stepperT.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      }
      else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }
    }
    else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                                 //wait to make sure all data in the Serial1 message has arived
      instruction = Serial.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial.read();
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial.available()) {                              //set elemetns of stringText to the Serial1 values sent
          char digit = Serial.read();                             //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        SerialFlush();                                            //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
      }
      else {
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial.available()) {                              //set elemetns of stringText to the Serial1 values sent
          char digit = Serial.read();                             //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        SerialFlush();                                            //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);              //converts stringText to a float
        if (instruction == '+') {                                 //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                             //wait to make sure all data in the Serial1 message has arived
          SerialFlush();                                          //Clear any excess data in the Serial1 buffer
          return;
        }
      }
    }
    else {
      return;
    }
  }
  else if (Serial2.available() > 0) {
    instruction = Serial2.read();
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial2.available() < 6) {                       //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial2Flush();                                     //  Clear the Serial2 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;

      short sliderStepSpeed = (Serial2.read() << 8) + Serial2.read();
      short panStepSpeed = (Serial2.read() << 8) + Serial2.read();
      short tiltStepSpeed = (Serial2.read() << 8) + Serial2.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -panMaxFactor, panMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -tiltMaxFactor, tiltMaxFactor);

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      else {
        rotate_stepperS.rotateAsync(stepper_slider);
        rotate_stepperS.overrideAcceleration(sliderAccelJoy);         // to make accel less when using joystick
        rotate_stepperS.overrideSpeed(speedFactorS);
      }

      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      else {
        rotate_stepperP.rotateAsync(stepper_pan);
        rotate_stepperP.overrideAcceleration(panAccelJoy);            // to make accel less when using joystick
        rotate_stepperP.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }
      else {
        rotate_stepperT.rotateAsync(stepper_tilt);
        rotate_stepperT.overrideAcceleration(tiltAccelJoy);           // to make accel less when using joystick
        rotate_stepperT.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      }
      else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }
    }
    else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                                 //wait to make sure all data in the Serial2 message has arived
      instruction = Serial2.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial2.read();
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial2.available()) {                             //set elemetns of stringText to the Serial2 values sent
          char digit = Serial2.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial2Flush();                                           //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);                 //converts stringText to an int
      } else {
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial2.available()) {                             //set elemetns of stringText to the Serial2 values sent
          char digit = Serial2.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial2Flush();                                           //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);                 //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);               //converts stringText to a float
        if (instruction == '+') {                                 //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                             //wait to make sure all data in the Serial2 message has arived
          Serial2Flush();                                         //Clear any excess data in the Serial2 buffer
          return;
        }
      }
    } else {
      return;
    }
  } else if (Serial1.available() > 0) {
    instruction = Serial1.read();
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial1.available() < 6) {                           //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial1Flush();                                         //  Clear the Serial1 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;

      short sliderStepSpeed = (Serial1.read() << 8) + Serial1.read();
      short panStepSpeed = (Serial1.read() << 8) + Serial1.read();
      short tiltStepSpeed = (Serial1.read() << 8) + Serial1.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -panMaxFactor, panMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -tiltMaxFactor, tiltMaxFactor);

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      else {
        rotate_stepperS.rotateAsync(stepper_slider);
        rotate_stepperS.overrideAcceleration(sliderAccelJoy);         // to make accel less when using joystick
        rotate_stepperS.overrideSpeed(speedFactorS);
      }

      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      else {
        rotate_stepperP.rotateAsync(stepper_pan);
        rotate_stepperP.overrideAcceleration(panAccelJoy);            // to make accel less when using joystick
        rotate_stepperP.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }
      else {
        rotate_stepperT.rotateAsync(stepper_tilt);
        rotate_stepperT.overrideAcceleration(tiltAccelJoy);           // to make accel less when using joystick
        rotate_stepperT.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      }
      else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }
    }
    else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                                 //wait to make sure all data in the Serial1 message has arived
      instruction = Serial1.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial1.read();
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial1.available()) {                             //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial1Flush();                                           //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
      }
      else {
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial1.available()) {                             //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial1Flush();                                           //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);              //converts stringText to a float
        if (instruction == '+') {                                 //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                             //wait to make sure all data in the Serial1 message has arived
          Serial1Flush();                                         //Clear any excess data in the Serial1 buffer
          return;
        }
      }
    }
    else {
      return;
    }
  }
  else if (Serial3.available() > 0) {
    instruction = Serial3.read();
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial3.available() < 6) {                       //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial3Flush();                                     //  Clear the Serial3 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;

      short sliderStepSpeed = (Serial3.read() << 8) + Serial3.read();
      short panStepSpeed = (Serial3.read() << 8) + Serial3.read();
      short tiltStepSpeed = (Serial3.read() << 8) + Serial3.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -panMaxFactor, panMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -tiltMaxFactor, tiltMaxFactor);

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      else {
        rotate_stepperS.rotateAsync(stepper_slider);
        rotate_stepperS.overrideAcceleration(sliderAccelJoy);         // to make accel less when using joystick
        rotate_stepperS.overrideSpeed(speedFactorS);
      }

      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      else {
        rotate_stepperP.rotateAsync(stepper_pan);
        rotate_stepperP.overrideAcceleration(panAccelJoy);            // to make accel less when using joystick
        rotate_stepperP.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }
      else {
        rotate_stepperT.rotateAsync(stepper_tilt);
        rotate_stepperT.overrideAcceleration(tiltAccelJoy);           // to make accel less when using joystick
        rotate_stepperT.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
      }
      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
      }
      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      }
      else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }
    }
    else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                                 //wait to make sure all data in the Serial3 message has arived
      instruction = Serial3.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial3.read();
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial3.available()) {                             //set elemetns of stringText to the Serial3 values sent
          char digit = Serial3.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial3Flush();                                           //Clear any excess data in the Serial3 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
      }
      else {
        memset(&stringText[0], 0, sizeof(stringText));            //clear the array
        while (Serial3.available()) {                             //set elemetns of stringText to the Serial3 values sent
          char digit = Serial3.read();                            //read in a char
          strncat(stringText, &digit, 1);                         //add digit to the end of the array
        }
        Serial3Flush();                                           //Clear any excess data in the Serial3 buffer
        SerialCommandValueInt = atoi(stringText);                //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);              //converts stringText to a float
        if (instruction == '+') {                                 //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                             //wait to make sure all data in the Serial3 message has arived
          Serial3Flush();                                         //Clear any excess data in the Serial3 buffer
          return;
        }
      }
    }
    else {
      return;
    }
  }
  else {
    return;
  }

  //Serial.println(instruction);
  //Serial.println(SerialCommandValueInt);

  if (!atPos1 && !atPos2 && !atPos3 && !atPos4 && !atPos5 && !atPos6 && !sentMoved) {
    Serial1.println("#s");          // not at any set pos
    Serial2.println("#s");
    Serial3.println("#s");
    sentMoved = true;
  }

  switch (instruction) {
    case INSTRUCTION_IS_CAM_DELAY: {
        if (dlyPos == 49) {
          dlyPos1Time = SerialCommandValueInt;
          Serial1.print("Delay before 2nd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
        else if (dlyPos == 50) {
          dlyPos2Time = SerialCommandValueInt;
          Serial1.print("Delay before 3rd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
        else if (dlyPos == 51) {
          dlyPos3Time = SerialCommandValueInt;
          Serial1.print("Delay before 4th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
        else if (dlyPos == 52) {
          dlyPos4Time = SerialCommandValueInt;
          Serial1.print("Delay before 5th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
        else if (dlyPos == 53) {
          dlyPos5Time = SerialCommandValueInt;
          Serial1.print("Delay before 6th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
      }
      break;
    case INSTRUCTION_IS_RUN_CAM: {
        Serial1.println("Run array of moves.");
        Serial1.println("#$");
        if (pos1set) {
          moveToIndex(1);
          timeElapsed = 0;
          if (pos2set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos1Time);
            Serial1.println("ms");
            previousTime = dlyPos1Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(2);
            timeElapsed = 0;
          }
          if (pos3set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos2Time);
            Serial1.println("ms");
            previousTime = dlyPos2Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(3);
            timeElapsed = 0;
          }
          if (pos4set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos3Time);
            Serial1.println("ms");
            previousTime = dlyPos3Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(4);
            timeElapsed = 0;
          }
          if (pos5set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos4Time);
            Serial1.println("ms");
            previousTime = dlyPos4Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(5);
            timeElapsed = 0;
          }
          if (pos6set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos5Time);
            Serial1.println("ms");
            previousTime = dlyPos5Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(6);
            timeElapsed = 0;
          }
        }
      }
      break;
    case INSTRUCTION_DIRECT_MOVE: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          moveToIndex(SerialCommandValueInt);
        }
      }
      break;
    case INSTRUCTION_SETPOS: {
        editKeyframe(SerialCommandValueInt);
      }
      break;
    case INSTRUCTION_CLEAR_ARRAY: {
        clearKeyframes();
      }
      break;
    case INSTRUCTION_INC_SLIDER_SPEED: {
        slider_set_speed = slider_set_speed + slider_inc_speed;
        if (slider_set_speed >= slider_max_speed) {
          slider_set_speed = slider_max_speed;
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

          Serial1.println("^=7");
          Serial2.println("^=7");
          Serial3.println("^=7");

          Serial.println(String("Slider at MAX speed: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println(String("Slider at MAX speed: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println("#$");
        }
        else {
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

          LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
          Serial1.print("^=");
          Serial1.println(LEDsliderSpeed);
          Serial2.print("^=");
          Serial2.println(LEDsliderSpeed);
          Serial3.print("^=");
          Serial3.println(LEDsliderSpeed);

          Serial.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_DEC_SLIDER_SPEED: {
        slider_set_speed = slider_set_speed - slider_inc_speed;
        if (slider_set_speed <= slider_min_speed) {
          slider_set_speed = slider_min_speed;
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

          Serial1.println("^=0");
          Serial2.println("^=0");
          Serial3.println("^=0");

          Serial.println(String("Slider at MIN speed: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println(String("Slider at MIN speed: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println("#$");
        }
        else {
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

          LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
          Serial1.print("^=");
          Serial1.println(LEDsliderSpeed);
          Serial2.print("^=");
          Serial2.println(LEDsliderSpeed);
          Serial3.print("^=");
          Serial3.println(LEDsliderSpeed);

          Serial.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_MAX_SLIDER_SPEED: {
        slider_set_speed = slider_max_speed;
        stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

        Serial1.println("#q");
        Serial2.println("#q");
        Serial3.println("#q");

        Serial.println(String("Set Slider Speed to MAX speed: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Speed to MAX speed: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_MIN_SLIDER_SPEED: {
        slider_set_speed = slider_min_speed;
        stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

        Serial1.println("#u");
        Serial2.println("#u");
        Serial3.println("#u");

        Serial.println(String("Set Slider Speed to MIN speed: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Speed to MIN speed: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_INC_SLIDER_SPEED: {
        slider_inc_speed = SerialCommandValueInt;
        Serial.println(String("Set Slider Speed Increment to: ") + slider_inc_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Increment to: ") + slider_inc_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_MIN_SLIDER_SPEED: {
        slider_min_speed = SerialCommandValueInt;
        if (slider_min_speed >= slider_set_speed) {
          slider_set_speed = slider_min_speed;
          Serial1.println("^=0");
          Serial2.println("^=0");
          Serial3.println("^=0");
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
        }
        else {
          LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
          Serial1.print("^=");
          Serial1.println(LEDsliderSpeed);
          Serial2.print("^=");
          Serial2.println(LEDsliderSpeed);
          Serial3.print("^=");
          Serial3.println(LEDsliderSpeed);
        }
        Serial.println(String("Set Slider Min Speed to: ") + slider_min_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Min Speed to: ") + slider_min_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_MAX_SLIDER_SPEED: {
        slider_max_speed = SerialCommandValueInt;
        if (slider_max_speed <= slider_set_speed) {
          slider_set_speed = slider_max_speed;
          Serial1.println("^=7");
          Serial2.println("^=7");
          Serial3.println("^=7");
          stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
        }
        else {
          LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
          Serial1.print("^=");
          Serial1.println(LEDsliderSpeed);
          Serial2.print("^=");
          Serial2.println(LEDsliderSpeed);
          Serial3.print("^=");
          Serial3.println(LEDsliderSpeed);
        }
        Serial.println(String("Set Slider Max Speed to: ") + slider_max_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Max Speed to: ") + slider_max_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_PAN_ACCEL: {
        pan_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_pan.setAcceleration(pan_accel);
        Serial.println(String("Pan accel : ") + pan_accel + String(" steps/s²"));
        Serial1.println(String("Pan accel : ") + pan_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TILT_ACCEL: {
        tilt_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_tilt.setAcceleration(tilt_accel);
        Serial.println(String("Tilt accel : ") + tilt_accel + String(" steps/s²"));
        Serial1.println(String("Tilt accel : ") + tilt_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_ACCEL: {
        slider_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_slider.setAcceleration(slider_accel);
        Serial.println(String("Slider accel : ") + slider_accel + String(" steps/s²"));
        Serial1.println(String("Slider accel : ") + slider_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_PAN_JOY_ACCEL: {
        panAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial.println(String("Pan Joy accel factor : ") + panAccelJoy);
        Serial1.println(String("Pan Joy accel factor : ") + panAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TILT_JOY_ACCEL: {
        tiltAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial.println(String("Tilt Joy accel factor : ") + tiltAccelJoy);
        Serial1.println(String("Tilt Joy accel factor : ") + tiltAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_JOY_ACCEL: {
        sliderAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial.println(String("Slider Joy accel factor : ") + sliderAccelJoy);
        Serial1.println(String("Slider Joy accel factor : ") + sliderAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SAVE_TO_EEPROM: {
        saveEEPROM();
      }
      break;
    case INSTRUCTION_DEBUG_STATUS: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          debugReport();
        }
      }
      break;
    case INSTRUCTION_POSITION_STATUS: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          positionReport();
        }
      }
      break;
    case INSTRUCTION_KEYFRAMES_STATUS: {
        printKeyframeElements();
      }
      break;
    case INSTRUCTION_RESET_LEDS: {
        doRemoteControlLEDs();
      }
      break;
    case INSTRUCTION_PAN_DEGREES: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          panDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          tiltDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          sliderMoveTo(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_PAN_DEGREES_REL: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          panDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES_REL: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          tiltDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES_REL: {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          sliderMMRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SET_PAN_SPEED: {
        pan_set_speed = SerialCommandValueFloat;
        pan_def_speed = pan_set_speed;                                                        //  set default speeds
        stepper_pan.setMaxSpeed(panDegreesToSteps(pan_set_speed));

        tilt_set_speed = SerialCommandValueFloat;
        tilt_def_speed = tilt_set_speed;                                                      //  set default speeds
        stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));

        Serial.print(instruction);
        Serial.println(pan_set_speed);
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

        Serial.println(String("Set Pan/Tilt Speed to: ") + pan_set_speed + String("°/s.\n"));
        Serial1.println(String("Set Pan/Tilt Speed to: ") + pan_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_TILT_SPEED: {
        tilt_set_speed = SerialCommandValueFloat;
        tilt_def_speed = tilt_set_speed;                                                      //  set default speeds
        stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));
        Serial.println(String("Set Tilt Speed to: ") + tilt_set_speed + String("°/s.\n"));
        Serial1.println(String("Set Tilt Speed to: ") + tilt_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED: {
        slider_set_speed = SerialCommandValueFloat;
        slider_def_speed = slider_set_speed;                                                  //  set default speeds
        stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

        LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
        Serial1.print("^=");
        Serial1.println(LEDsliderSpeed);
        Serial2.print("^=");
        Serial2.println(LEDsliderSpeed);
        Serial3.print("^=");
        Serial3.println(LEDsliderSpeed);

        Serial.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_IN: {
        zoom_speed = SerialCommandValueInt;
        zoomIN = true;
        zoomOUT = false;

        Serial1.print("#I");
        Serial1.println(zoom_speed);
        Serial2.print("#I");
        Serial2.println(zoom_speed);
        Serial3.print("#I");
        Serial3.println(zoom_speed);

        Serial.println("Zoom IN.");
        Serial1.println("Zoom IN.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_OUT: {
        zoom_speed = SerialCommandValueInt;
        zoomIN = false;
        zoomOUT = true;

        Serial1.print("#i");
        Serial1.println(zoom_speed);
        Serial2.print("#i");
        Serial2.println(zoom_speed);
        Serial3.print("#i");
        Serial3.println(zoom_speed);

        Serial.println("Zoom OUT.");
        Serial1.println("Zoom OUT.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_STOP_ZOOM: {
        zoomIN = false;
        zoomOUT = false;

        Serial1.println("#o");
        Serial2.println("#o");
        Serial3.println("#o");
        delay(20);
        Serial1.println("#o");                    // Just in case, it's important!
        Serial2.println("#o");
        Serial3.println("#o");

        Serial.println("STOP Zooming.\n");
        Serial1.println("STOP Zooming.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TOGGLE_RECORDING: {
        Serial1.println("#O");
        Serial2.println("#O");
        Serial3.println("#O");

        Serial.println("Toggle Record.\n");
        Serial1.println("Toggle Record.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_IS_RECORDING: {
        Serial1.println("#P");
        Serial2.println("#P");
        Serial3.println("#P");
      }
      break;
    case INSTRUCTION_IS_NOT_RECORDING: {
        Serial1.println("#p");
        Serial2.println("#p");
        Serial3.println("#p");
      }
      break;
    case INSTRUCTION_SET_ZERO_POS: {
        stepper_pan.setPosition(0);
        stepper_tilt.setPosition(0);
        stepper_slider.setPosition(0);
      }
      break;
    case INSTRUCTION_RESTORE_DEFAULT_SPEEDS: {
        pan_set_speed = pan_def_speed;
        tilt_set_speed = tilt_def_speed;
        slider_set_speed = slider_def_speed;

        LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
        Serial1.print("^=");
        Serial1.println(LEDsliderSpeed);
        Serial2.print("^=");
        Serial2.println(LEDsliderSpeed);
        Serial3.print("^=");
        Serial3.println(LEDsliderSpeed);

        Serial1.println("#d");
        Serial2.println("#d");
        Serial3.println("#d");

        Serial1.println(String("Default Speed Restored: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    default:
      break;    // if unrecognised charater, do nothing
  }
}
