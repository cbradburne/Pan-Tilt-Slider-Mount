//  Receive Serial data, and process

void SerialData(void) {
  char instruction;

  if (Serial2.available() > 0) {
    instruction = Serial2.read();
    if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);  //wait to make sure all data in the Serial message has arived
      instruction = Serial2.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial2.read();
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial2.available()) {                   //set elemetns of stringText to the Serial2 values sent
          char digit = Serial2.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial2Flush();                            //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);  //converts stringText to an int
      } else {
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial2.available()) {                   //set elemetns of stringText to the Serial2 values sent
          char digit = Serial2.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial2Flush();                              //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);    //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);  //converts stringText to a float
        if (instruction == '+') {                    //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                //wait to make sure all data in the Serial2 message has arived
          Serial2Flush();                            //Clear any excess data in the Serial2 buffer
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
      while (Serial1.available() < 6) {  //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial1Flush();  //  Clear the Serial1 buffer
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
          rotate_stepperP.stopAsync();
        }
      } else {
        if (!panRunning && (speedFactorP != 0)) {
          panRunning = true;
          rotate_stepperP.rotateAsync(stepper_pan);
          rotate_stepperP.overrideAcceleration(60);  // to make accel faster when using joystick
          rotate_stepperP.overrideSpeed(0);
        }
        if (upsideDown) {
          speedFactorP = (speedFactorP * -1);
        }
        rotate_stepperP.overrideSpeed(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        if (tiltRunning) {
          tiltRunning = false;
          rotate_stepperT.stopAsync();
        }
      } else {
        if (!tiltRunning && (speedFactorT != 0)) {
          tiltRunning = true;
          rotate_stepperT.rotateAsync(stepper_tilt);
          rotate_stepperT.overrideAcceleration(60);  // to make accel faster when using joystick
          rotate_stepperT.overrideSpeed(0);
        }
        rotate_stepperT.overrideSpeed(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        if (sliderRunning) {
          sliderRunning = false;
          rotate_stepperS.stopAsync();
        }
      } else {
        if (slideReverse) {
          speedFactorS = -speedFactorS;
          if ((findingHome == true) || ((findingHome == false) && (((stepper_slider.getPosition() > ((slideLimit * -1) * 0.97)) && (speedFactorS < 0)) || ((stepper_slider.getPosition() < ((slideLimit * -1) * 0.03)) && (speedFactorS > 0))))) {
            if (!sliderRunning && (speedFactorS != 0)) {
              sliderRunning = true;
              rotate_stepperS.rotateAsync(stepper_slider);
              rotate_stepperS.overrideAcceleration(10);  // to make accel faster when using joystick
              rotate_stepperS.overrideSpeed(0);
            }
            rotate_stepperS.overrideSpeed(speedFactorS);
          }
        } else {
          if ((findingHome == true) || ((findingHome == false) && (((stepper_slider.getPosition() < (slideLimit * 0.97)) && (speedFactorS > 0)) || ((stepper_slider.getPosition() > (slideLimit * 0.03)) && (speedFactorS < 0))))) {
            if (!sliderRunning && (speedFactorS != 0)) {
              sliderRunning = true;
              rotate_stepperS.rotateAsync(stepper_slider);
              rotate_stepperS.overrideAcceleration(10);  // to make accel faster when using joystick
              rotate_stepperS.overrideSpeed(0);
            }
            rotate_stepperS.overrideSpeed(speedFactorS);
          }
        }
      }

      if (speedFactorP == 0.0) {
        rotate_stepperP.stopAsync();
        stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
      }
      if (speedFactorT == 0.0) {
        rotate_stepperT.stopAsync();
        stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
      }
      if (speedFactorS == 0.0) {
        rotate_stepperS.stopAsync();
        stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      } else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }
    } else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);  //wait to make sure all data in the Serial1 message has arived
      instruction = Serial1.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial1.read();
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial1.available()) {                   //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial1Flush();                            //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);  //converts stringText to an int
      } else if (instruction == INSTRUCTION_IS_SETTINGS_REQUESTED) {
        delay(2);
        whichSetting = Serial1.read();
      } else {
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial1.available()) {                   //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial1Flush();                              //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);    //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);  //converts stringText to a float
        if (instruction == '+') {                    //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                //wait to make sure all data in the Serial1 message has arived
          Serial1Flush();                            //Clear any excess data in the Serial1 buffer
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
    Serial1.println("#s");  // not at any set pos
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
          if (withSlider) {
            slider_speed1 = SerialCommandValueInt;
          }
        } else if (whichSetting == 'S') {
          if (withSlider) {
            slider_speed2 = SerialCommandValueInt;
          }
        } else if (whichSetting == 'D') {
          if (withSlider) {
            slider_speed3 = SerialCommandValueInt;
          }
        } else if (whichSetting == 'F') {
          if (withSlider) {
            slider_speed4 = SerialCommandValueInt;
          }
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
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
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
        if (pantilt_set_speed == pantilt_speed1) {
          pantilt_speed1 = SerialCommandValueInt;
          pantilt_set_speed = pantilt_speed1;
          stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
          stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
          stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
          stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        } else {
          pantilt_speed1 = SerialCommandValueInt;
          Serial1.println(String("#d") + pantilt_speed1);
          Serial1.println(String("Pan/Tilt Speed 1 : ") + pantilt_speed1 + String("°/s"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED2:
      {
        if (pantilt_set_speed == pantilt_speed2) {
          pantilt_speed2 = SerialCommandValueInt;
          pantilt_set_speed = pantilt_speed2;
          stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
          stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
          stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
          stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        } else {
          pantilt_speed2 = SerialCommandValueInt;
          Serial1.println(String("#f") + pantilt_speed2);
          Serial1.println(String("Pan/Tilt Speed 2 : ") + pantilt_speed2 + String("°/s"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED3:
      {
        if (pantilt_set_speed == pantilt_speed3) {
          pantilt_speed3 = SerialCommandValueInt;
          pantilt_set_speed = pantilt_speed3;
          stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
          stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
          //stepper_pan.setAcceleration(pantilt_accel * (pantilt_set_speed / 10));
          //stepper_tilt.setAcceleration(pantilt_accel * (pantilt_set_speed / 10));
          stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
          stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        } else {
          pantilt_speed3 = SerialCommandValueInt;
          Serial1.println(String("#g") + pantilt_speed3);
          Serial1.println(String("Pan/Tilt Speed 3 : ") + pantilt_speed3 + String("°/s"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_SET_PANTILT_SPEED4:
      {
        if (pantilt_set_speed == pantilt_speed4) {
          pantilt_speed4 = SerialCommandValueInt;
          pantilt_set_speed = pantilt_speed4;
          stepper_pan.setMaxSpeed(panDegreesToSteps(pantilt_set_speed));
          stepper_tilt.setMaxSpeed(tiltDegreesToSteps(pantilt_set_speed));
          stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
          stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        } else {
          pantilt_speed4 = SerialCommandValueInt;
          Serial1.println(String("#h") + pantilt_speed4);
          Serial1.println(String("Pan/Tilt Speed 4 : ") + pantilt_speed4 + String("°/s"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED1:
      {
        if (withSlider) {
          if (slider_set_speed == slider_speed1) {
            slider_speed1 = SerialCommandValueInt;
            slider_set_speed = slider_speed1;
            stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
            stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
          } else {
            slider_speed1 = SerialCommandValueInt;
            Serial1.println(String("#j") + slider_speed1);
            Serial1.println(String("Silder Speed 1 : ") + slider_speed1 + String("mm/s"));
            Serial1.println("#$");
          }
        }
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED2:
      {
        if (withSlider) {
          if (slider_set_speed == slider_speed2) {
            slider_speed2 = SerialCommandValueInt;
            slider_set_speed = slider_speed2;
            stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
            stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
          } else {
            slider_speed2 = SerialCommandValueInt;
            Serial1.println(String("#k") + slider_speed2);
            Serial1.println(String("Silder Speed 2 : ") + slider_speed2 + String("mm/s"));
            Serial1.println("#$");
          }
        }
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED3:
      {
        if (withSlider) {
          if (slider_set_speed == slider_speed3) {
            slider_speed3 = SerialCommandValueInt;
            slider_set_speed = slider_speed3;
            stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
            stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
          } else {
            slider_speed3 = SerialCommandValueInt;
            Serial1.println(String("#l") + slider_speed3);
            Serial1.println(String("Silder Speed 3 : ") + slider_speed3 + String("mm/s"));
            Serial1.println("#$");
          }
        }
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED4:
      {
        if (withSlider) {
          if (slider_set_speed == slider_speed4) {
            slider_speed4 = SerialCommandValueInt;
            slider_set_speed = slider_speed4;
            stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
            stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);
          } else {
            slider_speed4 = SerialCommandValueInt;
            Serial1.println(String("#;") + slider_speed4);
            Serial1.println(String("Silder Speed 4 : ") + slider_speed4 + String("mm/s"));
            Serial1.println("#$");
          }
        }
      }
      break;
    case INSTRUCTION_SET_SLIDE_LIMIT:
      {
        if (withSlider) {
          slideLimit = sliderMillimetresToSteps(SerialCommandValueInt);
          Serial1.println(String("Slide Limit Set: ") + sliderStepsToMillimetres(slideLimit));
          Serial1.println("#$");
          if (stepper_slider.getPosition() >= slideLimit) {
            sliderAtLimit = true;
            Serial1.println("Slider @ Limit");
          }
        }
      }
      break;
    case INSTRUCTION_SET_ZOOM_LIMIT:
      {
        zoomLimit = SerialCommandValueInt;
        Serial1.println(String("Zoom Limit Set: ") + zoomLimit);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_PANTILT_ACCEL:
      {
        pantilt_accel = SerialCommandValueInt;
        stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);

        Serial1.println(String("#q") + pantilt_accel);
        Serial1.println(String("Pan/Tilt Accel : ") + pantilt_accel + String("steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_ACCEL:
      {
        if (withSlider) {
          slider_accel = SerialCommandValueInt;
          stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);

          Serial1.println(String("#Q") + slider_accel);
          Serial1.println(String("Slider Accel   : ") + slider_accel + String("steps/s²"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_SAVE_TO_EEPROM:
      {
        saveEEPROM();
      }
      break;
    case INSTRUCTION_DEBUG_STATUS:
      {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          debugReport();
        }
      }
      break;
    case INSTRUCTION_POSITION_STATUS:
      {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
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
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          if (upsideDown) {
            panDegrees(-SerialCommandValueFloat);
          } else {
            panDegrees(SerialCommandValueFloat);
          }
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES:
      {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          tiltDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES:
      {
        if (withSlider) {
          if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
            if (slideReverse) {
              SerialCommandValueFloat = -SerialCommandValueFloat;
              if (((stepper_slider.getPosition() >= (slideLimit * -1)) && (SerialCommandValueFloat < 0) && (!sliderAtLimit)) || ((stepper_slider.getPosition() <= 0) && (SerialCommandValueFloat > 0) && (!sliderAtZero))) {
                sliderRunning = true;
                sliderMoveTo(SerialCommandValueFloat);
                sliderRunning = false;
              }
            } else {
              if (((stepper_slider.getPosition() <= slideLimit) && (SerialCommandValueFloat > 0) && (!sliderAtLimit)) || ((stepper_slider.getPosition() >= 0) && (SerialCommandValueFloat < 0) && (!sliderAtZero))) {
                sliderRunning = true;
                sliderMMRel(SerialCommandValueFloat);
                sliderRunning = false;
              }
            }
          }
        }
      }
      break;
    case INSTRUCTION_PAN_DEGREES_REL:
      {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          if (upsideDown) {
            panDegreesRel(-SerialCommandValueFloat);
          } else {
            panDegreesRel(SerialCommandValueFloat);
          }
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES_REL:
      {
        if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          tiltDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES_REL:
      {
        if (withSlider) {
          if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
            if (slideReverse) {
              SerialCommandValueFloat = -SerialCommandValueFloat;
              if (((stepper_slider.getPosition() >= (slideLimit * -1)) && (SerialCommandValueFloat < 0) && (!sliderAtLimit)) || ((stepper_slider.getPosition() <= 0) && (SerialCommandValueFloat > 0) && (!sliderAtZero))) {
                sliderRunning = true;
                sliderMMRel(SerialCommandValueFloat);
                sliderRunning = false;
              }
            } else {
              if (((stepper_slider.getPosition() <= slideLimit) && (SerialCommandValueFloat > 0) && (!sliderAtLimit)) || ((stepper_slider.getPosition() >= 0) && (SerialCommandValueFloat < 0) && (!sliderAtZero))) {
                sliderRunning = true;
                sliderMMRel(SerialCommandValueFloat);
                sliderRunning = false;
              }
            }
          }
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
        stepper_pan.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);
        stepper_tilt.setAcceleration((pantilt_accel / 20) * pantilt_set_speed);

        Serial1.println(String("Set Pan/Tilt Speed to: ") + pantilt_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED:
      {
        if (withSlider) {
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
          stepper_slider.setAcceleration((slider_accel / 20) * slider_set_speed);

          Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
          Serial1.println("#$");
        }
      }
      break;
    case INSTRUCTION_ZOOM_IN:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = true;
        zoomOUT = false;

        Serial2.print("#I");
        Serial2.println(zoom_speed);

        Serial1.println("Zoom IN.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_OUT:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = false;
        zoomOUT = true;

        Serial2.print("#i");
        Serial2.println(zoom_speed);

        Serial1.println("Zoom OUT.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_STOP_ZOOM:
      {
        zoomIN = false;
        zoomOUT = false;

        Serial2.println("#o");
        delay(20);
        Serial2.println("#o");  // Just in case, it's important!

        Serial1.println("STOP Zooming.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_ZERO_POS:
      {
        stepper_slider.setPosition(0);
        findingHome = false;
      }
      break;
    case INSTRUCTION_FIND_ZERO_POS:
      {
        if (findingHome == false) {
          findingHome = true;
        } else {
          findingHome = false;
        }
      }
      break;
    case INSTRUCTION_TIMELAPSE_STEPS:
      {
        numberOfSteps = SerialCommandValueFloat;
      }
      break;
    case INSTRUCTION_TIMELAPSE_START:
      {
        if (TLStarted == false) {
          stepper_pan.setTargetAbs(keyframe_array[0].panStepCount);
          stepper_tilt.setTargetAbs(keyframe_array[0].tiltStepCount);
          stepper_slider.setTargetAbs(keyframe_array[0].sliderStepCount);
          //stepper_zoom.setTargetAbs(keyframe_array[0].zoomStepCount);

          isMoving = true;
          multi_stepper.move(stepper_pan, stepper_tilt, stepper_slider);
          //StepperGroup ({stepper_pan, stepper_tilt, stepper_slider, stepper_zoom}).move();
          isMoving = false;

          TLStarted = true;
        }
      }
      break;
    case INSTRUCTION_TIMELAPSE_STOP:
      {
        if (TLStarted) {
          TLStarted = false;
          numberOfStepsCount = 0;
        }
      }
      break;
    case INSTRUCTION_TIMELAPSE_STEP:
      {
        if (TLStarted) {
          numberOfStepsCount++;

          panStepDelta = (keyframe_array[0].panStepCount + ((keyframe_array[9].panStepCount - keyframe_array[0].panStepCount) * (numberOfStepsCount / numberOfSteps)));
          tiltStepDelta = (keyframe_array[0].tiltStepCount + ((keyframe_array[9].tiltStepCount - keyframe_array[0].tiltStepCount) * (numberOfStepsCount / numberOfSteps)));
          sliderStepDelta = (keyframe_array[0].sliderStepCount + ((keyframe_array[9].sliderStepCount - keyframe_array[0].sliderStepCount) * (numberOfStepsCount / numberOfSteps)));
          //zoomStepDelta = (keyframe_array[0].zoomStepCount + ((keyframe_array[9].zoomStepCount - keyframe_array[0].zoomStepCount) * (numberOfStepsCount / numberOfSteps)));

          //Serial1.println("TLSTEP");
          //Serial1.println(String("numberOfStepsCount: ") + numberOfStepsCount);
          //Serial1.println(String("numberOfSteps: ") + numberOfSteps);
          //Serial1.println(String("[0].panStepCount: ") + keyframe_array[0].panStepCount);
          //Serial1.println(String("[9].panStepCount: ") + keyframe_array[9].panStepCount);
          //Serial1.println(String("panStepDelta: ") + panStepDelta);
          //Serial1.println("#$");

          stepper_pan.setTargetAbs(panStepDelta);
          stepper_tilt.setTargetAbs(tiltStepDelta);
          stepper_slider.setTargetAbs(sliderStepDelta);
          //stepper_zoom.setTargetAbs(zoomStepDelta);

          isMoving = true;
          multi_stepper.move(stepper_pan, stepper_tilt, stepper_slider);
          //StepperGroup ({stepper_pan, stepper_tilt, stepper_slider, stepper_zoom}).move();
          isMoving = false;

          if (numberOfSteps == numberOfStepsCount) {
            TLStarted = false;
            numberOfStepsCount = 0;
            return;
          }
        }
      }
      break;
    case INSTRUCTION_IS_TOGGLE_SET_SPEEDS:
      {
        if (useKeyframeSpeeds == false) {
          useKeyframeSpeeds = true;
          Serial1.println("#I");
        }
        else if (useKeyframeSpeeds == true) {
          useKeyframeSpeeds = false;
          Serial1.println("#i");
        }
      }
      break;
    default:
      break;  // if unrecognised charater, do nothing
  }
}
