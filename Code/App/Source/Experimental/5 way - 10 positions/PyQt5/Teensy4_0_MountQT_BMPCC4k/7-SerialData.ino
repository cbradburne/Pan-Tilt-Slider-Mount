//  Receive Serial data, and process

void SerialData(void) {
  char instruction;
/*
  if (// Serial3.available() > 0) {
    instruction = // Serial3.read();
    if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                             //wait to make sure all data in the Serial message has arived
      instruction = // Serial3.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = // Serial3.read();
        memset(&stringText[0], 0, sizeof(stringText));      //clear the array
        while (// Serial3.available()) {                       //set elemetns of stringText to the // Serial3 values sent
          char digit = // Serial3.read();                      //read in a char
          strncat(stringText, &digit, 1);                   //add digit to the end of the array
        }
        // Serial3Flush();                                     //Clear any excess data in the // Serial3 buffer
        SerialCommandValueInt = atoi(stringText);           //converts stringText to an int
      } else {
        memset(&stringText[0], 0, sizeof(stringText));      //clear the array
        while (// Serial3.available()) {                       //set elemetns of stringText to the // Serial3 values sent
          char digit = // Serial3.read();                      //read in a char
          strncat(stringText, &digit, 1);                   //add digit to the end of the array
        }
        // Serial3Flush();                                     //Clear any excess data in the // Serial3 buffer
        SerialCommandValueInt = atoi(stringText);           //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);         //converts stringText to a float
        if (instruction == '+') {                           //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                       //wait to make sure all data in the // Serial3 message has arived
          // Serial3Flush();                                   //Clear any excess data in the // Serial3 buffer
          return;
        }
      }
    } else {
      return;
    }
  } else 
  
  */
  
  if (Serial1.available() > 0) {
    instruction = Serial1.read();
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial1.available() < 6) {                     //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial1Flush();                                   //  Clear the Serial1 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;
      atPos7 = false;
      atPos8 = false;
      atPos9 = false;
      atPos0 = false;

      short sliderStepSpeed = (Serial1.read() << 8) + Serial1.read();
      if (!withSlider) {
        sliderStepSpeed = 0;
      }
      short panStepSpeed = (Serial1.read() << 8) + Serial1.read();
      short tiltStepSpeed = (Serial1.read() << 8) + Serial1.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -pantiltMaxFactor, pantiltMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -pantiltMaxFactor, pantiltMaxFactor);

      previousMillisMoveCheck = millis();

      if (speedFactorP == 0.0) {
        if (panRunning) {
          panRunning = false;
          stepper_pan.overrideSpeed(0);
          stepper_pan.stopAsync();
        }
      } else {
        if (!panRunning) {
          panRunning = true;
          stepper_pan.setAcceleration(pantilt_accel * pantilt_set_speed * 10);
          stepper_pan.rotateAsync(pantilt_set_speed);
        }
        if (upsideDown) {
          speedFactorP = (speedFactorP * -1);
        }
        stepper_pan.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        if (tiltRunning) {
          tiltRunning = false;
          stepper_tilt.overrideSpeed(0);
          stepper_tilt.stopAsync();
        }
      } else {
        if (!tiltRunning) {
          tiltRunning = true;
          stepper_tilt.setAcceleration(pantilt_accel * pantilt_set_speed * 10);
          stepper_tilt.rotateAsync(pantilt_set_speed);
        }
        if (upsideDown) {
          speedFactorT = (speedFactorT * -1);
        }
        stepper_tilt.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        if (sliderRunning) {
          sliderRunning = false;
          stepper_slider.overrideSpeed(0);
          stepper_slider.stopAsync();

          stepper_slider.setAcceleration(slider_accel * slider_set_speed * 4);
        }
      } else {
        if (!sliderRunning) {
          sliderRunning = true;
          stepper_slider.rotateAsync(slider_set_speed);
        }
        if (slideReverse) {
          speedFactorS = (speedFactorS * -1);
        }
        if ((stepper_slider.getPosition() <= 1000) && (stepper_slider.getPosition() >= 0)) {
          stepper_slider.setAcceleration(10000);
          stepper_slider.overrideSpeed(speedFactorS);
        }
        else {
          stepper_slider.emergencyStop();
        }
      }

      if (speedFactorP == 0.0) {
        stepper_pan.setAcceleration(pantilt_accel);
      }
      if (speedFactorT == 0.0) {
        stepper_tilt.setAcceleration(pantilt_accel);
      }
      if (speedFactorS == 0.0) {
        stepper_slider.setAcceleration(slider_accel);
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      } else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }




    } else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);                                             //wait to make sure all data in the Serial1 message has arived
      instruction = Serial1.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial1.read();
        memset(&stringText[0], 0, sizeof(stringText));      //clear the array
        while (Serial1.available()) {                       //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                      //read in a char
          strncat(stringText, &digit, 1);                   //add digit to the end of the array
        }
        Serial1Flush();                                     //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);           //converts stringText to an int
      } else if (instruction == INSTRUCTION_IS_SETTINGS_REQUESTED) {
        delay(2);
        whichSetting = Serial1.read();
      } else {
        memset(&stringText[0], 0, sizeof(stringText));      //clear the array
        while (Serial1.available()) {                       //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                      //read in a char
          strncat(stringText, &digit, 1);                   //add digit to the end of the array
        }
        Serial1Flush();                                     //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);           //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);         //converts stringText to a float
        if (instruction == '+') {                           //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                       //wait to make sure all data in the Serial1 message has arived
          Serial1Flush();                                   //Clear any excess data in the Serial1 buffer
          return;
        }
      }
    } else {
      return;
    }
  } else {
    return;
  }

  if (!atPos1 && !atPos2 && !atPos3 && !atPos4 && !atPos5 && !atPos6 && !atPos7 && !atPos8 && !atPos9 && !atPos0 && !sentMoved) {
    Serial1.println("#s");                                  // not at any set pos
    sentMoved = true;
  }
  
  switch (instruction) {
    case INSTRUCTION_IS_SETTINGS_REQUESTED:
      {
        sendCamSettings();
      }
      break;
    case INSTRUCTION_IS_CHANGE_SETTINGS:
      {
        String stringText = Serial1.readStringUntil('\n');
        SerialCommandValueInt = stringText.toInt();

        if (whichSetting == 'a') {
          pantilt_speed1 = SerialCommandValueInt;
        } else if (whichSetting == 's') {
          pantilt_speed2 = SerialCommandValueInt;
        } else if (whichSetting == 'd') {
          pantilt_speed3 = SerialCommandValueInt;
        } else if (whichSetting == 'f') {
          pantilt_speed4 = SerialCommandValueInt;
        } else if (whichSetting == 'A') {
          slider_speed1 = SerialCommandValueInt;
        } else if (whichSetting == 'S') {
          slider_speed2 = SerialCommandValueInt;
        } else if (whichSetting == 'D') {
          slider_speed3 = SerialCommandValueInt;
        } else if (whichSetting == 'F') {
          slider_speed4 = SerialCommandValueInt;
        }
      }
      break;
    case INSTRUCTION_IS_CAM_DELAY:
      {
        if (dlyPos == 49) {
          dlyPos1Time = SerialCommandValueInt;
          Serial1.print("Delay before 2nd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 50) {
          dlyPos2Time = SerialCommandValueInt;
          Serial1.print("Delay before 3rd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 51) {
          dlyPos3Time = SerialCommandValueInt;
          Serial1.print("Delay before 4th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 52) {
          dlyPos4Time = SerialCommandValueInt;
          Serial1.print("Delay before 5th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 53) {
          dlyPos5Time = SerialCommandValueInt;
          Serial1.print("Delay before 6th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
      }
      break;
    case INSTRUCTION_IS_RUN_CAM:
      {
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
    case INSTRUCTION_DIRECT_MOVE:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          moveToIndex(SerialCommandValueInt);
        }
      }
      break;
    case INSTRUCTION_SETPOS:
      {
        editKeyframe(SerialCommandValueInt);
      }
      break;
    case INSTRUCTION_SLIDE_END1:
      {
        moveSliderToEnd1();
      }
      break;
    case INSTRUCTION_SLIDE_END2:
      {
        moveSliderToEnd2();
      }
      break;
    case INSTRUCTION_CLEAR_ARRAY:
      {
        clearKeyframes();
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED1:
      {
        pantilt_speed1 = SerialCommandValueInt;
        Serial1.println(String("#d") + pantilt_speed1);
        Serial1.println(String("Pan/Tilt Speed 1 : ") + pantilt_speed1 + String("°/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED2:
      {
        pantilt_speed2 = SerialCommandValueInt;
        Serial1.println(String("#f") + pantilt_speed2);
        Serial1.println(String("Pan/Tilt Speed 2 : ") + pantilt_speed2 + String("°/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED3:
      {
        pantilt_speed3 = SerialCommandValueInt;
        Serial1.println(String("#g") + pantilt_speed3);
        Serial1.println(String("Pan/Tilt Speed 3 : ") + pantilt_speed3 + String("°/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED4:
      {
        pantilt_speed4 = SerialCommandValueInt;
        Serial1.println(String("#h") + pantilt_speed4);
        Serial1.println(String("Pan/Tilt Speed 4 : ") + pantilt_speed4 + String("°/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED1:
      {
        slider_speed1 = SerialCommandValueInt;
        Serial1.println(String("#j") + slider_speed1);
        Serial1.println(String("Silder Speed 1 : ") + slider_speed1 + String("mm/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED2:
      {
        slider_speed2 = SerialCommandValueInt;
        Serial1.println(String("#k") + slider_speed2);
        Serial1.println(String("Silder Speed 2 : ") + slider_speed2 + String("mm/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED3:
      {
        slider_speed3 = SerialCommandValueInt;
        Serial1.println(String("#l") + slider_speed3);
        Serial1.println(String("Silder Speed 3 : ") + slider_speed3 + String("mm/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED4:
      {
        slider_speed4 = SerialCommandValueInt;
        Serial1.println(String("#;") + slider_speed4);
        Serial1.println(String("Silder Speed 4 : ") + slider_speed4 + String("mm/s"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_PANTILT_ACCEL:
      {
        pantilt_accel = SerialCommandValueInt;
        stepper_pan.setAcceleration(pantilt_accel * pantilt_set_speed);
        stepper_tilt.setAcceleration(pantilt_accel * pantilt_set_speed);

        Serial1.println(String("#q") + pantilt_accel);
        Serial1.println(String("Pan/Tilt Accel : ") + pantilt_accel + String("steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_ACCEL:
      {
        slider_accel = SerialCommandValueInt;
        stepper_slider.setAcceleration(slider_accel * slider_set_speed);
        
        Serial1.println(String("#Q") + slider_accel);
        Serial1.println(String("Slider Accel   : ") + slider_accel + String("steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SAVE_TO_EEPROM:
      {
        saveEEPROM();
      }
      break;
    case INSTRUCTION_DEBUG_STATUS:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          debugReport();
        }
      }
      break;
    case INSTRUCTION_POSITION_STATUS:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          positionReport();
        }
      }
      break;
    case INSTRUCTION_KEYFRAMES_STATUS:
      {
        printKeyframeElements();
      }
      break;
    case INSTRUCTION_RESET_LEDS:
      {
        doRemoteControlLEDs();
      }
      break;
    case INSTRUCTION_PAN_DEGREES:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          panDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          tiltDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          sliderMoveTo(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_PAN_DEGREES_REL:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          panDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES_REL:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          tiltDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES_REL:
      {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          sliderMMRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SET_PAN_SPEED:
      {
        if (SerialCommandValueInt == 1) {
          Serial1.println("^@1");
          Serial1.println("^@1");
          pantilt_set_speed = pantilt_speed1;
        } else if (SerialCommandValueInt == 2) {
          Serial1.println("^@3");
          Serial1.println("^@3");
          pantilt_set_speed = pantilt_speed2;
        } else if (SerialCommandValueInt == 3) {
          Serial1.println("^@5");
          Serial1.println("^@5");
          pantilt_set_speed = pantilt_speed3;
        } else if (SerialCommandValueInt == 4) {
          Serial1.println("^@7");
          Serial1.println("^@7");
          pantilt_set_speed = pantilt_speed4;
        }

        stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
        stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
        stepper_pan.setAcceleration(pantilt_accel * pantilt_set_speed);
        stepper_tilt.setAcceleration(pantilt_accel * pantilt_set_speed);

        Serial1.println(String("Set Pan/Tilt Speed to: ") + pantilt_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED:
      {
        if (SerialCommandValueInt == 1) {
          Serial1.println("^=1");
          Serial1.println("^=1");
          slider_set_speed = slider_speed1;
        } else if (SerialCommandValueInt == 2) {
          Serial1.println("^=3");
          Serial1.println("^=3");
          slider_set_speed = slider_speed2;
        } else if (SerialCommandValueInt == 3) {
          Serial1.println("^=5");
          Serial1.println("^=5");
          slider_set_speed = slider_speed3;
        } else if (SerialCommandValueInt == 4) {
          Serial1.println("^=7");
          Serial1.println("^=7");
          slider_set_speed = slider_speed4;
        }

        stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
        stepper_slider.setAcceleration(slider_accel * slider_set_speed);

        Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_IN:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = true;
        zoomOUT = false;

        // Serial3.print("#I");
        // Serial3.println(zoom_speed);

        Serial1.println("Zoom IN.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_OUT:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = false;
        zoomOUT = true;

        // Serial3.print("#i");
        // Serial3.println(zoom_speed);

        Serial1.println("Zoom OUT.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_STOP_ZOOM:
      {
        zoomIN = false;
        zoomOUT = false;

        // Serial3.println("#o");
        delay(20);
        // Serial3.println("#o");  // Just in case, it's important!

        Serial1.println("STOP Zooming.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_AUTOFOCUS_ON:
      {
        // Serial3.println("#F");
      }
      break;
    case INSTRUCTION_SET_AUTOFOCUS_OFF:
      {
        // Serial3.println("#f");
      }
      break;
    case INSTRUCTION_IS_AUTOFOCUS_ON:
      {
        Serial1.println("#O");
      }
      break;
    case INSTRUCTION_IS_AUTOFOCUS_OFF:
      {
        Serial1.println("#o");
      }
      break;
    case INSTRUCTION_TOGGLE_RECORDING:
      {
        // Serial3.println("#O");

        Serial1.println("Toggle Record.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_IS_RECORDING:
      {
        Serial1.println("#P");
      }
      break;
    case INSTRUCTION_IS_NOT_RECORDING:
      {
        Serial1.println("#p");
      }
      break;
    case INSTRUCTION_SET_ZERO_POS:
      {
        stepper_pan.setPosition(0);
        stepper_tilt.setPosition(0);
        stepper_slider.setPosition(0);
      }
      break;
    default:
      break;  // if unrecognised charater, do nothing
  }
}